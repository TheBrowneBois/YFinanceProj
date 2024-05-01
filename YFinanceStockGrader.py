from ast import Try
import yfinance as yfn
import math
from datetime import datetime
import pandas as pd

passingGrade = 80
passers = [[]]

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

tableData = {}

def main():
    while True:
        menu = input("1 -> Grade A Specific Stock\n2 -> Grade Stocks from a csv file\n3 -> Exit\n")
        if menu == "1":
            ticker = input("Enter the stock ticker: ")
            GradeStock(ticker, True)
        elif menu == "2":
            csvFile = False
            print("The csv file must only contain tickers, one each per line")
            print("if the csv file is in the same folder as this program then use the format, file.csv")
            print("otherwise type the whole path of the file, path/file.csv")
            csvName = input("Enter csv file: ")
            try:
                csvFile = open(csvName, "r")
                global passingGrade
                passingGrade = int(input("Enter the passing grade threshold (0-100): "))
            except:
                print("path does not exist\n\n")
            if csvFile != False:
                ScrapeCVS(csvFile)
        elif menu == "3":
            break
        else:
            print("Invalid input!\n")

def ScrapeCVS(fileReader):
    global passers
    passers = []
    for line in fileReader:
        if line == "":
            continue
        ticker = line.strip("\n")
        GradeStock(ticker, False)
    print("\n")
    for passed in passers:
        print(passed[1], "\n")

    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', None)
    pd.set_option("display.max_rows", None)
    survivors = pd.DataFrame(data=tableData, index=["Ticker", "Grade", "Price", "Price Wgt%", "P/E", "P/E Wgt%", "EPS", "EPS Wgt%", "EBITDA", "EBITDA Wgt%", "Revenue Growth", "Revenue Growth Wgt%", "Revenue", "Revenue Wgt%", "Operating Margins", "Operating Margins Wgt%", "Debt/Equity", "Debt/Equity Wgt%", "PS", "PS Wgt%", "Volume", "Volume Wgt%", "Beta", "Beta Wgt%", "Short % of Float", "Short % of Float Wgt%", "52 Week Change", "52 Week Change Wgt%", "Market Cap", "Market Cap Wgt%"])
    survivors = survivors.T

    if len(passers) <= 0:
        print("No stocks passed the threshold\n")
    else:
        writeYesNo = input("Would you like to write this data to a csv file (yes or no): ")
        if writeYesNo == "yes":
            fileName = str(input("What would you like to name your file?: "))
            survivors.to_csv(fileName)
            print("Data Written to file\n")

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
        Eps = EpsWgt * clamp(math.log(stockInfo["trailingEps"], 25), 0, 1)
        UnWgtEps = stockInfo["forwardEps"]
        EpsPerc = round(Eps/EpsWgt*100, 1)
    except:
        Eps = 0
        UnWgtEps = "None"
        EpsPerc = "None"

    PE = 0
    try: 
        PE = PEWgt * clamp(-math.log(stockInfo["trailingPE"], 10) + 3, 0, 1)
        UnWgtPE = stockInfo["forwardPE"]
        PEPerc = round(PE/PEWgt*100, 1)
    except:
        PE = 0
        UnWgtPE = "None"
        PEPerc = "None"

    ebitda = 0
    try:
        ebitda = ebitdaWgt * clamp(math.log(stockInfo["ebitdaMargins"], .2), 0, 1)
        UnWgtEbitda = stockInfo["ebitdaMargins"]
        ebitdaPerc = round(ebitda/ebitdaWgt*100, 1)
    except:
        ebitda = 0
        UnWgtEbitda = "None"
        ebitdaPerc = "None"

    revenue = 0
    try:
        revenue = revenueWgt * clamp((stockInfo["totalRevenue"] / 3000), 0, 1)
        UnWgtRevenue = stockInfo["totalRevenue"]
        revenuePerc = round(revenue/revenueWgt*100, 1)
    except:
        revenue = 0
        UnWgtRevenue = "None"
        revenuePerc = "None"

    revenueGrowth = 0
    try:
        revenueGrowth = revenueGrowthWgt * clamp(math.log(stockInfo["revenueGrowth"], .25), 0, 1)
        UnWgtRevenueGrowth = stockInfo["revenueGrowth"]
        revenueGrowthPerc = round(revenueGrowth/revenueGrowthWgt*100, 1)
    except:
        revenueGrowth = 0
        UnWgtRevenueGrowth = "None"
        revenueGrowthPerc = "None"

    operatingMargin = 0
    try:
        operatingMargin = operatingMarginWgt * clamp((stockInfo["operatingMargins"] / .3), 0, 1)
        UnWgtOperatingMargin = stockInfo["operatingMargins"]
        operatingMarginPerc = round(operatingMargin/operatingMarginWgt*100, 1)
    except:
        operatingMargin = 0
        UnWgtOperatingMargin = "None"
        operatingMarginPerc = "None"
    
    debtToEquity = 0
    try:
        debtToEquity = debtToEquityWgt * clamp((1 / stockInfo["debtToEquity"]), 0, 1)
        UnWgtDebtToEquity = stockInfo["debtToEquity"]
        debtToEquityPerc = round(debtToEquity/debtToEquityWgt*100, 1)
    except:
        debtToEquity = 0
        UnWgtDebtToEquity = "None"
        debtToEquityPerc = "None"

    PS = 0
    try:
        PS = PSWgt * clamp(math.log(stockInfo["priceToSalesTrailing12Months"], 10), 0, 1)
        UnWgtPS = stockInfo["priceToSalesTrailing12Months"]
        PSPerc = round(PS/PSWgt*100, 1)
    except:
        PS = 0
        UnWgtPS = "None"
        PSPerc = "None"

    volume = 0
    try:
        volume = volumeWgt * clamp((stockInfo["averageVolume"] / 3000), 0, 1)
        UnWgtVolume = stockInfo["averageVolume"]
        volumePerc = round(volume/volumeWgt*100, 1)
    except:
        volume = 0
        UnWgtVolume = "None"
        volumePerc = "None"

    beta = 0
    try:
        beta = betaWgt * clamp((1 - (1-stockInfo["beta"])), 0, 1)
        UnWgtBeta = stockInfo["beta"]
        betaPerc = round(beta/betaWgt*100, 1)
    except:
        beta = 0
        UnWgtBeta = "None"
        betaPerc = "None"

    shortPercentFloat = 0
    try:
        shortPercentFloat = shortPercentFloatWgt * clamp(math.log(stockInfo["shortPercentOfFloat"], .01), 0, 1)
        UnWgtShortPercentFloat = stockInfo["shortPercentOfFloat"]
        shortPercentFloatPerc = round(shortPercentFloat/shortPercentFloatWgt*100, 1)
    except:
        shortPercentFloat = 0
        UnWgtShortPercentFloat = "None"
        shortPercentFloatPerc = "None"

    Week52Range = 0
    try:
        Week52Range = Week52RangeWgt * clamp(-math.log(stockInfo["52WeekChange"], .6)+2, 0, 1)
        UnWgtWeek52Range = stockInfo["52WeekChange"]
        Week52RangePerc = round(Week52Range/Week52RangeWgt*100, 1)
    except:
        Week52Range = 0
        UnWgtWeek52Range = "None"
        Week52RangePerc = "None"

    marketCap = 0
    try:
        marketCap = marketCapWgt * clamp(math.log(stockInfo["marketCap"], 10**9), 0, 1)
        UnWgtMarketCap = stockInfo["marketCap"]
        marketCapPerc = round(marketCap/marketCapWgt*100, 1)
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


    details = "\nStockPrice: " + str(UnWgtStockPrice) + " | Weighting: " + str(stockPriceWgt) + "%" + " | % of Weight : " + str(stockPricePerc) + "%" + """
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
        tableData.update({name: [ticker, str(round(Grade, 1)) + "%", str(UnWgtStockPrice), str(stockPricePerc) + "%", str(UnWgtPE), str(PEPerc) + "%", str(UnWgtEps), str(EpsPerc) + "%", str(UnWgtEbitda), str(ebitdaPerc) + "%", str(UnWgtRevenueGrowth), str(revenueGrowthPerc) + "%", str(UnWgtRevenue), str(revenuePerc) + "%", str(UnWgtOperatingMargin), str(operatingMarginPerc) + "%", str(UnWgtDebtToEquity), str(debtToEquityPerc) + "%", str(UnWgtPS), str(PSPerc) + "%", str(UnWgtVolume), str(volumePerc) + "%", str(UnWgtBeta), str(betaPerc) + "%", str(UnWgtShortPercentFloat), str(shortPercentFloatPerc) + "%", str(UnWgtWeek52Range), str(Week52RangePerc) + "%", str(UnWgtMarketCap), str(marketCapPerc) + "%"]})
        Passingtext = name + " Passed with Score of " + str(round(Grade, 1)) + "%"
        if len(passers) == 0 or Grade <= passers[len(passers)-1][0]:
            passers.append([Grade, Passingtext + " : " + details])
        else:
            for i in range(len(passers), 0, -1):
                if Grade <= passers[i-1][0]:
                    passers.insert(i-1, [Grade, Passingtext + " : " + details])
                    break
            
def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n
if __name__ == "__main__":
    main()
