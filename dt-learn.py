import math
import copy
import sys
import random

candidateSplits = [[]]
predictedValue = []
actualValue = []
correctCount = 0
wrongCount = 0
serialNumber=0
accuracyList=[]
def main() :
	trainingSet = sys.argv[1]
	testingSet = sys.argv[2]
	m = int(sys.argv[3])
	"""trainingSet = "diabetes_train.arff"
	testingSet = "diabetes_test.arff"
	m = 2"""
	arrfFile = open(trainingSet)
	lines = [line.rstrip('\n') for line in arrfFile]
	data = [[]]
	attributeList=[]
	index = 0
	for line in lines :
		if(line.startswith('@attribute')) :
			attributeLine = line
			attributeLineSplit = attributeLine.split(' ',2)
			if "{" not in attributeLineSplit[2] :
				attr = Attribute()
				attr.setName(attributeLineSplit[1].replace('\'',''))
				attr.setType("real")
				attr.setIndex(index)
				attributeList.append(attr)
			else : 
				attr = Attribute()
				attr.setName(attributeLineSplit[1].replace('\'',''))
				attr.setType("nominal")
				attr.setIndex(index)
				attributeValueList = attributeLineSplit[2].replace('{',"")
				attributeValueList = attributeValueList.replace('}',"")
				attributeValues = [x.strip(" ") for x in attributeValueList.split(",")]
				attr.setValues(attributeValues)
				attributeList.append(attr)
			index+=1
		elif(not line.startswith('@data') and not line.startswith('@relation')) :
			data.append(line.split(','))
	del data[0]
	"""randomSelectionOfTrainingSet(data, int(len(data)), attributeList)
	print accuracyList
	print "Maximum accuracy : "+ str(max(accuracyList))
	sum = 0.0
	for a in accuracyList :
		sum+=a
	average = sum/len(accuracyList)
	print "Average accuracy : "+ str(average)
	print "Minimum accuracy : "+ str(min(accuracyList))"""
	Tree = Node()
	Tree = makeTree(data,attributeList,m,0,str(findMajority(data, attributeList)))
	sys.stdout.write("\n<Predictions for the Test Set Instances>\n")
	testDataFile = open(testingSet)
	testlines = [testline.rstrip('\n') for testline in testDataFile]
	testData = [[]]
	index = 0
	for line in testlines :
		if(not line.startswith('@data') and not line.startswith('@relation') and not line.startswith('@attribute')) :
			testData.append(line.split(','))
	for row in testData : 
		if(len(row)==0):
			continue
		testTheTree(row, Tree, attributeList)
	print "Number of correctly classified: "+str(correctCount)+"  Total number of test instances: "+str(wrongCount+correctCount)

def testTheTree(row, Tree, attributeList):
	count = 0
	global predictedValue
	global actualValue
	global correctCount
	global wrongCount
	global serialNumber
	for attr in attributeList:
		if(attr.getName()==Tree.getName()):
			break
		count+=1
	if(Tree.getType()=="nominal"):
		i=0
		for split in Tree.getSplitConditionNominal():
			if(row[count]==split):
				testTheTree(row,Tree.children[i], attributeList)
				break
			i+=1
	elif(Tree.getType()=="leaf"):
		name = Tree.getName()
		if(name==row[-1]):
			correctCount+=1
		else : 
			wrongCount+=1
		serialNumber+=1
		print("%3d: Actual: "%(serialNumber)+str(row[-1])+"  Predicted: "+str(name))
		predictedValue.append(name)
		actualValue.append(row[-1])		
	else:
		if(float(row[count])<=float(Tree.getSplitConditionNumeric())):
			testTheTree(row,Tree.children[0],attributeList)
		else : 
			testTheTree(row,Tree.children[1],attributeList)

class Attribute:
	Name = ""
	Type = ""
	Values = []
	candidateSplits = []
	bestSplit = []
	index = 0
	
	def __init__(self):
		self.setValues([])
		self.setType("")
		self.setName("")
	def __str__(self):
		return str(self.Name)
	def setName(self, val):
		self.Name = val
	def setType(self, val):
		self.Type = val
	def setIndex(self, val):
		self.Index = val
	def setCandidateSplits(self, val):
		self.candidateSplits = val
	def setBestSplit(self, val):
		self.bestSplit = val
	def setValues(self,values):
		self.Values = values
	def getName(self):
		return str(self.Name)
	def getType(self):
		return str(self.Type)
	def getIndex(self):
		return str(self.Index)
	def getValues(self):
		return self.Values
	def getCandidateSplits(self):
		return self.candidateSplits
	def getBestSplit(self):
		return self.bestSplit

