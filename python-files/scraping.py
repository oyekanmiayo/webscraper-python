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
    categories = html_str.find_all('a')
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
print(parse_page(url))