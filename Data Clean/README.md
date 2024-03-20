# Data Clean
## Introduction to the mandate
    Data cleaning tasks mainly include data structuring, outlier handling, and feature extraction.
## File description
### code
#### data_clean
    Lobs_data_clean_214.py - Initial structuring of the data and extraction of some of the mid-price, order-imbalance, total-volume and bid-ask-spread parameters.

    Lobs_data_clean_month_222.py - Consolidate data by month.

    Lobs_data_extra_314.py - The outliers were processed by removing 5% of the textual outlier values while adding more features.
    
    tapes_clean_316.py - Temporal structuring of tapes data.
#### data_combine
    data_combine_second.py - Merge lobs and tapes data at the second level.

    data_combine_min.py - Merge lobs and tapes data at the minute level.

    data_combine_hour.py - Merge lobs and tapes data at the hour level.

    data_second_total.py - his part of the code combines all the data at the second level.

    data_min_total.py - This part of the code combines all the data at the minute level.

    data_hour_total.py - This part of the code combines all the data at the hour level.
### data
    lob_cleaned - The primary processing of data mainly includes text conversion, time structuring, and feature separation.
    
    lob_cleaned_extra - Added more features and reduced outlier data by 5%.

    data_combine - All data combined in seconds, minutes, and hours.

    tapes_cleaned - The data is organized at the second level.

## Characteristics
    Bid_Price and Ask_Price: These two features represent the current bid and ask prices in the market. They directly reflect the immediate state of supply and demand in the market and are the basis for making any buy and sell decisions.

    Bid_Ask_Spread: The bid-ask spread is the difference between the bid and ask prices and can be used as a measure of market liquidity and participant nervousness. Smaller spreads usually imply high liquidity and lower transaction costs, and for automated trading systems, recognising a low spread environment may be beneficial for executing low-cost trades.

    Market_Depth_Bid and Market_Depth_Ask: Market Depth indicates the volume of orders at a given price level, with greater depth indicating greater willingness to buy and sell at that price level. 

    Historical_Volatility: Historical volatility is measured by the standard deviation of past price movements and reflects the level of uncertainty and risk in market price movements.

    Cumulative_Volume_Difference: The Cumulative Order Volume Difference reflects the overall imbalance between buy and sell orders. This indicator can be used to predict short-term price movements, e.g. buy orders outnumbering sell orders may signal upward pressure on prices.

    Total_Volume_Change_Corrected: The corrected change in total volume shows a change in the level of market activity. An increase or decrease in volume can be used as one indicator of the strength of a market trend and is particularly useful when determining entry or exit strategies.

    Order_imbalance: Order imbalance measures the imbalance between buy and sell orders and, similar to Cumulative_Volume_Difference, it can be used to sense how well the market is accepting the current price level and the direction of potential price movement.

    Weighted_Avg_Price: is the real-time trading price, where the data is supplemented using forward padding.

    Trade_Volume: trade volume.

## Content Updates
    V1.0.0 Text structuring
    V1.0.1 Consolidation of data into months
    V1.0.2 More features to improve readability
    V2.0.1 Consolidation of all cleaned data.
    V2.0.2 Calculation of data at different time levels, and data merging.