class Node:
	Name = ""
	Type = ""
	splitConditionNominal = []
	splitConditionNumeric = []
	children = []
	def __init__(self):
		self.setType("")
		self.setName("")
	def __str__(self):
		return str(self.Name)
	def setName(self, val):
		self.Name = val	
	def setType(self, val):
		self.Type = val
	def setSplitConditionNominal(self, val):
		self.splitConditionNominal = val
	def setSplitConditionNumeric(self,values):
		self.splitConditionNumeric = values
	def getName(self):
		return str(self.Name)
	def getType(self):
		return str(self.Type)
	def getSplitConditionNominal(self):
		return self.splitConditionNominal
	def getSplitConditionNumeric(self):
		return self.splitConditionNumeric
	def getChildren(self):
		return self.children

def findMajority (data, attributeList):
	map=[[]]
	class2=""
	if(len(attributeList[len(attributeList)-1].getCandidateSplits())!=0):
		class1 = attributeList[len(attributeList)-1].getCandidateSplits()[0]
		class2 = attributeList[len(attributeList)-1].getCandidateSplits()[1]
	else :
		class1 = data[0][-1]
		for row in data :
			if(row[-1] not in class1):
				class2 = row[-1]
				break
				
	map.append([class1, 0])
	map.append([class2, 0])
	del map[0]
	for row in data :
		if(row[len(row)-1]==class1):
			map[0][1]+=1
		else :
			map[1][1]+=1
	if(map[0][1]>=map[1][1]):
		return map[0][0]
	else :
		return map[1][0]

def makeTree(data, attributeList,m, recursionDepth, parentPlurality) :
	determineCandidateSplits(data,attributeList)
	classification = []
	classification2 = findClassification(data, attributeList)
	childs =[]
	if(len(data)==0):
		sys.stdout.write( ": "+attributeList[-1].candidateSplits[0])
		leaf = Node()
		leaf.setName(attributeList[-1].candidateSplits[0])
		leaf.setType("leaf")
		return leaf
	if(abs(int(classification2[0]+int(classification2[1])))<m):
		majority = str(findMajority(data, attributeList))
		sys.stdout.write( ": "+ majority)
		leaf = Node()
		leaf.setName(majority)
		leaf.setType("leaf")
		return leaf
	for row in data:
		if len(row)!= 0 :
			classification.append(row[-1])
	if(all_same(classification)):
		leaf = Node()
		leaf.setName(classification[0])
		leaf.setType("leaf")
		sys.stdout.write( ": "+str(findMajority(data, attributeList)))
		return leaf
	else :
		bestAttr = findBestSplit(data, attributeList)
		if(bestAttr == -1):
			m = str(findMajority(data, attributeList))
			sys.stdout.write(": "+m)
			leaf = Node()
			leaf.setName(m)
			leaf.setType("leaf")
			return leaf
		root = Node()
		root.setName(bestAttr.getName())
		root.setType(bestAttr.getType())
		if(bestAttr.getType()=="nominal"):
			root.setSplitConditionNominal(bestAttr.getCandidateSplits())
			for split in bestAttr.getCandidateSplits() :
				subsetData = subSet(data, bestAttr, split, attributeList, "nominal", "nominal")
				classification = findClassification(subsetData, attributeList)
				space = 0
				print "\n",
				while(space<recursionDepth):
					print "|      ",
					space+=1
				sys.stdout.write(" "+root.getName() + " = " + split)
				sys.stdout.write( " [")
				print str(classification[0])+" ",
				sys.stdout.write(str(classification[1]))
				sys.stdout.write("]")
				tempAttrList = copy.deepcopy(attributeList)
				child = Node()
				child = copy.deepcopy(makeTree(subsetData, tempAttrList,m,recursionDepth+1, str(findMajority(data, attributeList))))
				childs.append(child)
			recursionDepth+=1
		else :
			bestSplit = bestAttr.getBestSplit()
			root.setSplitConditionNumeric(bestSplit)
			subsetData1 = subSet(data,bestAttr, bestSplit, attributeList, "real","less than")
			classification = findClassification(subsetData1, attributeList)
			space = 0
			print "\n",
			while(space<recursionDepth):
				print "|      ",
				space+=1
			print root.getName(),
			sys.stdout.write(" <= %0.6f " %bestSplit)
			sys.stdout.write( "[")
			print str(classification[0])+" ",
			sys.stdout.write(str(classification[1]))
			sys.stdout.write("]")
			subsetData2 = subSet(data, bestAttr, bestSplit, attributeList, "real", "greater")
			classification = findClassification(subsetData2, attributeList)
			tempAttrList = copy.deepcopy(attributeList)
			z = 0
			for a in tempAttrList :
				if(a.getName()==bestAttr.getName()):
					tempAttrList[z].getCandidateSplits().remove(bestSplit)
				z+=1		
			temprecursionDepth=recursionDepth+1
			child1 = Node()
			child1 = copy.deepcopy(makeTree(subsetData1, tempAttrList,m,temprecursionDepth, str(findMajority(data, attributeList))))
			childs.append(child1)
			space = 0
			print "\n",
			while(space<recursionDepth):
				print "|      ",
				space+=1
			print root.getName(),
			sys.stdout.write(" > %0.6f " %bestSplit)
			sys.stdout.write( "[")
			print str(classification[0])+" ",
			sys.stdout.write(str(classification[1]))
			sys.stdout.write("]")
			child2 = Node()
			child2 = copy.deepcopy(makeTree(subsetData2, tempAttrList,m,temprecursionDepth, str(findMajority(data, attributeList))))
			childs.append(child2)
		root.children = childs
		return root

