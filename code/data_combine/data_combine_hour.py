import os
from datetime import datetime, timedelta
import pandas as pd


def data_clean(start_date, end_date):
    # Initialize the current_date to the start_date
    current_date = start_date

    while current_date <= end_date:
        # Format the filename based on the current date
        file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}combine.csv"
        # Specify the path to the file
        file_path = rf"E:\mini-project\data_combine\second\{file_name}"

        # Check if the file exists at the specified path
        if os.path.exists(file_path):
            print("Processing file:", file_path)

            # Load the data from CSV
            data = pd.read_csv(file_path)

            # Convert the 'DateTime' column to datetime format for accurate processing
            data['DateTime'] = pd.to_datetime(data['DateTime'])

            # Extract date and time up to minutes for detailed grouping
            data['DateTime_Hour'] = data['DateTime'].dt.floor('H')

            # Group the data by the new DateTime_Minute column and aggregate various columns
            grouped = data.groupby('DateTime_Hour').agg({
                'Bid1_Price': 'mean',
                'Bid1_Volume': 'sum',
                'Ask1_Price': 'mean',
                'Ask1_Volume': 'sum',
                'Bid2_Price': 'mean',
                'Bid2_Volume': 'sum',
                'Ask2_Price': 'mean',
                'Ask2_Volume': 'sum',
                'Mid-Price': 'mean',
                'Bid_Ask_Spread': 'mean',
                'Market_Depth_Bid': 'sum',
                'Market_Depth_Ask': 'sum',
                'Historical_Volatility': 'mean',
                'Total_volume': 'sum',
                'Cumulative_Volume_Difference': 'sum',
                'Total_Volume_Change_Corrected': 'sum',
                'Order_imbalance': 'mean',
                'Weighted_Avg_Price': ['min', 'max'],
                'Trade_Volume': 'sum'
            }).reset_index().round(2)

            # Update column names for clarity, combining them where necessary
            grouped.columns = ['_'.join(col).rstrip('_') for col in grouped.columns.values]

            # Explicitly rename columns for better understanding
            grouped = grouped.rename(columns={
                'Weighted_Avg_Price_min': 'Trade_Price_Min',
                'Weighted_Avg_Price_max': 'Trade_Price_Max'
                # The 'Weighted_Avg_Price_mean' renaming was removed as it's not directly calculated here
            })

            # Calculate the mean of Weighted_Avg_Price only for non-NaN Trade_Volume entries
            filtered_data = data[data['Trade_Volume'].notna()]
            weighted_avg_price_mean = filtered_data.groupby('DateTime_Hour')['Weighted_Avg_Price'].mean().to_frame(
                'Trade_Price_Mean').round(2)

            # Merge the calculated mean into the aggregated data
            grouped_with_filtered_mean = pd.merge(grouped, weighted_avg_price_mean, on='DateTime_Hour', how='left')

            # Define the output file name and path
            output_name = f'{file_name[:-4]}.csv'
            output_csv_path = rf'E:\mini-project\data_combine\hour\{output_name}'

            # Save the cleaned and aggregated data to CSV
            grouped_with_filtered_mean.to_csv(output_csv_path, index=False)

            # Log the path to the saved file
            print(f'Cleaned data saved to {output_csv_path}')
        else:
            print("File not found:", file_name)

        # Increment the current_date by one day
        current_date += timedelta(days=1)


# Define the start and end dates for cleaning
start_date = datetime(2025, 1, 2)
end_date = datetime(2025, 7, 1)

# Call the data_clean function with the specified start and end dates
data_clean(start_date, end_date)
