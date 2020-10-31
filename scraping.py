# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

executable_path = {'executable_path': 'chromedriver.exe'}
def scrape_all():
    # headless browser is a web browser without a graphical user interface.
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.utcnow(),
        "hemispheres": mars_hemisphere(browser)
    }
       # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #  `ul.item_list` means look for `<ul class="item_list">`

    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')
        slide_elem.find_all("div", class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    except AttributeError:
        return none
    return img_url

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    return df.to_html()

def mars_hemisphere(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []
    thumb_html = browser.html
    html_soup = soup(thumb_html,'html.parser')
    items = html_soup.find_all('div', class_='item')
    for item in items:
        href_element = item.find('a',class_='itemLink product-item')
        href = href_element['href']
        href = f'https://astrogeology.usgs.gov/{href}'
        hemisphere_image_urls.append({'title':item.div.a.text,'href':href})
    def jpg_href(url):
        # return the jpeg url
        browser.visit(url)
        html = browser.html
        soup_=soup(html,'html.parser')
        elem=soup_.find('div',class_='downloads')
        href=elem.find('a').get('href')
        return href
    for i in range(len(hemisphere_image_urls)):
        url = hemisphere_image_urls[i]['href']
        jpg = jpg_href(url)
        hemisphere_image_urls[i]['img_url']=jpg
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())