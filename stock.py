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
		return {self.name: ["${}".format(self.price), self.eps, self.pe, format(self.ebitda, ".2%"), format(self.revenueGrowth, ".2%"), format(self.operatingMargins, ".2%"), self.beta, format(self.volume, ",")]}



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
		#print("invalid price for", name)
		return None

	try:
		eps = tick_info["trailingEps"]
	except:
		return None
	if eps < 0: 
		#print("invalid eps for", name)
		return None

	try:
		pe = tick_info["trailingPE"]
	except:
		return None
	if pe > 50: 
		#print("invalid p/e for", name)
		return None

	try:
		ebitda = tick_info["ebitdaMargins"]
	except:
		return None
	if ebitda < 0.15: 
		#print("invalid ebitda for", name)
		return None

	try:
		revenue = tick_info["totalRevenue"]
	except:
		return None
	if revenue < 1000000000: 
		#print("invalid revenue for", name)
		return None

	try:
		revenueGrowth = tick_info["revenueGrowth"]
	except:
		return None
	if revenueGrowth < -0.2:
		#print("invalid revenue growth for", name)
		return None

	try:
		operatingMargins = tick_info["operatingMargins"]
	except:
		return None
	if operatingMargins < 0.18: 
		#print("invalid operating margins for", name)
		return None

	try:
		debtToEquity = tick_info["debtToEquity"]
	except:
		return None
	if debtToEquity > 100.25: 
		#print("invalid debt/equity for", name)
		return None

	try:
		volume = tick_info["averageVolume"]
	except:
		return None
	if volume < 3000000: 
		#print("invalid volume for", name)
		return None

	try:
		beta = tick_info["beta"]
	except:
		return None
	if beta > 1.35: 
		#print("invalid beta for", name)
		return None

	try:
		shortRatio = tick_info["shortPercentOfFloat"]
	except:
		return None
	if shortRatio > 0.1: 
		#print("invalid short ratio for", name)
		return None

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


sandp_companies = get_companies("data/spTickers.csv")

stock_list = []

for tickr in sandp_companies:
	tickr_stock = filterStock(yf.Ticker(tickr))

	if tickr_stock is not None:
		stock_list.append(tickr_stock)

print("Of the", len(sandp_companies), "companies listed, only", len(stock_list), "survived.")
print("Survivors:")

table_data = {}
for stoc in stock_list:
	table_data.update(stoc.toData())

survivors = pd.DataFrame(data=table_data, index=["Price", "EPS", "P/E", "EBITDA", "Revenue Growth", "Operatin Margins", "Beta", "Avg. Volume"])
survivors = survivors.T

print(survivors)
