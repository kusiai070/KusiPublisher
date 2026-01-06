import sys
print("Testing imports...")
try:
    import fastapi
    print("FastAPI imported")
    import uvicorn
    print("Uvicorn imported")
    import google.generativeai as genai
    print("Google Generative AI imported")
    from dotenv import load_dotenv
    print("Dotenv imported")
    print("ALL IMPORTS SUCCESSFUL")
except Exception as e:
    print(f"IMPORT ERROR: {e}")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
