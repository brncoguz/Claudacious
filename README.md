# Claudacious - Simple Claude Agent

This project is a Python-based chatbot that leverages Anthropic’s Claude API to simulate a customer support assistant for an online retailer, Acme Co. The chatbot can interact with users to:
- Look up user accounts by email, phone, or username.
- Retrieve order details by order ID.
- Fetch a customer’s order history.
- Cancel orders if they are still in the “Processing” state.


Features:
- Dynamic Tool Usage: The chatbot decides when to use tools (e.g., fetching user info, canceling orders) based on user queries.
- Conversation History: Maintains a chat history for context (up to 20 messages).
- Integration with Fake Database: Loads customer and order data from external JSON files for testing.

Installation:
- Clone the project:
  - `git clone https://github.com/your-repo/simple-claude-agent.git`
- Install the requirements:
  - `cd simple-claude-agent`
  - `pip install -r requirements.txt`
- Set your Anthropic API key:
  - `export ANTHROPIC_API_KEY=your_api_key_here`

Usage:
- Run the chatbot:
  - `python agent.py`
- And start talking to it about anything. You can also ask about your order status (e.g., “What’s my order status?”).
- Type `quit` to end the conversation.

Example Interaction:
```
User: Hello!

Acme Co Support: Hello! I'm the Acme Co. customer service bot. I can help you look up your account information, check on your orders, or help with canceling an order. What can I assist you with today?

User: I want to check my order status

Acme Co Support: I'll be happy to help you check your order status. Could you please provide either your email address, phone number, or username so I can look up your account?

User: my username is priya123
=====Claude wants to use the get_user tool=====
=====Claude wants to use the get_customer_orders tool=====

Acme Co Support: I found 2 recent orders for your account:
1. Order #97531: Bluetooth Speaker (Status: Shipped)
2. Order #28164: 2x Wireless Headphones (Status: Processing)

Would you like more details about any of these orders?

User: I would like to cancel my order 28164
=====Claude wants to use the cancel_order tool=====
=====Claude wants to use the get_order_by_id tool=====

Acme Co Support: I've successfully cancelled your order #28164 for the Wireless Headphones. The order status is now showing as Cancelled. Is there anything else I can help you with?

User: I want to check my order status one my time
=====Claude wants to use the get_customer_orders tool=====

Acme Co Support: Here are all your orders:
1. Order #97531: Bluetooth Speaker (Status: Shipped)
2. Order #28164: Wireless Headphones (Status: Cancelled)

Would you like more details about any of these orders?

User: great, have a nice day 

Acme Co Support: Thank you for shopping with Acme Co! Have a wonderful day. If you need any further assistance in the future, don't hesitate to ask!

User: quit

Acme Co Support: Thank you for chatting with Acme Co. customer service. Goodbye!
```

License:
- This project is for personal learning purposes and not for production use.
