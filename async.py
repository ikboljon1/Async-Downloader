import asyncio
import aiohttp
import hashlib

async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

async def calculate_hash(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        return hashlib.sha256(contents).hexdigest()

async def main():
    url = 'https://gitea.radium.group/radium/project-configuration/'
    temp_dir = '/tmp/project-configuration'
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            headers = response.headers
            if 'Content-Length' in headers:
                content_length = int(headers['Content-Length'])
                chunk_size = content_length // 3
                for i in range(3):
                    start_byte = i * chunk_size
                    end_byte = (i + 1) * chunk_size - 1
                    if i == 2:
                        end_byte = content_length - 1
                    filename = f'{temp_dir}/{i}.zip'
                    tasks.append(asyncio.create_task(download_file(url, filename, start_byte, end_byte)))
    await asyncio.gather(*tasks)
    hash_tasks = []
    for i in range(3):
        filename = f'{temp_dir}/{i}.zip'
        hash_tasks.append(asyncio.create_task(calculate_hash(filename)))
    hashes = await asyncio.gather(*hash_tasks)
    print(hashes)

if __name__ == '__main__':
    asyncio.run(main())