import os

def clearTerminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    