import asyncio
import aiohttp
import json

API: dict = {
    "gathering": {
        "START": "https://discord.com/api/v9/gorilla/activity/gathering/start",
        "COMPLETE": "https://discord.com/api/v9/gorilla/activity/gathering/complete",
    },
    "crafting": {
        "START": "https://discord.com/api/v9/gorilla/activity/crafting/start",
        "COMPLETE": "https://discord.com/api/v9/gorilla/activity/crafting/complete",
    },
    "combat": {
        "START": "https://discord.com/api/v9/gorilla/activity/combat/start",
        "COMPLETE": "https://discord.com/api/v9/gorilla/activity/combat/complete",
    },
}
headers: str = {
    # your headers
}

async def run_activity(session: aiohttp.ClientSession, activity: str):
    start_url = API[activity]["START"]
    complete_url = API[activity]["COMPLETE"]

    try:
        async with session.post(start_url, headers=headers) as resp_start:
            start_text = await resp_start.text()
            startJson = json.loads(start_text)
            print(f"[{activity}] START:", resp_start.status, startJson)

        async with session.post(complete_url, headers=headers) as resp_complete:
            complete_text = await resp_complete.text()
            completeJson = json.loads(complete_text)
            print(f"[{activity}] COMPLETE:", resp_complete.status, completeJson)

    except Exception as e:
        print(f"[{activity}] Error:", e)

async def gathering_loop(session: aiohttp.ClientSession):
    while True:
        await run_activity(session, "gathering")
        await asyncio.sleep(0)

async def crafting_loop(session: aiohttp.ClientSession):
    while True:
        await run_activity(session, "crafting")
        await asyncio.sleep(120)

async def combat_loop(session: aiohttp.ClientSession):
    while True:
        await run_activity(session, "combat")
        await asyncio.sleep(180)

async def main():
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        await asyncio.gather(
            gathering_loop(session),
            crafting_loop(session),
            combat_loop(session),
        )

if __name__ == "__main__":
    asyncio.run(main())