def findBestSplit(data, attributeList) :
	index = 0
	infoGainList = []
	for attr in attributeList :
		if(attr.getType()=="nominal" and "class" not in attr.getName()):
			infoGain = informationGain(data, attr, attr.getCandidateSplits(), attributeList, "nominal")
			infoGainList.append(infoGain)
		elif ("class" not in attr.getName() and len(attr.getCandidateSplits())!=0) :
			informationGainList = informationGain(data, attr, attr.getCandidateSplits(), attributeList, "real")
			if(len(informationGainList)==0):
				attr.setBestSplit("")
				infoGainList.append(-1)
			else :
				attr.setBestSplit(attr.getCandidateSplits()[informationGainList.index(max(informationGainList))])
				infoGainList.append(max(informationGainList))
		elif("class" not in attr.getName() and len(attr.getCandidateSplits())==0):
			attr.setBestSplit("")
			infoGainList.append(0)
		index+=1
	if(float(max(infoGainList)) == 0):
		return -1
	maxIG = max(infoGainList)
	if(maxIG==-1):
		return -1
	i = 0
	for ig in infoGainList:
		if(maxIG==ig):
			break;
		i+=1
	return attributeList[i]
	
	
def subSet(data, attribute, attributeValue, attributeList, Type, comparator):
	subset = [[]]
	index = 0
	for attr in attributeList:
		if(attr.getName()==str(attribute)):
			index = int(attr.getIndex())
			break;
	if Type=="nominal":
		for row in data :
			if(row[index]==attributeValue):
				subset.append(row)
	else :
		if("less than" in comparator):
			for row in data:
				if(float(row[index])<=float(attributeValue)):
					subset.append(row)
		else :
			for row in data : 
				if(float(row[index])>float(attributeValue)):
					subset.append(row)
	countEntry=0
	for entry in subset :
		if(len(entry)==0):
			del(subset[countEntry])
		countEntry+=1
	return subset

def informationGain(data, attribute, candidateSplits, attributeList, Type):
	classificationData = findClassification(data,attributeList)
	entropyData = 0.0
	for category in classificationData :
		ratio = (float(category)/len(data))
		if(ratio == 0):
			entropyData += 0
		else :
			entropyData+=-1*ratio*math.log(ratio,2)
	informationGain = entropyData
	if(Type == "nominal"):
		for value in candidateSplits  :
			subset = subSet(data,attribute,value,attributeList,Type,"nominal")
			classificationValueData = findClassification(subset,attributeList)
			entropyValueData = 0.0
			if (len(subset) == 0) :
				entropyValueData = 0.0
			else :
				for cat in classificationValueData :
					ratio = (float(cat)/len(subset))
					if(ratio == 0):
						entropyValueData+=0
					else :
						entropyValueData+=-1*ratio*math.log(ratio,2)
			valueTest = (float(len(subset))/len(data))*entropyValueData
			informationGain-=valueTest
		return round(informationGain,6)
	else :
		informationGainList = []
		for value in candidateSplits  :
			informationGain = entropyData
			subset1 = subSet(data,attribute,value,attributeList,Type, "less than")
			subset2 = subSet(data,attribute,value,attributeList,Type, "greater")
			classificationValueData1 = findClassification(subset1,attributeList)
			classificationValueData2 = findClassification(subset2,attributeList)
			entropyValueData1 = 0.0
			entropyValueData2 = 0.0
			if (len(subset1) == 0) :
				entropyValueData1= 0.0
			else :
				for cat in classificationValueData1:
					ratio = (float(cat)/len(subset1))
					if(ratio == 0):
						entropyValueData1+=0
					else:
						entropyValueData1+=-1*ratio*math.log(ratio,2)
			valueTest = (float(len(subset1))/len(data))*entropyValueData1
			informationGain-=valueTest
			if (len(subset2) == 0) :
				entropyValueData2 = 0.0
			else :
				for cat in classificationValueData2:
					ratio = (float(cat)/len(subset2))
					if (ratio==0) :
						entropyValueData2+=0
					else:
						entropyValueData2+=-1*ratio*math.log(ratio,2)
			valueTest = (float(len(subset2))/len(data))*entropyValueData2
			informationGain-=valueTest
			informationGainList.append(round(informationGain,6))
		return informationGainList
		
