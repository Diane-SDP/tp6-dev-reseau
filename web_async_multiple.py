import asyncio
import aiohttp
import sys
import aiofiles
import time

start_time = time.time()

async def get_content(url) :
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.read()
            return resp.decode()

async def write_content(content, file) :
    async with aiofiles.open(file, "w", encoding="utf-8") as out:
        await out.write(content)
        await out.flush() 

async def process(url):
    name = url.split("/")[2]
    content = await get_content(url)
    await write_content(content, f"./tmp/web_{name}")

async def main():
    f = open(sys.argv[1], "r")
    content = f.read()
    urls = content.split("\n")

    for i in range(1, len(sys.argv)) :   
        urls.append(sys.argv[i])

    tasks = []
    for elt in urls[:-1] :
        tasks.append(process(str(elt)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
