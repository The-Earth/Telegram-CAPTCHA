import time


class Timeout:
    _running: list['Timeout'] = []

    def __init__(self, chat_id: int, user_id: int, msg_id: int, timer: int):
        self.chat_id = chat_id
        self.user_id = user_id
        self.msg_id = msg_id
        self._valid = False
        self.timer = timer

    def run(self, callback, **callback_args):
        Timeout._add_to_list(self)
        self._valid = True
        time.sleep(self.timer)
        Timeout._remove_from_list(self)
        if self._valid:
            result = callback(**callback_args)
            self._valid = False
            return result
        else:
            return None

    def stop(self):
        self._valid = False

    @classmethod
    def _add_to_list(cls, timeout):
        cls._running.append(timeout)

    @classmethod
    def list_all(cls):
        return cls._running

    @classmethod
    def _remove_from_list(cls, timeout):
        cls._running.remove(timeout)
