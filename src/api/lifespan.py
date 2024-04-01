from contextlib import asynccontextmanager

from conversations.broker import broker


@asynccontextmanager
async def lifespan_context(app):
    await broker.start()
    try:
        yield
    finally:
        await broker.close()
