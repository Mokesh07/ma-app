import sys
import streamlit as st
import pandas as pd
import yfinance as yf
from scipy.stats import norm

def fetch_data(bigger_ma, smaller_ma):
    from datetime import date
    data = yf.download("^NSEI", start="2000-01-01", end=date.today())
    # Change the index and remove the unwanted columns
    data = data[["Close"]]
    data["Date"] = data.index
    data = data.reset_index(drop=True)
    data = pd.DataFrame(data)

    # Calculate 20-day moving average
    data['bigger_ma'] = data['Close'].rolling(window=bigger_ma).mean()

    # Calculate 7-day moving average
    data['smaller_ma'] = data['Close'].rolling(window=smaller_ma).mean()

    # Calculate the difference between the long-day and short-day moving averages
    data['ma_difference'] = ((data['smaller_ma'] - data['bigger_ma']) / data['bigger_ma']) * 100

    # Drop the na rows
    data = data.dropna()
    data = data.reset_index(drop=True)

    # Standardize the ma_percentage_difference column
    standardized_data = data['ma_difference'].dropna()

    # Calculating the stats for threshold
    ci = [0.95,0.90,0.80]
    confidence_interval = []
    mu, std = norm.fit(standardized_data)
    for i in range(len(ci)):
        interval = norm.interval(ci[i], loc=mu, scale=std)
        confidence_interval.append(interval)

    # Getting required information to return
    date = data.iloc[-1]["Date"].strftime('%d-%m-%Y')
    current_diff = data.iloc[-1]["ma_difference"].round(2)
    indication = []
    for i in range(len(confidence_interval)):
        if (current_diff <= confidence_interval[i][0]):
            indication.append("Buy")
        elif (current_diff >= confidence_interval[i][1]):
            indication.append("Sell")
        else:
            indication.append("Hold")

    return(date, ci, confidence_interval, current_diff, indication)

