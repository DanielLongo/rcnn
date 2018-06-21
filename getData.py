import numpy as np
import urllib.parse
import urllib.request
import json
import time
import datetime
import os
import sys
sys.path.append("./messenger.py")
from messenger import message #message and number
import random
import decimal

class GetData(object):
	def __init__(self):
		self.PrivateUrl = "https://poloniex.com/tradingApi" #base url for private API methods
		self.nonce = None
		self.currencyPairs = ["BTC_AMP","BTC_ARDR","BTC_BCN","BTC_BCY","BTC_BELA","BTC_BLK","BTC_BTCD","BTC_BTM","BTC_BTS","BTC_BURST","BTC_CLAM","BTC_DASH","BTC_DCR","BTC_DGB",
			"BTC_DOGE","BTC_EMC2","BTC_ETC","BTC_ETH","BTC_EXP","BTC_FCT","BTC_FLDC","BTC_FLO","BTC_GAME","BTC_GNO","BTC_GNT","BTC_GRC","BTC_HUC","BTC_LBC",
			"BTC_PPC","BTC_RADS","BTC_REP","BTC_RIC","BTC_SBD","BTC_SC","BTC_SJCX","BTC_STEEM","BTC_STR","BTC_STRAT","BTC_SYS","BTC_VIA","BTC_VRC","BTC_VTC",
			"BTC_XBC","BTC_XCP","BTC_XEM","BTC_XMR","BTC_XPM","BTC_XRP","BTC_XVC","BTC_ZEC","ETH_ETC","ETH_GNO","ETH_GNT","ETH_LSK","ETH_REP","ETH_STEEM",
			"ETH_ZEC","USDT_BTC","USDT_DASH","USDT_ETC","USDT_ETH","USDT_LTC","USDT_NXT","USDT_REP","USDT_STR","USDT_XMR","USDT_XRP","USDT_ZEC","XMR_BCN",
			"XMR_BLK","XMR_BTCD","XMR_DASH","XMR_LTC","XMR_MAID","XMR_NXT","XMR_ZEC"]
		self.repeat = False #if it is true: the downloading cycle repeates, it is meant for requests with erros
		self.numberOfRepeats = 0 
		self.maxNumberOfRepeats = 10
		# These items are not really necessary at this point for a public API call

	#PUBLIC METHODS
	def scrape(self,command,info={}):
		PublicMethods = ["returnTicker","returnOrderBook","returnTradeHistory","returnChartData","returnCurrencies","returnLoanOrders"]
		if command not in PublicMethods:
			print("ERROR 1")
			return 
		params = urllib.parse.urlencode(info) #Encode url paramenters to url style from dictionary
		# print("https://poloniex.com/public?command="+command+"&"+params+"")
		try:
			ret = urllib.request.urlopen("https://poloniex.com/public?command="+command+"&"+params+"",timeout=15).read() #Actual request to server here
		except:
			self.repeat = True
			print("ERROR 3")
		ret = ret.decode("utf8")
		return json.loads(ret) #converts to json

	#API COMMANDS

	def returnOrderBook(self,pair,depth): 
		#Returns the order book for a given market, as well as a sequence number for use with the Push API
		# and an indicator specifying whether the market is frozen. You may set currencyPair to "all" to get the order books of all markets 
		return self.scrape("returnOrderBook",info={"currencyPair":pair,"depth":depth})

	def returnTradeHistory(self,pair,start=None,end=None): #start and end are unix timestamps
		info = {}
		if type(start) != type(end):
			print("ERROR 2")
			return
		
		elif start != None and end != None: #if the dates are defined
			info["start"] = start
			info["end"] = end

		info["currencyPair"] = pair
		data = self.scrape("returnTradeHistory",info)
		if len(data) == 50000: #recursively breaks dates down until the range is small enough to fit all trades
			print("WARNING 1")
			diff = end-start
			dates1 = [start,start+int((diff)/2)] #INCLUSIVE INFORMATION
			dates2 = [dates1[1]+1,end]
			return self.returnTradeHistory(pair,start=dates1[0],end=dates1[1]) + self.returnTradeHistory(pair,start=dates2[0],end=dates2[1])
		return data
	#-----------------------------

	def dateUnix(x):
		date = x["date"]	 
		date = time.strptime(date, "%Y-%m-%d %H:%M:%S")
		date = datetime.fromtimestamp(time.mktime(date))
		date = date.timestamp()
		return int(date)


	def downloadTrades(self,path,start): #End is the current day rounded down.
		print(path)
		try:
			files = os.listdir(path)

		except FileNotFoundError:
			print("File Not Found")
			message("File Not Found")
			return "FINISHED downloadTrades"

		end = int(time.time())
		#86400 is the number of seconds in one day
		end -= int(end % 86400) #rounds the time down to start of day
		start -= int(start % 86400)
		dates = [x for x in range(start,end,86400)]
		total = len(self.currencyPairs)*len(dates)
		counter = 1
		dates.pop(0) #becuase start is calculated by subtracting from date
		try:
			for pair in self.currencyPairs:
				for date in dates:
					counter += 1
					# print(counter/total,time.time())
					start = date - 86400
					end  = date
					title = (pair + "_" + str(start) + "-" + str(end))
					if title in files: 
						# print("Already exists")
						continue
					print(counter/total,time.time())
					# print("hello")
					try:
						# time.sleep(random.uniform(.,1.317))
						data = self.returnTradeHistory(pair,start=start,end=end)
					except:
						message("An eror occured fetching data")
					with open(path+title, "w") as file:
						json.dump(data,file)
					# print(title)
		except:
			print("An error occured in downloading trades")
			message("An error occured in downloading trades")
			self.repeat = True

		if self.repeat == True :
			print("Repeating")
			self.numberOfRepeats += 1
			self.repeat = False
			if self.numberOfRepeats > self.maxNumberOfRepeats:
				self.repeat = False
				self.numberOfRepeats = 0
				print("REPEAT HAS FAILED")
				message("REPEAT HAS FAILED")
				return ("FINISHED downloadTrades")

			message("Repeating " + self.getTimestamp())
			self.downloadTrades(path,start)

		return ("FINISHED downloadTrades")


	def getTimestamp(self): #gets an English timestamp (can be understood by a 👤)
		time = datetime.datetime.now()
		timestamp = "day is " + str(time.day) + " hour is " + str(time.hour) + " min is " + str(time.minute)
		# timestamp = str(str(time.day),str(time.hour) + ":" + str(time.minute)).strip("(").strip(")")
		return timestamp



	def downloadAll(self,path,start): #Downloads continueously 
		try:
			while True:
				if int(datetime.datetime.now().hour) == 14: # 2 AM
					note = "Started Downloading " + self.getTimestamp()
					message(note)
					print(note)
					self.downloadTrades(path,start)
					note = "Finished Downloading " + self.getTimestamp()
					message(note)
					print(note)
					time.sleep(76400) #A bit then One day - 1 hour
				time.sleep(3600)

		except:
			print("THE CODE HAS BROKEN " + self.getTimestamp())
			message("THE CODE HAS BROKEN " + self.getTimestamp())
			return 


# GetData().downloadAll("/Volumes/DanielDrive/cryptoData/",start=1483228800)
GetData().downloadTrades("CryptoData/",start=1520985600)
print("Finished")


