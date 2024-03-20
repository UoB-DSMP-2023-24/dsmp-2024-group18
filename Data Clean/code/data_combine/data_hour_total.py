import os
from datetime import datetime, timedelta
import pandas as pd


def merge_files(start_date, end_date, output_combined_path):
    # 初始化一个空的DataFrame，用于合并所有数据
    combined_df = pd.DataFrame()

    current_date = start_date
    while current_date <= end_date:
        file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}combine.csv"
        file_path = rf"E:\mini-project\data_combine\hour\{file_name}"

        # 检查文件是否存在
        if os.path.exists(file_path):
            print("Processing file:", file_path)

            # 读取数据
            data = pd.read_csv(file_path)

            # 将读取的数据追加到combined_df中
            combined_df = pd.concat([combined_df, data], ignore_index=True)
        else:
            print("File not found:", file_name)

        # 到下一天
        current_date += timedelta(days=1)

    # 将合并后的数据保存到CSV文件
    combined_df.to_csv(output_combined_path, index=False)
    print(f'All data combined and saved to {output_combined_path}')


# 定义开始和结束日期
start_date = datetime(2025, 1, 2)
end_date = datetime(2025, 7, 1)

# 定义输出合并文件的路径
output_combined_path = r'E:\mini-project\data_combine\data_total_hour\data_hour_total.csv'

# 执行函数
merge_files(start_date, end_date, output_combined_path)