def findClassification(data,attributeList):
	classFreq=[0,0]
	class1 = attributeList[len(attributeList)-1].getCandidateSplits()[0]
	for row in data :
		if(row[len(row)-1]==class1):
			classFreq[0]+=1
		else :
			classFreq[1]+=1
	return classFreq

def all_same(items):
	return all(x == items[0] for x in items)

def determineCandidateSplits(data, attributeList):
	global candidateSplits
	count = 0
	for attr in attributeList : 
		if(attr.getType()=="nominal" and len(attr.getCandidateSplits())!=0):
			continue
		if(attr.getType()=="nominal"):
			attr.setCandidateSplits(attr.getValues())
			count+=1
		else : 
			value_class_pair = [[]]
			for row in data :
				value_class_pair.append([float(row[int(attr.getIndex())]),row[len(attributeList)-1]])
			count+=1
			del value_class_pair[0]
			value_class_pair =  sorted(value_class_pair, key=lambda tup: tup[0])
			i=0
			splits = []
			while ((i+1)<len(value_class_pair)):
				if(value_class_pair[i][0]==value_class_pair[i+1][0]):
					i+=1
					continue
				else : 	
					class1 = getAllClassificationsOfAttribute(value_class_pair, value_class_pair[i][0])
					class2 = getAllClassificationsOfAttribute(value_class_pair, value_class_pair[i+1][0])
					for c in class1:
						for c2 in class2:
							if(c2!=c):
								s = (float(value_class_pair[i][0])+float(value_class_pair[i+1][0]))/2
								if(s not in splits):
									splits.append((float(value_class_pair[i][0])+float(value_class_pair[i+1][0]))/2)
				i+=1
			attr.setCandidateSplits(splits)

def getAllClassificationsOfAttribute(value_class_pair , attributeValue):
	classes = []
	for value in value_class_pair :
		if(value[0] == attributeValue):
			if value[1] not in classes :
				classes.append(value[1])
		if(len(classes)==2):
			return classes
	return classes

def randomSelectionOfTrainingSet(data, setSize, attributeList):
	subSet=[[[]]]
	global correctCount
	global wrongCount
	global accuracyList
	count = 0
	del subSet[0][0]
	if(setSize==len(data)):
		subSet[count]=data
	else : 
		while count<10:
			while len(subSet[count])<setSize:
				line = random.choice(data)
				if(len(subSet)==0):
					subSet[count].append(line)
				elif line not in subSet[count] :
					subSet[count].append(line)
			subSet.append([[]])
			count+=1
			del subSet[count][0]
	i=0
	while(i<10):
		subset1 = subSet[i]
		i+=1
		Tree = Node()
		Tree = makeTree(subset1, attributeList, 4, 0, str(findMajority(subset1, attributeList)))
		testDataFile = open('diabetes_test.arff')
		testlines = [testline.rstrip('\n') for testline in testDataFile]
		testData = [[]]
		index = 0
		for line in testlines :
			if(not line.startswith('@data') and not line.startswith('@relation') and not line.startswith('@attribute')) :
				testData.append(line.split(','))
		for row in testData : 
			if(len(row)==0):
				continue
			testTheTree(row, Tree, attributeList)
		print "\nCorrect Count : "+str(correctCount)+" Total Count : "+str(wrongCount+correctCount) +" Accuracy : "+str(float(correctCount)/float(wrongCount+correctCount)*100)
		accuracyList.append(float(correctCount)/float(wrongCount+correctCount)*100)
		correctCount=0
		wrongCount=0
	return

main()
