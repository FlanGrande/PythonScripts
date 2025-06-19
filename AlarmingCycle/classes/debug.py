import os
import time
from datetime import datetime
import classes.config as Config
import classes.globals as Globals

class Debug:
    def __init__(self):
        pass

    @staticmethod
    def is_debug_enabled() -> bool:
        return Config.get_config_value("debug", Globals.app_name)

    @staticmethod
    def is_logging_enabled() -> bool:
        return Config.get_config_value("debug_log", Globals.app_name)

    @staticmethod
    def print_debug_message(topic: str, message: str) -> None:
        if Debug.is_debug_enabled():
            print(f"[DEBUG] {topic}:")
            print(message)
        
        if Debug.is_logging_enabled():
            Debug.log_debug_message(topic, message)

    @staticmethod
    def log_debug_message(topic: str, message: str) -> None:
        # Remove any new lines from the topic and message
        if isinstance(topic, str) and isinstance(message, str):
            topic = topic.replace("\n", "")
            message = message.replace("\n", "")

        if not os.path.exists("log"):
            os.makedirs("log")
        
        with open(f"log/{Globals.app_name}-{datetime.now().strftime('%Y-%m-%d')}-debug.log", "a", encoding="UTF-8") as file:
            file.write(f"[{time.ctime()}] {str.upper(topic)}: {message}\n")