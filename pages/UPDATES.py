import pandas as pd 
import streamlit as st 
import os
import numpy as np
import gspread
from openpyxl import load_workbook
from pathlib import Path
import traceback
import time
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_gsheets import GSheetsConnection
from datetime import datetime 
import datetime as dt

cluster = ''
consent = ''
district = ''
facility = ''
partners = ''
age = ''
name = ''
htn = ''
dm = ''
AS = ''
MH = ''
sex = ''
others = ''
otherissue = ''
adher = ''

st.write('**FOLLOW UP SECTION ON AREAS NOT COMPLETED FROM THE FIELD**')
if 'tx' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'DEMO', usecols=list(range(18)),ttl=5)
        tx = exist.dropna(how='all')
        st.session_state.tx = tx
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dfdemo = st.session_state.tx.copy()

if 'txa' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'ISSUES', usecols=list(range(17)),ttl=5)
        txa = exist.dropna(how='all')
        st.session_state.txa = txa
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dfiss = st.session_state.txa.copy()
#########################################################################################################

if 'txb' not in st.session_state:     
     try:
        #cola,colb= st.columns(2)
        conn = st.connection('gsheets', type=GSheetsConnection)
        exist = conn.read(worksheet= 'TESTS', usecols=list(range(18)),ttl=5)
        txb = exist.dropna(how='all')
        st.session_state.txb = txb
     except:
         st.write("POOR NETWORK, COULDN'T CONNECT TO DELIVERY DATABASE")
         st.stop()
dftest = st.session_state.txb.copy()

################################################################################################################

file = r'CLUSTERS.csv'
dfa = pd.read_csv(file)

clusters = dfa['CLUSTER'].unique()

cluster = st.radio('**CHOOSE A CLUSTER**', clusters, index= None, horizontal=True)

if not cluster:
    st.stop()
else:
    pass
if cluster:
    dfd = dfa[dfa['CLUSTER'] == cluster].copy()
    districts = dfd['DISTRICT'].unique()
    district = st.radio('**CHOOSE A district**', districts, index= None, horizontal=True)

if not district:
    st.stop()
else:
    pass
col1,col2, col3 = st.columns([2,1,2])
with col1:
    if district:
        fac = dfa[dfa['DISTRICT'] == district].copy()
        facilities = fac['FACILITY'].unique()
        facility = st.selectbox('**SELECT FACILITY**', facilities, index= None)

if not facility:
    st.stop()
else:
    pass
    
dftest['FACILITY'] = dftest['FACILITY'].astype(str)
dftest = dftest[dftest['FACILITY'] == facility].copy()

dfiss['FACILITY'] = dfiss['FACILITY'].astype(str)
dfiss = dfiss[dfiss['FACILITY'] == facility].copy()

dfdemo['FACILITY'] = dfdemo['FACILITY'].astype(str)
dfdemo = dfdemo[dfdemo['FACILITY'] == facility].copy()


filen = r'ALL.csv'
dfn = pd.read_csv(filen)

dfna = dfn[dfn['FACILITY'] == facility].copy()

check = st.pills('**WHAT DO YOU WANT TO DO?**', options = ['CHECK UPDATE STATUS', '','','MAKE UPDATES','', 'DOWNLOAD FORM'])

if not check:
    st.stop()
elif check == 'MAKE UPDATES':
    col1, col2,col3 = st.columns(3)
    art = col1.number_input('**SEARCH ART No.**', value=None, step=1)
    if not art:
         st.stop()
    # dftest['ART NO'] = pd.to_numeric(dftest['ART NO'], errors = 'coerce')
    # dfdemo['ART NO'] = pd.to_numeric(dfiss['ART NO'], errors = 'coerce')
    # dfiss['ART NO'] = pd.to_numeric(dfiss['ART NO'], errors = 'coerce')
    dfdemo = dfdemo[dfdemo['ART NO'] == art].copy()
    if dfdemo.shape[0] == 0:
         st.info(f'**ART NP {art} NOT FOUND IN THE DATA BASE**')
         st.stop()
    else:
         pass
    dftest= dftest[dftest['ART NO'] == art].copy()
    dfiss = dfiss[dfiss['ART NO'] == art].copy()
    partners = dfiss.iloc[0,8]
    st.write('**APN SECTION**')
    st.write(f'**Client with ART NO {art} had {partners} ellicited**')
    st.write(f'**OF THESE {partners}, how many have been:**')
    col1,col2,col3,col4 = st.columns(4)
    notif = col1.number_input('**NOTIFIED**', value=None, step=1)
    tested = col2.number_input('**TESTED**', value=None, step=1)
    col1,col2, col3 = st.columns(3) 
    pos = col1.number_input('**HOW MANY WERE NEWLY POSTIVE**', value=None, step=1)
    alread = col2.number_input('**HOW MANY WERE KNOWN POSTIVE**', value=None, step=1)
    linked = col3.number_input('**HOW MANY WERE LINKED**', value=None, step=1)
    st.write(f'**OF THE {pos}, how many have:**')
    col1,col2, col3 = st.columns(3) 
    recency = col1.number_input('**RECENCY TEST**', value=None, step=1)
    alread = col2.number_input('**RECENT RESULT**', value=None, step=1)
    linked = col3.number_input('**LONGTERM RESULTS**', value=None, step=1)
    
elif check == 'DOWNLOAD FORM':
    col1, col2,col3 = st.columns(3)
    art = col1.number_input('**SEARCH ART No.**')
elif check == 'MAKE UPDATES':
    pass

st.stop()
