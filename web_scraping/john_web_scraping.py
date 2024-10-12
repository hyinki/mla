import requests
from bs4 import BeautifulSoup
import time 
from openpyxl import Workbook

# Your ScraperAPI key
API_KEY = 'e61ca48721ffbc2eb375f486f96e6d08'

# Base URL of the page you want to scrape
url = 'https://www.tripadvisor.com.sg/Airline_Review-d8729151-Reviews-Singapore-Airlines'

# Build the ScraperAPI URL
def get_scraperapi_url(url):
    return f'http://api.scraperapi.com?api_key={API_KEY}&url={url}'

count = 0
# Function to get the next page URL
def get_next_page(soup):
    global count 
    count += 1
    # Currently only 10 pages, can do more pages, just change here
    if count == 1:
        return None 
    
    next_button = soup.find('a', class_='ui_button nav next primary')
    if next_button and 'href' in next_button.attrs:
        return 'https://www.tripadvisor.com.sg' + next_button['href']
    return None

# Function to scrape the reviews from a single page
def scrape_reviews(soup):
    titles = soup.find_all('a', class_='Qwuub')
    reviews = soup.find_all('span', attrs={'data-test-target': 'review-text'})
    dates = soup.find_all('span', class_='teHYY _R Me S4 H3')

    scraped_data = []
    if reviews and dates and titles:
        for review, date, title in zip(reviews, dates,titles):
            review_text = review.get_text(strip=True)
            date_text = date.get_text(strip=True)
            title_text = title.get_text(strip=True)
            scraped_data.append((date_text, title_text, review_text))
    return scraped_data

# Scrape reviews from multiple pages and write to Excel
def scrape_multiple_pages_to_excel(start_url, output_file):
    # Create an Excel workbook and select the active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Reviews"
    
    # Set the header row
    sheet.append(["Date", "Title", "Review Text"])

    current_url = start_url
    
    while current_url:
        print(f"Scraping page: {current_url}")
        response = requests.get(get_scraperapi_url(current_url))

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Scrape the current page
            page_reviews = scrape_reviews(soup)
            
            # Write the data to the Excel sheet
            for review_data in page_reviews:
                sheet.append(review_data)

            # Find the next page URL
            current_url = get_next_page(soup)
            
            # Small delay to avoid rate limits
            time.sleep(1)
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            break
    
    # Save the Excel file
    workbook.save(output_file)
    print(f"Scraping completed! Data saved to {output_file}")

# Run the scraper and save data to an Excel file
output_file = 'tripadvisor_reviews.xlsx'
scrape_multiple_pages_to_excel(url, output_file)