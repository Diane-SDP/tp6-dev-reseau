import asyncio
import aiohttp
import sys
import aiofiles



url = sys.argv[1]


async def get_content(url) :
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.read()
            return resp.decode()

async def write_content(content, file) :
    async with aiofiles.open(file, "w", encoding="utf-8") as out:
        await out.write(content)
        await out.flush() 

async def main() :
    content = await get_content(url)
    await write_content(content, "/tmp/web_page")

if __name__ == "__main__":
    asyncio.run(main())
