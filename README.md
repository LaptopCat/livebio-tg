# livebio-tg
## Make your telegram about me live.

## [General Install](#general-install-1)
## [Deploying to Replit](#deploying-to-replit-1)
## [Plugins](#plugins-1)

# Installing
## Deploying to Replit
### 1. Fork the repl
You will need to make an account and fork [this](https://replit.com/@livebio/livebio-on-replit?v=1) repl.
### 2. Create a Telegram Application
To work, livebio-tg requires a Telegram app to change your bio.

To create a Telegram application, go to this [page](https://my.telegram.org/apps) and log into your Telegram account.

After you login, you will need to fill out a form, you can fill it in with anything you want, but make sure that all fields are filled.

If there is no error while creating an app, you will see a screen with your app info.

You need to copy the "api_id" and the "api_hash" and write them down somewhere (you shouldn't share those values with anyone)

### 3. Configuring livebio
After you forked the repl, first - head to the Secrets tab.
Add the following values:
```yaml
telegram.app.id: your app_id
telegram.app.hash: your app_hash
telegram.auth.string: your Session String (get one by running the session.py file)
```
You will also need to edit the config.py file.
It is a Python dictionary (has JSON-like syntax)

#### Config Structure
Presented in a more readable format.
```yaml
telegram:
  app:
    id: int("Your api_id here")
    hash: str("Your api_hash here")
  auth:
    mode: mode_enum("Authentication mode here - can be string or file")
    string: str("Your session string here - set it if you are using string mode") (Default is "file")
    
script:
  splitter: str("A string that splits output of plugins") (Default is "|")
  template: str("The template used to generate your bio")
  delay: int(The delay between each bio change) (Default is 20)
  max_length: int(The max length of the bio) (Default is 70, set it to 140 if you have Telegram Premium)
 
 plugins:
  plugin_name:
    plugin: config
    is: here
```
Each plugin will have a reference on how you need to configure it.

[How do I make a template?](TEMPLATE.md)

Example Config (has some plugin configs):
```python
{
  "telegram": {
    "app": {
      "id": int(environ['telegram.app.id']),
      "hash": str(environ['telegram.app.hash'])
    },
    "auth": {
      "mode": mode_enum("string"),
      "string": str(environ["telegram.auth.string"])
    }
  },
  "script": {
    "splitter": "|",
    "template": str("{%plugin:timeUNSPLIT%} {%plugin:discord%} i use livebio btw 😎"),
    # Produces an output like this: "01:23 Playing Minecraft | i use livebio btw 😎"
    "delay": int(20),
    "max_length": int(70)
  },
  "plugins": {
    "time": {
      "time_formatting": str("%H:%M"),
      "timezone": str("Pacific/Tarawa"),
      "postprocess": False
    },
    "discord": {
      "token": str(environ["plugins.discord.token"]),
      "guild": int(46664),
      "user": int(4664),
      "pass_custom": False
    }
  }
}
```
### 4. Configuring UptimeRobot
After you run your repl, it will show a webview at the top right corner.
Copy the URL of it and write it down somewhere.

To keep your repl online 24/7, you can use [UptimeRobot](https://uptimerobot.com/).
First, create an account.
Then, Add a new monitor.

Recommended config:
```yaml
Monitor Type: HTTP(s)
Friendly Name: Any name you want
URL (or IP): The URL that you wrote down
Monitoring Interval: 15m
Monitoring Timeout: 30s
Monitor SSL Errors: No
Enable SSL expiry reminders: No
```
Keep anything else as-is.

Then, click on Create Monitor, and you should be done.
## Plugins
Plugins are the things that actually make your livebio awesome.

### [Plugins](https://github.com/LaptopCat/livebio-plugins)
