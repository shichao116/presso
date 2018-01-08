from asyncio import PriorityQueue


class EventQueue:
    __queue = None

    @staticmethod
    def get():
        if EventQueue.__queue:
            return EventQueue.__queue
        else:
            EventQueue.__queue = PriorityQueue()
