# import pandas as pd
# import numpy as np
# import math
# import matplotlib.pyplot as plt
# from Telegram_lib import *
# from Variables import *

from datetime import datetime
from datetime import timedelta
from Points_lib import *

Display_mode = True
Send_mmode = True

LastDate = datetime.today() - timedelta(1)
DateTill = LastDate.strftime('%Y-%m-%d') #str(LastDate.year) + "-" + str(LastDate.month) + '-' + str(LastDate.day)
LastDate = datetime.today() - timedelta(700)  # количество дней в б/д
DateFrom = LastDate.strftime('%Y-%m-%d') #str(LastDate.year) + "-" + str(LastDate.month) + '-' + str(LastDate.day)
TimeNow = str(datetime.today().hour) + "-" + str(datetime.today().minute) + " UTS"

# список компаний в листинге MOEX
df_company = pd.read_json(Path_for_data+Path_to_df+"df_company.json")
df_tmp = df_company[pd.notna(df_company['TRADE_CODE'])]
df_company = df_tmp[~df_tmp['TRADE_CODE'].str.contains("-RM")]

Calculate_points_of_entry(df_company, DateFrom, DateTill, Display_mode, Send_mmode)

