from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
from config import Config
from rich.console import Console
from rich.align import Align
from rich.markdown import Markdown
from rich.prompt import Prompt
console = Console()
print = console.print
print(Align.center("""
[bold blue]
  _      _______      ________ ____ _____ ____  
 | |    |_   _\ \    / /  ____|  _ \_   _/ __ \ 
 | |      | |  \ \  / /| |__  | |_) || || |  | |
 | |      | |   \ \/ / |  __| |  _ < | || |  | |
 | |____ _| |_   \  /  | |____| |_) || || |__| |
 |______|_____|   \/   |______|____/_____\____/ 
[/bold blue]
"""))
print(Align.center("Get Session String"))

async def getString():
    async with TelegramClient(StringSession(), Config.telegram.app.id, Config.telegram.app.hash, receive_updates=False) as client:
        print(Align.center("Your Session String :arrow_down:"))
        session = client.session.save()
        print(Markdown("```{}```".format(session)))
        print(Align.center("Do you want to save it to a text file? (session.txt)"))
        a = Prompt.ask("[blink]> [/blink]", choices=["y", "n"])
        if a == "y":
            with console.status("Writing to file...", spinner="point"):
                with open("session.txt", "w") as file:
                    file.write(session)
            print(Align.center("File Saved!"))
            exit()
            


asyncio.run(getString())