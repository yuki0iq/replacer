#!/usr/bin/pypy3

import re, os, os.path, sys
import asyncio, aiofile


tasks = []
inp: re.Pattern = None
out: str = None
mask: re.Pattern = None
folder: str = '.'


async def replace(filename: str):
    async with aiofile.async_open(filename, 'r') as f:
        data = await f.read()
    data = re.sub(inp, out, data)
    async with aiofile.async_open(filename, 'w') as f:
        await f.write(data)


if len(sys.argv) < 5:
    print(f"Usage: {sys.argv[0]} <in_pat> <out_pat> <filename_mask> <dir>")
else:
    inp, out, mask, folder = (sys.argv[1:5] + ['.'])[:4]
    
    inp = re.compile(inp)
    mask = re.compile(mask)
    
    loop = asyncio.get_event_loop()

    for root, dirs, files in os.walk(folder):
        dirs[:] = list(filter(lambda x: x[0] != '.', dirs))
        for file in filter(lambda f: re.fullmatch(mask, f), files):
            filename = os.path.join(root, file)
            tasks.append(loop.create_task(replace(filename)))

    if tasks:
        loop.run_until_complete(asyncio.wait(tasks))

