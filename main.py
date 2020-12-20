import aioredis
import asyncio
import json
import database


async def listen():
    await database.create()

    print("Existing rows:")
    for x in await database.select():
        print(x)
    print("-" * 80)

    redis = await aioredis.create_redis(("127.0.0.1", 6379))
    channel = (await redis.subscribe("action-logs"))[0]

    try:
        while True:
            message = json.loads((await channel.get()).decode("ascii"))
            print(message)
            await database.insert(message["ip_address"], message["action"], message["timestamp"])
    except Exception:
        redis.close()
        await redis.wait_closed()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen())
    asyncio.get_event_loop().run_forever()