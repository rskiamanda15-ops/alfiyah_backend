import asyncio
from typing import Any, List


class Broadcaster:
    """Manages SSE client connections and broadcasts messages."""

    def __init__(self):
        self.queues: List[asyncio.Queue] = []
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue:
        """Subscribes a client by creating and returning a new queue."""
        queue = asyncio.Queue()
        async with self._lock:
            self.queues.append(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue):
        """Unsubscribes a client by removing their queue."""
        async with self._lock:
            if queue in self.queues:
                self.queues.remove(queue)

    async def broadcast(self, message: Any):
        """Broadcasts a message to all subscribed clients."""
        # The message is cloned for each queue to prevent one consumer
        # from affecting others if the message object is mutable.
        async with self._lock:
            for queue in self.queues:
                await queue.put(message)


# Global singleton instance
broadcaster = Broadcaster()
