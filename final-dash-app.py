# W209-3 Harding, Post, Teo
# HOW LOW COULD YOU GO? An interactive tool to explore basic concepts in retirement savings

# Libraries
# Will need plotly sudo pip install plotly; conda install plotly

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools

from flask import Flask

from datetime import datetime
import pandas as pd
import numpy as np
import math
import os

# Outline of this script
# 1) Libraries
# 2) General functions
# 3) Data definitions
# 4) Web page design

# Function to calculate balances

def Savings(balance,expense,ret,inflation,years):
    """
    Function to return balances
    input - balance - starting balance, expense - monthly expense starting value, inflation - 1x1,
    years - horizon, return from savings
    output - balance at each period
    """
    balances = np.arange(years+1)
    expenses = np.arange(years+1)
    years = np.arange(2017, 2017+years)
    balances[0] = balance
    expenses[0] = expense

    for t in range(len(years)):
        balances[t+1] = (1+ret/100)*balances[t] - expenses[t]
        expenses[t+1] = expenses[t]*inflation

    return np.around(balances,2)


# Figure 1
# Define the data

years = 30 # Default in this app
colorscheme = ['#0B4156', '#347B98', '#B2D732', '#F0F7D4', '#FE2712']


x = np.arange(2017, 2017+years)
y1 = 1e6*np.ones(years)
y2 = np.round(Savings(1e6,1e6/years,0,1,years),2)

trace0 = go.Scatter(
        x=x,
        y=y1,
        name='Starting Savings',
        text='Starting Savings',
        mode='markers',
        marker=dict(color=colorscheme[0], size=10)
        )

trace1 = go.Bar(
        x=x,
        y=y2,
        name='Remaining Savings',
        text='Remaining Savings',
        marker=dict(color=colorscheme[1])
        )

d1 = [trace0, trace1] # data for Figure 1

# Figures 2, 3 on inflation and expenses, see callback

# Figure 4, 3% return

pi= 3 # inflation
ret = 3 # investment returns
exp = 3.43333e4 # initial expenses

x = np.arange(2017, 2017+years)
y1 = Savings(1e6,1e6/years,0,1,years)
y2 = Savings(1e6,exp,3,1+pi/100,years)

trace0 = go.Scatter(
        x=x,
        y=y1,
        name='Savings, 0% inflation, 0% return',
        text='Savings, 0% inflation, 0% return',
        mode='markers',
        marker=dict(color=colorscheme[0], size=5)
    )

trace1 = go.Bar(
        x=x, # assign x as the dataframe column 'x'
        y=y2,
        name='Savings, 3% Inflation, 3% Return',
        text='Savings, 3% Inflation, 3% Return',
        marker=dict(color=colorscheme[1])
    )

d4= [trace0, trace1]

# Figure 5, 5% return

pi= 3 # inflation
ret = 5 # investment returns
exp = 5e4 # initial expenses

x = np.arange(2017, 2017+years)
y1 = Savings(1e6,exp,0,1,years)
y2 = Savings(1e6,exp,3,1+pi/100,years)
y3 = Savings(1e6,exp,ret,1+pi/100, years)

trace0 = go.Scatter(
        x=x,
        y=y1,
        name='Savings, 0% Inflation, 0% Return',
        text='Savings, 0% Inflation, 0% Return',
        mode='markers',
        marker=dict(color=colorscheme[0], size=5)
    )

trace1 = go.Bar(
        x=x, # assign x as the dataframe column 'x'
        y=y2,
        name='Savings, 3% Inflation, 3% Return',
        text='Savings, 3% Inflation, 3% Return',
        marker=dict(color=colorscheme[1])
    )

trace2 = go.Bar(
        x=x, # assign x as the dataframe column 'x'
        y=y3,
        name='Savings, 3% Inflation, 5% Return',
        text='Savings, 3% Inflation, 5% Return',
        marker=dict(color=colorscheme[2])
    )


d5= [trace0, trace1, trace2]


# Figure 6, interactive impact of returns, see callback


# Figure 7, path

def SavingT(years,ret1,ret2):
    part1 = Savings(1e6,5e4,ret1,1.03,years+1)
    part2 = Savings(part1[-1],5.0e4*math.pow(1.03,15),ret2,1.03,years+1)

    return np.concatenate((part1, part2), axis=0)

