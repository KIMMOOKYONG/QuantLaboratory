from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf
import warnings
import datetime
import pickle
import joblib
import os
import json
import time
import requests

# set the style and ignore warnings
plt.style.use("seaborn-colorblind")
plt.rcParams["figure.figsize"] = [15, 8]
plt.rcParams.update({"font.size": 12}) 

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore")

class DownloadData():
    def __init__(self):
        pass

    def yfinance_data_download(self, start_date=None, end_date=None, ticker=None):
        """
        yfinance에서 주가 데이터 파일 다운로드하는 함수
        @start_date: 시작일, datetime
        @end_date: 종료일, datetime
        @ticker: 종목코드, string
        @return: 주가데이터, dataframe
        """

        if start_date is None:
            print("시작일 정보가 설정되지 않았습니다.")

        if end_date is None:
            print("종료일 정보가 설정되지 않았습니다.")

        if ticker is None:
            print("종목코드 정보가 설정되지 않았습니다.")

        data = yf.download(ticker, progress=True, actions=True, start=start_date, end=end_date)
        data = pd.DataFrame(data)

        return data

    def naver_data_download(self, start_date, end_date, ticker=None):
        """
        네이버에서 주가 데이터 파일 다운로드하는 함수
        @start_date: 시작일, datetime
        @end_date: 종료일, datetime
        @ticker: 종목코드, string
        @return: 주가데이터, dataframe
        """
        if start_date is None:
            print("시작일 정보가 설정되지 않았습니다.")

        if end_date is None:
            print("종료일 정보가 설정되지 않았습니다.")

        if ticker is None:
            print("종목코드 정보가 설정되지 않았습니다.")

        # 날짜 데이터를 문자열 형식으로 데이터로 변환(2020년1월1일 - > 20200101)
        start_date = start_date.strftime("%Y%m%d")
        end_date = end_date.strftime("%Y%m%d")

        time.sleep(0.2)
        url = f"https://fchart.stock.naver.com/siseJson.nhn?symbol={ticker}&requestType=1&startTime={start_date}&endTime={end_date}&timeframe=day"
        result = requests.post(url)

        data1 = result.text.replace("'",  '"').strip()
        data1 = json.loads(data1)

        data2 = pd.DataFrame(data1[1:], columns=data1[0])
        data2 = data2.reset_index()
        data2["날짜"] = pd.to_datetime(data2["날짜"])

        data = data2[["날짜","시가", "고가", "저가", "종가", "거래량"]].copy()
        data.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        data = data.set_index("Date")
        data = data.dropna()
        data.loc[:,["Open", "High", "Low", "Close", "Volume"]] = data.loc[:,["Open", "High", "Low", "Close", "Volume"]].astype(int)
        data = data.loc[:,["Open", "High", "Low", "Close", "Volume"]]

        return data

    def save(self, data=None, filename=None):
        """
        수집 데이터를 저장하는 함수
        @ticker: 종목코드
        @filename: 파일명
        """

        if data is None:
            print("저장할 데이터프레임이 설정되지 않았습니다.")

        if  filename is None:
            print("파일명이 설정되지 않았습니다.")

        data.to_csv(filename)
        print(f"{filename} 파일이 저장되었습니다.")