def main():
    st.title("Investing with Moving Averages")

    st.write("""
    Moving average is fundamental tool for an investors or traders alike.\
    They provide a smoothed representation of price data over a specified period, allowing analysts to identify \
    trends and potential reversal points in financial markets. 
    """)

    # Display picture
    st.image(r"C:\Users\um01\OneDrive - Pfizer\Desktop\My Work\Innovate\MA APP\single_ma.png",
             caption='21-Day Moving Average applied on Price Data')

    # Subtitle
    st.subheader("Moving Average Crossover")
    st.write("""
    The concept of moving average crossover is a popular technique used in \
    technical analysis by traders and investors to identify potential changes in trend direction.\
    It involves the comparison of two or more moving averages of different periods, \
    typically a shorter-term moving average and a longer-term moving average.
     """)

    st.write("""
    There are two different crossovers which is explained below:

    **Golden Cross:** This occurs when the shorter-term moving average crosses above \
    the longer-term moving average. It is considered a bullish signal, indicating a potential upward trend \
    reversal or continuation.\n
    **Death Cross:** This occurs when the shorter-term moving average crosses below the \
    longer-term moving average. It is considered a bearish signal, suggesting a potential downward trend \
    reversal or continuation.\n
    """)

    # Display picture
    st.image(r"C:\Users\um01\OneDrive - Pfizer\Desktop\My Work\Innovate\MA APP\double_ma.png",
             caption='21-Day/7-Day Moving Average applied on Price Data with Crossover(+)')

    st.subheader("Leveraging Moving Average for Market Entry Points")

    st.write("""
    Having a reliable method to pinpoint optimal times for investment in the stock market\
    is essential. Moving average presents us a straightforward approach where we compare the \
    shorter-term moving average to the longer-term moving average and when the shorter one \
    significantly lags behind the longer one, it could be a sign that the market is undervalued, \
    presenting a potential investment opportunity.\n 
    To understand how the difference between these moving averages typically behaves, it is required to\
    understand the past patterns. If the current difference between the long and short-term MA falls below a \
    threshold of 95% of the historical average, it suggests that the market is notably undervalued compared to its \
    historical norms. To put this strategy to the test,\
    thorough backtesting was done using historical data from NIFTY spanning over \
    a significant period, from 2007 to the present day. In this analysis, 21-day and 7-day moving average were used \
    to simulate real-world scenarios.\n
    Comparing this investment strategy with a conventional Systematic Investment Plan (SIP) approach, \
    where investors regularly invest a fixed amount every month, revealed a striking disparity in gains. \
    The analysis showcased that the strategy of leveraging moving average differentials outperformed the traditional SIP\
    method.""")

    st.subheader("Threshold Calculation")

    st.write(""" 
    The threshold value is calculated based on historical data, here considering Nifty 50 data \
    from 2007 to the present day (2024). The calculation involves collecting all the differences between the long \
    and short-term moving averages, here set at **21** and **7**, respectively. The outcome of this calculation\
    typically follows a normal distribution. By disregarding the 95% range from the mean and focusing\
    on values beyond that range, investors can determine when to invest.""")

    # Display picture
    st.image(r"C:\Users\um01\OneDrive - Pfizer\Desktop\My Work\Innovate\MA APP\boundary.png",
             caption='Historical difference between long and short-term MA')


    st.subheader("Results")

    st.write("""
    Assuming one person invests Rs 2000 every 22nd trading session (on average, a month has \
    22 trading sessions), and the other person gets credited Rs 2000 every month but holds their \
    money and only invests when the moving average difference is below the threshold. Here are the \
    results of how both would have performed, considering the investment period from 2017 to the \
    present day, every month.""")

    # Create two columns
    col1, col2 = st.columns(2)

    # Create first table
    data1 = {'Invested': ["368000"], 'Current': ["1102520.81"], "Gain (%)": ["299.59"]}
    df1 = pd.DataFrame(data1)
    col1.write("**SIP Method**")
    col1.table(df1.assign(hack='').set_index('hack'))

    # Create first table
    data2 = {'Invested': ["278000"], 'Current': ["921547.51"], "Gain (%)": ["331.49"]}
    df2 = pd.DataFrame(data2)
    col2.write("**Moving Average Investing**")
    col2.table(df2.assign(hack='').set_index('hack'))

    st.write("""
    **Threshold: -4.42%**\n
    **Threshold indicate that the investor has to invest only when the short-term MA is 4.42% lower\
    than the long-term MA.** \n
    **Note:** The invested amount is lower in Moving Average Investing method since the difference between \
    MAs never went below the threshold value after April, 2020 till April, 2024.\n
    This analysis demonstrates one of the methods investors can utilize to gauge whether the market \
    is undervalued or overvalued. By leveraging historical data and employing moving average \
    differentials, investors can potentially identify opportune moments for investment. 
    However, it's crucial to emphasize that this approach serves as a tool rather than a definitive \
    indicator. Investors should conduct their own comprehensive research before making any investment \
    decisions. While moving average strategies offer valuable insights, investing requires a holistic \
    approach that considers a wide range of factors to mitigate risks and maximize returns.""")

    st.subheader("Test it for yourself")
    st.write("""
    Please note that this tool uses **NIFTY 50** data. The results can be used to understand the \
    market valuation and decide whether to invest in index funds at this moment or not.""")

    # Get input words from user
    st.markdown("<h5>Enter the long-term moving average:</h5>", unsafe_allow_html=True)
    long_ma = st.text_input("", value="", max_chars=None, key="long_ma", type='default',
                            help=None)
    st.markdown("<h5>Enter the short-term moving average:</h5>", unsafe_allow_html=True)
    short_ma = st.text_input("", value="", max_chars=None, key="short_ma", type='default',
                             help=None)
    # Check button
    if st.button("Check"):
        if not long_ma.isdigit() or not short_ma.isdigit():
            st.warning("Please enter valid numerical values for moving averages.")
            sys.exit()
        if int(short_ma) >= int(long_ma):
            st.warning("Short-Term MA should be greater than Long-Term MA.")
            sys.exit()

        # Fetching the data
        date, ci, threshold, current_diff, indication = fetch_data(bigger_ma=int(long_ma), smaller_ma=int(short_ma))

        output = {"Date": [date,date,date],
                  "Confidence Interval": [str(ci[0] * 100)+"%",str(ci[1]*100)+"%",str(ci[2]*100)+"%"],
                  "Low Threshold":[threshold[0][0],threshold[1][0],threshold[2][0]],
                  "High Threshold":[threshold[0][1],threshold[1][1],threshold[2][1]],
                  "Current MA Difference":[current_diff, current_diff, current_diff],
                  "Indication": indication}

        output_data = pd.DataFrame(output)
        st.dataframe(output_data)

        st.success("Happy Investing!")

if __name__ == "__main__":
    main()
