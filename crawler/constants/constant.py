import os

LANGUAGE_MODEL_PATH = "https://drive.usercontent.google.com/download?id=1S20Mr4S0uaIr-HAMtFpeZ_eaQEIOd8x2&export=download&authuser=0&confirm=t&uuid=f267de8b-6613-482b-b207-8e407b81ff3d&at=ALoNOgnOI36I_sU3TLvccOwQrYCC%3A1746775757150"
HTTP_SCHEME = "http" + "://"


class RAW_PATH_CONSTANTS:
    MICROSERVER = HTTP_SCHEME + "trusted-micros-api:8010"
    HREF_TIMEOUT = 345600
    LOG_DIRECTORY = os.path.join(os.getcwd(), 'logs')
    SESSION_PATH = "session_data",
    PASTE_UNIQUE_TIMEOUT = 2592000
    S_SIGWIN_PATH = "bash"


class CRAWL_SETTINGS_CONSTANTS:
    S_USER_AGENT = "Mozilla/5.0"


class SPELL_CHECK_CONSTANTS:
    S_DICTIONARY_PATH = os.path.join(os.getcwd(), "raw", "dictionary.txt")
    S_DICTIONARY_MINI_PATH = os.path.join(os.getcwd(), "raw", "dictionary_mini.txt")


class TOR_CONSTANTS:
    S_SHELL_CONFIG_PATH = "/config/tor"
    S_TOR_PATH = "/config/tor"
