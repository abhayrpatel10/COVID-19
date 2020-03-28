from urllib.request import urlopen as request
import requests
import  json
import streamlit as st 
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pandas as pd 

def autolabel(rects):
    
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., int(height),
                '%d' %int(height),
        ha='center', va='bottom')

def indianStats():
    url='https://api.rootnet.in/covid19-in/stats/latest'
    data=requests.get(url)

    client=json.loads(data.content)

    summary=client['data']['summary']
    confirmed='''## Confirmed Cases ```  %d``` '''%summary['total']

    recovered='''## Recovered Cases ```  %d``` '''%summary['discharged']
    deaths='''## Deaths ```  %d``` '''%summary['deaths']
    indians='''## Indians ```  %d``` '''%summary['confirmedCasesIndian']
    othernationals='''## Foreign Nationals ```  %d``` '''%summary['confirmedCasesForeign']

    st.markdown(confirmed)
    st.markdown(recovered)
    st.markdown(deaths)
    st.markdown(indians)
    st.markdown(othernationals)

    objects = ('Deaths', 'Total Cases','Recovered')#labels for the bar chart
    y_pos = np.arange(len(objects))
    #active=int(confnum)-(int(recoverednum)+int(deathnum))#finding number of active cases
    values = [int(summary['deaths']),int(summary['total']),int(summary['discharged'])]#values for the bar chart
    ax=plt.bar(y_pos, values, align='center', alpha=0.7)#bar chart ----plotted using matplotlib
    plt.xticks(y_pos, objects)
    
    # Additional data for the graph
    plt.title('COVID-19')
    autolabel(ax)
    st.write(mpl_fig=ax)
    st.pyplot()





    df=json_normalize(client['data']['regional'])
    locations=df['loc'].tolist()
    choice=st.selectbox('Choose Location',locations)
    df=df.drop(['confirmedCasesForeign'],axis=1)
    df.rename(columns = {'loc':'Location','deaths':'Deaths','confirmedCasesIndian':'Confirmed cases','discharged':'Discharged'}, inplace = True)

    value=df.loc[df['Location']==choice]
    st.table(value)

    st.table(df)

    return





