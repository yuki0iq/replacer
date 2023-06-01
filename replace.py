#!/usr/bin/pypy3

import re
import io
import os, os.path, sys
import subprocess
import asyncio, aiofile


tasks = []
inp: re.Pattern = None
out: str = None
mask: re.Pattern = None
folder: str = '.'
ignore_mask: re.Pattern = None
dry: bool


async def replace(filename: str):
    async with aiofile.async_open(filename, 'r') as f:
        data = await f.read()
    data = re.sub(inp, out, data)
    print(filename, subprocess.run(['diff', filename, '-'], capture_output=True, input=data, encoding='utf-8').stdout)
    if not dry:
        async with aiofile.async_open(filename, 'w') as f:
            await f.write(data)


if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <in_pat> <out_pat> <filename_mask> <dir> <dir_ignore_mask> [dry]")
else:
    inp, out, mask, folder, ignore_mask = (sys.argv[1:6] + ['.', ''])[:5]
    rest = set(sys.argv[6:])
    dry = 'dry' in rest

    inp = re.compile(inp)
    mask = re.compile(mask)
    ignore_mask = re.compile(ignore_mask)
    
    loop = asyncio.get_event_loop()

    for root, dirs, files in os.walk(folder):
        dirs[:] = list(filter(lambda x: not re.fullmatch(ignore_mask, x), dirs))
        for file in filter(lambda f: re.fullmatch(mask, f), files):
            filename = os.path.join(root, file)
            tasks.append(loop.create_task(replace(filename)))

    if tasks:
        loop.run_until_complete(asyncio.wait(tasks))

