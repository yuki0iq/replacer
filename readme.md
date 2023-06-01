# replacer

Usage `./replacer.py from to mask dir excl [dry]` (uses pypy3)

Replace anything matching `from` regular expression to `to` string with `re.sub` in every file matching `mask` regular expression under `dir` directory recursively, ignoring dirs matching `excl`.

`dry` to only show changes, no write.

Uses `diff` to show what is replaced.

Depends on `aiofile`.

This is probably very slow but I am too lazy to write fast code.

