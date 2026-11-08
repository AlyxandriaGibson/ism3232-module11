# test_my_assistant.py
# Author: Alyxandria Gibson


from mock_model import MockModel
from my_assistant import FAQAssistant
from my_tool import FAQKnowledgeBase


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def reply(self, instructions, history):
        return None


def make_assistant():
    """Create a new assistant instance for testing."""
    faq_data = {
        "store hours": "We are open from 9 AM - 5 PM, Monday through Friday.",
        "shipping": "3-5 business days.",
        "policy": "We offer a 1-year warranty on all products.",
    }
    tool = FAQKnowledgeBase(faq_data)
    return FAQAssistant(
        "Bizzy", "Clearly answer and assist with FAQs.", tool, MockModel()
    )


def test_faq_questions_uses_tool():
    assistant = make_assistant()
    reply = assistant.respond("What are your store hours?")
    assert "We are open from 9 AM - 5 PM, Monday through Friday." in reply


def test_faq_policy_question_uses_tool():
    assistant = make_assistant()
    reply = assistant.respond("What is your store policy?")
    assert "1-year warranty" in reply


def test_unknown_questions_go_to_model():
    assistant = make_assistant()
    reply = assistant.respond("What is your favorite color?")
    assert "I'm not sure how to help you with that." in reply


def test_human_handoff_for_sensitive_topics():
    assistant = make_assistant()
    reply = assistant.respond("I want a refund for my order.")
    assert (
        "Financial and return requests require a human agent. I am routing you to customer support."
        in reply
    )


def test_unknown_request_gets_safe_fallback():
    faq_data = {"store hours": "We are open from 9 AM - 5 PM, Monday through Friday."}
    tool = FAQKnowledgeBase(faq_data)
    assistant = FAQAssistant(
        "Bizzy", "Clearly answer and assist with FAQs.", tool, SilentModel()
    )
    assert "try again" in assistant.respond("What is the meaning of life?")


def test_other_messages_go_to_model():
    assistant = make_assistant()
    assert assistant.respond("hello") == "Hello! How can I help you today?"


def test_history_records_turns():
    assistant = make_assistant()
    assistant.respond("hello")
    assistant.respond("What are your store hours?")
    assert len(assistant.history) == 4
