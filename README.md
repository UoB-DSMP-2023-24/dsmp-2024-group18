# Data Clean
## Introduction to the mandate
    Data cleaning tasks mainly include data structuring, outlier handling, and feature extraction.
## File description
    Data_clean_214.py Initial structuring of the data and extraction of some of the mid-price, order-imbalance, total-volume and bid-ask-spread parameters.
    Data_clean_month_222.py Consolidate data by month.
    data_extra_314.py The outliers were processed by removing 5% of the textual outlier values while adding more features.
## Characteristics
    Bid_Price and Ask_Price: These two features represent the current bid and ask prices in the market. They directly reflect the immediate state of supply and demand in the market and are the basis for making any buy and sell decisions.

    Bid_Ask_Spread: The bid-ask spread is the difference between the bid and ask prices and can be used as a measure of market liquidity and participant nervousness. Smaller spreads usually imply high liquidity and lower transaction costs, and for automated trading systems, recognising a low spread environment may be beneficial for executing low-cost trades.

    Market_Depth_Bid and Market_Depth_Ask: Market Depth indicates the volume of orders at a given price level, with greater depth indicating greater willingness to buy and sell at that price level. 

    Historical_Volatility: Historical volatility is measured by the standard deviation of past price movements and reflects the level of uncertainty and risk in market price movements.

    Weighted_Avg_Bid_Price and Weighted_Avg_Ask_Price: Weighted Average Bid and Ask Prices take into account the volume of orders at each price level, providing an average price indicator that takes into account the depth of the market. These indicators can be used to identify potential buying or selling opportunities, especially when prices deviate significantly from the weighted average price.

    Cumulative_Volume_Difference: The Cumulative Order Volume Difference reflects the overall imbalance between buy and sell orders. This indicator can be used to predict short-term price movements, e.g. buy orders outnumbering sell orders may signal upward pressure on prices.

    Total_Volume_Change_Corrected: The corrected change in total volume shows a change in the level of market activity. An increase or decrease in volume can be used as one indicator of the strength of a market trend and is particularly useful when determining entry or exit strategies.

    Order_imbalance: Order imbalance measures the imbalance between buy and sell orders and, similar to Cumulative_Volume_Difference, it can be used to sense how well the market is accepting the current price level and the direction of potential price movement.

## Content Updates
    V1.0.0 Text structuring
    V1.0.1 Consolidation of data into months
    V1.0.2 More features to improve readability

