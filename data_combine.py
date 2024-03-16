import os
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict


def data_clean(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        lob_file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}LOBs.csv"
        tape_file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}tapes.csv"
        lob_file_path = rf"E:\mini-project\lob_cleaned_extra\{lob_file_name}"
        tape_file_path = rf"E:\mini-project\tapes_cleaned\{tape_file_name}"
        combine_file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}combine.csv"

        if os.path.exists(lob_file_path) and os.path.exists(tape_file_path):
            print("Processing file:", lob_file_path)
            print("Processing file:", tape_file_path)
            # 加载LOB数据
            lobs_df = pd.read_csv(lob_file_path)
            # 将LOB数据中的时间转换为datetime.time对象，便于后续处理
            # 加载实时交易数据
            tapes_df = pd.read_csv(tape_file_path)

            # 假设实时交易数据的起始时间为07:30:00，并将时间转换为HH:MM:SS格式

            # Rename the columns to match for a proper merge
            tapes_df.rename(columns={'Trade_time': 'Time'}, inplace=True)

            # Convert time columns in both dataframes to datetime type for accurate merging
            lobs_df['Time'] = pd.to_datetime(lobs_df['Time'], format='%H:%M:%S').dt.time
            tapes_df['Time'] = pd.to_datetime(tapes_df['Time'], format='%H:%M:%S').dt.time

            # Merge the dataframes on the 'Time' column, keeping all rows from the LOBs dataframe
            merged_df = pd.merge(lobs_df, tapes_df, on='Time', how='left')

            # Now, we will backfill the 'Weighted_Avg_Price' column from the tapes dataframe
            merged_df['Weighted_Avg_Price'] = merged_df['Weighted_Avg_Price'].fillna(method='ffill')

            # Display the first few rows of the merged dataframe to confirm the merge and backfill
            output_name = f'{combine_file_name[:-4]}.csv'
            output_csv_path = rf'E:\mini-project\data_combine\{output_name}'
            merged_df.to_csv(output_csv_path, index=False)

            # 输出保存文件的路径
            print(f'Cleaned data saved to {output_csv_path}')

        else:
            print("File not found:", lob_file_name)
            print("File not found:", tape_file_name)
            pass
        current_date += timedelta(days=1)



start_date = datetime(2025, 1, 2)
end_date = datetime(2025, 7, 1)

data_clean(start_date, end_date)
