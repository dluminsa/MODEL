import pandas as pd 
import streamlit as st 
import os
import gspread
from pathlib import Path
import random
import plotly.express as px
import plotly.graph_objects as go
import traceback
import time
from streamlit_gsheets import GSheetsConnection
from datetime import datetime 


if 'tx' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'DEMO', usecols=list(range(20)),ttl=5)
        tx = exist.dropna(how='all')
        st.session_state.tx = tx
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dfdemo = st.session_state.tx.copy()

dfdemo['FACILITY'] = dfdemo['FACILITY'].astype(str)
dfdemo['DT'] = dfdemo['DATE'].astype(str)
facilities = dfdemo['FACILITY'].unique()

dfdemoz = []
for facil in facilities:
     dfissa = dfdemo[dfdemo['FACILITY']==facil].copy()
     dfissa[['YEAR','MONTH','DAY']] = dfissa['DT'].str.split('-', expand=True)
     dfissa[['ART NO', 'YEAR', 'MONTH', 'DAY']] = dfissa[['ART NO', 'YEAR', 'MONTH', 'DAY']].apply(pd.to_numeric, errors='coerce')
     dfissa = dfissa.sort_values(by = ['YEAR', 'MONTH', 'DAY'], ascending = [False, False, False])
     dfissa = dfissa.drop_duplicates(subset = ['ART NO', 'YEAR', 'MONTH', 'DAY'])
     dfdemoz.append(dfissa)
dfdemo = pd.concat(dfdemoz)
dfdemo[['ART NO', 'DAY', 'MONTH']] = dfdemo[['ART NO', 'DAY', 'MONTH']].astype(str)
dfdemo['ART'] = dfdemo['MONTH'] + dfdemo['DAY'] + dfdemo['ART NO'] 


if 'txa' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'ISSUES', usecols=list(range(18)),ttl=5)
        txa = exist.dropna(how='all')
        st.session_state.txa = txa
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dfiss = st.session_state.txa.copy()

dfiss['FACILITY'] = dfiss['FACILITY'].astype(str)
dfiss['DT'] = dfiss['DATE'].astype(str)
facilities = dfiss['FACILITY'].unique()

dfissz = []
for facil in facilities:
     dfissa = dfiss[dfiss['FACILITY']==facil].copy()
     dfdemu = dfdemo[dfdemo['FACILITY'] == facil].copy()
     try:
          distr = dfdemu.iloc[0,1]
          clus = dfdemu.iloc[0,0]
     except:
           distr = ''
           clus = ''
     dfissa[['YEAR','MONTH','DAY']] = dfissa['DT'].str.split('-', expand=True)
     dfissa[['ART NO', 'YEAR', 'MONTH', 'DAY']] = dfissa[['ART NO', 'YEAR', 'MONTH', 'DAY']].apply(pd.to_numeric, errors='coerce')
     dfissa = dfissa.sort_values(by = ['YEAR', 'MONTH', 'DAY'], ascending = [False, False, False])
     dfissa = dfissa.drop_duplicates(subset = ['ART NO', 'YEAR', 'MONTH', 'DAY'])
     dfissa['DISTRICT'] = distr
     dfissa['CLUSTER'] = clus
     dfissz.append(dfissa)
dfiss = pd.concat(dfissz)
dfiss[['ART NO', 'DAY', 'MONTH']] = dfiss[['ART NO', 'DAY', 'MONTH']].astype(str)
dfiss['ART'] = dfiss['MONTH'] + dfiss['DAY'] + dfiss['ART NO'] 


#########################################################################################################

if 'txb' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'TESTS', usecols=list(range(19)),ttl=5)
        txb = exist.dropna(how='all')
        st.session_state.txb = txb
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dftest = st.session_state.txb.copy()

dftest['FACILITY'] = dftest['FACILITY'].astype(str)
dftest['DT'] = dftest['DATE'].astype(str)
facilities = dftest['FACILITY'].unique()

