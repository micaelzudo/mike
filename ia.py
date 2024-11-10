from lms.agent_terminal import get_agent_terminal
import asyncio

async def main():
    termzr = get_agent_terminal()
    await termzr.a_cmdloop()

if __name__ == '__main__':
    asyncio.run(main())
