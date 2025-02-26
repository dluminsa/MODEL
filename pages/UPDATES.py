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
from docx import Document
from docx.shared import Inches
from io import BytesIO

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
        exist = conn.read(worksheet= 'DEMO', usecols=list(range(19)),ttl=5)
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
        exist = conn.read(worksheet= 'ISSUES', usecols=list(range(18)),ttl=5)
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
    #dfiss['ART NO'] = pd.to_numeric(dfiss['ART NO'], errors = 'coerce')
    dfdemo = dfdemo[dfdemo['ART NO'] == art].copy()
    if dfdemo.shape[0] == 0:
         st.info(f'**ART NO {art} NOT FOUND IN THE DATA BASE**')
         st.stop()
    else:
         pass
    dftest= dftest[dftest['ART NO'] == art].copy()
    #dftest['PARTNERS'] = pd.to_numeric(dftest['PARTNERS'], errors = 'coerce')
    dfiss = dfiss[dfiss['ART NO'] == art].copy()
    st.write('**APN SECTION**')
    partners = dftest.iloc[0,7]
    if partners > 0:
         #partners = int(0)
         st.write(f'**Client with ART NO {art} had {partners:,.0f} partners ellicited**')
         st.write(f'**OF THESE {partners:,.0f} partners, how many have been:**')
         col1,col2 = st.columns(2)
         notif = col1.number_input('**NOTIFIED**', value=None, step=1)
         if not notif:
              st.stop()
         if notif > partners:
              st.warning("**YOU CAN'T NOTIFY MORE THAN THOSE ELLICITED**")
         else:
              st.write(f'**OF THE {notif} NOTIFIED, how were (put 0, if none):**')
              col1,col2 = st.columns(2)
              tested = col1.number_input('**TESTED**', value=None, step=1)
              if tested or tested ==0:
                        pass
              else:
                   st.stop()
              alread = col2.number_input('**KNOWN POSTIVE**', value=None, step=1)
              if alread or alread ==0:
                   pass
              else:
                   st.stop()
              checkm = tested + alread
              if checkm > notif:
                   st.warning("**TESTED AND KNOWN POS ARE MORE THAN THOSE NOTIFIED**")
                   st.stop()
              if not tested:
                   st.stop()
              elif tested > notif:
                   st.warning("**YOU CAN'T TEST MORE THAN THOSE NOTIFIED**")
              elif tested == 0:
                   pass
              else:
                   st.write(f'**OF THE {tested} tested, HOW MANY WERE:**')
                   col1,col2, col3 = st.columns(3) 
                   neg = col1.number_input('**NEGATIVE**', value=None, step=1)
                   pos = col2.number_input('**NEWLY POSTIVE**', value=None, step=1)
                   if pos:
                        linked = col3.number_input('**HOW MANY WERE LINKED**', value=None, step=1)
                        if linked > pos:
                             st.warning("**YOU CAN'T LINK MORE THAN THOSE TESTED**")
                             st.stop()
                    
                   if pos or pos ==0:
                        pass
                   else:
                        st.stop()
                   if neg or neg ==0:
                        pass
                   else:
                        st.warning('Number negative is required or put a 0 (zero)**')
                        st.stop()
                   if (neg + pos) > tested:
                        st.warning('**Number positive and negative is greater than number tested**')
                        st.stop()
                   if pos:
                        st.write(f'**OF THE {pos}, how many have:**')
                        col1,col2, col3 = st.columns(3) 
                        recency = col1.number_input('**RECENCY TEST**', value=None, step=1)
                        alread = col2.number_input('**RECENT RESULT**', value=None, step=1)
                        linked = col3.number_input('**LONGTERM RESULTS**', value=None, step=1)
    
