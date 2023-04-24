from helpers import mode_enum, Objectify
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
    "template": str("i use livebio btw")
  },
  "plugins": {
    
  }
})
