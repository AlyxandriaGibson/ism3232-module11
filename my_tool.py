# my_tool.py
# Author: Alyxandria Gibson


class FAQKnowledgeBase:
    """A tool that looks up store policies and frequently asked questions."""

    def __init__(self, faq_data):
        """Store the FAQ dictionary with topic keywords to policy details."""
        self.faq_data = faq_data

    def find_topic(self, text):
        """Return the first known topic found in the message text, or None."""
        text_lower = text.lower()
        for topic in self.faq_data:
            topic_lower = topic.lower()
            if topic_lower in text_lower:
                return topic
            if topic_lower == "policies" and "store policy" in text_lower:
                return topic
        return None

    def answer_for(self, topic):
        """Return the answer for a specific topic, or None if the topic is unknown."""
        if topic is None:
            return None
        return self.faq_data.get(topic)
