# Notes:
# Dataset requirements: be a .csv, no missing/empty values, quantitative features,
# class as final column, no "id" type column

import matplotlib.pyplot as ply
import os
import csv
import math
import numpy as np
import random


########################################################################################################################
#Every row becomes an entity
class Entity:
    nearestHit  = 0
    nearestMiss = 0
    row = []
    clss = ""
    rowNum = 0

    def __init__(self, rowEntry, rowNum):
        self.rowNum = rowNum
        self.clss = rowEntry[len(rowEntry)-1]
        del rowEntry[len(rowEntry) -1]
        self.row = rowEntry

    def getRowNum (self):
        return self.rowNum

    def getHit(self):
        return self.nearestHit

    def setHit(self,hit):
        self.nearestHit = hit

    def getMiss(self):
        return self.nearestMiss

    def setMiss(self, miss):
        self.nearestMiss = miss

    def getClss(self):
        return self.clss

    def setClss(self,cls):
        self.clss = cls

    def getRow(self):
        return self.row
########################################################################################################################
#Every column minus the class one is a Feature
class Feature:
    header  = ""
    weight = 0.0

    def __init__(self, header):
        self.header = header

    def setWeight(self,weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def getHeader(self):
        return self.header

########################################################################################################################



########################################################################################################################
class framework:
    def startMain(self):
        #entries, headers = self.processFile("winequality-red-lite.csv")
        entries, headers, normalize = self.promt()
        print("Working...")
        clssHeader = headers[len(headers)-1]   #Extract the class header and delete the original
        del headers[len(headers)-1]
        arrayOfFeatures = self.phraseFeatures(headers)  #Sort the columns
        print("Finished Features...")
        arrayOfStuff = self.phraseEntries(entries)  #Sort the rows
        print("Finished Phrasing...")
        if normalize:
            arrayOfStuff = self.normalizeData(arrayOfStuff)
        print("Finished Normalizing... \nRunning relief algorithm...")
        arrayOfFeatures = self.reliefAlgo(arrayOfStuff,arrayOfFeatures)

        self.printResults(arrayOfFeatures)

    def normalizeData(self,array): #//Normalize the Data
        normArray = []
        row = []
        minMax = self.findMinMax(array)
        row = array[0].getRow()
        for i in range (0, len(row)-1):
            for element in array:
                x = float(element.getRow()[i])
                x = (x-minMax[i][0])/(minMax[i][1]-minMax[i][0])
                element.getRow()[i] = x
        return array

    def findMinMax(self,array): #Find the minimum and maximum of the entity array
        minMax = []
        row = array[0].getRow()
        for i in range (0, len(row)-1):
            min = float(row[i])
            max = float(row[i])
            for element in array:
                value = float(element.getRow()[i])
                if value < min:
                    min = value
                if value > max:
                    max = value
            minMax.append([min,max])
        return minMax

    def reliefAlgo(self,arrayOfEntities,arrayOfFeatures):   #Returns a list of weights based on minimum to maximum
        ############Find nhits and nmisses##########################
        for entry1 in arrayOfEntities:
            nearestHit = math.inf  #lazy but effective large number to compare to
            nearestMiss = math.inf
            #num = 100
            sample = random.sample(arrayOfEntities,20)
            for entry2 in sample:
                if(entry1.getRowNum() != entry2.getRowNum()):   #Dont compare the same rows thats nonsense
                    dist = self.calcDistance(entry1.getRow(),entry2.getRow())
                    if(entry1.getClss() == entry2.getClss() and dist < nearestHit):     #If the distance is lower than the current best and 2 pts are different classes
                        entry1.setHit(entry2.getRowNum())
                        nearestHit = dist
                    elif(entry1.getClss() != entry2.getClss() and dist < nearestMiss):
                        entry1.setMiss(entry2.getRowNum())
                        nearestMiss = dist
            #print(str(entry1.getHit()) + " " + str(entry1.getMiss()))

        ###################Find yo weights for each feature here##########################
        for feature in range(0,len(arrayOfFeatures)):
            #print(arrayOfFeatures[feature].getHeader())
            #print(arrayOfFeatures[feature].getWeight())
            sum = 0.0
            for entry in arrayOfEntities:
                diff1 = abs(float((arrayOfEntities[entry.getHit()]).getRow()[feature]) - float(entry.getRow()[feature]))**2
                diff2 = abs(float((arrayOfEntities[entry.getMiss()]).getRow()[feature]) - float(entry.getRow()[feature]))**2
                sum = sum - diff1 + diff2
                sum = sum
            arrayOfFeatures[feature].setWeight(sum/(len(arrayOfEntities)))
        return arrayOfFeatures
        #################################################################

    def phraseFeatures(self,array): #Phrases a Feature Object that contains the relevant data to it
        #counter = 0
        outputArray = []
        for element in array:
            outputArray.append(Feature(element))
            #counter +=1
        return outputArray

    def phraseEntries(self,array): #Phrases a Entry object which contains row information as well as the class related to it
        counter = 0
        outputArray = []
        for element in array:
            outputArray.append(Entity(element,counter))
            counter +=1
        return outputArray

    def processFile(self, f): #Reads in the data from the .csv file
        with open(f, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
        return data, headers

    def calcDistance(self, array1, array2):
        # Calculate Euclidean distance
        return float(np.linalg.norm(np.array(array1,dtype=np.float32) - np.array(array2,dtype=np.float32)))

    def promt(self): #Simple dialog/input descriptor
        print("Hello, Welcome to the Relief algorithm.")
        chosen = False
        options = []
        data = []
        headers = []
        for file in os.listdir():
            if file.endswith(".csv"):
                options.append(file)
        while (chosen == False):
            try:
                print("Please input the key number of the file you wish to open.")
                for file in range(0,len(options)):
                    print("(" + str(file) + ") " + options[file])
                print("(" + str(len(options)) + ") Other")
                selection = int(input(""))
                if selection == len(options):
                    print("Enter the full file location.\n")
                    selection = str(input(""))
                    data, headers = self.processFile(selection)
                else:
                    data, headers = self.processFile(options[selection])
                chosen = True
            except:
                print ("Oops, please make a diffrent/valid choice. ")
        print("Normalize the data y/n?")
        normalize = input("")
        if normalize == "y":
            normalize = True
        else:
            normalize = False
        return data, headers, normalize

    def useHistogram(self,array,yLabel,xLabel): #Function to create a histogram
        ply.hist(array) #bins=[-1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 1]
        ply.ylabel(yLabel)
        ply.xlabel(xLabel)
        ply.show()

    def plotGraph(self,array,yLabel,xLabel):#Function to create a plotting graph
        ply.plot(array)
        ply.ylabel(yLabel)
        ply.xlabel(xLabel)
        ply.show()

    def createScatter(self,array,yLabel,xLabel):#Funtion to create a scatter diagram
        ply.scatter(array)
        ply.ylabel(yLabel)
        ply.xlabel(xLabel)
        ply.show()

    def printResults(self,arrayOfFeatures):     #Prints results from a series of runs
        print ("\nShowing results...")
        arrayOfFeatures.sort(key=lambda x: x.getWeight(), reverse=True)


        for feature in arrayOfFeatures:
            print("{0} had a weight of {1:2g}".format(feature.getHeader(),feature.getWeight()))
            #print(str(feature.getHeader()) + " had a weight of " + round(float(feature.getWeight()),4))
        array = []
        for feature in arrayOfFeatures:
            array.append(float(feature.getWeight()))
        self.plotGraph(array, "Weight Value", "Feature Number")

    def randomList(self,numberOfItems): #Placeholder function - not relevant to project.
        tempList =[]
        for n in range (0,numberOfItems):
            tempList.append(random(0,1399))
        tempList.sort()
        return tempList
########################################################################################################################

mainProg = framework()
mainProg.startMain()
