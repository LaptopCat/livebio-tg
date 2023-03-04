# Livebio Templates
Templates show livebio how it needs to generate your bio.

What can you use in templates:
- Any text

(```asfdkja,fknm.dagsk```)
- {%plugin:PLUGIN_NAME%} to use output from PLUGIN_NAME plugin 

(```{%plugin:time%}``` -> ```13:37```)
- {%plugin:PLUGIN_NAMEUNSPLIT%} to use raw output from PLUGIN_NAME plugin 

(```{%plugin:timeUNSPLIT%} {%plugin:time%} {%plugin:time%}``` -> ```13:37 13:37 | 13:37```)


## Template Example
```{%plugin:sinoptikUNSPLIT%} {%plugin:time%}{%plugin:discord%} @lptpcat```
->
```⛅ 13:37 | Playing Minecraft | @lptpcat```
