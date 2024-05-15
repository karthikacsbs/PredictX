import streamlit as st,pandas as pd,numpy as np,yfinance as yf
import plotly.express as px

st.title('STOCK DASHBOARD')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker,start=start_date,end=end_date)
fig = px.line(data,x = data.index,y = data['Adj Close'],title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news,openAi = st.tabs(["Pricing Data", "Fundamental Data","Top 10 News","OpenAI CHATGPT"])

with pricing_data:
    st.header('Price Movements')
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1)
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100
    st.write('Annual Return is',annual_return,'%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is',stdev*100,'%')
    st.write('Risk Adj. Return is',annual_return/(stdev*100))

from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    key = ' J5R7H092BWDGAWZY'
    fd = FundamentalData(key,output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement =fd.get_income_statement_annual(ticker) [0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual (ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)
    
from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews (ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
      st.subheader (f'News {1+1}')
      st.write(df_news['published'][i])
      st.write(df_news['title'][i])
      st.write(df_news['summary'][i])
      title_sentiment = df_news['sentiment_title'][i]
      st.write(f'Title Sentiment {title_sentiment}')
      news_sentiment = df_news['sentiment_summary'][i]
      st.write(f'News Sentiment {news_sentiment}')
      
from pychatgpt import ChatGPT
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..0s9ixGlL_FMHNHz7.EsEYw99L_UHS0kctMlEl3I1sTH3C3n9Boq3RG5VK9sMzP1QvpYCyW32nW-jyhCBpi21X2n9vetZLMEPALzOVfa2XfVhf8EEbosv6F1J4Y_MH4689QEaXG3YB_UmOWpZ-m4yHvIBX57jYG4TWJEeop_7vfHUQBEP70EqRduJJ9dLWghvdcc3hea_3aym5O7-C_OrpuCDAYUL-Z2m0fIBqlXCgK8qhPt_ORAH62D4maR0YiTb_-fmiyqeBtmFKsjkg61nhEJ8XxgOpsUzqnuYrAVqMik9TYw_b8d6JJ1q8_Hwso05j1BoydSJGxVgPS6s_Ge57Jkm171OFNBD-svXrW4FXhhg6Tfa4gsH70FT-k-P_qJg28_N3XLrSLqztQ7jsO_cayS3EmGIw-sc7CooxllMgPzXwcCfj_b9naypbw6g0qej-yWW95A4EwzFfpQ-xkOsg6zLA0Y3znRQdstKkHKk0k5aHoSJJj1CJPzgNwcJwJArdHJqb13Cjel-08oKbsti0xVWJCNFj1g-VFiyddgKlb9Uyi-CRJTN-0p721ywbxNOf9-1yWqx765hwoTuzK77himd_i0aTVYVfSjqjk1r9kbOUHfhgIV6oCjDTiQHsxGeXBUeHMzaXBqN-cPqzVun0WfepiVdb7rD3UScDVHePd1XZTNvb0F4D3sasKPJsjPXsoAkBBfEoStMDgrRw_pKklbwsuGvblwas95h5mh_UOJG-Jz6H7DYdDlJ1oqFdqegBoJ0UpH97gqjPbpmSNM92gEs46bgwUMkiMqQAVm9UA-bUTHVyXQ4TOGcYMjF_S5NOaj_mBF4BH8RVy7lj_1h4ZgrNn46k2-bRD9Lq-wiiXg7Bw12wqopZZh1DlhD1qvXoxI9KBKghhb9lEWbuZdU4y2rOaP1VtDs3xw4BDFXzHPkpxCALSN71tvK655UHtYCiK1GHaLHpQdcRzjmfjvv9QwshpIEsM7nrYfLBPw7n7bjm-SmsphIDf_5u6ntEiRMsmKkBxY-jFH-FPOjPHG-1rjkMBpjik6aKBIjevfdY-4CcWM_SLOPLY6qP0FCwi9nFM2ndQIG0jRgzINdpDWHlugUjz03GfCxmROQAlpIjsV0DIvG9lPBgv2ZelGO4cpmt8Pp-7U94D-A-rFnvA557kM1_zAR5v8RftJrZK-N-XhLavHij3ySm2JjF3ZGrI2b4YhOaMDFy7j_BlMsqJZPBqkKuvN4PDDN432t9EYSQgWKm2sSoaT5ikcNOOoMvLcrtOwkMrzRtYSUkZ-PuJcQ6QQz0x0qa5o7f-OZIhlpligcbWvG4ZFf9dlr_cDJ09addBFdlaSITedDWVBavD1rHYpNweSH0ipcXRNF0mBJvQDVY3WFwpVelVwAlO_CQ3WLzNA4FGrPEfDBZcVphI79QkGthsx_homRMnqlsaYoETTQmxgTJR07MRHJCyqkcC3V_cvC-9Gx7lkz6Fu-uY4OCU_wHQQpdyZ_FislXt6Bzl_HolT3M6IOP2LCjcuFdW8XFX6-eIn7XcdtZ6yie536oDfgNsmsH-XEVMpC-SlKfXrLWdhEbeIPN0WisGrLfCOF8kYkboCUUmF9ZZjveEcUvuoSQbxA2N5sI7N8rCzzbDeoZsQFKNpFWdhYhcSBM-2Ku6SiSQ1GlUhR0YqHLhel9E5HdwnQPN06XazpJmslrp09VUMJkSjuhrcAH1PANGf6Y6aMFaB6nCZbI-_e-FAomRHv16kAlaepJwT-OAMtDQy1A9V4TsukathWA21i-yUi_wkLPxBXf62q9D3n6WhCcYNVgnlqO6kwIHfQYxYeFDVyO_rlwAPoWqatvM1gOtp9ZGHllGruJK9Vj5Dn974crXBjT3oXSE1f-k7o4fAJ1mmCcZq_GGbaRkFuJG-mjtSTmD_FxmyfgQVDrogMOckdBmC9HLIure6ARLX3HiNQPNIq6ea8QwYHQBWWr7BHLdWQQqvi-qQCpHhi70nZ5XRW0ua4C7ThILqryduw2BfcYpV76X31eisJK5uEP7x_zo_rqQ7IZhi16y5NPgjwXUwCuxpA8e9G0740CA6oe_g-yk8oMjdmdVP-o6PXNhimoW2COT9835NccpYJSF7CdZJKBSdb2hLfL4LlTZtHFHT3WkBcwW3vhDKym08xYDSFhqpIoPglPQ-v4Ciy9NILspRPcdFy9Un41EQedaVZorQNn_0eiQHUcqWCRam4j68VFqjinFx0LrwplYyMwG5pcsPvA1XuG-_5uzSCb5Qjx0RqGttykwbVGgwnWVAuLZpIJPeJBJWF7cgXxV7lIyVj8V3U5YU2b_V8MkkOH4izuK0TRR46EULJ-VU6qNnV164MVUnXVUNKFs_hlYFvnXTAitNjmkABvSGyuJ9toNGtzt9XNEciF7WDv-RKh58Qm5eqkzDJSsZb0cgwma9pT_dl4dxZ_5DQU1kQJbdsLERLqmcA8yx6aXeUO0yxYCbs7W3iFAraKHeXzUifA07CehgK8AUOaKnqeBWuLj0hS3xHzXVjhocsFw9M19LA0jERTZW1k8insiM1BIDcgzRdFpG7zzL_CvbRLBbsDdR3NZ7YonO6RBkWCfOqI_K2Bl4tXV9MAUedELwE-QtQP59EPV3chEyu1FukwVerxzmaHP0DzHYLdpX0GEImdNATSqofF8enYqFlTauVnDXwG_w36kpPGHOz84gCJ5Gk7-oen0a5nptpqVtR5tXUvsBHDSclaDq3t8qEkgwFYS9OSH3Jm35EdZ-d_cesAbaii-nPr6UHI7l3iYrND39QifztxUkBArybBMRzN2xuuquBur1NHMEjRVYqUyQK2tmgDzukMEI8.SuiN0nDusWJ0BKrtzJFkPg'
api2 = ChatGPT(session_token)
buy = api2.send_message(f'3 Reasons to buy {ticker} stock')
sell =  api2.send_message(f'3 Reasons to sell {ticker} stock')
swot =  api2.send_message(f'SwOT analysis of {ticker} stock')
with openAi:
      buy_reason, sell_reason, swot_analysis = st.tabs(['3 Reasons to buy', '3 Reasons to sell', 'sant analysis'])

      with buy_reason:
        st.subheader(f'3 reasons on why to Buy {ticker}Stock')
        st.write(buy['message'])
      with sell_reason:
        st.subheader(f'3 reasons on why to SELL {ticker} Stock')
        st.write(sell['message'])
      with swot_analysis:
        st.subheader(f'SWOT Analysis of {ticker} Stock')
        st.write(swot['message'])