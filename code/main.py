"""
PURPOSE: Generates simulation based on project guidelines
"""

import pandas as pd
import random
import sys
import helper
import time
import os

def main(length, storeFile, noCus=160, cusProb=0.25):
	print("########## SIMULATION BEGIN ##########")
	data = pd.read_csv(storeFile)
	lotList = data["Lot"].tolist()
	visitList = helper.updateVisitList([0 for i in range(data.shape[0])], data)
	nextVisit = min(visitList)
	if not os.path.exists("data/simulation/"):
		os.makedirs("data/simulation/")
	with open("data/simulation/%s.csv" % int(round(time.time(), 0)), "a") as output:
		output.write("week, cumTotOrders, cumCusOrders, cumStoreOrders, cumCost, curTotOrders, curCusOrders, curStoreOrders, curCost, currentCount\n")
		cumTotOrders = 0
		cumCusOrders = 0
		cumStoreOrders = 0
		cumCost = 0
		for i in range(int(length)):
			curCusOrders = helper.getCus(noCus, cusProb)
			curStoreOrders = 0
			if (i+1) == nextVisit:
				qList = []
				for j in range(len(visitList)):
					if visitList[j] == nextVisit:
						curStoreOrders += lotList[j]
						qList.append(lotList[j])
					else:
						qList.append(0)
				visitList = helper.updateVisitList(visitList, data)
				nextVisit = min(visitList)
				qList.append(curCusOrders)
			else:
				qList = [0 for row in visitList]
				qList.append(curCusOrders)
			curTotOrders = curCusOrders + curStoreOrders
			curCost = helper.getCost(qList)

			cumTotOrders += curTotOrders
			cumCusOrders += curCusOrders
			cumStoreOrders += curStoreOrders
			cumCost += curCost
			count = 0
			for k in qList[:-1]:
				if k > 0:
					count += 1
			count += qList[-1]
			output.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (i+1, cumTotOrders, cumCusOrders, cumStoreOrders, cumCost, curTotOrders, curCusOrders, curStoreOrders, curCost,count))
			print("%s WEEK %s : %s" % (helper.getProgress(i+1, int(length)), i+1, curTotOrders))

	print("########## SIMULATION END ##########")

if __name__ == "__main__":
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
	elif len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		for i in range(len(sys.argv)):
			print(sys.argv[i])
		raise IndexError("Invalid number of parameters")

# python code/main.py 1000000 config/config_file.1.csv