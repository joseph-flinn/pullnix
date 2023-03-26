#!/usr/bin/env python
from functools import lru_cache

from fastapi import FastAPI

from .tasks import repeat_every
from .sync import sync
from .nixos import build, vulnix, switch


class Api(FastAPI):
    config: dict = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


app = Api()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
@repeat_every(seconds=5 * 60)
def stdout_loop() -> None:
    in_sync, commit_hash = sync(app.config)
    if not in_sync:
        successful_build = build(commit_hash)

        if successful_build:
            if app.config["check-vuln"]:
               is_vulnerable = vulnix()
               if not is_vulnerable:
                   switch()
            else:
                switch()
