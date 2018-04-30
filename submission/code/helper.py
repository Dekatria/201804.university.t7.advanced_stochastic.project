"""
PURPOSE: provides helper functions that help with the basic functionalities of the simulation
"""

import numpy as np
import random
from copy import deepcopy

def getCus(noCus, cusProb):
	cusDecList = np.random.uniform(size=noCus)
	return len(cusDecList[np.where(cusDecList <= cusProb)])

def updateVisitList(visitList, data):
	newVisitList = deepcopy(visitList)
	nextVisit = min(visitList)
	for i in range(len(visitList)):
		if newVisitList[i] == nextVisit:
			randDet = random.random()
			row = data.iloc[[i]].values.tolist()[0][2:]
			count = 0
			for j in range(len(row)):
				count += row[j]
				if randDet <= count:
					newVisitList[i] += j + 1
					break
	return newVisitList
				
def getCost(qList):
	count = 0
	for i in qList[:-1]:
		if i > 0:
			count += 1
	count += qList[-1]
	return 5 + 0.1*count + 0.1*sum(qList) + 100*sum(qList)**(0.25) 

def getProgress(i, n):
	return "[ %s %% ]" % round(100*i/n, 2)