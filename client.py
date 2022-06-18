import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        headers = {
            'DETA-PROJECT-KEY': ...'),
            'DRIVE-NAME': ...,
            'FILE-NAME': ...'
        }
        async with session.post('https://cdn-flash.herokuapp.com/cdn', headers=headers) as resp:
            print(await resp.json())
            await session.close()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
