from ast import Try
import yfinance as yfn
import csv
import math

nasdaqFile = open("nasdaq-tickers.csv", "r")
nasdaqFileReader = csv.reader(nasdaqFile)
SandP500File = open("spTickers.csv", "r")
SandP500FileReader = csv.reader(SandP500File)
passingGrade = 70
passers = []
for key, value in yfn.Ticker("MSFT").info.items():
   print(str(key) + " : " + str(value))

stockPriceWgt = 2
EpsWgt = 10
PEWgt = 8
ebitdaWgt = 7
revenueWgt = 8
revenueGrowthWgt = 7
operatingMarginWgt = 8
debtToEquityWgt = 6
PSWgt = 6
volumeWgt = 10
betaWgt = 8
shortPercentFloatWgt = 7
Week52RangeWgt = 3
marketCapWgt = 10

def main():
    exit = False
    while exit == False:
        menu = input("Grade A Specific Stock (1)\nGrade Stocks from nasdaq cvs file (2)\nGrade Stocks from S&P 500 cvs file (3)\nExit (4)\n")
        if menu == "1":
            ticker = input("Enter the stock ticker\n\n")
            GradeStock(ticker, True)
        if menu == "2":
            ScrapeCVS(nasdaqFileReader)
        if menu == "3":
            ScrapeCVS(SandP500FileReader)
        if menu == "4":
            exit = True

def ScrapeCVS(fileReader):
    global passers
    passers = []
    firstValue = True
    for line in fileReader:
        if firstValue:
            ticker = line[0][3:].strip("\n")
            firstValue = False
        else:
            ticker = line[0].strip("\n")
        GradeStock(ticker, False)
    print("\n")
    for passed in passers:
        print(passed, "\n")
