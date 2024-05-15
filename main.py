import http.client
import json
import openai
import requests
from bs4 import BeautifulSoup
from collections import Counter

# Configure the OpenAI API key
client = openai
openai.api_key = "you-openai-key"

def search_google(query):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': 'your-serper-api-key',  # Replace with your actual SERPER.dev API key (we're using this because it's cheaper than SERPAPI)
        'Content-Type': 'application/json'
    }

    try:
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        results = json.loads(data.decode("utf-8"))

        if 'organic' in results:
            urls = [item['link'] for item in results['organic']]  # Fetching links from organic results
            print(f"Google search returned URLs: {urls}")
            return urls
        else:
            print("Google search did not return any organic results.")
            return []  # Return an empty list if there are no organic results
    except Exception as e:
        print(f"Error during Google search: {e}")
        return []  # Return an empty list in case of exceptions

def scrape_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'], limit=15)]
        text = ' '.join(soup.stripped_strings)[:500]
        if headings and text:
            print(f"Scraped content from {url}: HEADINGS: {headings}, TEXT: {text[:100]}...")
        else:
            print(f"No valid content found for {url}")
        return headings, text
    except Exception as e:
        print(f"Error during scraping content from {url}: {e}")
        return [], ""

def analyze_content(headings, text):
    try:
        prompt = f"I will provide a sample of the headings and the text. Based on the provided information, please give your best assessment as to what type of page this is. Options include: PLP/Category Page, PDP/Product Page, Content Article, 'Best' List, or Other. If Other, provide a short descriptive title of what to call it. Output as a JSON object with no other text.\n\nSAMPLE HEADINGS: {headings}\nSAMPLE PAGE TEXT: {text}\nOUTPUT:"
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        analysis_result = json.loads(response.choices[0].message.content.strip())
        print(f"Analysis result for content: {analysis_result}")
        return analysis_result
    except Exception as e:
        print(f"Error during content analysis: {e}")
        return {}

# Main execution
keyword = "enter your target keyword" # Enter the target keyword (the keyword you want to rank for)
target_url = "enter your web page URL"  # Enter the URL of the page you're trying to rank for the target keyword
urls = search_google(keyword) + [target_url]
results = {}

for url in urls:
    if url.startswith('http'):  # Ensure the URL is valid
        headings, text = scrape_content(url)
        if headings and text:  # Only analyze if we have valid content
            page_type = analyze_content(headings, text)
            results[url] = page_type
        else:
            print(f"Skipping URL due to missing content: {url}")

# Convert dictionaries to tuples of sorted items for counting
types = [tuple(sorted(results[url].items())) for url in urls if url != target_url and url in results]

if types:
    most_common_type = Counter(types).most_common(1)[0][0]
    target_type = tuple(sorted(results[target_url].items()))

    # Generate final assessment prompt
    ranking_content_types = '\n'.join([str(result) for url, result in results.items() if url != target_url])
    our_content_type = str(results[target_url])
    system_prompt = "You are a helpful assistant"
    user_prompt = f"This is the type of content Google considers relevant for our target search term - RANKING CONTENT: {ranking_content_types}\n\nThis is the type of content that our page has - OUR CONTENT: {our_content_type}\n\nIf the majority of content from RANKING CONTENT is a different type than OUR CONTENT, output: 'The majority of ranking content are of page type: {most_common_type}' and your content seems to be of page type {target_type}. To rank for this keyword, you will likely need to optimize a page that is: {most_common_type}.'\n\nHowever, if the majority of RANKING CONTENT and OUR CONTENT are of the SAME page type as the target url (and don't worry about exact terminology as long as they mean the same thing), simply output: %PASS%\n\nIf both types begin with 'Other:' AND the types basically mean the same thing. Then you also output %PASS%"

    try:
        final_assessment = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=150
        )
        output = final_assessment.choices[0].message.content.strip()
        # Check for "%PASS%" in the output and adjust message accordingly
        if "%PASS%" in output:
            print("Page Type Check Passed: Your Page Type is the correct type to rank for this keyword")
        else:
            print(output)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
else:
    print("No valid ranking content types found to compare.")
