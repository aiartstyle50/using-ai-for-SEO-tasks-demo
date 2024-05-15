# Using AI to Automate Human-Level SEO Tasks

Demo showcasing AI optimization of a high-level SEO task, illustrating potential for broader automation of expert-driven processes.

## Overview

This repository demonstrates how AI can optimize a small yet crucial part of on-page SEO—a task traditionally requiring the expertise of a seasoned SEO specialist. By automating the process of determining if the page you want to rank matches the type of pages already ranking for a given keyword, this demo illustrates that high-level human thought processes can be optimized. This example suggests that larger parts of the SEO process can also be enhanced with AI.

**Note:** This approach doesn't necessarily replace the human SEO as having human experts review AI outputs often helps avoid unnecessary errors while still saving significant time.

### Features

- **Automated Page-Type Analysis:** Uses AI to classify page types based on headings and text.
- **Comparison with Ranking Pages:** Compares the target page with top-ranking pages to provide insights on necessary optimizations.
- **Integration with SERPER.dev and OpenAI:** Utilizes these APIs for search results and language model processing.

### Prerequisites

- Obtain an API key from [SERPER.dev](https://serper.dev) to crawl Google search results.
- Obtain an API key from [OpenAI](https://openai.com) for the language model.

### Installation

Clone the repository:

```sh
git clone https://github.com/yourusername/using-ai-for-SEO-tasks-demo.git
cd seo-page-type-analysis-demo
```

Install the required Python packages:

```sh
Copy code
pip install -r requirements.txt
```

### Usage

- Configure API Keys:

Replace 'your-serper-api-key' with your SERPER.dev API key in the search_google function.
Replace 'your-openai-key' with your OpenAI API key.
Run the Script:

```sh
Copy code
python main.py
```

- Input Your Target Keyword and Page URL:

Update the keyword variable with the keyword you want to rank for.
Update the target_url variable with the URL of the page you want to rank for this keyword.

### Code Explanation

Here's a breakdown of the main components of the script:

**search_google(query):** Queries Google for the given keyword using the SERPER.dev API and returns the URLs of organic search results.

**scrape_content(url)** Scrapes the headings and text content from the provided URL.

**analyze_content(headings, text):** Uses prompts and crawled data to classify the type of page based on its content.

**Main Execution:** Combines the above functions to compare the target page with the top-ranking pages and provides a final assessment.


### Example Output: 

The below output shows an example final output. The program has crawled the ranking results, compared it with your page, and determined that your page is not the correct type to rank for this keyword. Thus completing the check.

```Page Type Check Result: The majority of ranking content are of page type: (('page_type', 'PLP/Category Page'),) and your content seems to be of page type (('page_type', 'Content Article'),). To rank for this keyword, you will likely need to optimize a page that is: (('page_type', 'PLP/Category Page'),).```

## Conclusion

This demo illustrates how AI can optimize specific high-level SEO tasks, paving the way for broader applications in SEO and beyond. By automating complex decision-making processes, AI can significantly enhance efficiency and accuracy in various domains.
