import pandas as pd
# Assuming values_check.py contains analyze_company_support
from values_check import analyze_company_support 
# Assuming email_crafting.py now contains the modified generate_cold_email
from email_crafting import generate_cold_email 
# Assuming linkeding_message_crafting.py contains generate_linkedin_connection_note
from linkeding_message_crafting import generate_linkedin_connection_note 

def process_excel_filter_and_generate_emails(
    input_filename='apollo_data.xlsx',
    output_filename='apollo_filtered_emails_output.xlsx',
    instructions_email='',
    instructions_linkedin='',
    limit_rows=-1    # limit row for testing, put -1 for full data
):
    # Read Excel file and limit rows for testing
    # Specify all columns you intend to use to avoid issues if some are missing initially
    df = pd.read_excel(input_filename, usecols=["company website", "posts"], engine='openpyxl')
    
    if limit_rows != -1:
        df = df.head(limit_rows)

    analysis_results = []
    explanations = []
    generated_email_subjects = [] # New list for subjects
    generated_email_bodies = []   # Modified to store only the body
    generated_linkedin_messages = []
    
    # Initialize new columns as empty strings
    df['email_subject'] = ''      # New column for subject line
    df['email_body'] = ''         # This will now hold only the body
    df['email'] = ''              # Placeholder for updated emails (if manually edited later)
    df['drafted'] = ''
    df['date_of_drafting'] = ''


    for index, row in df.iterrows():
        company_website = str(row["company website"]).strip()
        posts = str(row["posts"]).strip()

        print(f"\nAnalyzing row {index + 1}: {company_website}")

        # Call analyze_company_support, returns (bool, explanation)
        is_true, explanation = analyze_company_support(company_website, posts)

        analysis_results.append(is_true)
        explanations.append(explanation)

        email_subject = ""
        email_body = ""

        if not is_true:
            print(f"Company evaluated as FALSE - generating email...")
            # Call the modified generate_cold_email which returns a tuple
            email_subject, email_body = generate_cold_email(company_website, posts, instructions_email)
        else:
            print(f"Company evaluated as TRUE - skipping email generation.")
            # Subject and body remain empty for skipped companies

        generated_email_subjects.append(email_subject)
        generated_email_bodies.append(email_body) # Store only the body here

        # Generate LinkedIn connection note regardless of analysis result (or you can add logic if needed)
        linkedin_message = generate_linkedin_connection_note(company_website, posts, instructions_linkedin, return_response=True)
        generated_linkedin_messages.append(linkedin_message)

    # Add new columns to DataFrame
    df['supports_israel_or_haram'] = analysis_results
    df['explanation'] = explanations
    df['email_subject'] = generated_email_subjects  # Populate new subject column
    df['generated_email'] = generated_email_bodies  # This now contains only the body, renamed for clarity in output
    df['linkedin_message'] = generated_linkedin_messages

    # Reorder columns explicitly
    desired_column_order = [
        "company website",
        "posts",
        "supports_israel_or_haram",
        "explanation",
        "email_subject",        # New position for subject
        "generated_email",      # This now holds the body
        "email",                # Your manually updated email column
        "linkedin_message",
        "drafted",
        "date_of_drafting"
    ]
    
    existing_columns = df.columns.tolist()
    final_column_order = [col for col in desired_column_order if col in existing_columns]
    
    df = df[final_column_order]

    # Save to new Excel file
    df.to_excel(output_filename, index=False)
    print(f"\nFiltered emails, explanations, and LinkedIn messages saved to {output_filename}")






