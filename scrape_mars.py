# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # executable_path = {'executable_path':'resources/chromedriver'}
    executable_path = {'executable_path':ChromeDriverManager().install()}

    # create a new browser object by default it is firefox the default one
    browser = Browser('chrome', **executable_path, headless = False) #headless true will not open browser

    #----------------------------------------------------------------------#
    #                       NASA Mars' most recent news                    #
    #----------------------------------------------------------------------#

    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Open chrome and visit url
    browser.visit(nasa_url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    content_title = soup.find_all(class_='content_title')
    body_article = soup.find_all(class_='article_teaser_body')

    news_title=[]
    news_paragraph = []

    for title in content_title:
        try:
            news_title.append(title.a.text.strip())
        except:
            pass
        
    for body in body_article:
        try:
            news_paragraph.append(body.text.strip())
        except:
            pass
        
    recent_news = news_title[0]
    recent_paragraph = news_paragraph[0]
    news_dict = {}
    news_dict['recent_news'] = recent_news
    news_dict['recent_paragraph'] = recent_paragraph

    #----------------------------------------------------------------------#
    #              JPL Mars Space Images - Featured Image                  #
    #----------------------------------------------------------------------#

    # JPL Website
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    # Open chrome and visit url
    browser.visit(jpl_url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    main_image = soup.find_all('img', class_='headerimage')
    for image in main_image:
    #     print(image['src'])
        featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image['src']}"
    
    jpl_featured = {}
    jpl_featured['featured_jpl_image'] = featured_image_url


    #----------------------------------------------------------------------#
    #                             Mars Facts                               #
    #----------------------------------------------------------------------#

    # Scraped table containing facts about the planet
    mars_url = 'https://space-facts.com/mars/'

    # Read url and returned a list of DataFrames
    mars_table = pd.read_html(mars_url)
    mars_table = mars_table[1]

    # Converted data to HTML table string
    html_mars_table = mars_table.to_html()
    mars_facts_dict = {}
    mars_facts_dict['mars_fact'] = html_mars_table


    #----------------------------------------------------------------------#
    #                      Mars Hemispheres Name list                      #
    #----------------------------------------------------------------------#

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    names = soup.find_all(class_='description')

    # Create a list of hemisphere names to be used to iterate over them to navigate on the next loop
    hem_list = []
    for name in names:
        hem_list.append(name.a.h3.text)

    
    #----------------------------------------------------------------------#
    #                       Mars Hemispheres Images                        #
    #----------------------------------------------------------------------#

    # Navigate through all pages and get the full resolution hemisphere image
    browser.visit(hemispheres_url)
    hemisphere_image_urls={}
    for i in range(len(hem_list)):
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            browser.click_link_by_partial_text(hem_list[i])
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            title = hem_list[i]
            img_url = soup.find(class_='downloads')
            
            #title = f"title{i}"
            hemisphere_dict = {}
            hemisphere_dict['title{0}'.format(i)] = title
            hemisphere_dict['img_url{0}'.format(i)] = img_url.a['href']
            hemisphere_image_urls.update(hemisphere_dict)
            browser.back()

    #----------------------------------------------------------------------#
    #                       Close Chrome Browser                           #
    #----------------------------------------------------------------------#

    browser.quit()

    #----------------------------------------------------------------------#
    #                       Collection of dictionaries                     #
    #----------------------------------------------------------------------#
    # return mars_collection_dict
    mars_collection_dict = {}
    mars_collection_dict.update(news_dict)
    mars_collection_dict.update(jpl_featured)
    mars_collection_dict.update(mars_facts_dict)
    mars_collection_dict.update(hemisphere_image_urls)

    return mars_collection_dict

    