x = np.arange(2017, 2017+years+1)
y1 = Savings(1e6,5e4,0,1.03,years+1)
y2 = SavingT(years/2,5,7)
y3 = SavingT(years/2,7,5)

trace0 = go.Scatter(
        x=x,
        y=y1,
        name='Starting Savings',
        mode='markers'
    )

trace1 = go.Scatter(
        x=x, # assign x as the dataframe column 'x'
        y=y2,
        name='Low then High: 5% then 7%',
        text='Low then High: 5% then 7%',
        mode='markers',
        marker=dict(color=colorscheme[1], size=10)
    )

trace2 = go.Scatter(
        x=x, # assign x as the dataframe column 'x'
        y=y3,
        name='High then Low: 7% then 5%',
        text='High then Low: 7% then 5%',
        mode='markers',
        marker=dict(color=colorscheme[2], size=10)
    )

d7 = [trace2, trace1]

# Load data (from http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html)

source_data = pd.read_csv('Damoran_data.csv')
#source_data.Year = source_data.Year.astype(int)
#source_data.Year = pd.to_datetime(source_data.Year, format='%Y')
source_data = source_data.dropna(how='all')
data1 = source_data.drop(columns=['Unnamed: 10'],axis=0)
#data1 = source_data.drop(['Unnamed'],axis=1)

# Figure 8 as table

def niceformat(ret):
    """
    Converts to percentage and format to 1 decimal place
    """
    return round(ret*100,1)

trace0 = [['Financial Asset', '1 Year', '5 Years', '10 Years', '30 Years'],
            ['','' ,'' ,'' ,''],
            ['Stocks (S&P 500 Index)','' ,'' ,'' ,''],
            ['  Average Return', niceformat(data1['SP500'].rolling(1).mean().mean()), niceformat(data1['SP500'].rolling(5).mean().mean()),niceformat(data1['SP500'].rolling(10).mean().mean()),niceformat(data1['SP500'].rolling(30).mean().mean())],
            ['  Best Return', niceformat(data1['SP500'].rolling(1).mean().max()), niceformat(data1['SP500'].rolling(5).mean().max()),niceformat(data1['SP500'].rolling(10).mean().max()),niceformat(data1['SP500'].rolling(30).mean().max())],
            ['  Worst Return', niceformat(data1['SP500'].rolling(1).mean().min()), niceformat(data1['SP500'].rolling(5).mean().min()),niceformat(data1['SP500'].rolling(10).mean().min()),niceformat(data1['SP500'].rolling(30).mean().min())],
            ['','' ,'' ,'' ,''],
            ['Bonds (10Y US Treasuries)','' ,'' ,'' ,''],
            ['  Average Return', niceformat(data1['LIR'].rolling(1).mean().mean()), niceformat(data1['LIR'].rolling(5).mean().mean()),niceformat(data1['LIR'].rolling(10).mean().mean()),niceformat(data1['LIR'].rolling(30).mean().mean())],
            ['  Best Return', niceformat(data1['LIR'].rolling(1).mean().max()), niceformat(data1['LIR'].rolling(5).mean().max()),niceformat(data1['LIR'].rolling(10).mean().max()),niceformat(data1['LIR'].rolling(30).mean().max())],
            ['  Worst Return', niceformat(data1['LIR'].rolling(1).mean().min()), niceformat(data1['LIR'].rolling(5).mean().min()),niceformat(data1['LIR'].rolling(10).mean().min()),niceformat(data1['LIR'].rolling(30).mean().min())]]

fig8 = ff.create_table(trace0)
fig8.layout.width=1000
fig8.layout.margin=({'l':220, 'r':140, 't':50, 'b':50})

# Figure 9 Bond returns

clrred = colorscheme[4]
clrgrn = colorscheme[2]
clrs  = [clrred if data1['LIR'][x] < 0 else clrgrn for x in range(len(data1))]

trace0 = go.Bar(
        name="Annual Return (%)",
		x=data1['Year'], # assign x as the dataframe column 'x'
        y=data1['LIR']*100,
        marker=dict(color=clrs)
    )

trace1 = go.Scatter(
        name="Average (%)",
		x=data1['Year'],
        y=np.ones(len(data1))*data1['LIR'].mean()*100

    )

d9 = [trace0, trace1]

# Figure 10 Stock returns

lrred = colorscheme[4]
clrgrn = colorscheme[1]
clrs  = [clrred if data1['SP500'][x] < 0 else clrgrn for x in range(len(data1))]

