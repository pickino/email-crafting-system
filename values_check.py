import pandas as pd
from gemini_web_search_query import search_with_gemini

def analyze_company_support(company_website_url: str, prospect_social_content: str):
    instructions = f"""
You are an AI assistant designed to identify if a company, based *entirely on comprehensive web search results*, has *any* confirmed business relationship with Israel or Israeli entities, OR engages in activities widely considered 'haram' (e.g., gambling, pork products, interest-based lending, explicit adult content).

**Company to analyze (identified from website URL):** {company_website_url}

**Instructions for Analysis:**
1.  **Perform a comprehensive web search** for the company identified from the provided URL. Your analysis must rely *solely* on information found through this web search. Do not access or analyze the company's own website content directly; its URL is provided only to identify the company name for the search.
2.  Based on the web search results, determine if *any* of the following conditions are met. If even one condition is met, the overall result for that category (Israeli ties or Haram) is considered TRUE.
    * **Condition A: Direct Israeli Business Relationship:** Is there *any confirmed business relationship* between the company and *any* company or entity based in Israel? This explicitly includes, but is not limited to, partnerships, joint ventures, investments (receiving or making), client relationships, supplier relationships, or providing/receiving services.
    * **Condition B: Indirect Israeli Business Connection (via Pro-Israel Companies):** Is there *any confirmed business relationship* (e.g., partnership, client, supplier, major solution provider) between the company and another company that is publicly known to explicitly support Israel (e.g., through official statements, significant investments in Israel, or strong alignment with Israeli national interests)?
    * **Condition C: Haram Activities:** Is the company involved in core business activities or offers products/services that are widely considered 'haram' (e.g., primary business is alcohol, gambling, interest-based financial services, pork products, adult entertainment)?

**Ur response  Format should STRICTLY STRTS WITH :**
- Start with "TRUE" if **Condition A** OR **Condition B** OR **Condition C** is met.
- Start with "FALSE" if **none** of **Condition A**, **Condition B**, or **Condition C** are met.
- Follow the TRUE/FALSE with a brief, concise sentence explaining the **main reason** for your decision. This explanation MUST directly state which condition(s) were met and provide a specific, concise detail from the web search results (e.g., "TRUE. The company has a partnership with [Israeli company name].").
"""

    # Call Gemini and get response text
    response_text = search_with_gemini(instructions, return_response=True)

    # Determine boolean from response start (case-insensitive)
    is_true = response_text.strip().upper().startswith("TRUE")

    return is_true, response_text


def process_excel_and_write_true_only(input_filename='apollo_data.xlsx', output_filename='apollo_results_true_only.xlsx'):
    # Read Excel file
    df = pd.read_excel(input_filename, usecols=["company website", "posts"], engine='openpyxl')

    # Limit to first 3 rows for testing
    df = df.head(3)

    results = []
    for index, row in df.iterrows():
        company_website_url = str(row["company website"]).strip()
        prospect_social_content = str(row["posts"]).strip()

        print(f"\nProcessing row {index + 1}: {company_website_url}")
        is_true, explanation = analyze_company_support(company_website_url, prospect_social_content)

        if is_true:
            print(f"Result TRUE - adding to output Excel")
            results.append({
                "company website": company_website_url,
                "posts": prospect_social_content,
                "explanation": explanation
            })
        else:
            print(f"Result FALSE - skipping writing to Excel")

    if results:
        results_df = pd.DataFrame(results)
        results_df.to_excel(output_filename, index=False)
        print(f"\nResults saved to {output_filename}")
    else:
        print("\nNo TRUE results found. No Excel file created.")


if __name__ == "__main__":
    process_excel_and_write_true_only()
