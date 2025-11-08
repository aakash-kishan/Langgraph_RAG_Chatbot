from nodes.synthesis import synthesize
import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_synthesis_basic():
    text = "hello"
    output = synthesize(text)
    assert isinstance(output, str)
    assert len(output) > 0