trace0 = go.Bar(
        name="Annual Return (%)",
		x=data1['Year'], # assign x as the dataframe column 'x'
        y=data1['SP500']*100,
        marker=dict(color=clrs)
    )

trace1 = go.Scatter(
        name="Average (%)",
		x=data1['Year'],
        y=np.ones(len(data1))*data1['SP500'].mean()*100
    )

d10 = [trace0, trace1]

# Figure 11,12 Histogram - Bonds

trace0 = go.Histogram(
        x=data1['SP500']*100,
        xbins=dict(
            start=-50.0,
            end=60.0,
            size=5),
        marker=dict(color=colorscheme[1])
    )

trace1 = go.Histogram(
        x=data1['LIR']*100,
        xbins=dict(
            start=-50.0,
            end=60.0,
            size=5),
        marker=dict(color=colorscheme[2])
    )

d11 = [trace1]
d12 = [trace0]


# Figure 13 - Comparing Histograms

trace0 = go.Histogram(
        x=data1['SP500']*100,
        xbins=dict(
            start=-50.0,
            end=60.0,
            size=5),
        marker=dict(color=colorscheme[1]),
        name='1 Yr Returns on Stocks',
        text='1 Yr Returns on Stocks',
        opacity=0.6
    )

trace1 = go.Histogram(
        x=data1['LIR']*100,
        xbins=dict(
            start=-50.0,
            end=60.0,
            size=5),
        marker=dict(color=colorscheme[2]),
        name='1 Yr Returns on Bonds',
        text='1 Yr Returns on Bonds',
        opacity=0.6
    )

d13 = [trace0, trace1]

# Figure 14 - movement of bonds and equities

trace0 = go.Bar(
        name='Stocks',
		x=data1['Year'], # assign x as the dataframe column 'x'
        y=data1['SP500']*100,
        marker=dict(color=colorscheme[1])
    )

trace1 = go.Bar(
        name='Bonds',
		x=data1['Year'], # assign x as the dataframe column 'x'
        y=data1['LIR']*100,
        marker=dict(color=colorscheme[2])
    )

d14 = [trace0, trace1]

# Figure 15 - table for stocks bonds

trace0 = [['Year', 'Bonds', 'Stocks', '50/50 Mix'],
         [1999, -8.3, 20.9, 6.3],
		 [2000, 16.7, -9.0, 3.9],
		 [2001, 5.6, -11.9, -3.2],
		 [2002, 15.1, -22.2, -3.5],
		 [2008, 20.1, -36.5, -8.2],
		 [2009, -11.1, 25.9, 7.4],
		 [2013, -9.1, 32.2, 11.6],
         ]

fig14A = ff.create_table(trace0)
fig14A.layout.width=1000
fig14A.layout.margin=({'l':220, 'r':150, 't':50, 'b':50})

# Function for interactive viz

def SavingsMonte(trials, mix, balance, expense, inflation, years):
    """
    Returns balances with stochastic Returns
    return balances(trials,years)
    """

    muS = data1['SP500'].rolling(1).mean().mean()-.02 #Return
    volS = data1['SP500'].rolling(1).mean().std() # Std Dev
    muB = data1['LIR'].rolling(1).mean().mean()-.02
    volB = data1['LIR'].rolling(1).mean().std()

    balances = np.zeros((trials,years))
    expenses = np.zeros(years)
    annual_rs = np.zeros((trials,years))
    annual_rb = np.zeros((trials,years))
    annual_rm = np.zeros((trials,years))

    for i in range(trials):
        annual_rs[i,] = np.random.normal(muS,volS,years)
        annual_rb[i,] = np.random.normal(muB,volB,years)
        annual_rm[i,] = mix*annual_rs[i,] + (1-mix)*annual_rb[i,]

        balances[i][0] = balance
        expenses[0] = expense

        for t in range(years-1):
            balances[i][t+1] = (1+annual_rm[i][t])*balances[i][t] - expenses[t]
            expenses[t+1] = expenses[t]*inflation

    return balances

# Main Program

app = dash.Dash(__name__)

# Configuration files

hstyle = {  'text-align': 'center',
            'fontSize': 40,
            'font-family': 'Verdana',
            'marginTop': 50,
            'marginBottom':50,
            'marginLeft': 160,
            'marginRight':160
            }

