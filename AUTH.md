# What authentication mode should I choose, and why?

## It depends on your preference.

If you intend to deploy livebio, I recommend you to use the string mode.

If you want to use it on your desktop, you can use any mode.

# What is the difference?

## String

string mode uses a Session String to authenticate on Telegram.

You can use the session.py helper script provided with the project to get a session string.

A session string looks like this:
```
1aaNk8EX-YRfwoRsebUkugFvht6DUPi_Q25UOCzOAqzcAjf7jfdv9E0
```

## File

file mode stores a livebio.session file in the program directory, with session data required to authenticate inside.

With this mode, the program will ask you to log into your telegram account if there is no livebio.session file

> # You shouldn't leak your session file / session string as it gives people access to your telegram account