def GradeStock(ticker, giveDetails):
    stockInfo = yfn.Ticker(ticker).info

    stockPrice = 0
    try:
        if stockInfo["currentPrice"] > 5:
            stockPrice = stockPriceWgt
        UnWgtStockPrice = stockInfo["currentPrice"]
        stockPricePerc = 100
    except:
        stockPrice = 0
        UnWgtStockPrice = "None"
        stockPricePerc = "None"
    Eps = 0
    try:
        Eps = EpsWgt * clamp(math.log(stockInfo["forwardEps"], 25), 0, 1)
        UnWgtEps = stockInfo["forwardEps"]
        EpsPerc = Eps/EpsWgt*100
    except:
        Eps = 0
        UnWgtEps = "None"
        EpsPerc = "None"

    PE = 0
    try: 
        PE = PEWgt * clamp(-math.log(stockInfo["PE"], 10) + 3, 0, 1)
        UnWgtPE = stockInfo["forwardPE"]
        PEPerc = PE/PEWgt*100
    except:
        PE = 0
        UnWgtPE = "None"
        PEPerc = "None"

    ebitda = 0
    try:
        ebitda = ebitdaWgt * clamp(math.log(stockInfo["ebitdaMargins"], .2), 0, 1)
        UnWgtEbitda = stockInfo["ebitdaMargins"]
        ebitdaPerc = ebitda/ebitdaWgt*100
    except:
        ebitda = 0
        UnWgtEbitda = "None"
        ebitdaPerc = "None"

    revenue = 0
    try:
        revenue = revenueWgt * clamp((stockInfo["totalRevenue"] / 3000), 0, 1)
        UnWgtRevenue = stockInfo["totalRevenue"]
        revenuePerc = revenue/revenueWgt *100
    except:
        revenue = 0
        UnWgtRevenue = "None"
        revenuePerc = "None"

    revenueGrowth = 0
    try:
        revenueGrowth = revenueGrowthWgt * clamp(math.log(stockInfo["revenueGrowth"], .25), 0, 1)
        UnWgtRevenueGrowth = stockInfo["revenueGrowth"]
        revenueGrowthPerc = revenueGrowth/revenueGrowthWgt*100
    except:
        revenueGrowth = 0
        UnWgtRevenueGrowth = "None"
        revenueGrowthPerc = "None"

    operatingMargin = 0
    try:
        operatingMargin = operatingMarginWgt * clamp((stockInfo["operatingMargins"] / .3), 0, 1)
        UnWgtOperatingMargin = stockInfo["operatingMargins"]
        operatingMarginPerc = operatingMargin/operatingMarginWgt*100
    except:
        operatingMargin = 0
        UnWgtOperatingMargin = "None"
        operatingMarginPerc = "None"
    
    debtToEquity = 0
    try:
        debtToEquity = debtToEquityWgt * clamp((1 / stockInfo["debtToEquity"]), 0, 1)
        UnWgtDebtToEquity = stockInfo["debtToEquity"]
        debtToEquityPerc = debtToEquity/debtToEquityWgt*100
    except:
        debtToEquity = 0
        UnWgtDebtToEquity = "None"
        debtToEquityPerc = "None"

    PS = 0
    try:
        PS = PSWgt * clamp(math.log(stockInfo["priceToSalesTrailing12Months"], 10), 0, 1)
        UnWgtPS = stockInfo["priceToSalesTrailing12Months"]
        PSPerc = PS/PSWgt*100
    except:
        PS = 0
        UnWgtPS = "None"
        PSPerc = "None"

    volume = 0
    try:
        volume = volumeWgt * clamp((stockInfo["averageVolume"] / 3000), 0, 1)
        UnWgtVolume = stockInfo["averageVolume"]
        volumePerc = volume/volumeWgt*100
    except:
        volume = 0
        UnWgtVolume = "None"
        volumePerc = "None"

    beta = 0
    try:
        beta = betaWgt * clamp((1 - (1-stockInfo["beta"])), 0, 1)
        UnWgtBeta = stockInfo["beta"]
        betaPerc = beta/betaWgt*100
    except:
        beta = 0
        UnWgtBeta = "None"
        betaPerc = "None"

    shortPercentFloat = 0
    try:
        shortPercentFloat = shortPercentFloatWgt * clamp(math.log(stockInfo["shortPercentOfFloat"], .01), 0, 1)
        UnWgtShortPercentFloat = stockInfo["shortPercentOfFloat"]
        shortPercentFloatPerc = shortPercentFloat/shortPercentFloatWgt*100
    except:
        shortPercentFloat = 0
        UnWgtShortPercentFloat = "None"
        shortPercentFloatPerc = "None"

    Week52Range = 0
    try:
        Week52Range = Week52RangeWgt * clamp(math.log(stockInfo["52WeekChange"], .6), 0, 1)
        UnWgtWeek52Range = stockInfo["52WeekChange"]
        Week52RangePerc = Week52Range/Week52RangeWgt*100
    except:
        Week52Range = 0
        UnWgtWeek52Range = "None"
        Week52RangePerc = "None"

    marketCap = 0
    try:
        marketCap = marketCapWgt * clamp(math.log((stockInfo["sharesOutstanding"]*stockInfo["currentPrice"]), 10**9, 0, 1))
        UnWgtMarketCap = stockInfo["sharesOutstanding"]*stockInfo["currentPrice"]
        marketCapPerc = marketCap/marketCapWgt*100
    except:
        marketCap = 0
        UnWgtMarketCap = "None"
        marketCapPerc = "None"

    name = ""
    try:
        name = stockInfo["shortName"]
    except:
        name = ticker
    Grade = (stockPrice + PE + Eps + revenueGrowth + operatingMargin + debtToEquity + beta
            + ebitda + PS + revenue + volume + shortPercentFloat + Week52Range + marketCap)
    print(name, " : ", round(Grade, 1), "%")

    details = "\n\nStockPrice: " + str(UnWgtStockPrice) + " | Weighting: " + str(stockPriceWgt) + "%" + " | % of Weight : " + str(stockPricePerc) + "%" + """
"""  + "PE: " + str(UnWgtPE) + " | Weighting: " + str(PEWgt) + "%" + " | % of Weight : " + str(PEPerc) + "%" + """
"""  + "Eps: " + str(UnWgtEps) + " | Weighting: " + str(EpsWgt) + "%" + " | % of Weight : " + str(EpsPerc) + "%" +  """
"""  + "EBITDA: " + str(UnWgtEbitda) + " | Weighting: " + str(ebitdaWgt) + "%" + " | % of Weight : " + str(ebitdaPerc) + "%" +  """
"""  + "revenue growth: " + str(UnWgtRevenueGrowth) + " | Weighting:  " + str(revenueGrowthWgt) + "%" + " | % of Weight : " + str(revenueGrowthPerc) + "%" +  """
"""  + "revenue: " + str(UnWgtRevenue) + " | Weighting: " + str(revenueWgt) + "%" + " | % of Weight : " + str(revenuePerc) + "%" +  """
"""  + "operating margin: " + str(UnWgtOperatingMargin)+ " | Weighting: " + str(operatingMarginWgt) + "%" + " | % of Weight : " + str(operatingMarginPerc) + "%" +  """
"""  + "debt to equity: " + str(UnWgtDebtToEquity) + " | Weighting: " + str(debtToEquityWgt) + "%" + " | % of Weight : " + str(debtToEquityPerc) + "%" +  """
"""  + "P/S: " + str(UnWgtPS) + " | Weighting: " + str(PSWgt) + "%" + " | % of Weight : " + str(PSPerc) + "%" +  """
"""  + "volume: " + str(UnWgtVolume) + " | Weighting: " + str(volumeWgt) + "%" + " | % of Weight : " + str(volumePerc) + "%" +  """
"""  + "beta: " + str(UnWgtBeta) + " | Weighting: " + str(betaWgt) + "%" + " | % of Weight : " + str(betaPerc) + "%" +  """
"""  + "short percent float: " + str(UnWgtShortPercentFloat) + " | Weighting: " + str(shortPercentFloatWgt) + "%" + " | % of Weight : " + str(shortPercentFloatPerc) + "%" +  """
"""  + "52WeekRange: " + str(UnWgtWeek52Range) + " | Weighting: " + str(Week52RangeWgt) + "%" + " | % of Weight : " + str(Week52RangePerc)  + "%" +  """
"""  + "Market Cap: " + str(UnWgtMarketCap) + " | Weighting: " + str(marketCapWgt) + "%" + " | % of Weight : " + str(marketCapPerc) + "%" +  "\n"

    if giveDetails:
        print(details)
    elif Grade >= passingGrade:
        Passingtext = name + " Passed with Score of " + str(round(Grade, 1)) + "%"
        passers.append(Passingtext + " : " + details)
def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n
if __name__ == "__main__":
    main()
