import json
import os
import re

from anthropic import Anthropic

MAX_HISTORY_LENGTH = 20
    
class Agent:
    def __init__(self, db, tools_file="tools.json"):
        self.db = db
        with open(tools_file, "r") as f:
            self.tools = json.load(f)

    @staticmethod
    def extract_reply(text):
        """Extracts the reply from Claude's output."""
        pattern = r"<reply>(.*?)</reply>"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)
        return "Unable to extract reply."
    
    def process_tool_call(self, tool_name, tool_input):
        # Validate if the tool exists
        tool_mapping = {
            "get_user": self.db.get_user,
            "get_order_by_id": self.db.get_order_by_id,
            "get_customer_orders": self.db.get_customer_orders,
            "cancel_order": self.db.cancel_order,
        }

        if tool_name not in tool_mapping:
            return f"Error: Invalid tool name '{tool_name}'. Please verify the tool."

        try:
            # Call the corresponding database function with the provided input
            tool_function = tool_mapping[tool_name]
            result = tool_function(**tool_input)  # Unpack tool_input as function arguments
            return result
        except TypeError as e:
            return f"Error: Invalid input for tool '{tool_name}'. Details: {str(e)}"
        except Exception as e:
            return f"Error: Failed to execute tool '{tool_name}'. Details: {str(e)}"
    
    def simple_chat(self):
        system_prompt = """
        You are a customer support chat bot for an online retailer
        called Acme Co.Your job is to help users look up their account, 
        orders, and cancel orders.Be helpful and brief in your responses.
        You have access to a set of tools, but only use them when needed.  
        If you do not have enough information to use a tool correctly, 
        ask a user follow up questions to get the required inputs.
        Do not call any of the tools unless you have the required 
        data from a user. 

        In each conversational turn, you will begin by thinking about 
        your response. Once you're done, you will write a user-facing 
        response. It's important to place all user-facing conversational 
        responses in <reply></reply> XML tags to make them easy to parse.
        """
        user_message = input("\nUser: ")
        messages = [{"role": "user", "content": user_message}]

        # Keep a history of messages up to a certain length
        if len(messages) > MAX_HISTORY_LENGTH:
            messages = messages[-MAX_HISTORY_LENGTH:]

        while True:
            if user_message == "quit":
                break
            #If the last message is from the assistant, 
            # get another input from the user
            if messages[-1].get("role") == "assistant":
                user_message = input("\nUser: ")
                messages.append({"role": "user", "content": user_message})

            #Send a request to Claude
            response = client.messages.create(
                model=MODEL_NAME,
                system=system_prompt,
                max_tokens=4096,
                tools=self.tools,
                messages=messages
            )
            # Update messages to include Claude's response
            messages.append(
                {"role": "assistant", "content": response.content}
            )

            #If Claude stops because it wants to use a tool:
            if response.stop_reason == "tool_use":
                #Naive approach assumes only 1 tool is called at a time
                tool_use = response.content[-1] 
                tool_name = tool_use.name
                tool_input = tool_use.input
                print(f"=====Claude wants to use the {tool_name} tool=====")


                #Actually run the underlying tool functionality on our db
                tool_result = self.process_tool_call(tool_name, tool_input)

                #Add our tool_result message:
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": str(tool_result),
                            }
                        ],
                    },
                )
            else: 
                #If Claude does NOT want to use a tool, 
                #just print out the text reponse
                model_reply = self.extract_reply(response.content[0].text)
                print("\nAcme Co Support: " + f"{model_reply}" )    

class FakeDatabase:
    def __init__(self, customers_file="customers.json", orders_file="orders.json"):
        with open(customers_file, "r") as f:
            self.customers = json.load(f)
        with open(orders_file, "r") as f:
            self.orders = json.load(f)

    def get_user(self, key, value):
        if key in {"email", "phone", "username"}:
            for customer in self.customers:
                if customer[key] == value:
                    return customer
            return f"Couldn't find a user with {key} of {value}"
        else:
            raise ValueError(f"Invalid key: {key}")

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order["id"] == order_id:
                return order
        return None
    
    def get_customer_orders(self, customer_id):
        return [order for order in self.orders if order["customer_id"] == customer_id]

    def cancel_order(self, order_id):
        order = self.get_order_by_id(order_id)
        if order:
            if order["status"] == "Processing":
                order["status"] = "Cancelled"
                return "Cancelled the order"
            else:
                return "Order has already shipped.  Can't cancel it."
        return "Can't find that order!"

if __name__ == "__main__":
    db = FakeDatabase()
    MODEL_NAME="claude-3-5-sonnet-20241022"
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the ANTHROPIC_API_KEY environment variable.")
    
    client = Anthropic(api_key=api_key)
    agent = Agent(db)
    agent.simple_chat()