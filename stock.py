import yfinance as yf
import pandas as pd


class stock:
	def __init__(self, name, price, eps, pe, ebitda, revenue, revenueGrowth, operatingMargins, debtToEquity, volume, beta, shortRatio):
		self.name = name
		self.price = price
		self.eps = eps
		self.pe = pe
		self.ebitda = ebitda
		self.revenue = revenue
		self.revenueGrowth = revenueGrowth
		self.operatingMargins = operatingMargins
		self.debtToEquity = debtToEquity
		self.volume = volume
		self.beta = beta
		self.shortRatio = shortRatio

	def toData(self):
		return {self.symbol: [self.name, "${:.2f}".format(self.price), self.eps, self.pe, format(self.ebitda, ".2%"), format(self.revenueGrowth, ".2%"), format(self.operatingMargins, ".2%"), format(self.debtToEquity, ".2%"), self.beta, format(self.volume, ","), format(self.shortRatio, ".2%")]}



#takes yFinance ticker info and if the stock matches credentials, returns a stock object
def filterStock(ticker):
	tick_info = ticker.info

	try:
		name = tick_info["longName"]
	except:
		name = "N/A"

	try:
		price = tick_info["currentPrice"]
	except:
		return None
	if price < 5: 
		return (name, "Price")

	try:
		eps = tick_info["trailingEps"]
	except:
		return None
	if eps < 0: 
		return (name, "Eps")

	try:
		pe = tick_info["trailingPE"]
	except:
		return None
	if pe > 50: 
		return (name, "P/E")

	try:
		ebitda = tick_info["ebitdaMargins"]
	except:
		return None
	if ebitda < 0.15: 
		return (name, "EBITDA Margin")

	try:
		revenue = tick_info["totalRevenue"]
	except:
		return None
	if revenue < 1000000000: 
		return (name, "Revenue")

	try:
		revenueGrowth = tick_info["revenueGrowth"]
	except:
		return None
	if revenueGrowth < -0.2:
		return (name, "Revenue Growth")

	try:
		operatingMargins = tick_info["operatingMargins"]
	except:
		return None
	if operatingMargins < 0.18: 
		return (name, "Operating Margins")

	try:
		debtToEquity = tick_info["debtToEquity"]
	except:
		return None
	if debtToEquity > 100.25: 
		return (name, "Debt/Equity")

	try:
		volume = tick_info["averageVolume"]
	except:
		return None
	if volume < 3000000: 
		return (name, "Avg. Volume")

	try:
		beta = tick_info["beta"]
	except:
		return None
	if beta > 1.35: 
		return (name, "Beta")

	try:
		shortRatio = tick_info["shortPercentOfFloat"]
	except:
		return None
	if shortRatio > 0.1: 
		return (name, "Short % of Float")

	"""try:
		fiftyTwoWeek = tick_info["52WeekChange"]
	except:
		return None
	if fiftyTwoWeek > 0.1: return None"""

	return stock(name, price, eps, pe, ebitda, revenue, revenueGrowth, operatingMargins, debtToEquity, volume, beta, shortRatio)

#reads list of company tickers from a CSV file and turns it into a set
def get_companies(file_name):
	f = open(file_name, "r")
	comps = set()
	for line in f:
		comps.add(line.strip("\n"))
	f.close
	return comps


print("Data to read tickers from: ", end="")
ticker_data = input()
sandp_companies = get_companies(ticker_data)

stock_list = []
inv_ticker = []
inv_name   = []
inv_reason = []

for tickr in sandp_companies:
	tickr_stock = filterStock(yf.Ticker(tickr))

	if tickr_stock is not None:
		if type(tickr_stock) == type(("a", "b")):
			inv_ticker.append(tickr)
			inv_name.append(tickr_stock[0])
			inv_reason.append(tickr_stock[1])
		else:
			tickr_stock.symbol = tickr
			stock_list.append(tickr_stock)

print("Of the", len(sandp_companies), "companies listed, only", len(stock_list), "survived.")
print("Survivors:")

table_data = {}
for stoc in stock_list:
	table_data.update(stoc.toData())

survivors = pd.DataFrame(data=table_data, index=["Name", "Price", "EPS", "P/E", "EBITDA", "Revenue Growth", "Operatin Margins", "Debt/Equity", "Beta", "Avg. Volume", "Short % of Float"])
survivors = survivors.T
survivors.to_csv("survivors.csv", index=False)

print(survivors)

inv_data = {"Symbol": inv_ticker, "Name": inv_name, "Reason": inv_reason}
inv_table = pd.DataFrame(data=inv_data)
inv_table.to_csv("invalid.csv", index=False)
