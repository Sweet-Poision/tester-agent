from langchain_google_genai import ChatGoogleGenerativeAI
fr

try:
    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        max_retries = 3,
        temperature = 0.1,
        max_tokens = None,
    )
except Exception as e:  # noqa: BLE001
    print(f"Error initializing Gemini LLM: {e}")
    llm = None


async 