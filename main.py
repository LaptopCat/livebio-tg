from re import findall, compile
from os import listdir
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.sessions import StringSession
from asyncio import sleep, iscoroutinefunction, run
from config import Config
from time import perf_counter
from importlib.util import spec_from_file_location, module_from_spec
from rich.align import Align
from rich.live import Live
from threading import Thread, Event
from helpers import console
from sys import version as pyver

__version__ = "1.0"
plugin_regex = compile(r"\{%plugin:(.*?)%\}")
telegram = Config.telegram
script = Config.script
print = console.print
old = ""
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
print(Align.center("[bold blue]Livebio[/bold blue] Version [bold blue]{}[/bold blue] | [blue]Pyt[/blue][bold bright_yellow]hon[/bold bright_yellow] Version [bold blue]{}[/bold blue]".format(__version__, pyver.split(" (")[0])))
print(Align.center("\n[bold blue][link=https://github.com/LaptopCat/livebio-tg]GitHub[/link][/bold blue]\n"))


plugins = {}
stopper_event = Event()
def add_plugins():
  start = perf_counter()
  global plugins
  with console.status("Loading plugins...", spinner="point"):
    for plugin in listdir("./plugins"):
      if plugin.endswith(".plugin.py"):
        try:
          spec = spec_from_file_location(name=plugin, location="./plugins/"+plugin)
          plugins[plugin] = module_from_spec(spec)
          spec.loader.exec_module(plugins[plugin])
          loaded = plugins[plugin]
          try:
            assert type(loaded.__plugin__) is dict, "Plugin Metadata is invalid"
            assert iscoroutinefunction(loaded.gather), "Plugin does not have an async gather function"
            assert iscoroutinefunction(loaded.postprocess), "Plugin does not have an async postprocess function"
            manifest = loaded.__plugin__
          except Exception as e:
            del plugins[plugin]
            raise e
          Thread(target=loaded.setup, daemon=True, args=(stopper_event, )).start()
          console.log("[MAIN] Loaded plugin [link={}][bold blue]{}[/bold blue][/link] v[bold blue]{}[/bold blue] (by [bold blue]{}[/bold blue])".format(manifest.get("link", "https://github.com/LaptopCat/livebio-tg"), manifest.get("name"), manifest.get("version"), manifest.get("author")))
        except Exception as e:
          del plugins[plugin]
          console.log("[bold red][MAIN] Failed to load [bold blue]{}[/bold blue] plugin! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]".format(plugin.strip(".plugin.py"), type(e).__name__, str(e)))
  console.log("[MAIN] Loaded [bold blue]{}[/bold blue] plugin(s) in [bold blue]{}[/bold blue]s!\n".format(len(plugins), round(perf_counter()-start, ndigits=4)))


async def main():
  global old
  while True:
    with console.status("Generating status...", spinner="point"):
      generated = str(script.template)
      used_plugins = findall(plugin_regex, script.template)
      contributed_plugins = []
      for plugin in used_plugins:
        try:
          unsplit = "UNSPLIT" in plugin
          slug = "{%plugin:"+plugin+"%}"
          plugin=plugin.rstrip("UNSPLIT")
          try:
            this_plugin = plugins[plugin + ".plugin.py"]
          except KeyError:
            raise KeyError("Plugin {} was not found!".format(plugin))
          add = await this_plugin.gather()
          if add != None and add.strip() != "":
            generated=generated.replace(slug, add+((" {}{}".format(script.splitter, " " if used_plugins.index(plugin) != len(used_plugins)-1 else "")) if unsplit is False else ""), 1)
            contributed_plugins.append([plugin, add])
          else:
            generated=generated.replace(" "+slug, "", 1).replace(slug, "", 1)
        except Exception as e:
          console.log("[bold red]\[{}] Failed to generate content! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]".format(plugin, type(e).__name__, str(e)))
          generated=generated.replace(" "+slug, "", 1).replace(slug, "", 1)
          pass
      for plugin in contributed_plugins:
         try:
          unsplit = "UNSPLIT" in plugin[0]
          plugin[0]=plugin[0].rstrip("UNSPLIT")
          this_plugin = plugins[plugin[0] + ".plugin.py"]
          new = await this_plugin.postprocess(generated, plugin[1])
          if new == "":
            generated=generated.replace(" "+plugin[1]+((" {}{}".format(script.splitter, " " if contributed_plugins.index(plugin) != len(contributed_plugins)-1 else "")) if unsplit is False else ""), 1)
          elif new != None:
            generated=generated.replace(plugin[1], new, 1)
          else:
            pass
         except Exception as e:
           name = plugin[0]
           console.log("[bold red][{}] Failed to postprocess! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]".format(name, type(e).__name__, str(e)))
    with Live("[MAIN] Changing bio to [bold blue]{}[/bold blue]".format(generated), console=console, refresh_per_second=1) as live:
      if generated != old:
        old = str(generated)
        try:
          if telegram.auth.mode == "F":
            async with TelegramClient("livebio", telegram.app.id, telegram.app.hash) as client:
              await client(UpdateProfileRequest(about=generated))
          else:
            async with TelegramClient(StringSession(telegram.auth.string), telegram.app.id, telegram.app.hash) as client:
              await client(UpdateProfileRequest(about=generated))
        except Exception as e:
            live.update("[bold red]\[MAIN] Failed to edit bio to [bold blue]{}[/bold blue]! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]".format(generated, type(e).__name__, str(e)))
            live.stop()
        live.update("[MAIN] Changed bio to [bold blue]{}[/bold blue]".format(generated))
      else:
        live.update("[MAIN] Generated bio is identical to cached bio ([bold blue]{}[/bold blue]), not changing bio".format(generated))
      live.stop()
    with console.status("Sleeping...", spinner="point"):
      await sleep(script.delay)


try:
  add_plugins()
  run(main())
except BaseException as e:
  stopper_event.set()
  raise e