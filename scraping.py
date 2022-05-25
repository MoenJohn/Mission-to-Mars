import pandas as pd

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# Set up executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

##################
# Mars Headlines #
##################

def mars_news(browser):
    """
    Scrapes the most recent news title and blurb from https://redplanetscience.com

        Parameters:
            browser: An instantiated splinter browser

        Returns:
            news_title: The title of the story
            news_p: The blurb of the story
    """
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up HTML Parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Scrape the title and paragraph text
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`, then get paragraph text
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
        

    return news_title, news_p


###################
# Featured Images #
###################

def featured_image(browser):
    """
    Scrapes first image from https://spaceimages-mars.com and returns path to the photo
    """
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
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    return f'https://spaceimages-mars.com/{img_url_rel}'


##############
# Mars Facts #
##############

def mars_facts():
    """
    Reads mars facts from https://galaxyfacts-mars.com into a dataframe, returns html of dataframe
    """
    # Use 'read_html' to scrape the facts table into a dataframe
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


browser.quit()


