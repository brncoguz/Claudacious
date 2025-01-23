# Simple Claude Agent

This project is a Python-based chatbot that leverages Anthropic’s Claude API to simulate a customer support assistant for an online retailer, Acme Co. The chatbot can interact with users to:
- Look up user accounts by email, phone, or username.
- Retrieve order details by order ID.
- Fetch a customer’s order history.
- Cancel orders if they are still in the “Processing” state.


Features:
- Dynamic Tool Usage: The chatbot decides when to use tools (e.g., fetching user info, canceling orders) based on user queries.
- Conversation History: Maintains a history of the chat for context (up to 20 messages).
- Integration with Fake Database: Loads customer and order data from external JSON files for testing.

Installation:
- Clone the project:
- git clone https://github.com/your-repo/simple-claude-agent.git
- Install the requirements:
- cd simple-claude-agent
- pip install -r requirements.txt
- Set your Anthropic API key:
- export ANTHROPIC_API_KEY=your_api_key_here

Usage:
- Run the chatbot:
- python agent.py
- And start talking to it about anything. And you can ask about your order status (e.g., “What’s my order status?”)
- Type quit to end the conversation.

License:
- This project is for personal learning purposes and is not intended for production use.