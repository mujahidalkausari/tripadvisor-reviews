import re
import json
import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.tripadvisor.ca/Attraction_Review-g34345-d4170622-Reviews-Sunset_Sail_Key_West-Key_West_Florida_Keys_Florida.html')
soup = BeautifulSoup(response.text, 'html.parser')

reviews = []
for i in soup.find('div',{'data-test-target':'reviews-tab'}).findAll('div',{'class':'LnVzGwUB'}):
    try:
        name = (i.find('a',{'class':'ui_header_link _1r_My98y'}).text)
    except:
        name = ''
    try:
        date_ = (i.find('div',{'class':'_2fxQ4TOx'}).text.split('wrote a review')[-1].strip())
    except:
        date_ = ''
    try:
        rating = (int(int(i.find('div',{'data-test-target':'review-rating'}).find('span').get('class')[-1].split('_')[-1])/10))
    except:
        date_ = ''
    try:
        title = (i.find('div',{'data-test-target':'review-title'}).text)
    except:
        title = ''
    try:
        rev = []
        rev.append(i.find('q').text)
        try:
            rev.append(i.find('span',{'class':'_1M-1YYJt'}).text)
        except:
            pass
        review = ' .'.join(rev)
        desc = re.sub(u"(\u2018|\u2019)", "'", review)
    except:
        desc = ''


    data = {}

    data['Reviewer'] = name
    data['Date'] = date_
    data['Rating'] = rating
    data['Title'] = title
    data['Description'] = desc

    reviews.append(data)
    
#print(json.dumps(reviews, sort_keys=True, indent=2))
    
