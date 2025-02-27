# import_test.py
try:
    import langchain_asi
    print(f"Successfully imported langchain_asi from {langchain_asi.__file__}")
    from langchain_asi import ASI1ChatModel
    print("Successfully imported ASI1ChatModel")
except ImportError as e:
    print(f"Import error: {e}")