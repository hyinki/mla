import requests
from bs4 import BeautifulSoup
import concurrent.futures
import random
import time
import csv

# Darius ScraperAPI key
SCRAPERAPI_KEY = ''

# Base URL of the Skytrax Singapore Airlines review page
BASE_URL = 'https://www.airlinequality.com/airline-reviews/singapore-airlines/?sortby=post_date%3ADesc&pagesize=100'

# User-Agent rotation list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def get_scraperapi_url(url):
    return f'http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={url}'

def scrape_page(url):
    headers = {"User-Agent": random.choice(user_agents)}
    response = requests.get(get_scraperapi_url(url), headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    scraped_data = []
    
    # Skytrax review container
    review_containers = soup.find_all('article', {'itemprop': 'review'})
    for container in review_containers:
        title = container.find('h2', class_='text_header')
        review = container.find('div', class_='text_content')
        date = container.find('meta', {'itemprop': 'datePublished'})  # Adjusted to find the <meta> tag
        rating = container.find('span', {'itemprop': 'ratingValue'})  # Adjusted to find the span with ratingValue

        if title and review and date and rating:
            title_text = title.get_text(strip=True)
            review_text = review.get_text(strip=True)
            year_published = date.get('content').split('-')[0]  # Extract the year from date format "YYYY-MM-DD"
            month_published = date.get('content').split('-')[1]  # Extract the month from date format "YYYY-MM-DD"
            rating_value = rating.get_text(strip=True)  # Extract the rating value directly from the span
        
            review_data = (year_published, month_published, title_text, review_text,rating_value)
            scraped_data.append(review_data)

            # Logging the collected review data
            print(f"Collected Review: {review_data}")
                
    time.sleep(random.uniform(2, 6))  # Increase the random delay range
    return scraped_data

def scrape_multiple_pages_parallel(output_file, max_pages=50):
    current_url = BASE_URL
    all_reviews = []
    seen_urls = set()
    scraped_urls = 0
    page_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(scrape_page, current_url): current_url}

        while future_to_url:
            if page_count >= max_pages:
                print(f"Reached the maximum page limit of {max_pages}. Stopping.")
                break
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                page_count += 1
                try:
                    page_reviews = future.result()
                    if page_reviews:
                        all_reviews.extend(page_reviews)
                        scraped_urls += 1
                        print(f"Scraped {scraped_urls} pages so far. Total reviews collected: {len(all_reviews)}")

                    # Logging the URL being scraped
                    print(f"Scraped URL: {url}")

                    # Find the next page URL (Skytrax's pagination)
                    soup = BeautifulSoup(requests.get(get_scraperapi_url(url)).content, 'html.parser')
                    next_button = soup.find('a', string='>>')  # Finds the "Next" button by its text ">>"
                    
                    if next_button and 'href' in next_button.attrs:
                        next_url = 'https://www.airlinequality.com' + next_button['href']
                        if next_url not in seen_urls:
                            seen_urls.add(next_url)
                            future_to_url[executor.submit(scrape_page, next_url)] = next_url
                except Exception as e:
                    print(f"Error scraping {url}: {e}")
                finally:
                    del future_to_url[future]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Month", "Title", "Review Text", "Rating"])
        writer.writerows(all_reviews)
        print(f"Data written to CSV: {len(all_reviews)} reviews")

    print(f"Scraping completed! Data saved to {output_file}")

# Run the parallel scraper
output_file = 'skytrax_SIA_reviews.csv'
scrape_multiple_pages_parallel(output_file)