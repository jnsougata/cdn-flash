import aiohttp
import os
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        headers = {
            'DETA-PROJECT-KEY': os.getenv('DETA_TOKEN'),
            'DRIVE-NAME': 'PixeL_@11223344',
            'FILE-NAME': 'covers/default_card.png'
        }
        async with session.post('https://cdn-flash.herokuapp.com/cdn', headers=headers) as resp:
            print(await resp.read())
            await session.close()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
