import os
from google import genai
from google.genai.types import Tool, GoogleSearch, GenerateContentConfig

# Load your Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def search_with_gemini(query: str, return_response=False):
    print(f"\n--- Searching with Gemini: ---")

    google_search_tool = Tool(google_search=GoogleSearch())
    config = GenerateContentConfig(tools=[google_search_tool])

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=config
        )
        print("\n--- Gemini's Response ---")
        print(response.text)

        if return_response:
            return response.text

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Ensure your API key is correct and you have internet connectivity.")
        if return_response:
            return f"Error: {e}"


if __name__ == "__main__":
    # Define instruction and query separately
    instruction = ""
    query = "does https://www.nexsysone.com/ supports israel? "

    # Combine instruction and query into a single prompt
    final_prompt = f"{instruction}\nQuestion: {query}"

    # Call the function with the combined prompt
    search_with_gemini(final_prompt)


