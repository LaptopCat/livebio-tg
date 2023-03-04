# livebio-tg
## Make your telegram about me live.


# Installing
## Clean Install
(Installs livebio without any plugins)
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

### 2. Create a Telegram Application
To work, livebio-tg requires a Telegram app to change your bio.

To create a Telegram application, go to this [page](https://my.telegram.org/apps) and log into your Telegram account.

After you login, you will need to fill out a form, you can fill it in with anything you want, but make sure that all fields are filled.

If there is no error while creating an app, you will see a screen with your app info.

You need to copy the "api_id" and the "api_hash" and write them down somewhere (you shouldn't share those values with anyone)

### 3. Configuring livebio
After you cloned the repository, head to the config.py file.

It is a Python dictionary (has JSON-like syntax).

#### Config Structure:

```
telegram:
  app:
    id: "Your api_id here"
    hash: "Your api_hash here"
  auth:
    mode: "Authentication mode here - can be string or file"
```
[What authentication mode should i choose, and why?](AUTH.md)
