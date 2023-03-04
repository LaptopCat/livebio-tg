from helpers import environ, mode_enum, Objectify
### Actual config is below
Config = Objectify({
  "telegram": {
    "app": {
      "id": int(4664),
      "hash": str("Askfdweikltrjhwelkjth")
    },
    "auth": {
      "mode": mode_enum("file"), # "string" or "file"
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
})
