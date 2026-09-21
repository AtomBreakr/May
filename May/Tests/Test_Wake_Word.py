import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Sp_To_Txt.Wake_Word import State, Wake_Word_Gate

def test_ignores_speech_without_wake_word():
    gate = Wake_Word_Gate("may")
    event = gate.handle("what a nice day today", is_final=True)
    assert event.state is State.IDLE
    assert event.command_ready is None

def test_wake_word_alone_activates():
    gate = Wake_Word_Gate("may")
    event = gate.handle("may", is_final=True)
    assert event.state is State.ACTIVE
    assert event.command_ready is None

def test_wake_word_with_command():
    gate = Wake_Word_Gate("may")
    event = gate.handle("may what time is it", is_final=True)
    assert event.state is State.IDLE
    assert event.command_ready == "what time is it"

def test_command_captured_after_act():
    gate = Wake_Word_Gate("may")
    gate.handle("may", is_final=True)
    event = gate.handle("what is the weather in ruston", is_final=True)
    assert event.state is State.IDLE
    assert event.command_ready == "what is the weather in ruston"

def test_partial_results_while_active():
    gate = Wake_Word_Gate("may")
    gate.handle("may", is_final=True)
    event = gate.handle("what is", is_final=False)
    assert event.state is State.ACTIVE
    assert event.command_ready is None

def test_case_insensitive():
    gate = Wake_Word_Gate("may")
    event = gate.handle("MAY what time is it", is_final=True)
    assert event.command_ready == "what time is it"

def test_returns_to_idle():
    gate = Wake_Word_Gate("may")
    gate.handle("may", is_final=True)
    gate.handle("what time is it", is_final=True)
    assert gate.state is State.IDLE
    event = gate.handle("random background chatter", is_final=True)
    assert event.state is State.IDLE
    assert event.command_ready is None

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        t()
        passed += 1
        print(f" ok {t.__name__}")
    print(f"\n{passed}/{len(tests)} tests passed")