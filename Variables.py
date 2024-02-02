# Страна
country = "ru"

# Пути к данным
Path_for_data = "./Data/"
Path_to_df = "Data_df/"
Path_to_quotes = "Data_Quotes/"

# Telegram

TOKEN = "6861814836:AAEbcVRVpquCi_Rmm6m-JZYN5kGH_uFb-oM"
channel_id = "@MoexPoints"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
chat_id = "214846543"

# Date
# LastDate = datetime.today() - timedelta(1)
# DateTill = LastDate.strftime('%Y-%m-%d') #str(LastDate.year) + "-" + str(LastDate.month) + '-' + str(LastDate.day)
# LastDate = datetime.today() - timedelta(700)  # количество дней в б/д
# DateFrom = LastDate.strftime('%Y-%m-%d') #str(LastDate.year) + "-" + str(LastDate.month) + '-' + str(LastDate.day)
# TimeNow = str(datetime.today().hour) + "-" + str(datetime.today().minute) + " UTS"

# Vars
Cross_momentum = {"UP_momentum_UP_AO": ["LONG Возможен рост на восходящем тренде",'Рост'],
                      "UP_momentum_DOWN_AO": ["LONG Возможен рост после снижения",'Рост'],
                      "DOWN_momentum_UP_AO": ["SHORT Возможно снижение после роста",'Снижение'],
                      "DOWN_momentum_DOWN_AO": ["SHORT Возможно снижение на нисходящем тренде",'Снижение']}

Ratio = {"Первый уровень": 60, "Второй уровень": 65, "Третий уровень": 75}
Board = "TQBR"
arr_periods = [-10, -25]
cut_labels = ['меньше -10%', 'между - 10% и -5%', 'между - 5% и -0%', 'между 0% и +5%', 'между +5% и +10%', 'больше +10%']
cut_bins = [-100, -10, -5, 0, 5, 10, 100]
cut_labels_2 = ['Снижение', 'Рост']
cut_bins_2 = [-100, 0, 100]

mmnt_spred = 0.0025
