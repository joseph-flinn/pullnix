#!/usr/bin/env python

from fastapi import FastAPI

from .tasks import repeat_every
from .sync import sync
from .nixos import build, vulnix, switch


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
@repeat_every(seconds=3)
def stdout_loop() -> None:
    in_sync = sync()
    if not in_sync:
        build()
        is_vulnerable = vulnix()
        if not is_vulnerable:
            switch()



