# Declare the dependancies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager   

import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')

def load_splinter_browser():
    # Setup splinter, setup a browser to open  
    # (ensure chromeDriverMangager is installed, call by path mac vs windows path)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# SCRAPE all at once: optimize, so not loading browswer each time (small project)
# Various ways of scraping will be shown
# Time is given to load payload and sites

def scrape():
    # save information scraped into a dictionary
    mars_data = {}

    # initialize the splinter browser
    browser = load_splinter_browser()
    time.sleep(2) 

    #----------------------------#
    # NASA MARS NEWS SCRAPE, USING splinter/BEAUTIFUL SOUP
    # set up the url
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(2) 

    # setup for beautiful soup to read html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # get the title an information paragraphs
    # most recent is the first
    news_title = soup.find('div', class_='content_title').text
    news_p= soup.find('div', class_='article_teaser_body').text

    # dictionary format to save
    #add titles and paragraphs to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p


    #----------------------------#
    #JPL MARS SPACE IMAGE - Featured Image / scrape, OPTIMIZE more USING SPLINTER 
    # using same initialezd browser, go to new url
    
    # URL of page to scrape
    url = 'https://spaceimages-mars.com/'
    browser.visit(url) 
    html2 = browser.html
    time.sleep(2) 

    # scrape using splinter only
    try:
        #splinter finds the image
        find_image_big = browser.find_by_css('img[class="headerimage fade-in"]')
                
        if find_image_big:
            image_url_big = str(find_image_big['src'])
        
        
        # save Dictionary entry from FEATURED IMAGE
        mars_data['image_url_feature'] = image_url_big
        
    except Exception as e:
        print(e)
        
    
    #----------------------------#
    # MARS FACTS - scrape USING  PANDAS to get a table
    
    # URL of page to be scraped
    url = 'https://galaxyfacts-mars.com/'   
    
    # use pandas to read the tables
    tables = pd.read_html(url)
    try:

        # get the table of interest into a dataframe
        df = tables[0]
        # set headers for it
        df.columns = ["Description", "Mars", "Earth"]

        df.index.name=None
        # save changes made as html table 
        html_table= df.to_html(index=False, classes='table table-striped')  

        # save Dictionary entry from Mars Facts
        mars_data['tables'] = html_table
    except Exception as e:
        print(e)

    
    #----------------------------#
    # MARS HEMISPHERES scrape by USING BEAUTIFUL SOUP and SCRAPER
    
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # URL of page to be scraped   
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    time.sleep(2)

    html_hemispheres= browser.html
    # Parse HTML with Beautiful Soup
    soup3 = BeautifulSoup(html_hemispheres, 'html.parser')

    # save all of the 'hemisphere' items on page
    items = soup3.find_all('div', class_='item')

    try:
        for item in items: 
            h_img_url =""
            img_url_link=""
            # Store title
            title = item.find('h3').text
            
            # Store link that leads to full image website
            img_url_link = item.find('a', class_='itemLink product-item')['href']

            if img_url_link:
                img_url_link = hemi_url + img_url_link

                #splinter loads page of above link, for hemisphere
                browser.visit(img_url_link)  
                time.sleep(2)
                try:
                    #splinter finds the high resolution hemishpere image
                    find_image = browser.find_by_css('img[class="wide-image"]')
                    if find_image:
                        h_img_url = str(find_image['src'])
                        #print(f'images: {h_img_url}')
                        # Append the retreived information into a list of dictionaries 
                        hemisphere_image_urls.append({"title" : title, "img_url" : h_img_url})

                except Exception as e:
                    print(f'hemi error: {e}')
        #adding to dict
        mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    except Exception as e:
        print(e)
    
    print(mars_data)
    # close the browser
    browser.quit()
    
    return mars_data

if __name__ == "__main__":
    scrape()




























