import requests
from bs4 import BeautifulSoup
import concurrent.futures
import random
import time
import csv
from threading import Lock

# ScraperAPI key
SCRAPERAPI_KEY = ''

# Base URL of the TripAdvisor review page
BASE_URL = 'https://www.tripadvisor.com.sg/Airline_Review-d8729151-Reviews-Singapore-Airlines'

# User-Agent rotation list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
]

# Lock for synchronizing review_counts updates
lock = Lock()

def get_scraperapi_url(url):
    return f'http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={url}'

def scrape_page(url, review_counts, max_reviews_per_year):
    headers = {"User-Agent": random.choice(user_agents)}
    response = requests.get(get_scraperapi_url(url), headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    scraped_data = []
    review_containers = soup.find_all('div', class_='lgfjP Gi z pBVnE MD bZHZM')

    for container in review_containers:
        title = container.find('a', class_='Qwuub')
        review = container.find('span', attrs={'data-test-target': 'review-text'})
        date = container.find('span', class_='teHYY')
        rating = container.find('span', class_='ui_bubble_rating')

        if title and review and date and rating:
            title_text = title.get_text(strip=True)
            review_text = review.get_text(strip=True)
            date_text = date.get_text(strip=True).split(':')[-1]
            year = date_text.split()[-1]
            month = date_text.split()[0]
            rating_class = rating['class'][1]
            rating_value = int(rating_class.split('_')[-1]) / 10

            with lock:  # Use lock to update review_counts safely
                if year in review_counts and review_counts[year] < max_reviews_per_year:
                    review_data = (year, month, title_text, review_text, rating_value)
                    scraped_data.append(review_data)
                    review_counts[year] += 1

                    # Logging the collected review data
                    print(f"Collected Review: {review_data}")
                
    time.sleep(random.uniform(2, 6))  # Increase the random delay range
    return scraped_data

def scrape_multiple_pages_parallel(output_file, max_reviews_per_year=1000,max_pages=300):
    current_url = BASE_URL
    all_reviews = []
    review_counts = {'2022': 0, '2023': 0, '2024': 0}
    seen_urls = set()
    scraped_urls = 0
    page_count = 0
    

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(scrape_page, current_url, review_counts, max_reviews_per_year): current_url}

        while future_to_url and not all(count >= max_reviews_per_year for count in review_counts.values()):
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
                        print(f"Scraped {scraped_urls} pages so far. Total reviews collected: {sum(review_counts.values())}")
                        print(f"Review Counts: {review_counts}")

                    # Logging the URL being scraped
                    print(f"Scraped URL: {url}")

                    # Find the next page URL
                    soup = BeautifulSoup(requests.get(get_scraperapi_url(url)).content, 'html.parser')
                    next_button = soup.find('a', class_='ui_button nav next primary')
                    if next_button and 'href' in next_button.attrs:
                        next_url = 'https://www.tripadvisor.com.sg' + next_button['href']
                        if next_url not in seen_urls:
                            seen_urls.add(next_url)
                            future_to_url[executor.submit(scrape_page, next_url, review_counts, max_reviews_per_year)] = next_url
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
output_file = 'tripadvisor_SIA_reviews_parallel.csv'
scrape_multiple_pages_parallel(output_file, max_reviews_per_year=1000)