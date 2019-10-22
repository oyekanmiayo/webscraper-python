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

url = "https://blog.frame.io/2019/04/23/nab2019-session-cioni/"

# # Header

# title_html = header.find(class_ = "post-meta-title")
# #print(len(title_html.contents))

# title_str = title_html.contents[0].strip()
# #print(title_str)

# author_html = header.find(class_ = "author-name")
# # print(author_html.contents)
# anchor_contents = author_html.find('a')
# # print(anchor_contents.contents)
# author_str = anchor_contents.contents[0].strip()
# print(author_str)

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
    print(content.text.split())
    word_count = len(content.text.split())
    reading_level = textstat.flesch_kincaid_grade(content.text)

    links = content.find_all('a')
    link_count = len(links)

    images = content.find_all('img')
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
    read_time_str = header.find(class_ = 'read-time')
    time_str = read_time_str.contents[0].strip().lower().split()[0]
    time_int = int(time_str)
    pass

def extract_title(header):
    pass

def extract_author(header):
    pass

def extract_categories(header):
    pass

def extract_date(header):
    pass