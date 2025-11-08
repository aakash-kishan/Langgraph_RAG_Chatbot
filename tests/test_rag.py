import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_dummy_retriever():
    class Dummy:
        def invoke(self, q): return ["a","b"]

    r = Dummy()
    docs = r.invoke("test")
    assert len(docs) > 0
