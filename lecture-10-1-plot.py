import datetime as dt
import random
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_stock_data(tickers, start_date, end_date):
    """
    각 주식별로 정해진 기간에 대해 조정종가를 가져옴
    파라미터:
        팃커 리스트
        기간 시작점
        기간 종료점
    리턴:
        조정종가 DataFrame
    """
    try:
        data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
        return data.dropna(axis=0, how="any")
    except Exception as e:
        print(f"Failed to fetch the data: {e}")
        return None

def calculate_daily_return(prices):
    """매일수익퍼센트"""
    return prices.pct_change()

def generate_random_color():
    """헥사형태로 컬라 무작위로 추출출."""
    return "#" + "".join(random.choices("0123456789ABDE", k=6))

def plot_data(data, title, ylabel, subplots=True):
    """
    Plot stock data or returns.
    
    Parameters:
        data (DataFrame): Data to plot.
        title (str): Title of the plot.
        ylabel (str): Y-axis label.
        subplots (bool): Whether to plot in subplots or a single plot.
    """
    plt.style.use("Solarize_Light2")

    num_plots = len(data.columns)
    
    # Automatically disable subplots if only one column exists
    if num_plots == 1:
        subplots = False

    if subplots:
        fig, axes = plt.subplots(nrows=num_plots, ncols=1, figsize=(16, 4 * num_plots))
        for i, column in enumerate(data.columns):
            color = generate_random_color()
            axes[i].plot(data.index, data[column], label=column, color=color)
            axes[i].set_title(f'{title} - {column}')
            axes[i].set_ylabel(ylabel)
            axes[i].legend(loc="upper left")
        fig.subplots_adjust(hspace=0.8)
        fig.tight_layout()
    else:
        plt.figure(figsize=(12, 8))
        for column in data.columns:
            plt.plot(data.index, data[column], label=column)
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True) 

def plot_cumulative_return(daily_returns):
    """Plot cumulative returns on a single plot."""
    cumulative_return = (1 + daily_returns).cumprod()
    plot_data(cumulative_return, title="Cumulative Returns", ylabel="Cumulative Return", subplots=False)

def main(tickers, start, end):
    """
    Main function to fetch data, calculate returns, and generate plots.
    
    Parameters:
        tickers (list): List of stock tickers.
        start (datetime): Start date.
        end (datetime): End date.
    """
    cl_price = fetch_stock_data(tickers, start, end)
    if cl_price is not None:
        daily_return = calculate_daily_return(cl_price)
        plot_data(cl_price, title="Stock Price Evolution", ylabel="Price")
        plot_data(daily_return, title="Stock Daily Returns", ylabel="Daily Return")
        plot_cumulative_return(daily_return)

if __name__ == "__main__":
    tickers = ['CRWD', 'LDOS', 'CW', 'PLTR', 'PANW', 'FTNT']
    # tickers = ['CRWD','PANW', 'FTNT']
    # tickers=['MSFT', 'AMZN']
    # tickers = ['MSFT']
    start = dt.datetime.today() - dt.timedelta(days=365)
    end = dt.datetime.today()
    main(tickers, start, end)
