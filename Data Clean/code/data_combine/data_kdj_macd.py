import pandas as pd

# Load the datasets
data_min_path = r'C:\Users\samuel\dsmp-2024-group18\Data Clean\data\data_combine\data_total_min/data_min_total.csv'
data_hour_path = r'C:\Users\samuel\dsmp-2024-group18\Data Clean\data\data_combine\data_total_hour/data_hour_total.csv'

data_min = pd.read_csv(data_min_path)
data_hour = pd.read_csv(data_hour_path)

# Convert 'DateTime_Minute' to datetime and set it as index
data_min['DateTime_Minute'] = pd.to_datetime(data_min['DateTime_Minute'])
data_hourly = data_min.set_index('DateTime_Minute')

# Resample data to hourly frequency, taking the mean for MACD and KDJ calculations later
# Note: For visualization, we'll use the last trade price of each hour
data_hourly_mean = data_hourly.resample('H').mean()

# Also, get the last trade price for each hour for visualization purposes
data_hourly_last_price = data_hourly['Trade_Price_Mean'].resample('H').last()

# 为了计算MACD，我们需要确定适用的时间周期，通常是12日EMA和26日EMA
# 由于我们的数据是按小时计的，我们将按照相似的逻辑进行调整

# 计算EMA的快速和慢速线
ema_short = data_hour['Trade_Price_Mean'].ewm(span=12, adjust=False).mean()
ema_long = data_hour['Trade_Price_Mean'].ewm(span=26, adjust=False).mean()

# 计算DIF
dif = ema_short - ema_long

# 计算DEA
dea = dif.ewm(span=9, adjust=False).mean()

# 计算MACD
macd = dif - dea

# 添加MACD指标回数据框中
data_hour['MACD_DIF'] = dif
data_hour['MACD_DEA'] = dea
data_hour['MACD'] = macd

# 接下来计算KDJ指标
# 由于KDJ通常需要高、低、收盘价，我们将使用每小时的最高价、最低价和收盘价（Trade_Price_Mean）

# 计算RSV
low_min = data_hour['Trade_Price_Min'].rolling(window=9).min()
high_max = data_hour['Trade_Price_Max'].rolling(window=9).max()
rsv = (data_hour['Trade_Price_Mean'] - low_min) / (high_max - low_min) * 100

# 初始化K、D值
k = rsv.ewm(alpha=1/3, adjust=False).mean()
d = k.ewm(alpha=1/3, adjust=False).mean()
j = 3 * k - 2 * d

# 添加KDJ指标回数据框中
data_hour['K'] = k
data_hour['D'] = d
data_hour['J'] = j

path = r'C:\Users\samuel\dsmp-2024-group18\Data Clean\data\data_combine\data_kdj_macd\data_kdj_macd.csv'
data_hour.to_csv(path)



