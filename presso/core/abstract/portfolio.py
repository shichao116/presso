import asyncio
import sys

from presso.core.util.eventqueue import Eventqueue


class AbstractPortfolio:
    def __init__(self):
        self._transactions = []
        self._statistics = []
        self._init()

    def _execute(self, transaction):
        self._transactions.append(transaction)
        asyncio.ensure_future(transaction.execute(self))

    def _run_statistics(self):
        for stat in self._statistics:
            stat.run(self._transactions)

    def backetst(self):
        loop = asyncio.get_event_loop()
        # Load all history events to queue
        tasks = asyncio.Task.all_tasks()
        loop.run_until_complete(asyncio.gather(*tasks))
        # Process events synchronously
        event_queue = Eventqueue.get()
        while not event_queue.empty():
            loop.run_until_complete(event_queue.get_nowait())
        self._run_statistics()

    def realtime(self):
        event_queue = Eventqueue.get()
        loop = asyncio.get_event_loop()
        # Press ENTER to stop eventloop and run statistics
        loop.add_reader(sys.stdin, loop.stop)
        async def main():
            while True:
                asyncio.ensure_future(await event_queue.get())
        loop.run_until_complete(main())
        self._run_statistics()

    def _init(self):
        raise NotImplementedError
