import queue
import sounddevice as sd

def mic_chunks(sample_rate: int = 16000, block_size: int = 8000, device = None):
    audio_queue: "queue.Queue[bytes]" = queue.Queue()

    def _callback(indata, frames, time_info, status):
        if status:
            print(f"[mic] stream status: {status}")
        audio_queue.put(bytes(indata))


    with sd.RawInputStream(
        samplerate=sample_rate,
        blocksize=block_size,
        device=device,
        dtype="int16",
        channels=1,
        callback=_callback,
    ):
        while True:
            yield audio_queue.get()