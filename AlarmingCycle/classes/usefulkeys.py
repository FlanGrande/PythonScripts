class UsefulKey:
    def __init__(self, scan_code: int, name: str, is_keypad: bool) -> None:
        self.scan_code = scan_code
        self.name = name
        self.is_keypad = is_keypad

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, UsefulKey)
            and self.scan_code == other.scan_code
            and self.name == other.name
            and self.is_keypad == other.is_keypad
        )

    def __hash__(self) -> int:
        return hash((self.scan_code, self.name, self.is_keypad))
    
    def __repr__(self) -> str:
        return f"UsefulKey({self.scan_code} => {self.name}, Is Keypad: {self.is_keypad})"

class UsefulKeys:
    def __init__(self) -> None:
        self.useful_keys = [] # This list represents the keys that will be useful or "allowed"
        self.hotkeys = {}

    def add_useful_key(self, key: UsefulKey) -> None:
        self.useful_keys.append(key)

    def add_hotkey(self, label: str, *keys: UsefulKey) -> None:
        self.hotkeys[label] = set([key for key in keys])
    
    def remove_hotkey(self, label: str) -> None:
        del self.hotkeys[label]
    
    def get_hotkey(self, label: str) -> set:
        return self.hotkeys[label]
    
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, UsefulKeys)
            and self.hotkeys == other.hotkeys
        )