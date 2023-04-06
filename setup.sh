textinput () {
    printf ">\033[38;5;%sm " "$1"
    read $2
    echo -n "\033[0m"
}
cfg='from helpers import mode_enum, Objectify
### Actual config is below
Config = Objectify({
  "telegram": {
    "app": {
      "id": int(4664),
      "hash": str("Askfdweikltrjhwelkjth")
    },
    "auth": {
      "mode": mode_enum("file"),
      "string": str("isadfiuowehtkwhetkj")
    }
  },
  "script": {
    "splitter": "|",
    "template": str("i use livebio btw"),
    "delay": int(20),
    "max_length": int(70)
  },
  "plugins": {
    
  }
})'
echo "Would you like to configure livebio? You can always do it later. Please note that this will overwrite your current config. [y/n]"
textinput 27 cfg_yn
if [ "$cfg_yn" = "y" ]; then
    echo "You can type nothing and press Enter if you want to skip something"
    echo "Please enter your telegram app api_id (Check Step 3)"
    textinput 27 appid
    echo "Please enter your telegram app api_hash (Check Step 3)"
    textinput 27 apphash
    echo "Please enter your authentication method (default is file) (Check Step 4)"
    textinput 27 tauth
    echo "Please enter your splitter (default is |) (Check Step 4)"
    textinput 27 splitter
    echo "Please enter your template (Check Step 4)"
    textinput 27 template
    echo "Please enter your delay between each operation in seconds (default is 20) (Check Step 4)"
    textinput 27 delay
    echo "Please enter your bio length limit (70 is default, set 140 if you have tg premium) (Check Step 4)"
    textinput 27 maxlength
    string=""
    if [ "$tauth" = "" ]; then
        tauth="file"
    fi

    if [ "$tauth" = "string" ]; then
        echo "Please enter your session string (Check Step 4)"
        textinput 27 string
    fi

    if [ "$splitter" = "" ]; then
        splitter="|"
    fi

    if [ "$delay" = "" ]; then
        delay="20"
    fi

    if [ "$maxlength" = "" ]; then
        maxlength="70"
    fi
    echo "$cfg" | sed "s/4664/$appid/" | sed "s/isadfiuowehtkwhetkj/$string/" | sed "s/Askfdweikltrjhwelkjth/$apphash/" | sed "s/file/$tauth/" | sed "s/|/$splitter/" | sed "s/20/$delay/" | sed "s/70/$maxlength/" | sed "s/i use livebio btw/$template/" > config.py
else
    echo "Operation canceled."
fi
