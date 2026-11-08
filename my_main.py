# my_main.py
# Author: Alyxandria Gibson


from my_assistant import FAQAssistant
from my_tool import FAQKnowledgeBase
from ollama_model import OllamaModel

FAQ_DATA = {
    "hours": "We are open from 9 AM - 5 PM, Monday through Friday.",
    "shipping": "Standard shipping takes 3-5 business days, and is free on orders over $60.",
    "warranty": "We offer a 1-year warranty on all products.",
}


INSTRUCTIONS = """You are Bizzy, a helpful customer service assistant for Tampa Outfitters.
Answer in one short sentence.
Store hours are 9 AM to 5 PM, Monday through Friday.
Standard shipping takes 3-5 business days, and is free on orders over $60.
Store policy offers a 1-year warranty on all products.
Only state facts in these instructions.
If you do not know the answer, say you do not know and offer to pass the customer to a human agent."""


faq_tool = FAQKnowledgeBase(FAQ_DATA)
model = OllamaModel("granite4.1:3b")
assistant = FAQAssistant("Bizzy", INSTRUCTIONS, faq_tool, model)


print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")


print(f"Messages in this conversation: {len(assistant.history)}")
