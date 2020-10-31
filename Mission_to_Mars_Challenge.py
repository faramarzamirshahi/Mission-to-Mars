# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# %%
executable_path = {'executable_path': 'chromedriver.exe'}
# headless browser is a web browser without a graphical user interface.
browser = Browser('chrome', **executable_path)


# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# %% [markdown]
#  `ul.item_list` means look for `<ul class="item_list">`
#  

# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
slide_elem.find_all("div", class_='content_title')


# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### Featured Images

# %%
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# %%
# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# %%
# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# %% [markdown]
# ### Scrape facts

# %%
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# %%
df.to_html()


# %%
browser.quit()

# %% [markdown]
# # ************** Assignment starts here ********************

# %%
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# %%
# Path to chromedriver
get_ipython().system('where chromedriver')


# %%
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': './chromedriver'}
browser = Browser('chrome', **executable_path)

# %% [markdown]
# ### Visit the NASA Mars News Site

# %%
# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# %%
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# %%
slide_elem.find("div", class_='content_title')


# %%
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# %% [markdown]
# ### JPL Space Images Featured Image

# %%
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# %%
# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# %%
# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# %% [markdown]
# ### Mars Facts

# %%
df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# %%
df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# %%
df.to_html()

# %% [markdown]
# ### Mars Weather

# %%
# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# %%
# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# %%
# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# %% [markdown]
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# %% [markdown]
# ### Hemispheres

# %%
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
thumb_html = browser.html
html_soup = soup(thumb_html,'html.parser')
items = html_soup.find_all('div', class_='item')
for item in items:
    href_element = item.find('a',class_='itemLink product-item')
    href = href_element['href']
    href = f'https://astrogeology.usgs.gov/{href}'
    hemisphere_image_urls.append({'title':item.div.a.text,'href':href})

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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


# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# %%
# 5. Quit the browser
browser.quit()


# %%



