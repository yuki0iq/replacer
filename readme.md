# replacer

Usage `./replacer.py from to mask dir` (uses pypy3)

Replace anything matching `from` regular expression to `to` string with `re.sub` in every file matching `mask` regular expression under `dir` directory recursively, ignoring hidden dirs (name starts with dot).

Depends on `aiofile`.

This is probably very slow but I am too lazy to write fast code.

