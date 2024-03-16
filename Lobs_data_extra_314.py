import os
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict

start_date = datetime(2025, 1, 2)
end_date = datetime(2025, 7, 1)
# 加载数据

def data_clean(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}LOBs.csv"
        file_path = rf"E:\mini-project\test_data\{file_name}"
        if os.path.exists(file_path):
            print("Processing file:", file_name)

            data_lob = pd.read_csv(file_path)

            # 特征提取
            # 解析Bid和Ask的价格及数量
            data_lob[['Bid1_Price', 'Bid1_Volume']] = data_lob['Bid1'].str.strip('[]').str.split(', ', expand=True).astype(float)
            data_lob[['Ask1_Price', 'Ask1_Volume']] = data_lob['Ask1'].str.strip('[]').str.split(', ', expand=True).astype(float)
            data_lob[['Bid2_Price', 'Bid2_Volume']] = data_lob['Bid2'].str.strip('[]').str.split(', ', expand=True).astype(float)
            data_lob[['Ask2_Price', 'Ask2_Volume']] = data_lob['Ask2'].str.strip('[]').str.split(', ', expand=True).astype(float)

            # 计算特征
            data_lob['Bid_Ask_Spread'] = data_lob['Ask1_Price'] - data_lob['Bid1_Price']

            data_lob['Market_Depth_Bid'] = data_lob['Bid1_Volume'] + data_lob['Bid2_Volume']
            data_lob['Market_Depth_Ask'] = data_lob['Ask1_Volume'] + data_lob['Ask2_Volume']
            data_lob['Historical_Volatility'] = data_lob['Mid-Price'].rolling(window=5).std()
            data_lob['Weighted_Avg_Bid_Price'] = (data_lob['Bid1_Price'] * data_lob['Bid1_Volume']) / data_lob['Bid1_Volume']
            data_lob['Weighted_Avg_Ask_Price'] = (data_lob['Ask1_Price'] * data_lob['Ask1_Volume']) / data_lob['Ask1_Volume']
            data_lob['Cumulative_Volume_Difference'] = data_lob['Bid1_Volume'] + data_lob['Bid2_Volume'] - data_lob['Ask1_Volume'] - data_lob['Ask2_Volume']
            data_lob['Total_Volume_Change'] = data_lob['Total_volume'].diff()
            Q1 = data_lob['Total_Volume_Change'].quantile(0.25)
            Q3 = data_lob['Total_Volume_Change'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            data_lob['Total_Volume_Change_Corrected'] = data_lob['Total_Volume_Change'].apply(lambda x: min(max(x, lower_bound), upper_bound))

            # 异常值处理
            bid_5th_percentile = data_lob['Bid1_Price'].quantile(0.025)
            bid_95th_percentile = data_lob['Bid1_Price'].quantile(0.975)
            ask_5th_percentile = data_lob['Ask1_Price'].quantile(0.025)
            ask_95th_percentile = data_lob['Ask1_Price'].quantile(0.975)
            data_lob_filtered = data_lob[(data_lob['Bid1_Price'] >= bid_5th_percentile) & (data_lob['Bid1_Price'] <= bid_95th_percentile) & (data_lob['Ask1_Price'] >= ask_5th_percentile) & (data_lob['Ask1_Price'] <= ask_95th_percentile)]

            # 整理数据
            data_lob_final = data_lob_filtered[['Time', 'Bid1_Price', 'Bid1_Volume', 'Ask1_Price', 'Ask1_Volume', 'Bid2_Price', 'Bid2_Volume',
                                                'Ask2_Price', 'Ask2_Volume', 'Bid_Ask_Spread', 'Market_Depth_Bid', 'Market_Depth_Ask', 'Historical_Volatility', 'Weighted_Avg_Bid_Price', 'Weighted_Avg_Ask_Price',
                                                'Total_volume', 'Cumulative_Volume_Difference', 'Total_Volume_Change_Corrected', 'Order_imbalance']].copy()

            # 保存文件
            output_name = f'{file_name[:-4]}.csv'
            output_csv_path = rf'E:\mini-project\test_data_2\{output_name}'
            data_lob_final.to_csv(output_csv_path, index=False)

            # 输出保存文件的路径
            print(f'Cleaned data saved to {output_csv_path}')

        else:
            print("File not found:", file_name)
            pass
        current_date += timedelta(days=1)



data_clean(start_date, end_date)