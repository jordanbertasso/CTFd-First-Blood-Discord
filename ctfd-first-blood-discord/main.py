import asyncio
import logging
import config

from solve_handler import Solve_Handler


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    solve_handler = Solve_Handler()
    loop = asyncio.get_event_loop()
    loop.call_soon(solve_handler.handle_solves, loop)

    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    main()