elif check == 'DOWNLOAD FORM':
    col1, col2,col3 = st.columns(3)
    artu = col1.number_input('**SEARCH ART No.**', value=None, step=1)
    if artu:
         dfdemo = dfdemo[dfdemo['ART NO'] == artu].copy()
         dftest= dftest[dftest['ART NO'] == artu].copy()
         dfiss = dfiss[dfiss['ART NO'] == artu].copy()
    else:
         dfdemo = dfdemo.copy()
         dftest = dftest.copy()
         dfisss = dfiss.copy()
         Arts = dfdemo['ART NO'].unique()

    num = dfdemo.shape[0]
    if num ==0:
         st.info('**No forms available for this facility or ART NO selected**')
         st.stop()
    elif artu or num ==1:
              st.info('**1 form is available for this facility or ART NO selected**')
              def create_docx():
                   dfdemy= dfdemo.copy()
                   dftesty = dftest.copy()
                   dfisy = dfiss.copy()
                   
                   arty = dfdemy.iloc[0,3]
                   a = arty
                   b = dfdemy.iloc[0,12]
                   c = dfdemy.iloc[0,6]
                   d = dfdemy.iloc[0,7]
                   e = dfdemy.iloc[0,10]
                   f = dfdemy.iloc[0,9]
                   g = dfdemy.iloc[0,11]
                   dt = dfisy.iloc[0,17]
                   sp = ''
                   pm = dfdemy.iloc[0,8]
                   dob = dfdemy.iloc[0,5]
                   dr = dfdemy.iloc[0,4]
               
                   a1 = dfisy.iloc[0,2]
                   a2 = dfisy.iloc[0,3]
                   a3 = dfisy.iloc[0,4]
                   a4 = dfisy.iloc[0,5]
                   a5 = dfisy.iloc[0,6]
                   a6 = dfisy.iloc[0,7]
                   bar = f'{a1}, {a2}, {a3}, {a4}, {a5}, {a6}'
                   b1 = dfdemy.iloc[0,13]
                   b2 = dfdemy.iloc[0,14]
                   act = dfisy.iloc[0,8]
                   prev = dfisy.iloc[0,9]
                   econ = dfisy.iloc[0,12]
               
                   cd = dftesty.iloc[0,2]
                   tb = dftesty.iloc[0,14]
                   vl = dfisy.iloc[0,13]
               
                   apn = dftesty.iloc[0,7]
                   ht = dfdemy.iloc[0,15]
                   dm = dfdemy.iloc[0,16]
                   mh = dfdemy.iloc[0,18]
                   As = dfdemy.iloc[0,17]
               
                   hw = dfisy.iloc[0,15]
                   chw = dfisy.iloc[0,16]
                   
                   document = Document()
                   document.add_heading ('  IDI MWP CLIENT ENCOUNTER FORM', 0)
                   P = document.add_paragraph(f'   {sp} {sp} This visit, conducted on {dt} was a {b} IAC session for client {a}, a {c} year old {d} from {e} village, {f} district, located at {g}')
                   table1 = document.add_table(rows=1,cols=3, style='Table Grid')
                   table1.cell(0,0).text = f'RESULTS: {dr} copies/mL'
                   table1.cell(0,1).text = f'BLED ON: {dob}'
                   table1.cell(0,2).text = f'PMTCT: {pm}'
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('ADHRENCE BARRIERS, ACTIONS AGREED UP ON AND SERVICES GIVEN').bold=True
                   table1 = document.add_table(rows=5,cols=2, style='Table Grid')
                   table1.cell(0,0).text = 'ADHERENCE SCORE:'
                   table1.cell(0,1).text = f'{b1} % ({b2})'
                   table1.cell(1,0).text = 'BARRIERS IDENTIFIED:'
                   table1.cell(1,1).text = bar
                   table1.cell(2,0).text = 'ACTIONS AGREED UPON:'
                   table1.cell(2,1).text = str(act)
                   table1.cell(3,0).text = 'PREVENTION SERVICES GIVEN:'
                   table1.cell(3,1).text = str(prev)
                   table1.cell(4,0).text = 'ECONOMIC ADVICE:'
                   table1.cell(4,1).text = str(econ)
                   for row in table1.rows:
                       row.cells[0].width = Inches(1.5)
                       row.cells[1].width = Inches(5)
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('TESTS DONE').bold=True
                   table2 = document.add_table(rows=3,cols=2, style='Table Grid')
                   table2.cell(0,0).text = 'VL REBLEED:'
                   table2.cell(0,1).text = f'{vl}'
                   table2.cell(1,0).text = 'CD4 TESTING:'
                   table2.cell(1,1).text = f'{cd}'
                   table2.cell(2,0).text = 'TB SCREENING:'
                   table2.cell(2,1).text = f'{tb}'
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('APN, NCD CODES').bold=True
                   table2 = document.add_table(rows=1,cols=5, style='Table Grid')
                   table2.cell(0,0).text = f'Partners: {apn:,.0f}'
                   table2.cell(0,1).text = f'HTN: {ht}'
                   table2.cell(0,2).text = f'DM: {dm}'
                   table2.cell(0,3).text = f'MH: {mh}'
                   table2.cell(0,4).text = f'AS: {As}'
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('Name of H/worker:').bold =True
                   p.add_run(f'{hw}').bold =True
                   p = document.add_paragraph('')
                   p.add_run('Name of CHW:').bold =True
                   p.add_run(f'{chw}').bold =True
          
                   doc_io = BytesIO()
                   document.save(doc_io)
                   doc_io.seek(0)  # Move pointer to the start of the file
                   return doc_io
              
              doc_file = create_docx()
     
             # Provide a download button
              st.download_button(
                 label=f"DOWNLOAD FORM FOR ART NO: {artu:,.0f}",
                 data=doc_file,
                 file_name=f"FORM FOR ART NO: {artu:,.0f}.docx",
                 mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
    else:
         st.info(f'**{num} forms are available for this facility or ART NO selected**')
         for arty in Arts:
              def create_docx():
                   dfdemy = dfdemo[dfdemo['ART NO'] == arty].copy()
                   dfisy = dfiss[dfiss['ART NO'] == arty].copy()
                   dftsty = dftest[dftest['ART NO'] == arty].copy()            
                   a = arty
                   b = dfdemy.iloc[0,12]
                   c = dfdemy.iloc[0,6]
                   d = dfdemy.iloc[0,7]
                   e = dfdemy.iloc[0,10]
                   f = dfdemy.iloc[0,9]
                   g = dfdemy.iloc[0,11]
                   dt = dfisy.iloc[0,17]
                   sp = ''
                   pm = dfdemy.iloc[0,8]
                   dob = dfdemy.iloc[0,5]
                   dr = dfdemy.iloc[0,4]
               
                   a1 = dfisy.iloc[0,2]
                   a2 = dfisy.iloc[0,3]
                   a3 = dfisy.iloc[0,4]
                   a4 = dfisy.iloc[0,5]
                   a5 = dfisy.iloc[0,6]
                   a6 = dfisy.iloc[0,7]
                   bar = f'{a1}, {a2}, {a3}, {a4}, {a5}, {a6}'
                   b1 = dfdemy.iloc[0,13]
                   b2 = dfdemy.iloc[0,14]
                   act = dfisy.iloc[0,8]
                   prev = dfisy.iloc[0,9]
                   econ = dfisy.iloc[0,12]
               
                   cd = dftsty.iloc[0,2]
                   tb = dftsty.iloc[0,14]
                   vl = dfisy.iloc[0,13]
               
                   apn = dftsty.iloc[0,7]
                   ht = dfdemy.iloc[0,15]
                   dm = dfdemy.iloc[0,16]
                   mh = dfdemy.iloc[0,18]
                   As = dfdemy.iloc[0,17]
               
                   hw = dfisy.iloc[0,15]
                   chw = dfisy.iloc[0,16]
                   
                   document = Document()
                   document.add_heading ('  IDI MWP CLIENT ENCOUNTER FORM', 0)
                   P = document.add_paragraph(f'   {sp} {sp} This visit, conducted on {dt} was a {b} IAC session for client {a}, a {c} year old {d} from {e} village, {f} district, located at {g}')
                   table1 = document.add_table(rows=1,cols=3, style='Table Grid')
                   table1.cell(0,0).text = f'RESULTS: {dr} copies/mL'
                   table1.cell(0,1).text = f'BLED ON: {dob}'
                   table1.cell(0,2).text = f'PMTCT: {pm}'
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('ADHRENCE BARRIERS, ACTIONS AGREED UP ON AND SERVICES GIVEN').bold=True
                   table1 = document.add_table(rows=5,cols=2, style='Table Grid')
                   table1.cell(0,0).text = 'ADHERENCE SCORE:'
                   table1.cell(0,1).text = f'{b1} % ({b2})'
                   table1.cell(1,0).text = 'BARRIERS IDENTIFIED:'
                   table1.cell(1,1).text = bar
                   table1.cell(2,0).text = 'ACTIONS AGREED UPON:'
                   table1.cell(2,1).text = str(act)
                   table1.cell(3,0).text = 'PREVENTION SERVICES GIVEN:'
                   table1.cell(3,1).text = str(prev)
                   table1.cell(4,0).text = 'ECONOMIC ADVICE:'
                   table1.cell(4,1).text = str(econ)
                   for row in table1.rows:
                       row.cells[0].width = Inches(1.5)
                       row.cells[1].width = Inches(5)
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('TESTS DONE').bold=True
                   table2 = document.add_table(rows=3,cols=2, style='Table Grid')
                   table2.cell(0,0).text = 'VL REBLEED:'
                   table2.cell(0,1).text = f'{vl}'
                   table2.cell(1,0).text = 'CD4 TESTING:'
                   table2.cell(1,1).text = f'{cd}'
                   table2.cell(2,0).text = 'TB SCREENING:'
                   table2.cell(2,1).text = f'{tb}'
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('APN, NCD CODES').bold=True
                   table2 = document.add_table(rows=1,cols=5, style='Table Grid')
                   table2.cell(0,0).text = f'Partners: {apn:,.0f}'
                   table2.cell(0,1).text = f'HTN: {ht}'
                   table2.cell(0,2).text = f'DM: {dm}'
                   table2.cell(0,3).text = f'MH: {mh}'
                   table2.cell(0,4).text = f'AS: {As}'
                   p = document.add_paragraph('')
                   p = document.add_paragraph('')
                   p.add_run('Name of H/worker:').bold =True
                   p.add_run(f'{hw}').bold =True
                   p = document.add_paragraph('')
                   p.add_run('Name of CHW:').bold =True
                   p.add_run(f'{chw}').bold =True
          
                   doc_io = BytesIO()
                   document.save(doc_io)
                   doc_io.seek(0)  # Move pointer to the start of the file
                   return doc_io
              
              doc_file = create_docx()
     
             # Provide a download button
              st.download_button(
                 label=f"DOWNLOAD FORM FOR ART NO: {arty:,.0f}",
                 data=doc_file,
                 file_name=f"FORM FOR ART NO: {arty:,.0f}.docx",
                 mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 key = arty
                    )
    
    
elif check == 'MAKE UPDATES':
    pass

st.stop()
