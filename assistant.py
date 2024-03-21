import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

def fetch_search_results(query):
    url = f"https://www.google.com/search?q={query}"  # Replace 'example.com' with the actual search engine URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Error fetching search results")
        return None

def parse_search_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Extract relevant information such as title, URL, and content from search results
    # Example: 
    # titles = [result.find('h3').text for result in soup.find_all('div', class_='result')]
    # urls = [result.a['href'] for result in soup.find_all('div', class_='result')]
    # contents = [result.find('p').text for result in soup.find_all('div', class_='result')]
    # return titles, urls, contents
    pass

def summarize_content(content):
    # Tokenize the content into sentences
    sentences = sent_tokenize(content)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_sentences = [word for word in sentences if word.lower() not in stop_words]
    
    # Calculate word frequency distribution
    words = word_tokenize(" ".join(filtered_sentences))
    fdist = FreqDist(words)
    
    # Select top 3 most frequent words
    top_words = [word for word, _ in fdist.most_common(3)]
    
    # Generate summary by selecting sentences containing top words
    summary = [sentence for sentence in sentences if any(word in sentence.lower() for word in top_words)]
    
    return " ".join(summary)

def main():
    query = input("Enter your search query: ")
    html = fetch_search_results(query)
    if html:
        titles, urls, contents = parse_search_results(html)
        for title, url, content in zip(titles, urls, contents):
            summarized_content = summarize_content(content)
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Summarized Content: {summarized_content}\n")

if __name__ == "__main__":
    main()
