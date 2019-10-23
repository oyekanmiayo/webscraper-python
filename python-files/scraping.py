from IPython.core.display import display, HTML
display(HTML("<style> .container { width: 100% !important; }</style>"))

import requests
from bs4 import BeautifulSoup
from dateutil import parser
from textstat.textstat import textstat

# headers to tell the website the request is coming from a browser
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'referrer': 'https://google.com'
}

# Scrape Single Article
def parse_page(url_link):
    res = requests.get(url_link, headers = headers)
    html = res.text.strip()
    # lxml will help us search for classes and ids
    soup = BeautifulSoup(html, 'lxml')

    # Header
    header = soup.find(class_ = 'entry-header')
    read_time = extract_read_time(header)
    title = extract_title(header)

    author = extract_author(header)
    categories = extract_categories(header)

    date = extract_date(header)
    date_res = parser.parse(date)
    month = date_res.strftime('%B')
    weekday = date_res.strftime('%A')

    # Body
    content = soup.find(class_ = 'entry-content')
    word_count = len(content.text.split())
    reading_level = textstat.flesch_kincaid_grade(content.text)

    links = content.findAll('a')
    link_count = len(links)

    images = content.findAll('img')
    image_count = len(images)

    page_data = {
        'reading_time' : read_time,
        'title': title,
        'date': date,
        'month': month,
        'weekday': weekday,
        'author': author,
        'categories': categories,
        'word_count': word_count,
        'reading_level': reading_level,
        'link_count': link_count,
        'image_count': image_count
    }

    return page_data

def extract_read_time(header):
    html_str = header.find(class_ = 'read-time')
    time_str = html_str.contents[0].strip().lower().split()[0]
    time_int = int(time_str)
    return time_int

def extract_title(header):
    html_str = header.find(class_ = "post-meta-title")
    title_str = html_str.contents[0].strip()
    return title_str

def extract_author(header):
    html_str = header.find(class_ = "author-name")
    anchor_contents = html_str.find('a')
    author_str = anchor_contents.contents[0].strip()
    return author_str

def extract_categories(header):
    html_str = header.find(class_ = "single-post-cat")
    categories = html_str.findAll('a')
    category_list = []
    for link in categories:
        category_name = link.contents[0].lower().strip()
        category_list.append(category_name)
    return category_list

def extract_date(header):
    html_str = header.find(class_ = "single-post-date")
    date_str = html_str.contents[0].strip()
    return date_str


url = "https://blog.frame.io/2019/04/23/nab2019-session-cioni/"
# print(parse_page(url))

# Scrape Single Category
articles_store = []
def parse_category(url):
    res = requests.get(url, headers=headers)
    html = res.text.strip()
    soup = BeautifulSoup(html, 'lxml')

    article_cards = soup.findAll(class_ = 'post-content')

    for article in article_cards:
        title = article.find(class_ = 'post-meta-title')
        link = title.contents[0]['href']
        print('Parsing url: %s' %link)
        page = parse_page(link)
        articles_store.append(page)

    next_link = find_next_link(soup)

    if next_link is not None:
        print('Parsing next page: %s' %next_link)
        parse_category(next_link)

    return None

def find_next_link(soup_item):
    bottom_nav = soup_item.find(class_ = 'navigation')

    if bottom_nav == None:
        return None
    
    links = bottom_nav.findAll('a')
    next_page = links[-1]
    
    if next_page.contents[0] == 'Next':
        next_link = next_page['href']
        return next_link

    return None

# url = "https://blog.frame.io/category/production/"
# parse_category(url)
# print(len(articles_store))
# print(articles_store[0])

def parse_all_categories(url):
    res = requests.get(url, headers=headers)
    html = res.text.strip()
    soup = BeautifulSoup(html, 'lxml')

    # Find List of Categories
    category_nav = soup.find(id = "menu-cat-menu")
    category_list = category_nav.findAll('li')

    all_links = []
    # Get Link of each Category
    for aList in category_list:
        category_subcategory_menu = aList.find(role = 'menu')
        if category_subcategory_menu is not None:
            all_link = category_subcategory_menu.find('a')['href'].strip()
            all_links.append(all_link)
    
    for link in all_links:
        parse_category(link)


url = "https://blog.frame.io/"
parse_all_categories(url)
print(len(articles_store))

import json

with open('data/articles.json', 'w') as document:
    json.dump(articles_store, document)