import yfinance
import csv
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

symbols_file = open("constituents_csv.csv", "r")
symbols = symbols_file.readline().split(",")
symbols = symbols[155:]


f = open("stock_data.txt", "w")
writer = csv.writer(f)

#tickers = ["CNNA", "CKSG", "WRAP", "BBIG", "VPOR", "SVAP", "SPXC", "SOLI", "NWL", "HON", "MLCG", "EFTI", "BORK", "AGTX", "ARCW", "CVR", "CIX", "BOOM", "WIRE", "FRD", "ROCK", "VATE", "MLI", "MATW", "NNBR", "PERT", "SVT", "ROLL", "TLDN", "TKR", "VMI", "AOS", "AVOZ", "APOG", "ARCS", "CPWY", "CNR", "GFF", "TILE", "LGBS", "LGNC", "LYTS", "MAS", "DOOR", "MEGH", "NDDG", "PGTI", "PLPC"]
#print(len(tickers))
#broken = ["3M", "BMMX", ]

for ticker in symbols:
    stock = yfinance.Ticker(ticker)
    print(ticker)
    bs_dict = stock.get_balancesheet(as_dict=True)
    cf_dict = stock.get_cashflow(as_dict=True)
    fin_dict = stock.get_financials(as_dict=True)

    #print(yfinance.download('VXZ'))


    #data = yfinance.download(ticker,start='2019-03-31',end='2019-04-30')
    #close_data = data['Close'].head(1).to_string()
    #close_data = close_data.split()


    balance_sheet_list = ['Total Liab','Total Assets','Cash','Total Current Liabilities','Total Current Assets','Net Tangible Assets']
    cash_flow_list = ['Change In Cash','Total Cash From Operating Activities','Dividends Paid']
    fin_list = ['Research Development','Gross Profit','Total Revenue']
    price_list = ['Current Price','Increase In Price From 1yr','Increase In Price From 2yr','Increase In Price From 3yr','Increase In Price From 4yr','Increase In Price From 5yr']
    dowj_list = ['DOWJ at current', 'DOWJ increase 1yr', 'DOWJ increase 2yr','DOWJ increase 3yr','DOWJ increase 4yr','DOWJ increase 5yr', "y-value"]
    dates = []
    date_format = '%Y-%m-%d'


    key_list = []
    print(bs_dict)
    for key in bs_dict.keys():
        key_list.append(key)
        date = key.date()
        dates.append(date)

    date = dates[0]
    next_day = date + timedelta(days=1)
    new_date1 = date.strftime(date_format)
    new_date2 = next_day.strftime(date_format)
    data = yfinance.download(ticker,start=new_date1,end=new_date2)

    while data.empty:
        next_day += timedelta(days=1)
        new_date2 = next_day.strftime(date_format)
        data = yfinance.download(ticker,start=new_date1,end=new_date2)

    close_data = data['Close'].head(1).to_string()
    close_data = close_data.split()
    y = close_data[2]


    key_list.pop(0)
    dates.pop(0)
    print(dates)


    count = 0
    for key in key_list:
        attributes_dict_1 = bs_dict[key]
        value_list_1 = []
        for key2 in attributes_dict_1.keys():
            if key2 in balance_sheet_list:
                if attributes_dict_1[key2] != None:
                    value_list_1.append(attributes_dict_1[key2])
                else:
                    value_list_1.append(0)

        attributes_dict_2 = cf_dict[key]
        value_list_2 = []
        for key3 in attributes_dict_2.keys():
            if key3 in cash_flow_list:
                if attributes_dict_2[key3] != None:
                    value_list_2.append(attributes_dict_2[key3])
                else:
                    value_list_2.append(0)

        attributes_dict_3 = fin_dict[key]
        value_list_3 = []
        for key4 in attributes_dict_3.keys():
            if key4 in fin_list:
                if attributes_dict_3[key4] != None:
                    value_list_3.append(attributes_dict_3[key4])
                else:
                    value_list_3.append(0)
        
        value_list_4 = []
        value_list_5 = []
        for i in range(6):
            print("*")
            if i == 0:
                date = dates[count]
            next_day = date + timedelta(days=10)
            prev_day = date - timedelta(days=10)
            new_date1 = date.strftime(date_format)
            new_date2 = next_day.strftime(date_format)
            data = yfinance.download(ticker,start=new_date1,end=new_date2)
            dowj_data = yfinance.download('SPY',start=new_date1,end=new_date2)

            while data.empty:
                next_day += timedelta(days=10)
                prev_day -= timedelta(days=10)
                new_date2 = next_day.strftime(date_format)
                data = yfinance.download(ticker,start=new_date1,end=new_date2)
                if data.empty:
                    new_date2 = next_day.strftime(date_format)
                    data = yfinance.download(ticker,start=new_date1,end=new_date2)

            while dowj_data.empty:
                next_day += timedelta(days=10)
                prev_day -= timedelta(days=10)
                new_date2 = next_day.strftime(date_format)
                data = yfinance.download("SPY",start=new_date1,end=new_date2)
                if data.empty:
                    new_date2 = next_day.strftime(date_format)
                    data = yfinance.download("SPY",start=new_date1,end=new_date2)
            
            close_data = data['Close'].head(1).to_string()
            close_data = close_data.split()
            dowj_close_data = dowj_data['Close'].head(1).to_string()
            dowj_close_data = dowj_close_data.split()

            value_list_4.append(close_data[2])
            value_list_5.append(dowj_close_data[2])
            date = date - timedelta(days=365)

        count += 1
        
        final_list = value_list_1 + value_list_2 + value_list_3 + value_list_4 + value_list_5
        final_list.append(y)

        writer.writerow(final_list)
        f.flush()

f.close()