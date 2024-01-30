import pandas as pd
import os
import shutil
from Variables import *

# Создаём новый или очищаем старый каталог для хранения котировок
def Clear_and_create_dir(Display_mode):
    try:
        shutil.rmtree(Path_for_data+Path_to_quotes)
        if Display_mode:
            print(f"Directory {Path_for_data+Path_to_quotes} is deleted!")
    except Exception as e:
        print(f"get_quotes.py Error: Directory {Path_for_data+Path_to_quotes} is not deleted \n{e}")
        #Email_sent.Calculate(f"get_quotes.py Error: Directory Quotes_{country.lower()} is not deleted", Sent_email_mode=True)
    # Создаём каталог QUOTES и для заполнения новыми данными
    try:
        os.mkdir(Path_for_data+Path_to_quotes)
        if Display_mode:
            print(f"Directory {Path_for_data+Path_to_quotes} is created!")
    except Exception as e:
        print(f"get_quotes.py Error: Directory {Path_for_data+Path_to_quotes}is not created: \n{e}")
        #Email_sent.Calculate(f"get_quotes.py Error: Directory Quotes_{country.lower()} is not created", Sent_email_mode=True)
    return

# качаем котировки
def Get_quotes(df_company, DateFrom, DateTill, Display_mode):
  for company in df_company.itertuples():
    # качаем график по текущей компании
    try:
      ticker_df = pd.read_csv(
                  "https://iss.moex.com/iss/engines/stock/markets/shares/boards/"
                  + Board + "/securities/" + company.TRADE_CODE + "/candles.csv?from=" + DateFrom +
                  "&till=" + DateTill + "&interval=24", sep=";", skiprows=2)

      # индексируем по дате
      ticker_df["Date"] = pd.to_datetime(ticker_df["begin"])
      ticker_df.set_index("Date", inplace=True)
      ticker_df.to_json(Path_for_data+Path_to_quotes+str(company.TRADE_CODE)+".json")
      if Display_mode:
        print(f"File {company.TRADE_CODE}.json is created")
    except Exception as e:
      if Display_mode:
        print(f"Error {e} File {company.TRADE_CODE}.json")

