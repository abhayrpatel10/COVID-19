from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC


import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


#driver=webdriver.Chrome('chromedriver.exe')

def news(city='india'):


    place=city.replace(" ","+")
    driver.get("https://www.google.com/search?q=covid+19+"+place+"&sxsrf=ALeKk02Xr7Z-nSW9zKyGbCVfeDSNWp13qQ:1585121646630&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjm-bCljrXoAhXq4zgGHYSTB_8Q_AUoAXoECBoQAw&biw=1920&bih=937")


    links=driver.find_elements_by_class_name('lLrAF')
    links_list=[link.get_attribute('href') for link in links]
    headlines=[link.text for link in links]
    news_data=driver.find_elements_by_class_name('st')
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
    
    return(news_markdown)






