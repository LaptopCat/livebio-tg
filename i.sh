textinput () {
    printf ">\033[38;5;%sm " "$1"
    read $2
    echo -n "\033[0m"
}
echo "\033[38;5;160m"
echo "
  _      _______      ________ ____ _____ ____  
 | |    |_   _\ \    / /  ____|  _ \_   _/ __ \ 
 | |      | |  \ \  / /| |__  | |_) || || |  | |
 | |      | |   \ \/ / |  __| |  _ < | || |  | |
 | |____ _| |_   \  /  | |____| |_) || || |__| |
 |______|_____|   \/   |______|____/_____\____/ 
"
echo "\033[0m"
echo "Press Enter to start installation"
textinput 27 none
if [ -d "./livebio-tg" ]; then
    echo "\033[38;5;196mERROR: 'livebio-tg' directory already exists\033[0m"
    echo "Would you like to delete it? This opperation is \033[38;5;196mirreversible\033[0m and may \033[38;5;196mpermanently delete\033[0m your config if it is in that directory [y/n]"
    textinput 196 delete_yn
    if [ "$delete_yn" = "y" ]; then
        rm -rf livebio-tg
        echo "'livebio-tg' has been deleted."
    else
        echo "Operation canceled."
    fi
else
    git clone https://github.com/LaptopCat/livebio-tg
    cd livebio-tg
    echo "\033[38;5;27mInstalling Python dependencies...\033[0m"
    python3 -m pip install telethon 
    python3 -m pip install rich
    chmod +x setup.sh
    ./setup.sh
    echo "Livebio has been setup!"
fi