dftestz = []
for facil in facilities:
     dftisa = dftest[dftest['FACILITY']==facil].copy()
     dfdemu = dfdemo[dfdemo['FACILITY'] == facil].copy()
     try:
          distr = dfdemu.iloc[0,1]
          clus = dfdemu.iloc[0,0]
     except:
           distr = ''
           clus = ''
     dftisa[['YEAR','MONTH','DAY']] = dftisa['DT'].str.split('-', expand=True)
     dftisa[['ART NO', 'YEAR', 'MONTH', 'DAY']] = dftisa[['ART NO', 'YEAR', 'MONTH', 'DAY']].apply(pd.to_numeric, errors='coerce')
     dftisa = dftisa.sort_values(by = ['YEAR', 'MONTH', 'DAY'], ascending = [False, False, False])
     dftisa = dftisa.drop_duplicates(subset = ['ART NO', 'YEAR', 'MONTH', 'DAY'])
     dftisa['DISTRICT'] = distr
     dftisa['CLUSTER'] = clus
     dftestz.append(dftisa)
     
dftest = pd.concat(dftestz)
dftest[['DAY', 'MONTH']] = dftest[['DAY', 'MONTH']].astype(int)
dftest[['ART NO', 'DAY', 'MONTH']] = dftest[['ART NO', 'DAY', 'MONTH']].astype(str)
dftest['ART'] = dftest['MONTH'] + dftest['DAY'] + dftest['ART NO'] 


################################################################################################################
if 'txy' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'UPDATES', usecols=list(range(19)),ttl=5)
        txy = exist.dropna(how='all')
        st.session_state.txy = txy
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dfup = st.session_state.txy.copy()
# ################################################################################################################


#ONE MERGED ONE
facilities = dfdemo['FACILITY'].unique()

dfdemz = []
dfissx = dfiss.drop(columns = ['DT', 'DISTRICT', 'CLUSTER', 'YEAR', 'MONTH', 'DAY', 'ART NO', 'DATE'])
for fac in facilities:
     dfdemu = dfdemo[dfdemo['FACILITY']==fac].copy()
     dfissu = dfissx[dfissx['FACILITY']==fac].copy()
     dfissu = dfissu.drop(columns ='FACILITY')
     dfdemu['ART'] = pd.to_numeric(dfdemu['ART'], errors = 'coerce')
     dfissu['ART'] = pd.to_numeric(dfissu['ART'], errors = 'coerce')
     dfd = pd.merge(dfdemu, dfissu, on = 'ART', how = 'inner')
     dfdemz.append(dfd)
     
dfdemo1 = pd.concat(dfdemz)

############################################################################
#last merged

dfdemoz = []

dfissy = dftest.drop(columns = ['DT', 'DISTRICT', 'CLUSTER', 'YEAR', 'MONTH', 'DAY', 'ART NO', 'DATE'])

for fac in facilities:
     dfdemux = dfdemo1[dfdemo1['FACILITY']==fac].copy()
     dfissh = dfissy[dfissy['FACILITY']==fac].copy()
     dfissh = dfissh.drop(columns ='FACILITY')
     dfdemux['ART'] = pd.to_numeric(dfdemux['ART'], errors = 'coerce')
     dfissh['ART'] = pd.to_numeric(dfissh['ART'], errors = 'coerce') 
     dfd = pd.merge(dfdemux, dfissh, on = 'ART', how = 'inner')
     dfdemoz.append(dfd)

dfdemo2 = pd.concat(dfdemoz)
dfuse = dfdemo2.copy()
#########################################################################################################
#FILTERS
clusters = dfuse['CLUSTER'].unique()
# #FILTERS
st.sidebar.subheader('**Filter from here**')
cluster = st.sidebar.multiselect('CHOOSE A CLUSTER', clusters, key='a')

# #create for the state
if not cluster:
     dfuse2 = dfuse.copy()
     
else:
     dfuse['CLUSTER'] = dfuse['CLUSTER'].astype(str)
     dfuse2 = dfuse[dfuse['CLUSTER'].isin(cluster)].copy()
     
district = st.sidebar.multiselect('**CHOOSE A DISTRICT**', dfuse2['DISTRICT'].unique(), key='J')

