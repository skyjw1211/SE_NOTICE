import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import pandas as pd  
from io import BytesIO



def get_gsheet():
  scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
  # Create a connection object.
  credentials = service_account.Credentials.from_service_account_info(
      st.secrets["gcp_service_account"],
      scopes=[
          "https://www.googleapis.com/auth/spreadsheets",
      ],
  )
  client = gspread.authorize(credentials)

  # 작업자별 누적 작업량이 기록된 시트 이름
  sheet_name = '[관리] CLOVA X_RLHF 데이터 구축 프로젝트'

  # 작업자별 누적 작업량 시트 불러오기
  sheet = client.open(sheet_name).worksheet('smart editor tracking DB')

  # 데이터 읽어오기
  data = sheet.get_all_records()

  #미배분 파일 가져오기 (파일명 - key)
  df = pd.DataFrame(data)

  return sheet, df

sheet, df = get_gsheet()


# (1)'작업 유형'을 기준으로 묶은 뒤, 전체 개수
# '작업자' 값이 ''인 개수, 작업 종료일?

for work_type in ['글나누기', '바꿔쓰기', '줄여쓰기', '요약하기']:
  st.write(work_type, '남은 작업량:', len(df.loc[(df['작업 유형'] == work_type) & (df['작업자'] == '')]))