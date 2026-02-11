from crawler.constants.constant import RAW_PATH_CONSTANTS, TOR_CONSTANTS


class TOR_COMMANDS:
    S_START = 1
    S_RESTART = 2
    S_GENERATED_CIRCUIT = 3
    S_RELEASE_SESSION = 4
    S_CREATE_SESSION = 5
    S_PROXY = 6


class TOR_CMD_COMMANDS:
    S_START_DIRECT = RAW_PATH_CONSTANTS.S_SIGWIN_PATH + " " + TOR_CONSTANTS.S_SHELL_CONFIG_PATH + " " + TOR_CONSTANTS.S_TOR_PATH + " " + "build-start-tor"
    S_START_DOCKERISED = "." + TOR_CONSTANTS.S_SHELL_CONFIG_PATH + " " + TOR_CONSTANTS.S_TOR_PATH + " " + "build-start-tor"


class TOR_STATUS:
    S_RUNNING = 1
    S_PAUSE = 2
    S_STOP = 3
    S_READY = 4
    S_START = 5
    S_CLOSE = 6


TOR_PROXIES = [
    {
        "http": "socks5h://172.15.0.10:" + "9552",
        "https": "socks5h://172.15.0.10:" + "9552"
    }
    # ,
    # {
    #   "http": "socks5h://172.15.0.11:" + "9554",
    #   "https": "socks5h://172.15.0.11:" + "9554"
    # },
    # {
    #   "http": "socks5h://172.15.0.12:" + "9556",
    #   "https": "socks5h://172.15.0.12:" + "9556"
    # },
    # {
    #   "http": "socks5h://172.15.0.13:" + "9558",
    #   "https": "socks5h://172.15.0.13:" + "9558"
    # },
    # {
    #   "http": "socks5h://172.15.0.14:" + "9560",
    #   "https": "socks5h://172.15.0.14:" + "9560"
    # },
    # {
    #   "http": "socks5h://172.15.0.15:" + "9562",
    #   "https": "socks5h://172.15.0.15:" + "9562"
    # },
    # {
    #   "http": "socks5h://172.15.0.16:" + "9564",
    #   "https": "socks5h://172.15.0.16:" + "9564"
    # },
    # {
    #   "http": "socks5h://172.15.0.17:" + "9566",
    #   "https": "socks5h://172.15.0.17:" + "9566"
    # },
    # {
    #   "http": "socks5h://172.15.0.18:" + "9568",
    #   "https": "socks5h://172.15.0.18:" + "9568"
    # },
    # {
    #   "http": "socks5h://172.15.0.19:" + "9570",
    #   "https": "socks5h://172.15.0.19:" + "9570"
    # }
]
TOR_CONTROL_PROXIES = [
    {
        "proxy": "172.15.0.10",
        "port": 9553
    }
    # ,
    # {
    #   "proxy": "172.15.0.11",
    #   "port": 9555
    # },
    # {
    #   "proxy": "172.15.0.12",
    #   "port": 9557
    # },
    # {
    #   "proxy": "172.15.0.13",
    #   "port": 9559
    # },
    # {
    #   "proxy": "172.15.0.14",
    #   "port": 9561
    # },
    # {
    #   "proxy": "172.15.0.15",
    #   "port": 9563
    # },
    # {
    #   "proxy": "172.15.0.16",
    #   "port": 9565
    # },
    # {
    #   "proxy": "172.15.0.17",
    #   "port": 9567
    # },
    # {
    #   "proxy": "172.15.0.18",
    #   "port": 9569
    # },
    # {
    #   "proxy": "172.15.0.19",
    #   "port": 9571
    # }
]
