from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Mars News site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find_all('div', class_='content_title')
    news_title = article[1].text.strip()
    news_paragraph = soup.find('div', class_='article_teaser_body').text.strip()

    # Mars Image site
    base_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    pic_info = soup.find('figure', class_='lede')
    featured_image_url = base_url+image_url
    print(featured_image_url)

    # Mars Facts site
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_df = tables[0]
    mars_df.columns = ['Mars Info', 'Values']
    html_table = mars_df.to_html()

    # Mars Hemisphere Image site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    section = soup.find('div', class_ = 'collapsible results')
    categories = section.find_all('div', class_ = 'description')

    hemisphere_list = []
    url_list = []
    hemisphere_url_list = []

    for category in categories:
        hem = category.find('h3').text.strip()
        hemisphere_list.append(hem)
        hem_url = category.find('a')['href']
        url_list.append(hem_url)

    hemisphere_url_list = ['https://astrogeology.usgs.gov' + url for url in url_list]

    img_urls = []
    
    for hem_url in hemisphere_url_list:
        url = hem_url
        browser.visit(url)
        browser.click_link_by_partial_text('Open')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        category = section.find('div', class_='downloads')
        hem_image = category.find('ul')
        hem_image_text = hem_image.find('a')
        hem_image_url = hem_image_text.attrs['href']
        img_urls.append(hem_image_url)

    hemisphere_image_urls = []

    for item in range(0,4):
        hem = {"title": hem_list[item], "img_url": img_urls[item]}
        hemisphere_image_urls.append(hem)

    mars_data = {
        "news_title": news_title,
        "news_p": news_paragraph,
        "featured_image_url": featured_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls,}   

# Close the browser after scraping
    browser.quit()

    return mars_data

if __name__ == "__main__":
    result = scrape()
    print(result)
