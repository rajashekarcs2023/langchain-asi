# tests/test_simple.py
def test_import():
    """Test that langchain_asi can be imported."""
    import langchain_asi
    assert hasattr(langchain_asi, "ASI1ChatModel")