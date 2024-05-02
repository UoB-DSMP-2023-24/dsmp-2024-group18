import os
import ast
import pandas as pd
from datetime import datetime

# 前处理函数，保持不变
def preprocess_line(line):
    parts = line.split(',', 2)
    if len(parts) > 1:
        parts[1] = f" '{parts[1].strip()}'"
    return ','.join(parts)

def parse_data(data):
    id_value = data[0]
    name = data[1]
    bid = data[2][0] if data[2] else []
    ask = data[2][1] if data[2] else []
    first_two_bids = bid[:2] if bid else []
    first_two_asks = ask[:2] if ask else []

    # 提取出价格和数量，确保它们都是数值类型
    bid_prices = [x[0] for x in bid if isinstance(x, list) and len(x) > 1 and isinstance(x[0], (int, float))]
    ask_prices = [x[0] for x in ask if isinstance(x, list) and len(x) > 1 and isinstance(x[0], (int, float))]
    bid_volumes = [x[1] for x in bid if isinstance(x, list) and len(x) > 1 and isinstance(x[1], (int, float))]
    ask_volumes = [x[1] for x in ask if isinstance(x, list) and len(x) > 1 and isinstance(x[1], (int, float))]

    # 计算中间价
    if bid_prices and ask_prices:
        mid_price = (max(bid_prices, default=0) + min(ask_prices, default=0)) / 2
    else:
        mid_price = 0  # 如果没有数据则填充0

    # Calculate Bid-Ask Spread
    if bid_prices and ask_prices:
        bid_ask_spread = min(ask_prices) - max(bid_prices) if bid_prices and ask_prices else 0
    else:
        bid_ask_spread = 0

    # 计算总量，卖量和买量
    volume_data = sum(bid_volumes) + sum(ask_volumes)
    ask_volume_data = sum(ask_volumes)
    bid_volume_data = sum(bid_volumes)

    # Calculate Order Imbalance
    if bid_volume_data + ask_volume_data != 0:
        order_imbalance = (bid_volume_data - ask_volume_data) / (bid_volume_data + ask_volume_data)
        order_imbalance = "{:.4f}".format(order_imbalance)
    else:
        order_imbalance = "0.0000"

    return [id_value, name, bid, ask, mid_price, volume_data, bid_ask_spread, ask_volume_data, bid_volume_data,
            order_imbalance, first_two_bids, first_two_asks]


# 解析文件名中的日期
def parse_date_from_filename(filename):
    # Assuming the date is always after the third underscore and followed by "LOBs.txt"
    date_part = filename.split('_')[2]  # This will be something like "2025-01-02LOBs.txt"
    date_str = date_part[:10]  # This will extract just the "2025-01-02" part
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return date


# 初始化一个空的DataFrame
all_data = pd.DataFrame()

# 指定文件夹路径，这需要您根据实际情况进行调整
folder_path = 'LOB'  # 替换为实际文件夹路径

# 列名，根据您的需要进行调整
columns = ["TimeStamp", "Exchange_name", "Bid", "Ask", "Mid-Price", "Volume Data", "Bid-Ask Spread", "Ask Volume Data", "Bid Volume Data", "Order Imbalance","First Two Bids", "First Two Asks"]

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_date = parse_date_from_filename(filename)
        # 检查日期是否在指定范围内
        if datetime(2025, 1, 2) <= file_date <= datetime(2025, 4, 14):
            file_path = os.path.join(folder_path, filename)
            result = []  # 存储单个文件的结果
            with open(file_path, 'r') as file:
                for line in file:
                    preprocessed_line = preprocess_line(line.strip())
                    try:
                        data = ast.literal_eval(preprocessed_line)
                        details = parse_data(data)
                        result.append(details)
                    except ValueError as e:
                        print(f"Error processing line in {filename}: {line.strip()}")
                        print(str(e))
                        continue  # 继续处理下一行
            df = pd.DataFrame(result, columns=columns)
            all_data = pd.concat([all_data, df], ignore_index=True)

# 将合并后的数据保存为CSV文件
output_csv_path = 'combined_data.csv'
all_data.to_csv(output_csv_path, index=False)

print(f"DataFrame saved to {output_csv_path}")
print(f"Total number of rows: {len(all_data)}")
