from asyncio import ensure_future

from presso.core.util.eventqueue import Eventqueue


class AbstractDataEvent:
    def __init__(self, alpha=None):
        # Start data event generator when the fist alpha is added
        if not self._alphas:
            ensure_future(self.__start())
            self._init()
        # When alpha is None, generate history events only
        self._alphas[alpha.name if alpha else ''] = alpha

    async def __start(self):
        for tstamp, data in await self._next():
            for alpha in self._alphas.values():
                # Skip callback when alpha is None
                if alpha:
                    Eventqueue.get().put_nowait((tstamp, alpha.onData(data)))

    @property
    def _alphas(self):
        raise NotImplementedError

    def _init(self):
        raise NotImplementedError

    async def _next(self):
        raise NotImplementedError

    async def getHistory(self, num):
        raise NotImplementedError
