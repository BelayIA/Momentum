#import pandas as pd
from datetime import datetime
from datetime import timedelta
from Get_quotes_lib import *
from Variables import *

Display_mode = True

LastDate = datetime.today() - timedelta(1)
DateTill = LastDate.strftime('%Y-%m-%d') #str(LastDate.year) + "-" + str(LastDate.month) + '-' + str(LastDate.day)
LastDate = datetime.today() - timedelta(1000)  # количество дней в б/д
DateFrom = LastDate.strftime('%Y-%m-%d') #str(LastDate.year) + "-" + str(LastDate.month) + '-' + str(LastDate.day)
TimeNow = str(datetime.today().hour) + "-" + str(datetime.today().minute) + " UTS"

# список компаний в листинге MOEX
df_company = pd.read_json(Path_for_data+Path_to_df+"df_company.json")
df_tmp = df_company[pd.notna(df_company['TRADE_CODE'])]
df_company = df_tmp[~df_tmp['TRADE_CODE'].str.contains("-RM")]

Clear_and_create_dir(Display_mode)
Get_quotes(df_company, DateFrom, DateTill, Display_mode)

