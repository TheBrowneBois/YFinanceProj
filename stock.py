import yfinance as yf
import pandas as pd


class stock:
	def __init__(self, name, price, eps, pe, ebitda, revenue, revenueGrowth, operatingMargins, debtToEquity, volume, beta, shortRatio, invalid, inv_reason, na_count):
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
		self.invalid = invalid
		if invalid:
			self.inv_reason = inv_reason
		self.na_count = na_count

	def print_reasons(self):
		r_list = ""
		for r in self.inv_reason:
			r_list = r_list + r + ", "
		return r_list

	def toData(self):
		p = self.price
		if type(self.price) is not type("N/A"):
			p = "${:.2f}".format(self.price)

		e = self.ebitda
		if type(self.ebitda) is not type("N/A"):
			e = format(self.ebitda, ".2%")

		rg = self.revenueGrowth
		if type(self.revenueGrowth) is not type("N/A"):
			rg = format(self.revenueGrowth, ".2%")

		om = self.operatingMargins
		if type(self.operatingMargins) is not type("N/A"):
			om = format(self.operatingMargins, ".2%")

		de = self.debtToEquity
		if type(self.debtToEquity) is not type("N/A"):
			de = format(self.debtToEquity, ".2%")

		v = self.volume
		if type(self.volume) is not type("N/A"):
			v = format(self.volume, ",")

		sr = self.shortRatio
		if type(self.shortRatio) is not type("N/A"):
			sr = format(self.shortRatio, ".2%")

		if self.invalid:
			return {self.symbol: [self.name, p, self.eps, self.pe, e, rg, om, de, self.beta, v, sr, self.print_reasons()]}
		else:
			return {self.symbol: [self.name, p, self.eps, self.pe, e, rg, om, de, self.beta, v, sr]}



#takes yFinance ticker info and if the stock matches credentials, returns a stock object
def filterStock(ticker):
	tick_info = ticker.info
	invalid = False
	inv_reason = []
	na_count = 0

	try:
		name = tick_info["longName"]
	except:
		name = "N/A"
		na_count = na_count + 1

	try:
		price = tick_info["currentPrice"]
		if price < 5: 
			invalid = True
			inv_reason.append("Price")
	except:
		price = "N/A"
		na_count = na_count + 1

	try:
		eps = tick_info["trailingEps"]
		if eps < 0: 
			invalid = True
			inv_reason.append("Eps")
	except:
		eps = "N/A"
		na_count = na_count + 1

	try:
		pe = tick_info["trailingPE"]
		if pe > 50: 
			invalid = True
			inv_reason.append("P/E")
	except:
		pe = "N/A"
		na_count = na_count + 1

	try:
		ebitda = tick_info["ebitdaMargins"]
		if ebitda < 0.15: 
			invalid = True
			inv_reason.append("EBITDA Margin")
	except:
		ebitda = "N/A"
		na_count = na_count + 1

	try:
		revenue = tick_info["totalRevenue"]
		if revenue < 1000000000: 
			invalid = True
			inv_reason.append("Revenue")
	except:
		revenue = "N/A"
		na_count = na_count + 1

	try:
		revenueGrowth = tick_info["revenueGrowth"]
		if revenueGrowth < -0.2:
			invalid = True
			inv_reason.append("Revenue Growth")
	except:
		revenueGrowth = "N/A"
		na_count = na_count + 1

	try:
		operatingMargins = tick_info["operatingMargins"]
		if operatingMargins < 0.18: 
			invalid = True
			inv_reason.append("Operating Margins")
	except:
		operatingMargins = "N/A"
		na_count = na_count + 1

	try:
		debtToEquity = tick_info["debtToEquity"]
		if debtToEquity > 100.25: 
			invalid = True
			inv_reason.append("Debt/Equity")
	except:
		debtToEquity = "N/A"
		na_count = na_count + 1

	try:
		volume = tick_info["averageVolume"]
		if volume < 3000000: 
			invalid = True
			inv_reason.append("Avg. Volume")
	except:
		volume = "N/A"
		na_count = na_count + 1

	try:
		beta = tick_info["beta"]
		if beta > 1.35: 
			invalid = True
			inv_reason.append("Beta")
	except:
		beta = "N/A"
		na_count = na_count + 1

	try:
		shortRatio = tick_info["shortPercentOfFloat"]
		if shortRatio > 0.1: 
			invalid = True
			inv_reason.append("Short % of Float")
	except:
		shortRatio = "N/A"
		na_count = na_count + 1

	"""try:
		fiftyTwoWeek = tick_info["52WeekChange"]
	except:
		return None
	if fiftyTwoWeek > 0.1: return None"""

	return stock(name, price, eps, pe, ebitda, revenue, revenueGrowth, operatingMargins, debtToEquity, volume, beta, shortRatio, invalid, inv_reason, na_count)

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
inv_list = []

for tickr in sandp_companies:
	try:
		yft = yf.Ticker(tickr)
	except:
		continue

	tickr_stock = filterStock(yft)

	if tickr_stock.na_count >= 3:
		continue

	tickr_stock.symbol = tickr

	if tickr_stock.invalid:
		inv_list.append(tickr_stock)
	else:
		stock_list.append(tickr_stock)

print("Of the", len(sandp_companies), "companies listed, only", len(stock_list), "survived.")
print("Survivors:")

table_data = {}
for stoc in stock_list:
	table_data.update(stoc.toData())

survivors = pd.DataFrame(data=table_data, index=["Name", "Price", "EPS", "P/E", "EBITDA", "Revenue Growth", "Operatin Margins", "Debt/Equity", "Beta", "Avg. Volume", "Short % of Float"])
survivors = survivors.T
survivors.to_csv("survivors.csv")

print(survivors)

inv_data = {}
for stoc in inv_list:
	inv_data.update(stoc.toData())

inv_table = pd.DataFrame(data=inv_data, index=["Name", "Price", "EPS", "P/E", "EBITDA", "Revenue Growth", "Operatin Margins", "Debt/Equity", "Beta", "Avg. Volume", "Short % of Float", "Invalid Reasons"])
inv_table = inv_table.T
inv_table.to_csv("invalid.csv")
