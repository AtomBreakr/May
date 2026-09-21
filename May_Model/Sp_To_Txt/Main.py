import sys

from Sp_To_Txt import Config
from Sp_To_Txt.Mic_Stream import mic_chunks
from Sp_To_Txt.Stt_Engine import STT_Engine
from Sp_To_Txt.Wake_Word import State, Wake_Word_Gate

def main():
    print(f"Loading Vosk omdel rom '{Config.MODEL_PATH}' ...")
    stt = STT_Engine(Config.MODEL_PATH, sample_rate=Config.SAMPLE_RATE)
    gate = Wake_Word_Gate(Config.WAKE_WORD)

    print(f"Ready. Say '{Config.WAKE_WORD}' to get my attention. (Ctrl+C to quit)\n")

    try:
        for chunk in mic_chunks(sample_rate=Config.SAMPLE_RATE, block_size=Config.BLOCK_SIZE):
            result = stt.process_chunk(chunk)
            if not result.text and not result.is_final:
                continue

            event = gate.handle(result.text, result.is_final)

            if event.state is State.ACTIVE:
                sys.stdout.write(f"\r[listening] {event.display_text}" + " " * 10)
                sys.stdout.flush()

            if event.command_ready is not None:
                print(f"\n>>> Command captured: '{event.command_ready}'\n")
                print(f"Say '{Config.WAKE_WORD}' again for the next command.\n")

    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()