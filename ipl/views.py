from curses.ascii import HT
from multiprocessing import context
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
import uuid, base64
import csv
import os
import numpy as np
import pandas as pd 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO


for dirname, _, filenames in os.walk('E:\Projects\Paralaxiom\backend\kaggle'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
matches = pd.read_csv('./kaggle/matches.csv')
deliveries = pd.read_csv('./kaggle/deliveries.csv')


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def landing1():
    matches.groupby('season')['match_id'].count().plot.bar(color=['#5c3449','#c85c53'],figsize=(15,8))
    plt.title("number of matches played per year of all the years in IPL".upper())
    plt.xlabel("Year".upper())
    plt.ylabel("Matches".upper())
    plt.xticks(rotation=45)
    landing_graph_1 = get_graph()
    return landing_graph_1


def landing2():
    data = matches.groupby(['season','winner'])['match_id'].nunique()
    data.unstack().plot.bar(stacked=True,figsize=(15,8), color = ['#003f5c','#274470','#51447b','#7b3f7a','#9f396c','#b93a53','#c34b33','#5c0024','#5c0024','#722453','#794885','#6f6db4','#5492d9','#27b7f3','#00daff'] )
    plt.title('matches won of all teams over all the years of IPL'.upper())
    plt.xlabel("years".upper())
    plt.ylabel("win count".upper())
    plt.legend(loc="upper right")
    plt.xticks(rotation=45)
    landing_graph_2 = get_graph()
    return landing_graph_2


def home(request):
    plt.switch_backend('AGG')
    landing_graph_1 = landing1()
    landing_graph_2 = landing2()
    context = {"landing_graph_1": landing_graph_1,
    "landing_graph_2": landing_graph_2}
    return render (request, 'home.html', context)


def extra_runs(request):
    plt.switch_backend('AGG')
    df = deliveries.groupby('batting_team')['extra_runs'].sum()
    df.plot.bar(color=['#5c3449','#c85c53'],figsize=(15,8))
    plt.title("extra runs conceded per team".upper())
    plt.xlabel("team".upper())
    plt.ylabel("extra runs".upper())
    plt.tight_layout()
    extra_runs = get_graph()
    return render (request, 'extraruns.html', {"extra_runs": extra_runs})


def eco_bowlers(request):
    plt.switch_backend('AGG')
    result = pd.merge(matches, deliveries, on ='match_id')
    bowler_list = result.groupby(['season','bowler'])

    df = pd.DataFrame()
    df['total_runs'] = bowler_list['total_runs'].sum()
    df['total_balls'] = bowler_list['ball'].count()
    df['economy'] = df['total_runs']/df['total_balls']
    df['min'] = df.groupby('season')['economy'].transform('min')
    df[(df['economy'].isin(df['min']))]

    df2 = df.loc[df.groupby('season')['economy'].idxmin()]
    df3 = df2.drop(['total_runs','total_balls','min'], axis=1)

    df3.plot.bar(color='#5c3449',figsize=(15,8))
    plt.title("the top economical bowlers for each year".upper())
    plt.xlabel("year, bowler".upper())
    plt.ylabel("economy rate".upper())
    plt.tight_layout()
    eco_bowlers = get_graph()
    return render (request, 'ecobowlers.html', {"eco_bowlers": eco_bowlers})


def played_vs_won(request):
    plt.switch_backend('AGG')
    wins = matches.groupby(['season','winner'])['match_id'].nunique()
    data = matches.groupby('season')
    count_team1 = data['team1'].value_counts() 
    count_team2 = data['team2'].value_counts()

    df = pd.DataFrame()
    df['0'] = count_team1
    df['matches2'] = count_team2
    df['total_matches'] = df['0'] + df['matches2']
    df['total_wins'] = wins

    x = (df.apply(lambda x: x[0],axis=1)) 
    y = pd.DataFrame(x).reset_index()
    df2 = pd.merge(y,df,on=['season','team1']).drop([0, '0','matches2'], axis=1)
    
    a = df2['season'].value_counts()
    year_list = list(a.index.sort_values())
    
    dic = {}
    for year in year_list:
        team = df2[df2['season']==year].drop(columns=['season'])
        dic.update({year:team})

    fig = plt.figure(figsize=(15,60))
    i = 10
    j = 2
    k = 1
    for key,value in dic.items():   
        ax = plt.subplot(i,j,k)
        bar1 = ax.bar(value['team1'],value['total_matches'], color='#c85c53', width=0.5)
        bar2 = ax.bar(value['team1'],value['total_wins'], color='#5c3449', width=0.5)
        title = str("Year: "+str(key)) 
        ax.set_title(title,fontsize=17,color="#5c0024")
        ax.set_ylabel("Runs", fontsize=13)
        ax.set_yticks([0, 4, 8, 12, 16, 20])
        ax.tick_params(axis='x', labelrotation=90)
        k = k+1
        ax.bar_label(bar1, padding=3)
        ax.bar_label(bar2, padding=3)
        ax.legend(labels=['Total matches played', 'Total wins'], loc='upper right')
        
    plt.suptitle('Matches played vs matches won for each team per year'.upper(), fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.965);

    played_vs_won = get_graph()
    return render (request, 'playedvswon.html', {"played_vs_won": played_vs_won})