import os
from datetime import datetime, timedelta
import ast
import pandas as pd
from collections import defaultdict

start_date = datetime(2025, 1, 2)
end_date = datetime(2025, 7, 1)


# Define function to convert trading session time to HH:MM:SS format
def convert_seconds_to_trading_time(seconds):
    """Converts seconds since session start (7:30 AM) into HH:MM:SS format."""
    session_start = pd.Timestamp('2025-01-02 07:30:00')
    time = session_start + pd.Timedelta(seconds=seconds)
    return time.time()


def update_dates(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}tapes.csv"
        file_path = rf"E:\mini-project\JPMorgan_Set01\Tapes\{file_name}"
        if os.path.exists(file_path):
            # Load the data
            print("Processing file:", file_name)
            data = pd.read_csv(file_path, header=None)
            data.columns = ['Time', 'Price', 'Volume']
            # Apply the correct time conversion and aggregation logic
            data['Time'] = data['Time'].apply(lambda x: int(x))  # Round to nearest second for aggregation
            data['Weighted_Price'] = data['Price'] * data['Volume']  # Calculate weighted price for each row

            # Group by Time, then calculate weighted sum price and total volume
            aggregated_data = data.groupby('Time').agg(
                Weighted_Sum_Price=('Weighted_Price', 'sum'),
                Trade_Volume=('Volume', 'sum')
            ).reset_index()

            # Calculate weighted average price
            aggregated_data['Weighted_Avg_Price'] = (aggregated_data['Weighted_Sum_Price'] / aggregated_data['Trade_Volume']).round(2) # Calculate weighted average
            # Convert time since session start into HH:MM:SS format
            aggregated_data['Trade_time'] = aggregated_data['Time'].apply(convert_seconds_to_trading_time)

            # Select only the necessary columns for the final output
            final_data = aggregated_data[['Trade_time', 'Weighted_Avg_Price', 'Trade_Volume']]

            output_name = f'{file_name[:-4]}.csv'
            output_csv_path = rf'E:\mini-project\tapes_cleaned\{output_name}'
            final_data.to_csv(output_csv_path, index=False)

            print(f"DataFrame saved to {output_csv_path}")
            print(f"Total number of rows (Volume Data): {len(final_data)}")
            # 在这里调用处理文件的函数
            # process_file(file_path)
        else:
            print("File not found:", file_name)
            pass
        current_date += timedelta(days=1)


if __name__ == '__main__':
    update_dates(start_date, end_date)
