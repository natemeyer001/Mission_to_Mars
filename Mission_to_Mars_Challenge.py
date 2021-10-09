# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()


### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'


### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df.to_html()


### Hemispheres
# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
url = 'https://marshemispheres.com/'
browser.visit(url)

hemisphere_image_urls = [] # list to hold the images and titles
html = browser.html
results = soup(html, 'html.parser')
hemis = results.find_all(class_='item')

for i in range(4):
    hemispheres = {} # dictionary to add to hemisphere_image_urls
    ending = hemis[i].a['href']  # url suffix for each hemisphere
    browser.visit(url+ending)
    
    # parse individual hemisphere page data
    new_html = browser.html
    new_data = soup(new_html, 'html.parser')
    
    # get the data and add to structures
    image = new_data.find('ul').a['href']
    title = new_data.find('h2', class_='title').text
    hemispheres['img_url'] = url+image
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)

# print the list that holds the dictionary of each image url and title.
#print(hemisphere_image_urls)

# quit the browser
browser.quit()

