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
st.write(dftest.shape[0])

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
     dftisa[['ART NO', 'YEAR', 'MONTH', 'DAY']] = dfissa[['ART NO', 'YEAR', 'MONTH', 'DAY']].apply(pd.to_numeric, errors='coerce')
     dftisa = dftisa.sort_values(by = ['YEAR', 'MONTH', 'DAY'], ascending = [False, False, False])
     dftisa = dftisa.drop_duplicates(subset = ['ART NO', 'YEAR', 'MONTH', 'DAY'])
     dftisa['DISTRICT'] = distr
     dftisa['CLUSTER'] = clus
     dftestz.append(dftisa)
     
dftest = pd.concat(dftestz)
dftest[['ART NO', 'DAY', 'MONTH']] = dftest[['ART NO', 'DAY', 'MONTH']].astype(str)
dftest['ART'] = dftest['MONTH'] + dftest['DAY'] + dftest['ART NO'] 
st.write(dftest.shape[0])


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


clusters = dfdemo['CLUSTER'].unique()
# #FILTERS
st.sidebar.subheader('**Filter from here**')
cluster = st.sidebar.multiselect('CHOOSE A CLUSTER', clusters, key='a')

# #create for the state
if not cluster:
     dfdemo2 = dfdemo.copy()
     dftest2 = dftest.copy()
     dfup2 = dfup.copy()
     
else:
      pass
if cluster:
     dfd = dfdemo[dfdemo['CLUSTER'] == cluster].copy()
     districts = dfd['DISTRICT'].unique()
     district = st.radio('**CHOOSE A district**', districts, index= None, horizontal=True)

     dfearly['CLUSTER'] = dfearly['CLUSTER'].astype(str)
     dfearly2 = dfearly[dfearly['CLUSTER'].isin(CLUSTER)]

     dfrep['CLUSTER'] = dfrep['CLUSTER'].astype(str)
     dfrep2 = dfrep[dfrep['CLUSTER'].isin(CLUSTER)]
    
     water['CLUSTER'] = water['CLUSTER'].astype(str)
     water2 = water[water['CLUSTER'].isin(CLUSTER)]
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
st.write(dfdemo1.columns)

dfissy = dftest.drop(columns = ['DT', 'DISTRICT', 'CLUSTER', 'YEAR', 'MONTH', 'DAY', 'ART NO', 'DATE'])
st.write(dfissy.columns)
for fac in facilities:
     dfdemux = dfdemo1[dfdemo1['FACILITY']==fac].copy()
     dfissh = dfissy[dfissy['FACILITY']==fac].copy()
     dfissh = dfissh.drop(columns ='FACILITY')
     dfdemux['ART'] = pd.to_numeric(dfdemux['ART'], errors = 'coerce')
     dfissh['ART'] = pd.to_numeric(dfissh['ART'], errors = 'coerce')
     dfd = pd.merge(dfdemux, dfissh, on = 'ART', how = 'inner')
     dfdemoz.append(dfd)
     
dfdemo2 = pd.concat(dfdemoz)

st.write(dfdemo2.shape[0])
st.write(dfdemo2.columns)
dfdemo['ART'] = pd.to_numeric(dfdemo['ART'], errors = 'coerce')
dftest['ART'] = pd.to_numeric(dftest['ART'], errors = 'coerce')
dfdemo2['ART'] = pd.to_numeric(dfdemo2['ART'], errors = 'coerce')

dfck = dfdemo[~dfdemo['ART'].isin(dfdemo2['ART'])]
st.write(dfck)

dfck = dftest[~dftest['ART'].isin(dfdemo2['ART'])]
st.write(dfck)

# cluster = st.radio('**CHOOSE A CLUSTER**', clusters, index= None, horizontal=True)

# if not cluster:
#     st.stop()
# else:
#     pass
# if cluster:
#     dfd = dfa[dfa['CLUSTER'] == cluster].copy()
#     districts = dfd['DISTRICT'].unique()
#     district = st.radio('**CHOOSE A district**', districts, index= None, horizontal=True)

# if not district:
#     st.stop()
# else:
#     pass
# col1,col2, col3 = st.columns([2,1,2])
# with col1:
#     if district:
#         fac = dfa[dfa['DISTRICT'] == district].copy()
#         facilities = fac['FACILITY'].unique()
#         facility = st.selectbox('**SELECT FACILITY**', facilities, index= None)

# if not facility:
#     st.stop()
# else:
#     pass
    
# dftest['FACILITY'] = dftest['FACILITY'].astype(str)
# dftest = dftest[dftest['FACILITY'] == facility].copy()

# dfiss['FACILITY'] = dfiss['FACILITY'].astype(str)
# dfiss = dfiss[dfiss['FACILITY'] == facility].copy()

# dfdemo['FACILITY'] = dfdemo['FACILITY'].astype(str)
# dfdemo = dfdemo[dfdemo['FACILITY'] == facility].copy()
# factz = dfdemo['FACILITY'].unique()
# num = dfdemo.shape[0]
# if num ==0:
#      st.warning('**THERE IS NO DATA FOR THIS FACILITY**')
#      st.stop()
# dfdemoz =[]
# for facx in factz:
#      dfdemof = dfdemo[dfdemo['FACILITY']==facx].copy()
#      dfdemof = dfdemof.drop_duplicates(subset = 'ART NO', keep='last')
#      dfdemoz.append(dfdemof)
# dfdemo = pd.concat(dfdemoz)

# dfissuez =[]
# for facx in factz:
#      dfissf = dfiss[dfiss['FACILITY']==facx].copy()
#      dfissf = dfissf.drop_duplicates(subset = 'ART NO', keep='last')
#      dfissuez.append(dfissf)
# dfiss = pd.concat(dfissuez)

# dftestz =[]
# for facx in factz:
#      dftestf = dftest[dftest['FACILITY']==facx].copy()
#      dftestf = dftestf.drop_duplicates(subset = 'ART NO', keep='last')
#      dftestz.append(dftestf)
# dftest = pd.concat(dftestz)




# filen = r'ALL.csv'
# dfn = pd.read_csv(filen)

# dfna = dfn[dfn['FACILITY'] == facility].copy()
