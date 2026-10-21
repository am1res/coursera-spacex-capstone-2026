"""Create actual historical launch map and runnable dashboard from official snapshots."""
import json
from pathlib import Path
import pandas as pd
import folium
from folium.plugins import MarkerCluster
ROOT=Path(__file__).resolve().parent
frame=pd.read_csv(ROOT/'derived_dataset_part_2.csv')
version=pd.read_csv(ROOT/'Spacex_SQL.csv')[['Date','Booster_Version']]
version['BoosterVersionCategory']=version.Booster_Version.str.extract(r'^(F9\s+\S+)')
# Join public course snapshots by launch date, requiring unique date records.
frame=frame.merge(version[['Date','BoosterVersionCategory']],on='Date',how='left',validate='one_to_one')
missing_dates=frame.loc[frame.BoosterVersionCategory.isna(),'Date'].tolist()
(ROOT/'snapshot-join-notes.json').write_text(json.dumps({'missing_sql_dates':missing_dates,'handling':'Preserve the API-snapshot row and use Unknown in SQL snapshot for booster category; do not invent a version.'},indent=2))
frame['BoosterVersionCategory']=frame.BoosterVersionCategory.fillna('Unknown in SQL snapshot')
frame.to_csv(ROOT/'dashboard_launches.csv',index=False)
m=folium.Map(location=[35,-95],zoom_start=4)
for site,group in frame.groupby('LaunchSite'):
 row=group.iloc[0];coord=[row.Latitude,row.Longitude]
 folium.Circle(coord,radius=1300,color='#256d85',fill=True,popup=f'{site}: {len(group)} historical flights').add_to(m)
 folium.Marker(coord,tooltip=site,icon=folium.DivIcon(html=f'<div style="font-size:12px;font-weight:bold;white-space:nowrap">{site}</div>')).add_to(m)
cluster=MarkerCluster(name='Launches (2010–2020)').add_to(m)
for row in frame.itertuples():
 folium.Marker([row.Latitude,row.Longitude],tooltip=f'Flight {row.FlightNumber}: {row.Date}',popup=f'{row.LaunchSite}; payload {row.PayloadMass:.0f} kg; course class {row.Class}',icon=folium.Icon(color='green' if row.Class else 'red',icon='rocket',prefix='fa')).add_to(cluster)
folium.LayerControl().add_to(m);m.save(ROOT/'historical_launch_map.html')
print('Map created for',len(frame),'flights at',frame.LaunchSite.nunique(),'sites.')
