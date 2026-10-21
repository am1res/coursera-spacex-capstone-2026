"""Historical course dashboard; run locally on 127.0.0.1:8055."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash,dcc,html,Input,Output
DATA=Path(__file__).resolve().parent/'dashboard_launches.csv'
df=pd.read_csv(DATA)
app=Dash(__name__)
app.layout=html.Main([
 html.H1('SpaceX launches: a historical course dataset'),
 html.P('90 recorded flights, 2010–2020. Success follows the course landing label and includes successful ocean outcomes.'),
 html.Label('Launch site'),dcc.Dropdown(id='site',options=[{'label':'All sites','value':'ALL'}]+[{'label':s,'value':s} for s in sorted(df.LaunchSite.unique())],value='ALL',clearable=False),
 html.Label('Payload mass (kg)'),dcc.RangeSlider(id='payload',min=0,max=16000,step=500,value=[0,16000],marks={0:'0',4000:'4,000',8000:'8,000',12000:'12,000',16000:'16,000'}),
 dcc.Graph(id='success-pie'),dcc.Graph(id='payload-scatter'),
 html.P('The API and SQL snapshots differ: the 2016-09-01 row has no SQL booster-version category and is labeled Unknown. These data do not describe current launch reliability or pricing.')
],style={'maxWidth':'1100px','margin':'30px auto','fontFamily':'Arial, sans-serif'})

def empty_figure(message):
 f=go.Figure();f.add_annotation(text=message,x=.5,y=.5,showarrow=False);f.update_layout(xaxis_visible=False,yaxis_visible=False);return f

@app.callback(Output('success-pie','figure'),Output('payload-scatter','figure'),Input('site','value'),Input('payload','value'))
def update_figures(site,mass_range):
 low,high=mass_range
 subset=df[df.PayloadMass.between(low,high)]
 if site!='ALL':subset=subset[subset.LaunchSite.eq(site)]
 if subset.empty:return empty_figure('No flights in this selection'),empty_figure('No flights in this selection')
 if site=='ALL':
  successes=subset.loc[subset.Class.eq(1)].groupby('LaunchSite').size().reset_index(name='Successful course labels')
  pie=px.pie(successes,names='LaunchSite',values='Successful course labels',title='Successful course labels by launch site') if not successes.empty else empty_figure('No successful labels in this payload range')
 else:
  counts=subset.Class.value_counts().reindex([0,1],fill_value=0)
  pie=go.Figure(go.Pie(labels=['Other outcome (0)','Successful course label (1)'],values=counts.values));pie.update_layout(title=f'{site}: outcomes in selected payload range')
 scatter=px.scatter(subset,x='PayloadMass',y='Class',color='BoosterVersionCategory',hover_data=['FlightNumber','Date','LaunchSite'],title=f'Payload and recorded outcome: {site}')
 scatter.update_yaxes(tickvals=[0,1],ticktext=['Other (0)','Successful (1)']);scatter.update_xaxes(title='Payload mass (kg)')
 return pie,scatter

if __name__=='__main__':app.run(host='127.0.0.1',port=8055,debug=False)
