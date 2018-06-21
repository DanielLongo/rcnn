import datetime
from datetime import datetime
import os
import json
import time
import numpy as np
import pandas as pd 
import numpy as np
import sys

class ReadData(object):
	def __init__(self, start, end, time):
		self.path = "/Users/DanielLongo 1/Desktop/CryptoRnn/cryptoData/"
		self.currencyPairs = ["BTC_AMP","BTC_ARDR","BTC_BCN","BTC_BCY","BTC_BELA","BTC_BLK","BTC_BTCD","BTC_BTM","BTC_BTS","BTC_BURST","BTC_CLAM","BTC_DASH","BTC_DCR","BTC_DGB",
			"BTC_DOGE","BTC_EMC2","BTC_ETC","BTC_ETH","BTC_EXP","BTC_FCT","BTC_FLDC","BTC_FLO","BTC_GAME","BTC_GNO","BTC_GNT","BTC_GRC","BTC_HUC","BTC_LBC",
			"BTC_LSK","BTC_LTC","BTC_MAID","BTC_NAV","BTC_NEOS","BTC_NMC","BTC_NXC","BTC_NXT","BTC_OMNI","BTC_PASC","BTC_PINK","BTC_POT",
			"BTC_PPC","BTC_RADS","BTC_REP","BTC_RIC","BTC_SBD","BTC_SC","BTC_STEEM","BTC_STR","BTC_STRAT","BTC_SYS","BTC_VIA","BTC_VRC","BTC_VTC",
			"BTC_XBC","BTC_XCP","BTC_XEM","BTC_XMR","BTC_XPM","BTC_XRP","BTC_XVC","BTC_ZEC","ETH_ETC","ETH_GNO","ETH_GNT","ETH_LSK","ETH_REP","ETH_STEEM",
			"ETH_ZEC","USDT_BTC","USDT_DASH","USDT_ETC","USDT_ETH","USDT_LTC","USDT_NXT","USDT_REP","USDT_STR","USDT_XMR","USDT_XRP","USDT_ZEC","XMR_BCN",
			"XMR_BLK","XMR_BTCD","XMR_DASH","XMR_LTC","XMR_MAID","XMR_NXT","XMR_ZEC"]
		self.start = start
		self.end = end
		self.time = time

	def dateUnix(self,x):
		date = x["date"]
		date = time.strptime(date, "%Y-%m-%d %H:%M:%S")
		date = datetime.fromtimestamp(time.mktime(date))
		date = date.timestamp()
		return int(date)

	def fetchJson(self, pair):
		final = []

		#makes files inlcusive of data 
		start_file = self.start
		if self.start % 86400 != 0:
			print("Start is not exact to a day")
			start_file = (self.start - (self.start % 86400))
			print("start_file", end_file)

		end_file = self.end
		if  self.end % 86400 != 0:
			print("End is not exact to a day")
			end_file = (self.end + (86400 - (self.end % 86400)))
			print("end_file", end_file)

		dates = [x for x in range(start_file , end_file, 86400)]

		for date in dates:
			start = date
			end = date + 86400
			fileName = self.path + pair + "_" + str(start) + "-" + str(end)
			try:
				final += json.load(open(fileName))
			except FileNotFoundError:
				print("invalid path", fileName)
			except json.decoder.JSONDecodeError:
				print("Json decoder error", fileName)
		return final

	def read_to_array(self, x):
		final = []
		for trade in x:
			#makes timestamp smaller so not overly weighted
			cur_timestamp = self.dateUnix(trade) / 99999999
			
			cur_type = trade["type"]
			if cur_type == "sell":
				cur_type = 0
			else:
				cur_type = 1

			cur_rate = float(trade["rate"])
			cur_amount = float(trade["amount"])
			final += [[cur_timestamp, cur_type, cur_rate, cur_amount]]
		return final

	def read_data(self):
		final = []
		for pair in self.currencyPairs:
			print("Pair", pair)
			json = self.fetchJson(pair)
			array = self.read_to_array(json)
			print("array", np.shape(array))
			final += [array]

		return final


x = ReadData(1520121600, 
	1520294400, 10)

z = x.read_data()
print(np.shape(z))


