# echo_model.py
# Author: Alyxandria Gibson


class EchoModel:
    """A model that echos back the last message in the history."""

    def reply(self, instructions, history):
        """Return 'You said: ' followed by the latest meassage in the history."""
        last_message = history[-1]["content"]
        return f"You said: {last_message}"
