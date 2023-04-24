# livebio-tg
## Make your telegram about me live.

## [General Install](#general-install-1)
## [Deploying to Replit](https://github.com/LaptopCat/livebio-tg/tree/replit)
## [Plugins](#plugins-1)

# Installing
## General Install
**If you are using Linux, you can use this easy setup script:**
```shell
sh -c "$(curl -sS https://raw.githubusercontent.com/LaptopCat/livebio-tg/files/i.sh)"
```
### 1. Clone this repository
You can do this using the git CLI (if you have it installed) or just download the zip file on the Code page.
### 2. Install Python and the required dependencies
Download Python from [here](https://www.python.org/downloads/) (Latest version is recommended, but anything higher than Python 3.7 should work)

Make sure to choose "Add Python to PATH" when installing to make this tutorial easy to follow!

Now, open your command prompt and use those commands to install the required modules:
```commandline
pip install telethon
```

```commandline
pip install rich
```

### 3. Create a Telegram Application
To work, livebio-tg requires a Telegram app to change your bio.

To create a Telegram application, go to this [page](https://my.telegram.org/apps) and log into your Telegram account.

After you login, you will need to fill out a form, you can fill it in with anything you want, but make sure that all fields are filled.

If there is no error while creating an app, you will see a screen with your app info.

You need to copy the "api_id" and the "api_hash" and write them down somewhere (you shouldn't share those values with anyone)

### 4. Configuring livebio
After you cloned the repository, head to the config.py file.

It is a Python dictionary (has JSON-like syntax)

#### Config Structure

<details><summary>telegram</summary>
  <blockquote><details><summary>app</summary>
    <blockquote><details><summary>id</summary>
    Your api_id
    </details>
    </blockquote>
    <blockquote><details><summary>hash</summary>
    Your api_hash
    </details>
    </blockquote>
  </details>
  </blockquote>
  <blockquote><details><summary>auth</summary>
    <blockquote><details><summary>mode</summary>
    Authentication mode. Can be string or file. Defaults to file.
    </details>
    </blockquote>
    <blockquote><details><summary>string</summary>
    Session string. Only needed with the string authentication mode. For more info on authentication modes, look below.
    </details>
    </blockquote>
  </details>
  </blockquote>  
</details>

<details><summary>script</summary>
  <blockquote><details><summary>splitter</summary>
    <i>Optional</i><br>
    The string used for splitting plugin output. Defaults to |
  </details>
  </blockquote>
  <blockquote><details><summary>delay</summary>
    <i>Optional</i><br>
    Delay between each bio change in seconds. Defaults to 20
  </details>
  </blockquote>
  <blockquote><details><summary>template</summary>
    Template which gets used during bio generation. For more info on templates, look below.
  </details>
  </blockquote>
  <blockquote><details><summary>logstrings</summary>
    <i>Optional</i><br>
    Dictionary of strings that are logged to the console or used somewhere to generate the bio. Default logstrings are <i href="https://github.com/LaptopCat/livebio-tg/blob/main/main.py#L26">on line 26 of main.py</i>
  </details>
  </blockquote>
</details>
Each plugin will have a reference on how you need to configure it.

[What authentication mode should I choose, and why?](AUTH.md)

[How do I make a template?](TEMPLATE.md)

Example Config (has some plugin configs):
```python
{
  "telegram": {
    "app": {
      "id": int(4664),
      "hash": str("asdf")
    },
    "auth": {
      "mode": mode_enum("string"),
      "string": str("12i3j1ijsewetweT")
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
      "token": str("Asdasfasfasdf"),
      "user": int(4664),
      "pass_custom": False
    }
  }
}
```

## Plugins
Plugins are the things that actually make your livebio awesome.

### [Plugins](https://github.com/LaptopCat/livebio-plugins)
