import json
from dataclasses import dataclass
from pathlib import Path

from vosk import KaldiRecognizer, Model

@dataclass
class STT_Result:
    text: str
    is_final: bool

class STT_Engine:
    def __init__(self, model_path: str, sample_rate: int = 16000):
        model_dir = Path(model_path)
        if not model_dir.exists():
            raise FileNotFoundError(f"Vosk model not found at '{model_path}.")
        self._model = Model(model_path)
        self._recognizer = KaldiRecognizer(self._model, sample_rate)
        self._recognizer.SetWords(True)

    def process_chunk(self, chunk: bytes) -> STT_Result:
        if self._recognizer.AcceptWaveform(chunk):
            result = json.loads(self._recognizer.Result())
            return STT_Result(text=result.get("text", "").strip(), is_final=True)
        else:
            result = json.loads(self._recognizer.PartialResult())
            return STT_Result(text=result.get("partial", "").strip(), is_final=False)

    def reset(self):
        self._recognizer.Reset()
