import pandas as pd
import numpy as np
import Ma_lib as ta
# from math import fabs
from Variables import *
from Telegram_lib import *

# Перебор всех компаний из листинга
def Calculate_points_of_entry(df_company, DateFrom, DateTill, Display_mode, Send_mmode):
  for company in df_company.itertuples():
    # качаем график по текущей компании
    try:
      try:
        ticker_df = pd.read_json(Path_for_data+Path_to_quotes+str(company.TRADE_CODE)+".json")
      except:
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

      ticker_df["Place_of_Cross"]  = np.NaN
      ticker_df["Change_of_Price"] = np.NaN
      # считаем индикаторы

      ticker_df["TypicalPrice"] = (ticker_df["close"] + ticker_df["high"] + ticker_df["low"]) / 3
      ticker_df["AO"] = np.array(ta.EMA(ticker_df["TypicalPrice"], 5)) - np.array(ta.EMA(ticker_df["TypicalPrice"], 34))
      ticker_df["Momentum"] = 100*ticker_df["close"]/ticker_df["close"].shift(periods=5)

      # если было пересечение Momentum
      var_cross = ""
      #print(""*150, end="\r")
      #print(f'Company {company.TRADE_CODE}', end=" ") #{ticker_df["Momentum"][-1:].values[0]} {ticker_df["Momentum"][-2:-1].values[0]} {ticker_df["AO"][-1:].values[0]}', end=" ")
      #time.sleep(0.5)

      flag_spred = mmnt_spred < abs(1 - ticker_df["Momentum"][-2:-1].values[0] / ticker_df["Momentum"][-1:].values[0])

      if (ticker_df["Momentum"][-1:].values[0] > 100) & \
              (ticker_df["Momentum"][-2:-1].values[0] < 100) & \
              (ticker_df["AO"][-1:].values[0] > 0) & flag_spred:
        # spred= abs(1 - ticker_df["Momentum"][-2:-1].values[0] / ticker_df["Momentum"][-1:].values[0])
        # print(f"spred {spred}")
        var_cross = "UP_momentum_UP_AO"
        ticker_df.loc[(ticker_df["Momentum"] > 100) & (ticker_df["Momentum"].shift(periods=1) < 100) \
        & (ticker_df["AO"] > 0) & \
        (mmnt_spred < abs(1 - ticker_df["Momentum"].shift(periods=1)/ ticker_df["Momentum"])), \
        "Place_of_Cross"] = True

      elif (ticker_df["Momentum"][-1:].values[0] > 100) & \
              (ticker_df["Momentum"][-2:-1].values[0] < 100) & \
              (ticker_df["AO"][-1:].values[0] < 0) & flag_spred:
        # spred = abs(1 - ticker_df["Momentum"][-2:-1].values[0] / ticker_df["Momentum"][-1:].values[0])
        # print(f"spred {spred}")
        var_cross = "UP_momentum_DOWN_AO"
        ticker_df.loc[(ticker_df["Momentum"] > 100) & (ticker_df["Momentum"].shift(periods=1) < 100)
        & (ticker_df["AO"] < 0) & \
        (mmnt_spred < abs(1 - ticker_df["Momentum"].shift(periods=1) / ticker_df["Momentum"])), \
        "Place_of_Cross"] = True

      elif (ticker_df["Momentum"][-1:].values[0] < 100) & \
              (ticker_df["Momentum"][-2:-1].values[0] > 100) & \
              (ticker_df["AO"][-1:].values[0] > 0) & flag_spred:
        # spred = abs(1 - ticker_df["Momentum"][-2:-1].values[0] / ticker_df["Momentum"][-1:].values[0])
        # print(f"spred {spred}")
        var_cross = "DOWN_momentum_UP_AO"
        ticker_df.loc[(ticker_df["Momentum"] < 100) & (ticker_df["Momentum"].shift(periods=1) > 100)
        & (ticker_df["AO"] > 0) & \
        (mmnt_spred < abs(1 - ticker_df["Momentum"].shift(periods=1) / ticker_df["Momentum"])), \
        "Place_of_Cross"] = True

      elif (ticker_df["Momentum"][-1:].values[0] < 100) & \
              (ticker_df["Momentum"][-2:-1].values[0] > 100) & \
              (ticker_df["AO"][-1:].values[0] < 0) & flag_spred:
        # spred = abs(1 - ticker_df["Momentum"][-2:-1].values[0] / ticker_df["Momentum"][-1:].values[0])
        # print(f"spred {spred}")
        var_cross = "DOWN_momentum_DOWN_AO"
        ticker_df.loc[(ticker_df["Momentum"] < 100) & (ticker_df["Momentum"].shift(periods=1) > 100)
        & (ticker_df["AO"] < 0) & \
        (mmnt_spred < abs(1 - ticker_df["Momentum"].shift(periods=1) / ticker_df["Momentum"])), \
        "Place_of_Cross"] = True

      if var_cross:
        #print(f"var_cross: {var_cross}", end='\n')
        for i in arr_periods:
          # Считаем историю процента изменений цены от даты пересечения Momentum
          ticker_df["close_mean"] = ticker_df["close"].rolling(-1*i).mean()
          ticker_df.loc[ticker_df["Place_of_Cross"] == True, "Change_of_Price"] = 100*(ticker_df["close_mean"].shift(periods=i)-ticker_df["close"])/ticker_df["close"]
          # Делаем бинарное разбиение процента изменений цен
          ticker_df['Cut2'] = pd.cut(ticker_df['Change_of_Price'],
                            bins=cut_bins_2,
                            labels=cut_labels_2)
          # Если соотношение хорошее, то выдаем рекомендацию
          var_bin = ticker_df.Cut2.value_counts(normalize=True)*100
          #print(f"{var_bin}")
          #time.sleep(0.5)
          #print(f"var_bin[Cross_momentum[var_cross][1]] {var_bin[Cross_momentum[var_cross][1]]}", end='\n')
          if var_bin[Cross_momentum[var_cross][1]] > Ratio[company.LIST_SECTION]:
            ticker_df['Cut_many'] = pd.cut(ticker_df['Change_of_Price'],
                            bins=cut_bins,
                            labels=cut_labels)
            #print(end='\n')
            #print(f'Company {company.TRADE_CODE} {ticker_df["Momentum"][-1:].values[0]} {ticker_df["Momentum"][-2:-1].values[0]} {ticker_df["AO"][-1:].values[0]}', end="\n")

            message = f"""
{company.TRADE_CODE} {company.EMITENT_FULL_NAME}
{company.LIST_SECTION}
Данные для анализа взяты за {DateTill}
Прогноз на {-1*i} дней
{Cross_momentum[var_cross][0]}

Бинарный прогноз вероятностей изменения цены
{var_bin}

Разбиение прогноза вероятностей изменения цены
{ticker_df.Cut_many.value_counts(normalize=True)*100
            }"""

            if Display_mode:
              print(message)

            if Send_mmode:
              # Слать данные в канал
              Send_telegram(message, TOKEN, channel_id)
              # Слать данные в бот
              # url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
              # print(requests.get(url).json()) # Эта строка отсылает сообщение в бот

    except Exception as e:
      if Display_mode:
        print(f"Error {e}", end='\n')
  return