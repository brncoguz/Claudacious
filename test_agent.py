import unittest

from agent import Agent, FakeDatabase

class TestAgentProcessToolCall(unittest.TestCase):
    def setUp(self):
        # Set up a FakeDatabase and Agent instance for testing
        self.db = FakeDatabase()
        self.agent = Agent(self.db)

    def test_get_user_valid(self):
        result = self.agent.process_tool_call(
            "get_user", {"key": "email", "value": "john@gmail.com"}
        )
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["email"], "john@gmail.com")

    def test_get_user_invalid_key(self):
        result = self.agent.process_tool_call("get_user", {"key": "invalid", "value": "123"})
        self.assertIn("Error", result)

    def test_get_order_by_id_valid(self):
        result = self.agent.process_tool_call("get_order_by_id", {"order_id": "24601"})
        self.assertEqual(result["product"], "Wireless Headphones")

    def test_get_order_by_id_invalid(self):
        result = self.agent.process_tool_call("get_order_by_id", {"order_id": "99999"})
        self.assertIsNone(result)

    def test_cancel_order_processing(self):
        result = self.agent.process_tool_call("cancel_order", {"order_id": "13579"})
        self.assertEqual(result, "Cancelled the order")

    def test_cancel_order_shipped(self):
        result = self.agent.process_tool_call("cancel_order", {"order_id": "24601"})
        self.assertEqual(result, "Order has already shipped.  Can't cancel it.")

    def test_invalid_tool_name(self):
        result = self.agent.process_tool_call("invalid_tool", {})
        self.assertEqual(result, "Error: Invalid tool name 'invalid_tool'. Please verify the tool.")

class TestAgentExtractReply(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(None)  # `db` isn't needed for this test

    def test_extract_reply_valid(self):
        response_text = "<reply>Hello! How can I help you?</reply>"
        reply = self.agent.extract_reply(response_text)
        self.assertEqual(reply, "Hello! How can I help you?")

    def test_extract_reply_no_reply_tag(self):
        response_text = "Hello! How can I help you?"
        reply = self.agent.extract_reply(response_text)
        self.assertEqual(reply, "Unable to extract reply.")

class TestFakeDatabase(unittest.TestCase):
    def setUp(self):
        self.db = FakeDatabase()

    def test_get_user_by_email(self):
        user = self.db.get_user("email", "john@gmail.com")
        self.assertEqual(user["name"], "John Doe")

    def test_get_user_invalid_email(self):
        user = self.db.get_user("email", "nonexistent@gmail.com")
        self.assertEqual(user, "Couldn't find a user with email of nonexistent@gmail.com")

    def test_get_order_by_id(self):
        order = self.db.get_order_by_id("24601")
        self.assertEqual(order["product"], "Wireless Headphones")

    def test_get_order_invalid_id(self):
        order = self.db.get_order_by_id("99999")
        self.assertIsNone(order)

    def test_get_customer_orders(self):
        orders = self.db.get_customer_orders("1213210")
        self.assertEqual(len(orders), 3)  # John Doe has 3 orders

    def test_cancel_order_processing(self):
        result = self.db.cancel_order("13579")  # Processing order
        self.assertEqual(result, "Cancelled the order")

    def test_cancel_order_shipped(self):
        result = self.db.cancel_order("24601")  # Shipped order
        self.assertEqual(result, "Order has already shipped.  Can't cancel it.")

    def test_cancel_order_invalid(self):
        result = self.db.cancel_order("99999")  # Nonexistent order
        self.assertEqual(result, "Can't find that order!")