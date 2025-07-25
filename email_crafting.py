import os
from google import genai
from google.genai.types import GenerateContentConfig

# Initialize Gemini client (make sure GEMINI_API_KEY is set in your environment)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_cold_email(company_website: str, posts: str, instructions: str) -> tuple[str, str]:
    """
    Generate a personalized cold email (subject and body) using Gemini AI without web search tool.

    Args:
        company_website (str): URL of the company website.
        posts (str): LinkedIn posts or social media content for personalization.
        instructions (str): Full detailed instructions for email crafting.

    Returns:
        tuple[str, str]: A tuple containing (subject_line, email_body).
                        Returns (error_msg, error_msg) if an error occurs.
    """

    # Added clear instructions for formatting the output with a separator
    prompt = f"""
Company Website:
{company_website}

LinkedIn Posts:
{posts if posts.strip() else "No specific social media content provided."}

Instructions:
{instructions}

Please write a full cold email including subject line and body based on the above.
Crucially, format your response strictly as follows:
---SUBJECT_START---
[Your Generated Subject Line Here]
---SUBJECT_END---
---BODY_START---
[Your Generated Email Body Here]
---BODY_END---
Do not include any other text or formatting outside these delimiters.
"""

    config = GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.7,
        tools=[]  # No search tool enabled
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=config
        )
        full_response_text = response.text.strip()

        # Parse the response to extract subject and body
        subject_start_tag = "---SUBJECT_START---"
        subject_end_tag = "---SUBJECT_END---"
        body_start_tag = "---BODY_START---"
        body_end_tag = "---BODY_END---"

        subject_line = ""
        email_body = ""

        if subject_start_tag in full_response_text and subject_end_tag in full_response_text:
            subject_start_index = full_response_text.find(subject_start_tag) + len(subject_start_tag)
            subject_end_index = full_response_text.find(subject_end_tag)
            subject_line = full_response_text[subject_start_index:subject_end_index].strip()
        
        if body_start_tag in full_response_text and body_end_tag in full_response_text:
            body_start_index = full_response_text.find(body_start_tag) + len(body_start_tag)
            body_end_index = full_response_text.find(body_end_tag)
            email_body = full_response_text[body_start_index:body_end_index].strip()

        # Fallback if parsing fails or tags are not found
        if not subject_line and not email_body:
            # If tags not found, treat the whole response as body and leave subject empty
            print("Warning: Email parsing failed. Returning full response as body.")
            email_body = full_response_text
            subject_line = "Subject Parsing Failed" # Provide a default subject for clarity

        return subject_line, email_body

    except Exception as e:
        error_msg = f"Error generating email: {e}"
        print(error_msg) # Print error for debugging
        return error_msg, error_msg # Return error message in both parts of the tuple

# Example usage (for testing this module independently)
if __name__ == "__main__":
    test_instructions = """
    Create a very short and direct cold email about a new AI chatbot for customer support.
    Subject line should be concise.
    Body should quickly mention reducing support team workload and improving response times.
    Focus on being brief.
    """
    subject, body = generate_cold_email(
        company_website="https://example.com",
        posts="Recent post about customer service challenges.",
        instructions=test_instructions
    )
    print(f"\n--- Generated Email ---")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")





