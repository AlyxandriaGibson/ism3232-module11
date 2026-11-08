# my_assistant.py
# Author: Alyxandria Gibson


HANDOFF_WORDS = ["refund", "dispute", "return", "complaint"]


class FAQAssistant:
    """A mock FAQ assistant for Tampa Outfitters. Rules handle what must be right and the model handles the rest."""


    def __init__(self, name, instructions, faq_tool, model):
        """Set up an assistant with its own name, instructions, faq tool, model, and history."""
        self.name = name
        self.instructions = instructions
        self.faq_tool = faq_tool
        self.model = model
        self.history = []


    def respond(self, user_message):
        """Record the message, determine a reply, record the reply, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply


    def choose_reply(self, user_message):
        """Use a rule when one applies. Otherwise, ask the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "Financial and return requests require a human agent. I am routing you to customer support."
        faq_keywords = ["policy", "policies", "warranty", "hour", "hours", "shipping", "ship"]
        if any(keyword in text for keyword in faq_keywords):
            return self.faq_reply(user_message)
        return self.model_reply()


    def model_reply(self):
        """Ask the model for a reply. Give a safe answer if the model has none."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "I'm sorry, I can't answer that righ now, please try again later."
        return reply


    def needs_human(self, text):
        """Return True if the request requires a human to handle it."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False


    def faq_reply(self, user_message):
        """Retrieve an answer using the FAQ tool."""
        topic = self.faq_tool.find_topic(user_message)
        if topic is None:
            return "Which topic? Please ask about store hours, shipping, or policies."
        answer = self.faq_tool.answer_for(topic)
        return answer