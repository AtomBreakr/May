from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class State(Enum):
    IDLE = auto()
    ACTIVE = auto()

@dataclass
class Gate_Event:
    state: State
    display_text: str
    command_ready: Optional[str] = None

class Wake_Word_Gate:
    def __init__(self, wake_word: str):
        self.wake_word = wake_word.lower().strip()
        self.state = State.IDLE

    def handle(self, text: str, is_final: bool) -> Gate_Event:
        text_lower = text.lower().strip()

        if self.state is State.IDLE:
            if self.wake_word and self.wake_word in text_lower:
                remainder = text_lower.split(self.wake_word, 1)[1].strip()
                if is_final and remainder:
                    self.state = State.IDLE
                    return Gate_Event(State.IDLE, display_text="", command_ready=remainder)
                self.state = State.ACTIVE
                return Gate_Event(State.ACTIVE, display_text=remainder)
            
            return Gate_Event(State.IDLE, display_text="")

        if is_final:
            self.state = State.IDLE
            return Gate_Event(State.IDLE, display_text=text, command_ready=text_lower or None)
        return Gate_Event(State.ACTIVE, display_text=text)