# === Test the function ===
if __name__ == "__main__":
    test_company_website = "http://www.yallaplus.com/"
    test_posts = (
        """
        0 notifications total

Skip to search

Skip to main content

Keyboard shortcuts
Close jump menu
Search
new feed updates notifications
Home
My Network
Jobs
Messaging
1
1 new notification
Notifications
pickino denero
Me

For Business
Try Premium for MAD0
Abdullah Alrabeh
Abdullah Alrabeh 
CEO @ Yalla Plus | Board Member | Investor

Follow

Message
All activity

Posts

Comments

Images

Reactions
Loaded 12 Posts posts
Feed post number 1
Abdullah Alrabeh
Abdullah Alrabeh reposted this

View Ibrahim Aldlaigan’s  graphic link
Ibrahim AldlaiganIbrahim Aldlaigan
 • 3rd+3rd+
Founder at StreampayFounder at Streampay
1mo •  1 month ago • Visible to anyone on or off LinkedIn

Follow
It’s been a while since I started my journey as Founder & CEO of Streampay, but I wanted to share this update with everyone.

I also never got the chance to do an appreciation post for my time at STV — which was nothing short of exceptional. I’m deeply grateful to everyone I worked with: the team and partners, the founders, and the broader ecosystem. I learned so much.

Excited for what’s coming — simplifying billing & payments with Stream 🚀
…more
Activate to view larger image,
text, logo
Activate to view larger image,
likecelebratelove
346
138 comments
3 reposts

Like

Comment

Repost

Send
Feed post number 2
Abdullah Alrabeh
Abdullah Alrabeh reposted this

Abdullah Alrabeh
Abdullah AlrabehAbdullah Alrabeh
 • 3rd+3rd+
CEO @ Yalla Plus | Board Member | InvestorCEO @ Yalla Plus | Board Member | Investor
9mo • Edited •  9 months ago • Edited • Visible to anyone on or off LinkedIn

Follow
Proud to announce Yalla Plus seed round, driving our mission of empowering the hospitality sector; as we serve 2M customers, in 11 countries, across thousands of locations. Excited for the next chapter of our journey!

فخورون في يلّا بلس بالإعلان عن جولة البذرة الاستثمارية، لننطلق بمهمتنا لتمكين قطاع الضيافة، ونخدم ملايين المستفيدين، وآلاف منشآت الضيافة، في ١١ دولة حول العالم!
…more

Yalla PlusYalla Plus
19,602 followers19,602 followers
9mo • Edited •  9 months ago • Edited • Visible to anyone on or off LinkedIn

Follow
فخورون بالإعلان عن إغلاق جولة استثمارية بقيمة 10,000,000 ريال بقيادة ميراك كابيتال Merak Capital ، ومشاركة خوارزمي ڤنتشرز Khwarizmi Ventures ومستثمرين عالميّين، لبناء الشريك التقني الأول لقطاع الضيافة في المنطقة.

نسعى من خلال هذا الاستثمار إلى بناء عملاق تقني سعودي يخدم 100 ألف رائد أعمال خلال السنوات الخمس المقبلة في قطاع الضيافة والتجزئة.
لمزيد من التفاصيل : http://bit.ly/3WTRPI8

hashtag#venturecapital hashtag#startups hashtag#fundraising hashtag#yallaplus
…more

Show translation
Activate to view larger image,
يسعدنا الإعلان عن إغلاق جولة استثمارية بقيمة 10 مليون ريال مدعومة من مستثمرين عالميين لتعزيز الابتكار وبناء مستقبل تقني قوي في المملكة.

نؤمن بأن شركاءنا من العملاء والمستثمرين هم الأساس الذي نبني عليه لتقديم حلول مبتكرة ودعم رواد الأعمال من المطاعم والمقاهي والشركات في كل مكان. 
نسعى من خلال هذا الاستثمار إلى بناء عملاق تقني سعودي يخدم 100 ألف رائد أعمال خلال السنوات الخمس المقبلة في قطاع الضيافة وتجار التجزئة.

#venturecapital #startups #fundraising #yallaplus
Activate to view larger image,
likecelebratelove
297
53 comments
14 reposts

Like

Comment

Repost

Send
Feed post number 3
Abdullah Alrabeh
Abdullah AlrabehAbdullah Alrabeh
 • 3rd+3rd+
CEO @ Yalla Plus | Board Member | InvestorCEO @ Yalla Plus | Board Member | Investor
9mo • Edited •  9 months ago • Edited • Visible to anyone on or off LinkedIn

Follow

Proud to announce Yalla Plus seed round, driving our mission of empowering the hospitality sector; as we serve 2M customers, in 11 countries, across thousands of locations. Excited for the next chapter of our journey!

فخورون في يلّا بلس بالإعلان عن جولة البذرة الاستثمارية، لننطلق بمهمتنا لتمكين قطاع الضيافة، ونخدم ملايين المستفيدين، وآلاف منشآت الضيافة، في ١١ دولة حول العالم!
…more

Yalla PlusYalla Plus
19,602 followers19,602 followers
9mo • Edited •  9 months ago • Edited • Visible to anyone on or off LinkedIn

Follow
فخورون بالإعلان عن إغلاق جولة استثمارية بقيمة 10,000,000 ريال بقيادة ميراك كابيتال Merak Capital ، ومشاركة خوارزمي ڤنتشرز Khwarizmi Ventures ومستثمرين عالميّين، لبناء الشريك التقني الأول لقطاع الضيافة في المنطقة.

نسعى من خلال هذا الاستثمار إلى بناء عملاق تقني سعودي يخدم 100 ألف رائد أعمال خلال السنوات الخمس المقبلة في قطاع الضيافة والتجزئة.
لمزيد من التفاصيل : http://bit.ly/3WTRPI8

hashtag#venturecapital hashtag#startups hashtag#fundraising hashtag#yallaplus
…more

Show translation
Activate to view larger image,
يسعدنا الإعلان عن إغلاق جولة استثمارية بقيمة 10 مليون ريال مدعومة من مستثمرين عالميين لتعزيز الابتكار وبناء مستقبل تقني قوي في المملكة.

نؤمن بأن شركاءنا من العملاء والمستثمرين هم الأساس الذي نبني عليه لتقديم حلول مبتكرة ودعم رواد الأعمال من المطاعم والمقاهي والشركات في كل مكان. 
نسعى من خلال هذا الاستثمار إلى بناء عملاق تقني سعودي يخدم 100 ألف رائد أعمال خلال السنوات الخمس المقبلة في قطاع الضيافة وتجار التجزئة.

#venturecapital #startups #fundraising #yallaplus
Activate to view larger image,
likecelebratelove
297
53 comments
14 reposts

Like

Comment

Repost

Send
Feed post number 4
Abdullah Alrabeh
Abdullah Alrabeh reposted this

View Larry Fink’s  graphic link
Larry FinkLarry Fink
  • 3rd+Influencer • 3rd+
Chairman and CEO at BlackRockChairman and CEO at BlackRock
1yr •  1 year ago • Visible to anyone on or off LinkedIn

Follow
This week, I visited Saudi Arabia along with many of our clients who are interested in learning more about the country's future and investment opportunities. The Kingdom is undergoing a rapid transformation, changing from an oil-and-gas nation to a modern diversified economy – a country with strong technology, manufacturing, tourism and renewable energy sectors.

According to Saudi Arabia’s National Investment Strategy, this transformation is going to take an estimated $3.3 trillion dollars by the end of the decade, which makes Saudi Arabia’s “Vision 2030” one of the largest economic development efforts in history. To transform the economy, Saudi Arabia will need to draw in outside financing, which creates significant investment opportunities.

So, together with the Ministry of Finance of Saudi Arabia, we convened a summit for the CEOs and CIOs of some of our largest clients around the world to deepen their knowledge of the investment landscape in the country. These investments will broaden the Saudi equity and fixed income markets, and drive economic diversification in mining, manufacturing, and tourism. We all found the discussions rewarding and insightful.

A few other things happened in Saudi Arabia this week. We announced the formation of BlackRock Riyadh Investment Management, a new project with Public Investment Fund (PIF). It’s a multi-asset class investment platform that will be managed by a Riyadh-based portfolio management team and supported by BlackRock’s global distribution and research capabilities. 

And on Monday, the Kingdom put on an impressive display of convening power by hosting the World Economic Forum hashtag#specialmeeting24, at which I participated in an interesting panel about investing in turbulent times and the shifting geopolitical landscape’s impact on the world economy.
…more
Activate to view larger image,
No alternative text description for this image
Activate to view larger image,
likecelebrateinsightful
6,286
204 comments
211 reposts

Like

Comment

Repost

Send
Feed post number 5
Abdullah Alrabeh
Abdullah Alrabeh reposted this

View Abdulmajeed Alsukhan’s  graphic link
Abdulmajeed AlsukhanAbdulmajeed Alsukhan
 • 3rd+3rd+
Driven By ImpactDriven By Impact
1yr • Edited •  1 year ago • Edited • Visible to anyone on or off LinkedIn

Follow
Graduates programs are an integral part of our stratgy in building a generational company. It fills me with pride and joy to see the brightest talents in the region join our mission in empowering YOU with financial services you deserve.

Join us, lets build the future of daily banking 🚀
…more

TamaraTamara
201,750 followers201,750 followers
1yr •  1 year ago • Visible to anyone on or off LinkedIn

Follow
Calling all future Business Analysts! Ready to launch your career with us? As the Kingdom's leading fintech unicorn, we're all about rapid growth and innovation. And guess what? We want YOU to be part of our journey!🚀

Introducing our exclusive Business Analyst Graduate Program, designed to cultivate the next generation of analytical experts. Over 12 dynamic months, you'll immerse yourself in data analysis while honing your expertise across multiple business domains.👨🏻‍💻

We're on the lookout for top-tier Saudi talent who excel in problem-solving, thrive on challenges, and execute with precision.🇸🇦

If you are eager to embark on a transformative learning adventure and join a team committed to your success, then don't wait! Apply now and be part of shaping the future of fintech with us.📝

Learn more: https://lnkd.in/gVPMdrxk
…more
cms-image
Our Business Analyst Graduate Program transforms exceptional graduates into the change-makers of Saudi Arabia
tamara.co
likecelebratelove
170
8 comments
11 reposts

Like

Comment

Repost

Send
Feed post number 6
Abdullah Alrabeh
Abdullah Alrabeh reposted this


SoumSoum
56,398 followers56,398 followers
1yr • Edited •  1 year ago • Edited • Visible to anyone on or off LinkedIn

Follow
Today and after two years of launching!

We are thrilled to announce that we successfully secured $18 million in Series A funding led by Jahez International Company, with participation from Isometry Capital along with existing investors participating, Khwarizmi Ventures, AlRajhi Partners and Outliers Venture Capital.

We are proudly serving 4 million users across 150+ cities, with a remarkable 40x growth in sales over the past 18 months. Here's to the journey and the exciting road ahead

This Series A funding will accelerate the company’s expansion regionally, as well as beyond its core vertical of secondhand electronics in which it enjoys market leadership in KSA.

As we closed this round, we are sure the best is yet to come for Soumers and Soum's customers
…more

Re-commerce marketplace Soum gets $18M backing to scale in MENA | TechCrunch
techcrunch.com
likecelebratelove
717
66 comments
58 reposts

Like

Comment

Repost

Send
Feed post number 7
Abdullah Alrabeh
Abdullah Alrabeh reposted this

View Roderico (Rocco) Puno’s  graphic link
Roderico (Rocco) PunoRoderico (Rocco) Puno
 • 3rd+3rd+
Southeast Asia for OpenFXSoutheast Asia for OpenFX
1yr • Edited •  1 year ago • Edited • Visible to anyone on or off LinkedIn

Follow
After (very tiny) angel investments at Asaak and XSwap, I've decided to reach far outside my comfort zone and join the movement for financial inclusion by joining TANGGapp 🎉 

Ever since I could remember I always wanted to build something for my fellow countrymen. From the moment I met Rebecca and heard about her idea to use tech to reduce remittance fees and create more convenient international payment options for Filipinos, I was hooked. I can think of no better way to align my career with my values than to help build wealth for those who sacrifice the most for their loved ones. 

I'm incredibly excited to be joining this amazing team and to begin this new journey. Let's build ⚒ 💪
…more


Starting a New Position
likecelebratelove
225
17 comments
1 repost

Like

Comment

Repost

Send
Feed post number 8
Abdullah Alrabeh
Abdullah Alrabeh reposted this


MisMar | مسمارMisMar | مسمار
9,010 followers9,010 followers
2yr •  2 years ago • Visible to anyone on or off LinkedIn

Follow
Once Again, hashtag#MisMar is Top Charting the Saudi hashtag#AppStore
Activate to view larger image,
graphical user interface, application
Activate to view larger image,
likecelebratelove
61
2 comments
3 reposts

Like

Comment

Repost

Send
Feed post number 9
Abdullah Alrabeh
Abdullah Alrabeh reposted this


SoumSoum
56,398 followers56,398 followers
2yr •  2 years ago • Visible to anyone on or off LinkedIn

Follow
!سعيدين بكوننا التطبيق الأول في المملكة في متجر تطبيقات أبل

We’re happy to be ranked the #1 app in the app store again across all apps in the iOS app store!
…more
Activate to view larger image,
No alternative text description for this image
Activate to view larger image,
likecelebratelove
202
5 comments
25 reposts

Like

Comment

Repost

Send
Feed post number 10
Abdullah Alrabeh
Abdullah Alrabeh reposted this

Abdullah Alrabeh
Abdullah AlrabehAbdullah Alrabeh
 • 3rd+3rd+
CEO @ Yalla Plus | Board Member | InvestorCEO @ Yalla Plus | Board Member | Investor
2yr •  2 years ago • Visible to anyone on or off LinkedIn

Follow
As hashtag#LEAP23 concluded, it's become evident that Saudi Arabia has cemented its position as the regional tech hub. In a few short years, Riyadh has leaped from a nascent tech ecosystem, into becoming the launchpad of choice for thousands of entrepreneurs, startups, and tech investors. It’s the place where several secular macro trends converge: young tech-savvy population, strong digital infrastructure, advanced gov services, and forward-thinking policies. At the same time, many of the historical business and social barriers have been eliminated, and new industries, like tourism and entertainment, are open for business. The results of such macro changes often panout over several decades, but the early results are very promising. Today, early stage Saudi startups such as Drahim | دراهمjoined YC; rocketships like Tamara got backed by top global investors; and late stage companies like Jahez International Company went public. On the other hand, Saudi tech investors are more active than ever; as Sanabil Investments, Impact46, and STV, all led $100M+ rounds; SVC deployed more than $500M, and many new funds entered the market. All these signals indicate a broader long-term shift in the regional technological landscape, with Saudi Arabia accelerating towards a future filled with boundless potential. Thank you to all the enablers of the ecosystem, and especially Abdullah Alswaha, and the great team of Ministry of Communications and Information Technology of Saudi Arabia
 hashtag#saudiarabia
…more

No alternative text description for this image

No alternative text description for this image
Activate to view larger image,
likelovecelebrate
149
13 reposts

Like

Comment

Repost

Send
Feed post number 11
Abdullah Alrabeh
Abdullah AlrabehAbdullah Alrabeh
 • 3rd+3rd+
CEO @ Yalla Plus | Board Member | InvestorCEO @ Yalla Plus | Board Member | Investor
2yr •  2 years ago • Visible to anyone on or off LinkedIn

Follow

As hashtag#LEAP23 concluded, it's become evident that Saudi Arabia has cemented its position as the regional tech hub. In a few short years, Riyadh has leaped from a nascent tech ecosystem, into becoming the launchpad of choice for thousands of entrepreneurs, startups, and tech investors. It’s the place where several secular macro trends converge: young tech-savvy population, strong digital infrastructure, advanced gov services, and forward-thinking policies. At the same time, many of the historical business and social barriers have been eliminated, and new industries, like tourism and entertainment, are open for business. The results of such macro changes often panout over several decades, but the early results are very promising. Today, early stage Saudi startups such as Drahim | دراهمjoined YC; rocketships like Tamara got backed by top global investors; and late stage companies like Jahez International Company went public. On the other hand, Saudi tech investors are more active than ever; as Sanabil Investments, Impact46, and STV, all led $100M+ rounds; SVC deployed more than $500M, and many new funds entered the market. All these signals indicate a broader long-term shift in the regional technological landscape, with Saudi Arabia accelerating towards a future filled with boundless potential. Thank you to all the enablers of the ecosystem, and especially Abdullah Alswaha, and the great team of Ministry of Communications and Information Technology of Saudi Arabia
 hashtag#saudiarabia
…more

No alternative text description for this image

No alternative text description for this image
Activate to view larger image,
likelovecelebrate
149
13 reposts

Like

Comment

Repost

Send
Feed post number 12
Abdullah Alrabeh
Abdullah AlrabehAbdullah Alrabeh
 • 3rd+3rd+
CEO @ Yalla Plus | Board Member | InvestorCEO @ Yalla Plus | Board Member | Investor
2yr • Edited •  2 years ago • Edited • Visible to anyone on or off LinkedIn

Follow

My first born will always have a special place in my heart!

ShgardiShgardi
14,708 followers14,708 followers
2yr •  2 years ago • Visible to anyone on or off LinkedIn

Follow
At Shgardi we are thrilled to have been chosen to be a part of the groundbreaking program, which aims to foster the growth of tech unicorns in Saudi Arabia. This is a testament to the immense potential of Shgardi, and the hard work and growth the team was able to achieve. We are confident that through this program, and the great support of the ecosystem, will be able to reach new heights and make a lasting impact. 🚀

We are proud to be part of this exciting initiative and look forward to the opportunities that it will bring for Shgardi and the startup ecosystem in Saudi Arabia. Thank you Ministry of Communications and Information Technology of Saudi Arabia, Misk Foundation, National Technology Development Program 

Thank you your excellency Abdullah Alswaha and Eng. Bader Alkahail PMP, CICA for cultivating the ecosystem and taking Saudi startups to new heights!
…more

No alternative text description for this image

No alternative text description for this image
Activate to view larger image,
with Abdulaziz Almoosa
likecelebratelove
67

Like

Comment

Repost

Send
People you may knowPeople you may know
From Abdullah's schoolFrom Abdullah's school

Stefan Anders
Stefan Anders
Stefan Anders
Hedge Fund Analyst at Eclipse AI InvestmentsHedge Fund Analyst at Eclipse AI Investments

Connect
Eli from Sooth®
Eli from Sooth®
Eli from Sooth®
Predictive Intelligence System at Sooth®Predictive Intelligence System at Sooth®

Connect
Ben Bingus
Ben Bingus
Ben Bingus
Student at Harvard Business SchoolStudent at Harvard Business School

Connect
Willow Amaris
Willow Amaris
Willow Amaris
Victim Advocate at Safe HorizonVictim Advocate at Safe Horizon

Connect
Sophia Chen
Sophia Chen
Sophia Chen
Student at Harvard Business SchoolStudent at Harvard Business School

Connect

Show more
About
Accessibility
Help Center

Privacy & Terms
Ad Choices
Advertising

Business Services
Get the LinkedIn app
More
 LinkedIn Corporation © 2025
pickino deneroStatus is online
MessagingYou are on the messaging overlay. Press enter to open the list of conversations.

Compose message
You are on the messaging overlay. Press enter to open the list of conversations.

        """
    )
    test_instructions = """
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
Introduction: Either: "As-salamu alaykom [Name], we have yet to be properly introduced, but I'm Otmane Hanine and..." (signals prior research).
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

    email_text = generate_cold_email(test_company_website, test_posts, test_instructions, return_response=True)
    print("\n=== Generated Email ===")
    print(email_text)
