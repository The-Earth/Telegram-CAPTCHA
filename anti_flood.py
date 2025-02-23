from catbot import Message, Chat


class AntiFlood:
    def __init__(self):
        self.message: Message | None = None
        self.enabled = False
        self.counter = 0

    @property
    def chat(self) -> Chat:
        return self.message.chat

    @property
    def chat_id(self):
        return self.chat.id

    @property
    def msg_id(self):
        return self.message.id

    def enable(self, msg: Message):
        self.enabled = True
        self.message = msg
        self.counter = 0

    def disable(self):
        self.enabled = False
