from urllib.request import urlopen,Request 
from bs4 import BeautifulSoup as soup
import requests

def list_cities():
    cities=["Delhi","Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","Puducherry"]
    return  cities

def news(city='india'):
    place=city.replace(" ","+")

    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
    url="https://www.google.com/search?q=covid+19+"+place+"&sxsrf=ALeKk02Xr7Z-nSW9zKyGbCVfeDSNWp13qQ:1585121646630&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjm-bCljrXoAhXq4zgGHYSTB_8Q_AUoAXoECBoQAw&biw=1920&bih=937"

    req = requests.get(url=url,headers=headers)
    html = req.content
    print(html)
    parsed_data=soup(html,'html.parser')

    links=parsed_data('a',{'class':'l lLrAF'})
    links_list=[link['href'] for link in links]


    headlines=[link.text for link in links]



    news_data=parsed_data.findAll('div',{'class','st'})
    news=[n.text.strip().replace(u'\xa0', u' ') for n in news_data]

    
    news_markdown=''

    for i in range(0,len(news)):
        temp='''
        [%s](%s) 
        ### %s 
        ###
        '''%(headlines[i],links_list[i],news[i])
        news_markdown=news_markdown+temp
        print(temp)
        i=i+1
    
    print(news_markdown)
    return news_markdown


print(news())

