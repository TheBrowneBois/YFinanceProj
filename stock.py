import yfinance as yf

print("Ticker: ", end="")
usr_tkr = input()

this_ticka = yf.Ticker(usr_tkr)
tick_info = this_ticka.info

print(tick_info["longName"])
print("Value:", tick_info["currentPrice"])
print("Avg Volume:", tick_info["averageVolume"])
print("Market Cap:", tick_info["marketCap"])
print("Beta:", tick_info["beta"])
print("Price/Earnings:", tick_info["trailingPE"])
print("Earnings per Share:", tick_info["trailingEps"])
print("Price/Sales:", tick_info["priceToSalesTrailing12Months"])
print("ebidta:", tick_info["ebitda"])
