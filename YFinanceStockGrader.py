from ast import Try
import yfinance as yfn
import csv

nasdaqFile = open("nasdaq-tickers.csv", "r")
nasdaqFileReader = csv.reader(nasdaqFile)
SandP500File = open("spTickers.csv", "r")
SandP500FileReader = csv.reader(SandP500File)
passingGrade = .7
passers = []

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
            exit = False

def ScrapeCVS(fileReader):
    global passers
    passers = list()
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
    try: 
        PE = 80 * clamp((10 / stockInfo["forwardPE"]), 0, 1)
        UnWgtPE = stockInfo["forwardPE"]
    except:
        PE = 0
        UnWgtPE = "None"

    try:
        Eps = 60 * clamp((stockInfo["forwardEps"] / 30), 0, 1)
        UnWgtEps = stockInfo["forwardEps"]
    except:
        Eps = 0
        UnWgtEps = "none"

    try:
        revenueGrowth = 50 * clamp((stockInfo["revenueGrowth"] / .4), 0, 1)
        UnWgtRevenueGrowth = stockInfo["revenueGrowth"]
    except:
        revenueGrowth = 0
        UnWgtRevenueGrowth = "none"

    try:
        operatingMargin = 80 * clamp((stockInfo["operatingMargins"] / .4), 0, 1)
        UnWgtOperatingMargin = stockInfo["operatingMargins"]
    except:
        operatingMargin = 0
        UnWgtOperatingMargin = "none"

    try:
        debtToEquity = 40 * clamp((1 / stockInfo["debtToEquity"]), 0, 1)
        UnWgtDebtToEquity = stockInfo["debtToEquity"]
    except:
        debtToEquity = 0
        UnWgtDebtToEquity = "none"

    try:
        beta = 75 * clamp((1 - abs(1-stockInfo["beta"])), 0, 1)
        UnWgtBeta = stockInfo["beta"]
    except:
        beta = 0
        UnWgtBeta = "none"

    try:
        shortPercentFloat = 70 * clamp((.01 / stockInfo["shortPercentOfFloat"]), 0, 1)
        UnWgtShortPercentFloat = stockInfo["shortPercentOfFloat"]
    except:
        shortPercentFloat = 0
        UnWgtShortPercentFloat = "none"

    try:
        Week52Range = 30 * clamp((.4 / stockInfo["52WeekChange"]), 0, 1)
        UnWgtWeek52Range = stockInfo["52WeekChange"]
    except:
        Week52Range = 0
        UnWgtWeek52Range = "none"

    Grade = (PE + Eps + revenueGrowth + operatingMargin + debtToEquity + beta + shortPercentFloat + Week52Range) / 485
    print(ticker, " : ", round(Grade*100, 1), "%")
    details = "\nPE : " + str(UnWgtPE) + "  Weighting : 80" + "  Weighted PE : " + str(PE) + "\nEps : " + str(UnWgtEps) + "  Weighting : 60" + "  Weighted PE : " + str(Eps) + "\nrevenueGrowth : " + str(UnWgtRevenueGrowth) + "  Weighting : 50" + "  Weighted revenueGrowth : " + str(revenueGrowth) + "\noperatingMargin : " + str(UnWgtOperatingMargin)+ "  Weighting : 80" + "  Weighted operatingMargin : " + str(operatingMargin) + "\ndebtToEquity : " + str(UnWgtDebtToEquity) + "  Weighting : 40" + "  Weighted debtToEquity : " + str(debtToEquity) + "\nbeta : " + str(UnWgtBeta) + "  Weighting : 75" + "  Weighted beta : " + str(beta) + "\nshortPercentFloat : " + str(UnWgtShortPercentFloat) + "  Weighting : 70" + "  Weighted shortPercentFloat : " + str(shortPercentFloat) + "\n52WeekRange : " + str(UnWgtWeek52Range) + "  Weighting : 30" + "  Weighted 52WeekRange : " + str(Week52Range) + "\n"
    if giveDetails:
        print(details)
    elif Grade >= passingGrade:
        Passingtext = ticker + " Passed with Score of " + str(round(Grade*100, 1)) + "%"
        passers.append(Passingtext + "\n" + details)

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n
if __name__ == "__main__":
    main()