if __name__ == "__main__":
    
    # Paste your detailed instructions here
    linkedin_instructions = (
        "Create a concise, polite LinkedIn connection note for cold outreach, personalized using the company website and LinkedIn posts."
    )
    
    email_instructions = """
Comprehensive Guidelines for High-Reply Cold Emails
To generate high-reply cold emails for executives, I will follow these guidelines:

Research & Personalization (Your Input)
I will use the prospect's:

LinkedIn Profile/Posts: For deep research into their personal interests, professional insights, recent activities, shared philosophies/mindset, and company context.
Company Website: For understanding their core business, services, key challenges, goals, and regional focus.
Common SaaS Customer Pain Points: (For my reference to integrate as relevant to the prospect's context. Your chatbot addresses these):
Overwhelmed Support Teams: Customer support teams are drowning in repetitive inquiries, leading to email overload and an endless cycle of tickets.
Slow Customer Response Times: Customers expect immediate answers 24/7, but human teams can't always provide instant, around-the-clock support.
Technical Implementation Barriers: Building sophisticated chatbots typically requires significant technical resources and AI expertise, preventing companies from freeing up their team's time with automated support.
Wasted Potential: Support teams spend too much valuable time on routine, low-value queries instead of focusing on complex tasks that truly leverage their skills.
Inconsistent Brand Representation: Generic chatbot solutions lack the customization needed to perfectly match your brand's visual identity, tone, and specific interaction guidelines.
Email Crafting Principles (Strict Adherence)
The email will be structured and written according to these rules:

Subject Line (Key to Open)
Highly personalized: It should only make sense to the specific recipient.
Use '+' signs: To break up verbiage.
Authentic: Avoid generic, salesy language; be human and authentic. The hook must feel genuine, not misleading.
Length: Secondary to personalization (do not adhere to less than four words).
First Sentence (Preview Text / Hook)
Introduction: Either: "As-salamu alaikum [Name]
We have yet to be properly introduced, but I'm Otmane Hanine and..." (signals prior research).
Personalization: Or: Immediately reference a specific, authentic detail from their profile (e.g., a post, a personal interest) and tie it back.
Website Pivot (If no personal insights): If personal LinkedIn insights are lacking or feel inauthentic to leverage, pivot to referencing specific, observable information from their company website (e.g., core services, specific challenges they address, stated goals). Directly connect this to a common industry pain point that your chatbot solves. Frame this connection genuinely, showing an understanding of their business.
Value Proposition (Challenge Solved)
Specific Challenge: Focus on the exact challenge your conversational AI chatbot solves for this particular buyer and their company, drawing directly from and personalizing the common pain points.
Relatable Examples: When discussing pain points like "overwhelmed support teams," provide specific, relatable examples of the types of questions or information needs related to their company's services, products, or industry context (e.g., "questions about NCA compliance," "how to set up data protection," etc.). This makes the pain point concrete.
Objection Handling: Anticipate and address common objections/rebuttals within the email itself.
Product Context
My chatbot is a RAG solution. It empowers my customers (the users of my SaaS platform) to create their own custom chatbots by scraping web content from their specified sources and/or by allowing them to upload their own content (e.g., documents, FAQs). This content is then used to train their specific chatbot.
It is focused on the Arabic region.
Critical Constraint
NEVER use the word 'agent' to describe my product, as it's a conversational chatbot, not technical tech terms that prospect won't understand, words like scrape, rag,... .
Authenticity & Partnership (Unique Value Proposition)
New Venture: Convey authenticity about being a new venture.
Collaborative Shaping: Emphasize a desire to partner with forward-thinking companies to collaboratively shape and refine the product for the Arabic region, making it clear they would be early adopters.
Email Body Length
Aim for more comprehensive emails (longer than typical short ones) to fully convince the buyer that time spent with me will be valuable.
Call to Action (CTA)
AVOID: Calendar links; specific short timelines (e.g., 'tomorrow,' 'Monday at 1 pm').
RECOMMENDED Format: "Do you have time over the next week or two to learn more? Let me know what works for you and I'll send a calendar invite along accordingly."
Tone & Language
Professional & Respectful: Maintain a tone suitable for executives.
6th/7th Grade Level (HIGHLY EMPHASIZED): Adjust language complexity throughout the entire email to be easily understood by a 6th or 7th grader. This means using simple vocabulary, shorter sentences, and direct phrasing.

"""

    process_excel_filter_and_generate_emails(
        input_filename='apollo_data.xlsx',
        output_filename='apollo_filtered_emails_output.xlsx',
        instructions_email=email_instructions,
        instructions_linkedin=linkedin_instructions,
        limit_rows=3
    )
