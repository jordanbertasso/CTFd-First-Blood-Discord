import asyncio
import logging

from db import DB
from solve_handler import SolveHandler


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.WARN)

    handler = logging.FileHandler("./data/ctfd-first-blood-discord.log")
    handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)

    DB.init_db()

    solve_handler = SolveHandler()
    loop = asyncio.new_event_loop()
    loop.create_task(solve_handler.handle_past_solves())

    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    main()
