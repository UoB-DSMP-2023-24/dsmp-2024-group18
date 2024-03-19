import os
from datetime import datetime, timedelta
import pandas as pd


def clean_and_merge_data(start_date, end_date):
    """
    Cleans and merges limit order book (LOB) and trade tape data from CSV files
    for a given date range, then saves the combined data to new CSV files.

    Parameters:
    - start_date: The start date for data processing (inclusive).
    - end_date: The end date for data processing (inclusive).
    """
    current_date = start_date
    while current_date <= end_date:
        # Define file names based on the current date
        lob_file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}LOBs.csv"
        tape_file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}tapes.csv"

        # Define file paths
        lob_file_path = rf"E:\mini-project\lob_cleaned_extra\{lob_file_name}"
        tape_file_path = rf"E:\mini-project\tapes_cleaned\{tape_file_name}"

        # Output combined file name
        combine_file_name = f"UoB_Set01_{current_date.strftime('%Y-%m-%d')}combine.csv"

        # Check if both LOB and tape files exist
        if os.path.exists(lob_file_path) and os.path.exists(tape_file_path):
            print(f"Processing LOB file: {lob_file_path}")
            print(f"Processing tape file: {tape_file_path}")

            # Load LOB and tape data
            lobs_df = pd.read_csv(lob_file_path)
            tapes_df = pd.read_csv(tape_file_path)

            # Rename columns to ensure consistency for merging
            tapes_df.rename(columns={'Trade_time': 'Time'}, inplace=True)

            # Convert time columns to datetime.time for accurate time-based operations
            lobs_df['Time'] = pd.to_datetime(lobs_df['Time'], format='%H:%M:%S').dt.time
            tapes_df['Time'] = pd.to_datetime(tapes_df['Time'], format='%H:%M:%S').dt.time

            # Merge LOB and tape data on 'Time' column, filling missing trade data forward
            merged_df = pd.merge(lobs_df, tapes_df, on='Time', how='left')
            merged_df['Weighted_Avg_Price'] = merged_df['Weighted_Avg_Price'].fillna(method='ffill')

            # Create a 'DateTime' column from the 'Time' column and current date
            merged_df['DateTime'] = current_date.strftime('%Y-%m-%d') + ' ' + merged_df['Time'].apply(
                lambda x: x.strftime('%H:%M:%S'))

            # Prepare the final DataFrame for saving
            merged_df.set_index('DateTime', inplace=True)
            merged_df.reset_index(inplace=True)
            merged_df.drop('Time', axis=1, inplace=True)

            # Save the cleaned and merged data to a CSV file
            output_csv_path = rf'E:\mini-project\data_combine\second\{combine_file_name}'
            merged_df.to_csv(output_csv_path, index=False)
            print(f'Cleaned and merged data saved to: {output_csv_path}')
        else:
            # Handle missing files
            print(f"File not found: {lob_file_name}")
            print(f"File not found: {tape_file_name}")

        # Move to the next date
        current_date += timedelta(days=1)


# Specify the start and end dates for the data cleaning process
start_date = datetime(2025, 1, 2)
end_date = datetime(2025, 7, 1)

# Call the function to begin the data cleaning and merging process
clean_and_merge_data(start_date, end_date)