if not district:
     dfuse3 = dfuse2.copy()
     
else:
     dfuse2['DISTRICT'] = dfuse2['DISTRICT'].astype(str)
     dfuse3 = dfuse2[dfuse2['DISTRICT'].isin(district)].copy()

facility = st.sidebar.multiselect('**CHOOSE A DISTRICT**', dfuse3['FACILITY'].unique(), key='M')

if not facility:
     dfuse4 = dfuse3.copy()
     
else:
     dfuse3['FACILITY'] = dfuse3['FACILITY'].astype(str)
     dfuse4 = dfuse3[dfuse3['FACILITY'].isin(facility)]

dfuse = dfuse4.copy()
if cluster:
    dfuse = dfuse[dfuse['CLUSTER'].isin(cluster)].copy()

if district:
     dfuse = dfuse[dfuse['DISTRICT'].isin(district)].copy()
     
if facility:
     dfuse = dfuse[dfuse['FACILITY'].isin(facility)].copy()


#########################################################################################################
##QUICK SUMMARY
st.divider()
cola, colb, colc = st.columns(3)
colb.success('**QUICK SUMMARY**')
cola, colb, colc, cold = st.columns(4)
cola.info('**TOTAL VISITED**')
colb.info('**HLVs**')
colc.info('**PARTNERS**')
cold.info('**REBLED**')
#cole.info('**SPUTUM**'

q1 = dfuse.shape[0]
bal = pd.to_numeric(dfuse['PARTNERS'], errors='coerce').sum()
bal = int(bal)
hlvs  = dfuse[dfuse['RESULTS']>999].copy()
q2 = hlvs.shape[0]
reb = dfuse[dfuse['VL']=='YES'].copy()
txm = reb.shape[0]
#txmp = pd.to_numeric(dfuse['PICKED'], errors='coerce').sum() 


cola.metric(label='a', value =f'{q1}', label_visibility='hidden')
colb.metric(label='b', value =f'{q2}', label_visibility='hidden')
colc.metric(label='c', value =f'{bal}', label_visibility='hidden')
cold.metric(label='d', value =f'{txm}', label_visibility='hidden')
#cole.metric(label='e', value =f'{txmp}', label_visibility='hidden')
st.divider()

check = dfuse['DISTRICT'].unique()

if len (check) ==1:
     dfuse['USE'] = dfuse['FACILITY']
     word = 'FACILITY'
     label_name = 'FACILITY'
else:
     dfuse['USE'] = dfuse['DISTRICT']
     word = 'DISTRICT'
     label_name = 'DISTRICT'
     
# Get counts
district_counts = dfuse['USE'].value_counts().reset_index()
district_counts.columns = [word, 'count']
district_counts = district_counts.sort_values(by='count', ascending=True)  # Ascending for hbar

# Plot horizontal bar chart with uniform light blue color
fig = px.bar(
    district_counts,
    y=word,
    x='count',
    title=f'Number of visits done per {label_name}',
    labels={word: label_name, 'count': 'NUMBER VISITED'},
)
fig.update_traces(
    marker_color='green',                 # Set all bars to light blue
    text=district_counts['count'],            # Labels for each bar
    textposition='auto',                      # Auto label positioning
    textfont=dict(color='black', size=12)     # Label font style
)
fig.update_layout(yaxis=dict(tickfont=dict(size=12)), xaxis_title='NUMBER VISITED')

# Show plot
st.plotly_chart(fig, use_container_width=True)
st.divider()
st.write('**AHD CASCADE**')
#####
st.divider()
st.write('**APN CASCADE**')
st.divider()
st.write('**VL CASCADE***')
st.divider()
st.write('**TB CASCADE***')
st.divider()

with st.expander('**DOWNLOAD DATASET HERE**'):
         dat = dfuse.copy()
         csv_data = dat.to_csv(index=False)
         tot = dat.shape[0]
         st.write(f'**CONTAINS {tot} VISITS**')
         st.download_button(
                      label="ALL DATA SET",
                      data=csv_data,
                      file_name=f"{facility} ICSDM.csv",
                      mime="text/csv")
     
















