import asyncio
import logging

from db import db
from solve_handler import SolveHandler


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    handler = logging.FileHandler("./data/ctfd-first-blood-discord.log")
    handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)

    db.init_db()

    solve_handler = SolveHandler()
    loop = asyncio.new_event_loop()
    loop.call_soon(solve_handler.handle_past_solves, loop)

    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    main()
