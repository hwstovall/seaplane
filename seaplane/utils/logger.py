from colorama.ansi import Fore


def info_log(message: str):
    print(Fore.CYAN + 'SEAPLANE: ' + message)