h3style = {  'text-align': 'center',
            'fontSize': 18,
			'font-style': 'italic',
            'font-family': 'Verdana',
            'marginTop': 50,
            'marginLeft': 200,
            'marginRight':200,
			'marginBottom': 50
            }

h2style = {  'text-align': 'center',
            'fontSize': 20,
            'font-family': 'Verdana',
            'marginTop': 100,
            'marginLeft': 200,
            'marginRight':200
            }

pstyle = {  'text-align': 'left',
            'fontSize': 18,
            'font-family': 'Georgia',
            'color':'DimGrey',
            'marginLeft': 200,
            'marginRight':200
            }

sstyle = {  'text-align': 'left',
            'fontSize': 14,
            'font-family': 'Verdana',
            'color':'DimGrey',
            'marginLeft': 170,
            'marginRight':170
            }

tstyle = {  'text-align': 'center',
            'fontSize': 14,
            'font-family': 'Verdana',
            'color':'DimGrey',
            'marginLeft': 150,
            'marginRight':150
            }


config = {'showLink': False}

app.layout = html.Div([

    html.H1('HOW MUCH DO I NEED FOR RETIREMENT?',
    style=hstyle),

    html.H3('“It’s tough to make predictions, especially about the future”:  Yogi Berra',
	style=h3style),

	html.P('Planning for retirement used to be easier. Lifespans were shorter, and many people received annual pensions. Today, you could live for thirty years in retirement, but without a company pension, it’s crucial to have saved enough to fund your living expenses.',
    style=pstyle),

    html.P('So how much is enough? What is the impact of inflation and spending? And is it better to play it safe, or invest in riskier assets?',
	style=pstyle),

    html.P('Scroll down to explore how to plan for retirement in an uncertain world.',
    style=pstyle),

    html.H3('In a perfect world...',
    style=h2style),

    html.P('You know your lifespan, your expenses are the same each year, and you have enough savings at the start to allow you to spend that amount every year for the rest of your life. That ideal scenario is shown below. Rollover the chart to see the amount you have left each year.',
    style=pstyle),

    dcc.Graph(
        id='figure1',
        figure={
            'data': d1,
            'layout':
            go.Layout(
            autosize=True,
            title='$1 Million Will Last 30 Years If You Spend About $33,000 Per Year',
            xaxis=dict(title='Year', range=[2017,2047]),
            yaxis=dict(title='Dollars',
            rangemode='nonnegative',
            autorange=True),
            margin=go.Margin(
                l=160,
                r=160,
                b=100,
                t=100),
            annotations=[
                dict(x=2047,y=0,
                    xref='x', yref='y',
                    text='Just Enough!',
                    showarrow=True,
                    arrowhead=7,
                    ax=0,
                    ay=-40)
            ]
            )
            },
        config=config
        ),

    html.H3("But in the real world there's inflation",
    style=h2style),

    html.P('Inflation increases your living expenses over time. With only 3% inflation each year, your $33,000 of annual expenses would rise to almost $80,000 in 2047. More expenses = Less savings. Use the slider on the chart below to see the impact of increasing inflation.',
    style=pstyle),

    dcc.Graph(id='figure2'),

    html.Div(['Explore the impact of inflation: ',dcc.Slider(
        id='inflation-slider',
        min=0,
        max=10,
        value=0,
        step=1,
        marks={str(inflation): '{}%'.format(inflation) for inflation in np.arange(0,10,1)})], style=sstyle),

    html.H3('And your expenses may be different',
    style=h2style),

    html.P('In our perfect world, you can only spend just over 3% of your starting assets each year for 30 years. But how does spending impact retirement savings? On the chart below, adjust your spending with the slider and see the effect.',
    style=pstyle),

    dcc.Graph(id='figure3'),

    html.Div(['Expenses as a percentage of starting savings: ',dcc.Slider(
        id='expenses-slider',
        min=1,
        max=10,
        value=1,
        step=1,
        marks={str(expenses): '{}%'.format(expenses) for expenses in np.arange(1,11,1)})], style=sstyle),

    html.H3('The solution to inflation: Earn a return on your assets',
    style=h2style),

    html.P('Earning a reasonable return each year allows you to maintain your spending for longer. If you experience 3% inflation, but also earn 3% on your assets, your money can again last the full 30 years.',
    style=pstyle),

    dcc.Graph(
        id='figure4',
        figure={
            'data': d4,
            'layout':
            go.Layout(
            autosize=True,
            title='Inflation and Returns Can Offset Each Other',
            xaxis=dict(title='Year',range=[2017,2047]),
            yaxis=dict(title='Dollars\n',
            rangemode='nonnegative',
            autorange=True),
            margin=go.Margin(
                l=160,
                r=160,
                b=100,
                t=100),
            annotations=[
                dict(x=2047,y=0,
                    xref='x', yref='y',
                    text='Just Enough<br>Again!',
                    showarrow=True,
                    arrowhead=7,
                    ax=0,
                    ay=-80)
                ]
                )
        }, config=config),


    html.H3('The solution to inflation and expenses: Earn a higher return',
    style=h2style),

    html.P('In this example your starting expenses are higher at $50,000. Earn the same as inflation and your savings last twenty years. Earn 5% and your money still only lasts an extra five years.',
    style=pstyle),

    dcc.Graph(
        id='figure5',
        figure={
            'data': d5,
            'layout':
            go.Layout(
            autosize=True,
            title='Earning More Will Help Stretch Your Savings',
            xaxis=dict(title='Year',range=[2017,2047]),
            yaxis=dict(title='Dollars',
            rangemode='nonnegative',
            autorange=True),
            margin=go.Margin(
                l=160,
                r=160,
                b=100,
                t=100),
            annotations=[
                dict(x=2044,y=0,
                    xref='x', yref='y',
                    text='Not Good Enough',
                    showarrow=True,
                    arrowhead=7,
                    ax=0,
                    ay=-100)
                ]
                )
        }, config=config),

    html.H3('So what return is good enough?',
    style=h2style),

    html.P('Investment returns can make all the difference between donating to charity and needing charity in retirement. With the same $50,000 spending and 3% inflation as before, use the slider in the chart below to see the impact of different returns on your savings.',
    style=pstyle),

    dcc.Graph(id='figure6'),

    html.Div(['Annual return on your savings: ',
        dcc.Slider(
        id='return-slider',
        min=0,
        max=10,
        value=5,
        step=1,
        marks={str(returns): '{}%'.format(returns) for returns in np.arange(0,11,1)})], style=sstyle),

    html.H3('Returns matter: So does timing',
    style=h2style),

    html.P('It’s clear that a higher average return is better. But averages can be misleading. The two scenarios below look very different, but in both cases you earn 7% for 15 years, and 5% for 15 years. The only difference is which comes first.',
    style=pstyle),

    dcc.Graph(
        id='figure7',
        figure={
            'data': d7,
            'layout': go.Layout(title='Same Returns, Different Order, Different Outcome',
            xaxis=dict(title='Year',range=[2017,2047]),
            yaxis=dict(title='Dollars',
            rangemode='nonnegative',
            autorange=True),
            margin=go.Margin(
                l=160,
                r=160,
                b=100,
                t=100)
            )
        }, config=config),

    html.P('Higher returns at the beginning are more beneficial, because your savings are larger.', style=pstyle),

    html.H3('The real world of investing in retirement',
    style=h2style),

    html.P('The Savings Ideal: A guaranteed return, well above inflation.',
    style=pstyle),

	html.P('The Savings Reality: No guarantee. To supplement Social Security income, most people have to fund their retirements with stocks and bonds.',
    style=pstyle),

	html.P('There are many different stocks and bonds. To simplify this analysis, the tables and charts use the S&P500 Index (an index of the 500 largest companies by market capitalization in the US) as a proxy for stocks, and a US government bond with a ten year maturity as a proxy for bonds. A summary of the returns for the last hundred years is shown below.',
    style=pstyle),

    dcc.Graph(
        id='figure8',
        figure=fig8),


    html.H3('Bonds: Reasonable return, with some risk',
    style=h2style),

    html.P("US Government bonds are considered very safe, but there have been years where investors made a lot more or a lot less than the average. Rollover the chart below to examine the returns.",
    style=pstyle),

    dcc.Graph(
        id='figure9',
        figure={
            'data': d9,
            'layout': go.Layout(title='Annual Returns of Bonds (10 year US Treasuries) 1928-2016',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Percent\n',
                autorange=True),
            margin=go.Margin(
                l=160,
                r=160,
                b=100,
                t=100),
			annotations=[
                dict(x='2008',y=35,
                    xref='x', yref='y',
                    text='Great<br>Recession<br>2008-09',
                    showarrow=False),
                dict(x='1974',y=35,
                    xref='x', yref='y',
                    text="Mid 70's<br>Recession",
                    showarrow=False),
			    dict(x='2001',y=35,
                    xref='x', yref='y',
                    text='Tech<br>Bust<br>2000-02',
                    showarrow=False)
				    ]
            )
        }, config=config),

    html.H3('Stocks: Higher returns, more risk',
    style=h2style),

    html.P('Note the higher average return. But it comes with greater volatility. Again rollover the chart to compare each year with the average.',
    style=pstyle),

    dcc.Graph(
        id='figure10',
        figure={
            'data': d10,
            'layout': go.Layout(title='Annual Returns of Stocks (S&P500 Index) 1928-2016',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Percent\n',
                autorange=True),
            margin=go.Margin(
                l=160,
                r=160,
                b=100,
                t=100),
            annotations=[
                dict(x='2008',y=50,
                    xref='x', yref='y',
                    text='Great<br>Recession<br>2008-09',
                    showarrow=False,
                    ),
                dict(x='1974',y=50,
                    xref='x', yref='y',
                    text="Mid 70's<br>Recession",
                    showarrow=False),
				dict(x='2001',y=50,
                    xref='x', yref='y',
                    text='Tech<br>Bust<br>2000-02',
                    showarrow=False,
                    )
				    ]
                )
        }, config=config),

    html.H3('Another way of looking at those returns',
    style=h2style),

    html.P('This chart shows the distribution of those annual returns. Around 40% of the time, those returns have been between 0% and 5%, though there have also been very good years, such as 1982, and poor years such as 2009.',
    style=pstyle),

    dcc.Graph(
        id='figure11',
        figure={
        'data':d11,
        'layout': go.Layout(title='The Distribution of Returns on Bonds',
        xaxis=dict(title='Annual Returns', range=[-50,60]),
        yaxis=dict(title='Occurences'),
        hovermode = False,
		margin=go.Margin(
            l=160,
            r=160,
            b=100,
            t=100),
		annotations=[
            dict(x='22.5',y=38,
                xref='x', yref='y',
                text='2008',
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
	        dict(x='17.5',y=38,
                xref='x', yref='y',
                text='2000<br>2002',
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-40),
	        dict(x='-12.5',y=38,
                xref='x', yref='y',
                text='2009',
				font=dict(
                family='Verdana',
                size=12,
                color='Red'
                ),
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
			dict(x='-7.5',y=38,
                xref='x', yref='y',
                text='2013',
                font=dict(
                family='Verdana',
                size=12,
                color='Red'
                ),
				showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
			dict(x='7.5',y=38,
                xref='x', yref='y',
                text='2001',
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
			dict(x='32.5',y=38,
                xref='x', yref='y',
                text='1982',
				font=dict(
                family='Verdana',
                size=12,
                color='DarkGray'
                ),
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30)

			    ]
            )
    }, config=config),

    html.H3('The equivalent distribution for stocks',
    style=h2style),

    html.P('Greater dispersion. The average may be 11%, but in most years, you will either make quite a lot more or less than the average.',
    style=pstyle),

    dcc.Graph(
        id='figure12',
        figure={
        'data':d12,
        'layout': go.Layout(title='The Distribution of Returns on Stocks',
        xaxis=dict(title='Annual Returns', range=[-50,60]),
        yaxis=dict(title='Occurences'),
        hovermode = False,
		margin=go.Margin(
            l=160,
            r=160,
            b=100,
            t=100),
		annotations=[
            dict(x='27.5',y=38,
                xref='x', yref='y',
                text='2009',
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
	        dict(x='-12.5',y=38,
                xref='x', yref='y',
                text='2001',
                font=dict(
                family='Verdana',
                size=12,
                color='Red'
                ),
				showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
	        dict(x='-37.5',y=38,
                xref='x', yref='y',
                text='2008',
				font=dict(
                family='Verdana',
                size=12,
                color='Red'
                ),
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
			dict(x='-7.5',y=38,
                xref='x', yref='y',
                text='2000',
                font=dict(
                family='Verdana',
                size=12,
                color='Red'
                ),
				showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
			dict(x='-22.5',y=38,
                xref='x', yref='y',
                text='2002',
                font=dict(
                family='Verdana',
                size=12,
                color='Red'
                ),
				showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
			dict(x='32.5',y=38,
                xref='x', yref='y',
                text='2013',
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30),
		    dict(x='22.5',y=38,
                xref='x', yref='y',
                text='1982',
				font=dict(
                family='Verdana',
                size=12,
                color='DarkGray'
                ),
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=-30)
		    ]
        )
    }, config=config),

    html.H3('Stocks or bonds or both?',
    style=h2style),

    html.P('Higher returns or less risk? Rather than considering stocks and bonds as an either / or proposition, there are good reasons to consider both together. Different factors drive the returns of stocks and bonds.',
    style=pstyle),

	html.P('There are years like 1982, when both do well. More recently, in the tech bust and great recession, bad years for stocks have been good years for bonds and vice versa. The table below shows the returns from both, along with the returns of a 50/50 mix.',
    style=pstyle),

    dcc.Graph(
    id='figure14A',
    figure=fig14A),

	# dcc.Graph(
        # id='figure14',
        # figure={
        # 'data':d14,
        # 'layout': go.Layout(title='When Stocks are Up, Bonds are Usually Down and Vice Versa',
        # barmode='group',
        # xaxis=dict(title='Year'),
        # yaxis=dict(title='Percent'),
        # margin=go.Margin(
            # l=160,
            # r=160,
            # b=100,
            # t=100)
        # )
    # }, config=config),


    html.H3('Now it’s your turn…',
    style=h2style),

    html.P('Explore how inflation, spending and your investment allocation influence the future value of your retirement assets. Adjust the sliders below to match your expectations, then view some of the potential outcomes.',
    style=pstyle),

    html.P('---'),

    html.Div(['Set your expected rate of inflation: ',
        dcc.Slider(
        id='inflation_inter',
        min=0,
        max=10,
        value=3,
        step=1,
        marks={str(inflation_inter): '{}%'.format(inflation_inter) for inflation_inter in np.arange(0,11,1)})], style=sstyle),

    html.P('---'),

    html.Div(['Set your expenses as a percentage of your starting savings: ',
        dcc.Slider(
        id='expenses_inter',
        min=0,
        max=10,
        value=5,
        step=1,
        marks={str(expenses_inter): '{}%'.format(expenses_inter) for expenses_inter in np.arange(0,11,1)})], style=sstyle),

    html.P('---'),

    html.Div(['Set your preferred investment mix: (0 = all bonds, 1 = all stocks): ',
        dcc.Slider(
        id='mix_slider',
        min=0,
        max=1,
        value=.5,
        step=.1,
        marks={0: '0', 0.1:'0.1', 0.2:'0.2', 0.3:'0.3',0.4:'0.4', 0.5:'0.5', 0.6:'0.6', 0.7:'0.7',0.8:'0.8',0.9:'0.9', 1:'1'}
        )], style=sstyle),

    html.P('---'),

    dcc.Graph(
        id='figure15',
        config=config
        ),

    html.P('Each line in the graph above is one possible outcome. The graph below gives you a sense of the number of outcomes which are above 0. If you want to be sure of a high likelihood of having enough savings, you will need to spend less or take some risk to earn higher returns.', style=pstyle),

    dcc.Graph(
        id='figure16',
        config=config
        )

])

@app.callback(dash.dependencies.Output('figure2','figure'),
                [dash.dependencies.Input('inflation-slider', 'value')])

def show_d2_graph(inflation):
    trace = go.Bar(
             x=np.arange(2017, 2017+years),
             y=Savings(1e6,1e6/years,0,(1+inflation/100),years),
             name='Savings',
             text='Savings',
             marker=dict(color=colorscheme[1])
             )

    return {
        'data': [trace],
        'layout':
        go.Layout(
        title='Higher Inflation Will Reduce Your Savings',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Dollars',
        rangemode='nonnegative',
        autorange=True),
        margin=go.Margin(
            l=160,
            r=160,
            b=100,
            t=100)
        )
    }

@app.callback(dash.dependencies.Output('figure3','figure'),
                [dash.dependencies.Input('expenses-slider', 'value')])

def show_d3_graph(expenses):
    trace = go.Bar(
             x=np.arange(2017, 2017+years),
             y=Savings(1e6,expenses/100*1e6,0,1,years),
             name='Savings',
             text='Savings',
             marker=dict(color=colorscheme[1])
             )

    return {
        'data': [trace],
        'layout':
        go.Layout(
        title='Higher Expenses Will Reduce Your Savings',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Dollars\n',
        rangemode='nonnegative',
        autorange=True),
        margin=go.Margin(
            l=160,
            r=160,
            b=100,
            t=100)
        )
    }

@app.callback(dash.dependencies.Output('figure6','figure'),
                [dash.dependencies.Input('return-slider', 'value')])

def show_d6_graph(returns):
    trace = go.Bar(
             x=np.arange(2017, 2017+years),
             y=Savings(1e6,5e4,returns,1.03,years),
             name='Savings',
             text='Savings',
             marker=dict(color=colorscheme[2])
             )

    return {
        'data': [trace],
        'layout':
        go.Layout(
        title='Higher Returns Will Increase Your Savings',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Dollars\n',
        rangemode='nonnegative',
        autorange=True),
        margin=go.Margin(
            l=160,
            r=160,
            b=100,
            t=100)
        )
    }


@app.callback(dash.dependencies.Output('figure15','figure'),
                [dash.dependencies.Input('inflation_inter', 'value'),
                dash.dependencies.Input('expenses_inter', 'value'),
                dash.dependencies.Input('mix_slider', 'value')])

def show_d15_graph(inflation_inter,expenses_inter,mix_slider):

    years = 31

    balances = SavingsMonte(100,mix_slider,1e6,expenses_inter/100*1e6,1+inflation_inter/100,years)

    d = []
    for i in np.arange(balances.shape[0]):
        trace0 = go.Scatter(
            y = balances[i,],
            x = np.arange(2017,2017+years),
            hoverinfo='none',
            showlegend=False,
            mode='line',
            line=dict(color=colorscheme[4], width=0.5, dash='dot'
            )
            )
        d.append(trace0)


    return {
        'data': d,
        'layout':
        go.Layout(
        title='Possible Outcomes Over the Next 30 Years',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Dollars',
        range=[-1e6,5e6]),
        margin=go.Margin(
            l=160,
            r=160,
            b=100,
            t=100)
        )
    }

@app.callback(dash.dependencies.Output('figure16','figure'),
                [dash.dependencies.Input('inflation_inter', 'value'),
                dash.dependencies.Input('expenses_inter', 'value'),
                dash.dependencies.Input('mix_slider', 'value')])

def show_d16_graph(inflation_inter,expenses_inter,mix_slider):

    years = 31

    balances = SavingsMonte(1000,mix_slider,1e6,expenses_inter/100*1e6,1+inflation_inter/100,years)

    trace0 = go.Scatter(
        y = np.count_nonzero(balances >= 0, axis=0)/1000*100,
        x = np.arange(2017,2017+years),
        #name = 'Percent',
        #hoverinfo = 'y' + 'text',
        text = 'Percent of Outcomes Have Some Savings',
        mode = 'markers',
        marker = dict(color=colorscheme[1], size=8),
        showlegend=False
        )

    trace1 = go.Scatter(
        x = np.arange(2017,2017+years),
        y = 50*np.ones(years),
        showlegend = False,
        hoverinfo='none',
        mode = 'lines',
        line=dict(width=2, dash='dash',
              color=colorscheme[4])

        )

    return {
        'data': [trace0, trace1],
        'layout':
        go.Layout(
        title='Percentage of Outcomes With Income Greater Than Zero Over the Year',
        xaxis=dict(title='Year',
        range=[2017,2047]),
        yaxis=dict(title='Percent',
        range=[0,105]),
        margin=go.Margin(
            l=160,
            r=160,
            b=100,
            t=100),
        annotations=[
            dict(x='2023',y=90,
                xref='x', yref='y',
                text='More confident',
                font=dict(
                    family='Verdana',
                    size=12,
                    color='Green'
                    ),
				showarrow=True,
                arrowhead=1,
                ax=0,
                ay=35),
            dict(x='2023',y=10,
                xref='x', yref='y',
                text='Less confident',
                font=dict(
                    family='Verdana',
                    size=12,
                    color='Red'
                    ),
				showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-35)]
        )
    }

if __name__ == '__main__':
#    port =vint(os.environ.get("PORT", 61014))
#    app.run_server(host='0.0.0.0', port=port, debug=True)
    app.run_server(host='0.0.0.0', debug=True)
