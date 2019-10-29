from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

import json
from collections import Counter

with open('./code/webscraper-python/python-files/data/articles.json','r') as document:
    articles_store = json.loads(document.read())

times = []
months = []
weekdays = []
authors = []
categories = []

for article in articles_store:

    times.append(article['reading_time'])
    avg_time = sum(times) / float(len(times))
    avg_time = round(avg_time, 2)

    # Posts by month
    months.append(article['month'])
    month_count = Counter(months)


    # Posts by weekday
    weekdays.append(article['weekday'])
    weekday_count = Counter(weekdays)

    #Count by Category
    print(article['categories'])
    for eachCat in article['categories']:
        if eachCat not in categories:
            categories.append(eachCat)
    category_count = Counter(categories)
    print(categories)
    print('---------------------------')

    # Count by Author
    authors.append(article['author'])
    author_count = Counter(authors)


print("Average reading time:", avg_time)
print("Posts by month", month_count)
print("Posts by weekday", weekday_count)
print("Posts by category", category_count)
print("Posts by author", author_count)

stats = { 
    'reading_time': avg_time, 
    'num_articles': len(articles_store) 
}

with open('./code/webscraper-python/python-files/data/stats.json', 'w') as document:
    json.dump(stats, document)

with open('./code/webscraper-python/python-files/data/weekday.json', 'w') as document:
    json.dump(weekday_count, document)
    
with open('./code/webscraper-python/python-files/data/month.json', 'w') as document:
    json.dump(month_count, document)
    
with open('./code/webscraper-python/python-files/data/category.json', 'w') as document:
    json.dump(category_count, document)

with open('./code/webscraper-python/python-files/data/author.json', 'w') as document:
    json.dump(author_count, document)