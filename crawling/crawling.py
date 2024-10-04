import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from firecrawl import FirecrawlApp
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import re
import time

# MongoDB atlas config
client = MongoClient("mongodb+srv://minhtri171997:test123@cluster0.vv0ot.mongodb.net/?retryWrites=true&w=majority")
db = client['llm_db']
collection = db['llm_collection']

# Initialize FirecrawlApp with API key
api_key = 'fc-62a2871d464f4531b19dd86031cb2750'
app = FirecrawlApp(api_key=api_key)

# embedding model
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# clean markdown
def clean_content(content):
    cleaned = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    cleaned = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '', cleaned)  
    cleaned = re.sub(r'[#*_]', '', cleaned)  
    cleaned = re.sub(r'\s+', ' ', cleaned) 
    return cleaned.strip()

# chunking
def chunk_text(content, chunk_size=512):
    words = content.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# process paragraph with tag <article class="fck_detail"> as viewing the console of vnexpress format
def process_article(article_url):
    print(f"Processing: {article_url}")
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # extract <article class="fck_detail">
    article_content = soup.find('article', class_='fck_detail')
    if article_content:
        paragraphs = article_content.find_all('p', class_='Normal')
        full_content = ' '.join([p.get_text() for p in paragraphs])  # join paragraphs
        cleaned_content = clean_content(full_content)
        
        if cleaned_content:
            chunks = chunk_text(cleaned_content)
            for chunk in chunks:
                embedding = embedding_model.embed_documents([chunk])[0]
                mongo_data = {
                    'text': chunk,
                    'embedding': embedding,
                    'metadata': {}  
                }
                collection.insert_one(mongo_data)
                print(f"Inserted chunk of content from: {article_url}")
                print(chunk)
    else:
        print(f"Content not found for {article_url}")

def crawl_all_categories(main_url, max_articles_per_category=10):
    categories = extract_categories(main_url)
    
    for category_url in categories:
        print(f"Crawling category: {category_url}")
        article_links = extract_articles(category_url)
        for article_url in article_links[:max_articles_per_category]:
            try:
                process_article(article_url)
                time.sleep(1)  # delay avoid being exceed quota crawling token
            except Exception as e:
                print(f"Error processing article {article_url}: {e}")

def extract_categories(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith(main_url) and 'https://vnexpress.net' in href:
            categories.append(href)
    return list(set(categories))  

def extract_articles(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    article_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('https://vnexpress.net/')]
    return list(set(article_links))

main_url = 'https://vnexpress.net'
crawl_all_categories(main_url, max_articles_per_category=5)
