import re
import json
import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    url = 'https://www.tripadvisor.ca/Hotel_Review-g60982-d87016-Reviews-Hilton_Hawaiian_Village_Waikiki_Beach_Resort-Honolulu_Oahu_Hawaii.html'
    page1 = requests.get(url)
    soup1 = BeautifulSoup(page1.text, 'html.parser')

    reviews = []
    for i in soup1.find('div',{'data-test-target':'reviews-tab'}).findAll('div',{'data-test-target':'HR_CC_CARD'}):
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
        """
        try:
            rev = []
            rev.append(i.find('q').text)
            try:
                rev.append(i.find('span',{'class':'_1M-1YYJt'}).text)
            except:
                pass
            review = ' .'.join(rev)
        except:
            review = ''
        """

        data = {}

        data['Reviewer'] = name
        data['Date'] = date_
        data['Rating'] = rating
        data['Title'] = title
        #data['Description'] = review

        reviews.append(data)

    base_url = re.search('https?://([A-Za-z_0-9.-]+).*', url)
    next_page = "https://"+ base_url.group(1) + str(soup1.find('div',{'data-test-target':'reviews-tab'}).find('div',{'class':'_16gKMTFp'}).find('div',{'class':'pageNumbers'}).find('a').get('href'))

    page2 = requests.get(next_page)
    soup2 = BeautifulSoup(page2.text, 'html.parser')

    flag = 1
    for i in soup2.find('div',{'data-test-target':'reviews-tab'}).findAll('div',{'data-test-target':'HR_CC_CARD'}):
        if flag == 1:
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
            """
            try:
                rev = []
                rev.append(i.find('q').text)
                try:
                    rev.append(i.find('span',{'class':'_1M-1YYJt'}).text)
                except:
                    pass
                review = ' .'.join(rev)
            except:
                review = ''
            """

            data = {}

            data['Reviewer'] = name
            data['Date'] = date_
            data['Rating'] = rating
            data['Title'] = title
            #data['Description'] = review

            reviews.append(data)
            flag += 1
            
    #print(json.dumps(reviews, sort_keys=True, indent=2))
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(reviews)
    }
