import os
from datetime import datetime, timedelta
import ast
import pandas as pd
from collections import defaultdict


def preprocess_line(line):
    parts = line.split(',', 2)
    if len(parts) > 1:
        parts[1] = f" '{parts[1].strip()}'"
    return ','.join(parts)


def parse_data(data):
    id_value = data[0]
    name = data[1]
    bid = data[2][0][1][:2] if data[2] else []
    ask = data[2][1][1][:2] if data[2] else []

    bid_list = data[2][0][1] if data[2] else []
    ask_list = data[2][1][1] if data[2] else []

    bid_1 = bid_list[0] if bid_list else []
    bid_2 = bid_list[1] if len(bid_list) > 1 else []

    ask_1 = ask_list[0] if ask_list else []
    ask_2 = ask_list[1] if len(ask_list) > 1 else []

    return [id_value, name, bid, bid_1, bid_2, ask, ask_1, ask_2]



def convert_timestamp_to_time(timestamp):
    total_seconds = timestamp + 7.5 * 3600  # Add 7 hours and 30 minutes
    hour = total_seconds // 3600
    minute = (total_seconds % 3600) // 60
    second = total_seconds % 60
    return f"{int(hour):02d}:{int(minute):02d}:{int(second):02d}"


start_date = datetime(2025, 7, 1)
end_date = datetime(2025, 7, 2)


def update_dates(start_date, end_date):
    monthly_data = defaultdict(list)

    current_date = start_date
    while current_date <= end_date:
        file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}LOBs.txt"
        file_path = rf"E:\mini-project\JPMorgan_Set01\LOBs\{file_name}"
        if os.path.exists(file_path):
            print("Processing file:", file_name)
            merge_bid1 = defaultdict(list)
            merge_bid2 = defaultdict(list)
            merge_ask1 = defaultdict(list)
            merge_ask2 = defaultdict(list)

            with open(file_path, 'r') as file:
                for line in file:
                    preprocessed_line = preprocess_line(line.strip())
                    try:
                        data = ast.literal_eval(preprocessed_line)
                        details = parse_data(data)
                        timestamp = int(data[0])

                        merge_bid1[timestamp].append(details[3])
                        merge_bid2[timestamp].append(details[4])
                        merge_ask1[timestamp].append(details[6])
                        merge_ask2[timestamp].append(details[7])

                    except ValueError as e:
                        print(f"Error processing line: {line.strip()}")
                        print(str(e))
                        break

            merged_result = []
            start_timestamp = 0
            end_timestamp = 8.5 * 3600  # 16:00的时间戳
            for timestamp in sorted(set(merge_bid1.keys()) | set(merge_bid2.keys()) | set(merge_ask1.keys()) | set(
                    merge_ask2.keys())):
                if timestamp < start_timestamp:
                    continue
                elif timestamp >= end_timestamp:
                    break
                merged_data = [convert_timestamp_to_time(timestamp)]

                # Bid 1
                bid1_sum = 0
                bid1_volume = 0
                for data in merge_bid1[timestamp]:
                    if len(data) == 0:
                        bid1_sum += 0
                        bid1_volume += 0
                    else:
                        bid1_sum += data[0] * data[1]
                        bid1_volume += data[1]
                bid1_avg = bid1_sum / bid1_volume if bid1_volume != 0 else 0

                # Bid 2
                bid2_sum = 0
                bid2_volume = 0
                for data in merge_bid2[timestamp]:
                    if len(data) == 0:
                        bid2_sum += 0
                        bid2_volume += 0
                    else:
                        bid2_sum += data[0] * data[1]
                        bid2_volume += data[1]
                bid2_avg = bid2_sum / bid2_volume if bid2_volume != 0 else 0

                # Ask 1
                ask1_sum = 0
                ask1_volume = 0
                for data in merge_ask1[timestamp]:
                    if len(data) == 0:
                        ask1_sum += 0
                        ask1_volume += 0
                    else:
                        ask1_sum += data[0] * data[1]
                        ask1_volume += data[1]
                ask1_avg = ask1_sum / ask1_volume if ask1_volume != 0 else 0

                # Ask 2
                ask2_sum = 0
                ask2_volume = 0
                for data in merge_ask2[timestamp]:
                    if len(data) == 0:
                        ask2_sum += 0
                        ask2_volume += 0
                    else:
                        ask2_sum += data[0] * data[1]
                        ask2_volume += data[1]
                ask2_avg = ask2_sum / ask2_volume if ask2_volume != 0 else 0

                mid_price = (bid1_avg + ask1_avg) / 2

                bid_volume = bid1_volume + bid2_volume
                ask_volume = ask1_volume + ask2_volume
                total_volume = bid1_volume + bid2_volume + ask1_volume + ask2_volume

                bid_ask_spread = ask1_avg - bid1_avg

                if bid_volume + ask_volume != 0:
                    order_imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)
                else:
                    order_imbalance = 0.0000

                bid1_avg = round(bid1_avg, 2)
                bid2_avg = round(bid2_avg, 2)
                ask1_avg = round(ask1_avg, 2)
                ask2_avg = round(ask2_avg, 2)
                mid_price = round(mid_price, 2)
                bid_ask_spread = round(bid_ask_spread, 2)
                order_imbalance = round(order_imbalance, 2)

                merged_data.extend(
                    [[bid1_avg, bid1_volume], [bid2_avg, bid2_volume], [ask1_avg, ask1_volume], [ask2_avg, ask2_volume],
                     mid_price, total_volume, bid_ask_spread, order_imbalance])
                merged_result.append(merged_data)

            columns = ["Time", "Bid1", "Bid2", "Ask1", "Ask2", "Mid-Price", 'Total_volume', 'Bid_ask_spread',
                       'Order_imbalance']

            df = pd.DataFrame(merged_result, columns=columns)

            df['Day'] = current_date.strftime('%Y-%m-%d')
            cols = ['Day'] + [col for col in df.columns if col != 'Day']
            df = df[cols]
            month_key = current_date.strftime('%Y-%m')
            monthly_data[month_key].append(df)

            # output_name = f'{file_name[:-4]}.csv'
            # output_csv_path = rf'E:\mini-project\test_data\{output_name}'
            # df.to_csv(output_csv_path, index=False)
            #
            # print(f"DataFrame saved to {output_csv_path}")
            # print(f"Total number of rows (Volume Data): {len(df)}")
            # 在这里调用处理文件的函数
            # process_file(file_path)
        else:
            print("File not found:", file_name)
            pass
        current_date += timedelta(days=1)
    # 合并每个月的DataFrame，并保存为单独的CSV文件
    for month, dfs in monthly_data.items():
        monthly_df = pd.concat(dfs, ignore_index=True)
        output_csv_path = rf'E:\mini-project\test_data\data_monthly\merged_{month}.csv'
        monthly_df.to_csv(output_csv_path, index=False)
        print(f"Monthly DataFrame for {month} saved to {output_csv_path}")





profile = update_dates(start_date, end_date)
