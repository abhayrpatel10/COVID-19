import streamlit as st
from urllib.request import urlopen as request
import json
from bs4 import BeautifulSoup as soup
from languages import *
from helpline import helpline
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt 
from pandas.io.json import json_normalize
from PIL import Image
from symptoms import symptoms
import requests


def list_cities():
    cities=["Delhi","Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","Puducherry"]
    return  cities




#labelling the bar plot
def autolabel(rects):
    
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., int(height),
                '%d' %int(height),
        ha='center', va='bottom')

def getdata():
    #get the data
    url='https://coronavirus-tracker-api.herokuapp.com/v2/locations'
    data=request(url)
   
    #convert data from bytes to json
    final_data=json.loads(data.read())
    final_data=final_data['locations']

    #sort the data ,using number of cases as the key
    sorted_data=sorted(final_data,key=lambda k: k['latest']['confirmed'],reverse=True)

    #convert data to dataframe
    df=json_normalize(sorted_data)
    df=df.drop(['coordinates.longitude','coordinates.latitude','last_updated','latest.recovered','id','country_code'],axis=1)
    df.rename(columns = {'province':'Province','latest.deaths':'Deaths','latest.confirmed':'Confirmed Cases','country':'Country'}, inplace = True)
    

    
    return df
def main():
    st.title('COVID - 19')
    menuItems=['Guidelines','Statistics','News','Symptoms','Helpline']
    st.sidebar.title('Menu')
    
    
    itemSelected=st.sidebar.selectbox('',menuItems)
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    github='''[ Fork/Star on Github](https://github.com/abhayrpatel10/COVID-19)'''
    st.sidebar.info(github)

    if(itemSelected=='Helpline'):
        st.markdown(helpline())
   


    if(itemSelected=='Guidelines'):
        
        langugaes=['English','हिंदी','ગુજરાતી','தமிழ்','తెలుగు','ਪੰਜਾਬੀ','മലയാളം','ಕನ್ನಡ']
        lang=st.selectbox('Choose Langugae',langugaes)
        st.subheader('WHO Guidelines')
        
        if(lang=='English'):
           st.markdown(english())
        elif(lang=='தமிழ்'):
            st.markdown(tamil())
        elif(lang=='हिंदी'):
            st.markdown(hindi())
        elif(lang=='ગુજરાતી'):
            st.markdown(gujarati())
        elif(lang=='తెలుగు'):
            st.markdown(telugu())
        elif(lang=='ਪੰਜਾਬੀ'):
            st.markdown(punjabi())
        elif(lang=='മലയാളം'):
            st.markdown(malayalam())
        elif(lang=='ಕನ್ನಡ'):
            st.markdown(kannada())
        

    if(itemSelected=='Statistics'):
        ogstatsurl='https://coronavirus-tracker-api.herokuapp.com/v2/latest'
        #making get request to the API
        client=request(ogstatsurl)
        data=client.read()
        client.close()
        #bytes to json
        final=json.loads(data)
        
        #number of confirmed cases all around the world ---------variable name - confnum
        confnum=final['latest']['confirmed']
        confirmed='''## Confirmed Cases ```  %d``` '''%(confnum)
        st.markdown(confirmed)

        #number of deaths around the world ---------variable name -deathnum
        deathnum=final['latest']['deaths']
        deaths='''## Deaths ``` %d ``` '''%(deathnum)
        st.markdown(deaths)

        ##Getting recovered data 
        url='https://www.worldometers.info/coronavirus/'
        client=request(url)
        raw_html=client.read()
        parsed_html=soup(raw_html,'html.parser')
        #-----------Number of people recovered -variable name - =recoverednum
        
        
        #using beautiful soup to find div tag with given style
        recoverednum=parsed_html.find('div',{'style':'color:#8ACA2B '}).text
        recoverednum=recoverednum.strip().replace(",","")
        recovered='''## Recovered ``` %s ``` '''%(recoverednum)
        st.markdown(recovered)

        
        objects = ('Recovered', 'Deaths', 'Active')#labels for the bar chart
        y_pos = np.arange(len(objects))
        active=int(confnum)-(int(recoverednum)+int(deathnum))#finding number of active cases
        values = [int(recoverednum),int(deathnum),int(active)]#values for the bar chart
        ax=plt.bar(y_pos, values, align='center', alpha=0.7)#bar chart ----plotted using matplotlib
        plt.xticks(y_pos, objects)
        
        # Additional data for the graph
        plt.title('COVID-19')
        autolabel(ax)
        st.write(mpl_fig=ax)
        st.pyplot()

        
        df=getdata()

        #getting the list of countries 
        country_list=df['Country'].tolist()
        country_list=sorted(list(set(country_list)))
        
        choice=st.selectbox('Choose Country',country_list)
        #finding data related to specific country and displaying
        value=df.loc[df['Country']==choice]
        st.table(value)

        #dsplaying all data
        st.table(df)
        
    if(itemSelected=='News'):
        st.subheader('News')
        image = Image.open('verified.png')
        st.image(image)
        choice=st.selectbox('Choose state or UT',list_cities())
        place=choice.replace(" ","+")

        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',}
        url="https://www.google.com/search?q=covid+19+"+place+"&sxsrf=ALeKk02Xr7Z-nSW9zKyGbCVfeDSNWp13qQ:1585121646630&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjm-bCljrXoAhXq4zgGHYSTB_8Q_AUoAXoECBoQAw&biw=1920&bih=937"

        req = requests.get(url=url, headers=headers) 
        html = req.text

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
            i=i+1
    
        st.markdown(news_markdown)

        

    if(itemSelected=='Symptoms'):
        st.markdown(symptoms())
        st.write('Source : WHO')



        



if __name__ == '__main__':
    main()

