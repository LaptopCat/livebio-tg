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

print = console.print
__version__ = "2.0"
plugin_regex = compile(r"\{%plugin:(.*?)%\}")
telegram = Config.telegram
script = Config.script
script.logstrings = getattr(script, "logstrings", None)
telegram.auth.mode = getattr(telegram.auth, "mode", "F")
script.splitter = getattr(script, "splitter", "|")
script.delay = getattr(script, "delay", 20)
script.max_length = getattr(script, "max_length", 70)
default_logstrings = {
      "banner": """[bold blue]
  _      _______      ________ ____ _____ ____  
 | |    |_   _\ \    / /  ____|  _ \_   _/ __ \ 
 | |      | |  \ \  / /| |__  | |_) || || |  | |
 | |      | |   \ \/ / |  __| |  _ < | || |  | |
 | |____ _| |_   \  /  | |____| |_) || || |__| |
 |______|_____|   \/   |______|____/_____\____/ 
[/bold blue]""",
      "versions": "[bold blue]Livebio[/bold blue] Version [bold blue]{}[/bold blue] | [blue]Pyt[/blue][bold bright_yellow]hon[/bold bright_yellow] Version [bold blue]{}[/bold blue]",
      "github": "\n[bold blue][link=https://github.com/LaptopCat/livebio-tg]GitHub[/link][/bold blue]\n",
      "loading": "Loading plugins...",
      "nometa": "Plugin Metadata is invalid",
      "nogather": "Plugin does not have an async gather function",
      "nopostprocess": "Plugin does not have an async postprocess function",
      "nosetup": "Plugin does not have a setup function",
      "loadedplugin": "[MAIN] Loaded plugin [link={}][bold blue]{}[/bold blue][/link] v[bold blue]{}[/bold blue] (by [bold blue]{}[/bold blue])",
      "loadfailed": "[bold red][MAIN] Failed to load [bold blue]{}[/bold blue] plugin! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]",
      "loaded": "[MAIN] Loaded [bold blue]{}[/bold blue] plugin(s) in [bold blue]{}[/bold blue]s!\n",
      "generating": "Generating status...",
      "notfound": "Plugin {} was not found!",
      "didntgenerate": "[bold red]\[{}] Failed to generate content! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]",
      "didntpostprocess": "[bold red][{}] Failed to postprocess! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]",
      "changing": "[MAIN] Changing bio to [bold blue]{}[/bold blue]",
      "didntedit": "[bold red]\[MAIN] Failed to edit bio to [bold blue]{}[/bold blue]! ([bold blue]{}[/bold blue]: [bold blue]{}[/bold blue])[/bold red]",
      "edited": "[MAIN] Changed bio to [bold blue]{}[/bold blue]",
      "cached": "[MAIN] Generated bio is identical to cached bio ([bold blue]{}[/bold blue]), not changing bio",
      "sleeping": "Sleeping...",
      "didntauth": "[MAIN] Failed to authenticate."
}
def logstring(name):
  return getattr(script.logstrings, name, default_logstrings[name])
old = ""
print(Align.center(logstring("banner")))
print(Align.center(logstring("versions").format(__version__, pyver.split(" (")[0])))
print(Align.center(logstring("github")))
async def check_auth():
  try:
    if telegram.auth.mode == "F":
      async with TelegramClient("livebio", telegram.app.id, telegram.app.hash, receive_updates=False):
        pass
    elif telegram.auth.mode == "S":
      async with TelegramClient(StringSession(telegram.auth.string), telegram.app.id, telegram.app.hash, receive_updates=False):
        pass
    else:
      return False, None
  except BaseException as e:
    return False, e
  return True, None

plugins = {}
stopper_event = Event()
def add_plugins():
  start = perf_counter()
  global plugins
  with console.status(logstring("loading"), spinner="point"):
    for plugin in listdir("./plugins"):
      if plugin.endswith(".plugin.py"):
        try:
          spec = spec_from_file_location(name=plugin, location="./plugins/"+plugin)
          plugins[plugin] = module_from_spec(spec)
          spec.loader.exec_module(plugins[plugin])
          loaded = plugins[plugin]
          try:
            assert type(loaded.__plugin__) is dict, logstring("nometa")
            assert iscoroutinefunction(loaded.gather), logstring("nogather")
            assert iscoroutinefunction(loaded.postprocess), logstring("nopostprocess")
            assert type(loaded.setup).__name__ == "function", logstring("nosetup")
            manifest = loaded.__plugin__
          except Exception as e:
            del plugins[plugin]
            raise e
          Thread(target=loaded.setup, daemon=True, args=(stopper_event, )).start()
          console.log(logstring("loadedplugin").format(manifest.get("link", "https://github.com/LaptopCat/livebio-tg"), manifest.get("name"), manifest.get("version"), manifest.get("author")))
        except Exception as e:
          try: del plugins[plugin]
          except: pass
          console.log(logstring("loadfailed").format(plugin.strip(".plugin.py"), type(e).__name__, str(e)))
  console.log(logstring("loaded").format(len(plugins), round(perf_counter()-start, ndigits=4)))


async def main():
  global old
  while True:
    with console.status(logstring("generating"), spinner="point"):
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
            raise KeyError(logstring("notfound").format(plugin))
          add = await this_plugin.gather()
          if add != None and add.strip() != "":
            generated=generated.replace(slug, add+((" {}{}".format(script.splitter, " " if used_plugins.index(plugin) != len(used_plugins)-1 else "")) if unsplit is False else ""), 1)
            contributed_plugins.append([plugin, add])
          else:
            generated=generated.replace(" "+slug, "", 1).replace(slug, "", 1)
        except Exception as e:
          raise e
          console.log(logstring("didntgenerate").format(plugin, type(e).__name__, str(e)))
          generated=generated.replace(" "+slug, "", 1).replace(slug, "", 1)
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
           console.log(logstring("didntpostprocess").format(plugin[0], type(e).__name__, str(e)))
    with Live(logstring("changing").format(generated), console=console, refresh_per_second=1) as live:
      if generated != old:
        old = str(generated)
        try:
          if telegram.auth.mode == "F":
            async with TelegramClient("livebio", telegram.app.id, telegram.app.hash, receive_updates=False) as client:
              await client(UpdateProfileRequest(about=generated))
          elif telegram.auth.mode == "S":
            async with TelegramClient(StringSession(telegram.auth.string), telegram.app.id, telegram.app.hash, receive_updates=False) as client:
              await client(UpdateProfileRequest(about=generated))
        except Exception as e:
            live.update(logstring("didntedit").format(generated, type(e).__name__, str(e)))
            live.stop()
        live.update(logstring("edited").format(generated))
      else:
        live.update(logstring("cached").format(generated))
      live.stop()
    with console.status(logstring("sleeping"), spinner="point"):
      await sleep(script.delay)

try:
  result = run(check_auth())
  if result[0] is False:
    console.log(logstring("didntauth")+(" ({}: {})".format(type(result[1]).__name__, (str(result[1]))) if result[1] is not None else ""))
  else:
    add_plugins()
    run(main())
except BaseException as e:
  stopper_event.set()
  raise e
