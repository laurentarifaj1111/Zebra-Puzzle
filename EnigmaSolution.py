from collections import OrderedDict 

class Constraints():

    def __init__(self, homes):
        
        self.homes = homes

        self.homesPossibleCombinations  = {
            'home1' : {'color':[],'nationality':[], 'cigaretteBrands':[], 'drink':[], 'pet':[] },
            'home2' : {'color':[],'nationality':[], 'cigaretteBrands':[], 'drink':[], 'pet':[] },
            'home3' : {'color':[],'nationality':[], 'cigaretteBrands':[], 'drink':[], 'pet':[] },
            'home4' : {'color':[],'nationality':[], 'cigaretteBrands':[], 'drink':[], 'pet':[] },
            'home5' : {'color':[],'nationality':[], 'cigaretteBrands':[], 'drink':[], 'pet':[] },
        }

        self.constraintsDict = {
            'constraint1' : {'color':'Red', 'nationality' : 'Englishman'},
            'constraint2' : {'color':'Yellow', 'cigaretteBrands' : 'Kools', 'pet' : ['Horse',1]},
            'constraint3' : {'nationality' : 'Spaniard', 'pet' : 'Dog'},
            'constraint4' : {'cigaretteBrands' : 'Chesterfields','pet' :  ['Fox', 1, -1]},
            'constraint5' : {'cigaretteBrands' : 'Old Gold ', 'pet' : 'Snails'},
            'constraint6' : {'cigaretteBrands' : 'Lucky Strike', 'drink' : 'Orange juice'},
            'constraint7' : {'nationality' : 'Ukrainian', 'drink' : 'Tea'},
            'constraint8' : {'nationality' : 'Japanese', 'cigaretteBrands' : 'Parlament' },
            'constraint9' : {'color':'Green', 'drink' : 'Coffee', 'color1':['Ivory', -1]},
            'constraint10': {'nationality' : 'Norwegian' , 'color':['Blu', 1,-1]},
            'constraint11': {'drink' : 'Water'},
            'constraint12': {'pet' : 'Zebra'},
        }

        self.existsFromTheStart = []
        self.lastConstraintPlaces = []
        self.alredyUsedConstraintName = []
    

    def solveEnigma(self):
        if self.isComplete(self.homes) == True:
            self.printHomes()
            return True

        homeName, homeArr, optionName, optionValue = self.isComplete(self.homes)   
        for option in self.homesPossibleCombinations[homeName][optionName]:
            value, constraintArr = self.returnValue(homeName, optionName, option)
            self.lastConstraintPlaces.append([])
            if isinstance(value, list):
                for constraintOptionName, constraintOptionValue in constraintArr.items():
                    if value[0] == homeName:
                        self.callMethodsToAddData(homeName, constraintOptionName, constraintOptionValue,keyOfHome= 0, value ='')

                    else:
                        self.callMethodsToAddData(homeName, constraintOptionName, constraintOptionValue,keyOfHome = 1, value = value[0])

            else:
                for constraintOptionName, constraintOptionValue in constraintArr.items():
                    self.callMethodsToAddData(homeName, constraintOptionName, constraintOptionValue,keyOfHome= 0, value ='')

            self.emptyHomesPossibleCombinations()
            self.addHomesPossibleCombinations(self.alredyUsedConstraintName)

            
            if self.solveEnigma():
                return True
            
            self.reverseSteps(self.alredyUsedConstraintName)
        return False


    def addHomesPossibleCombinations(self, alredyUsedConstraint = []):
        t=0           
        for k,v in self.homes.items():
            for constraints, constraintsArray in self.constraintsDict.items(): 
                if constraints not in alredyUsedConstraint:
                    homesToPutData = []
                    for key, element in constraintsArray.items():                
                        alredyTried = []    
                        if element in self.existsFromTheStart:
                            homesToPutData.append('exists')

                        elif isinstance(element, list):
                                for i in range(1, len(element)):
                                    keyIndex = list(self.homes).index(k)
                                    if(keyIndex + element[i] >= 0 and keyIndex + element[i] < len(list(self.homes))):
                                        key, homeKey = self.checkKey(k, key, element[i])
                                        if self.homes[homeKey][key] == '':
                                            homesToPutData.append(k)
                                            t=element[i]
                        else:
                            for variant , option in v.items():
                                if variant in key and option == '':
                                    homesToPutData.append(k)
                    if len(homesToPutData) >= len(constraintsArray):
                        if self.checkIfContainsList(constraintsArray):
                            for optionName, optionValue in dict(OrderedDict(sorted(constraintsArray.items()))).items():
                                if isinstance(optionValue, list):
                                    for i in range(1, len(optionValue)):
                                        keyIndex = list(self.homes).index(k)
                                        if(keyIndex + optionValue[i] >= 0 and keyIndex + optionValue[i] < len(list(self.homes))):                                    
                                            optionName, homeKey = self.checkKey(k, optionName, optionValue[i])

                                            arr = []
                                            arr.extend([k, element[0], element[i]])
                                            self.homesPossibleCombinations[homeKey][optionName].append(arr)
                                            if  'exists' in  homesToPutData:
                                                for constraintOptionName, constraintOptionValue in constraintsArray.items():
                                                    if constraintOptionValue in self.existsFromTheStart:
                                                        continue

                                                    else:
                                                                optionArr = []
                                                                optionArr.extend([k, constraintOptionValue[0], i])
                                                                self.homesPossibleCombinations[k][constraintOptionName].insert(0,optionArr)
                                                           


                                            else:
                                                for constraintOptionName, constraintOptionValue in constraintsArray.items():
                                                     if constraintOptionValue != optionValue:
                                                        constraintOptionName, k = self.checkKey(k, constraintOptionName)    
                                                        optionArr = []
                                                        optionArr.extend([k, constraintOptionValue, i])
                                                        self.homesPossibleCombinations[k][constraintOptionName].append(optionArr)


                        else:
                            if  'exists' in  homesToPutData:
                                for optionName, optionValue in constraintsArray.items():
                                    if optionValue in self.existsFromTheStart:
                                        continue
                                    
                                    else:
                                        optionName, k = self.checkKey(k, optionName)
                                        self.homesPossibleCombinations[k][optionName].append(optionValue)


                            else:
                                for optionName, optionValue in constraintsArray.items():
                                    optionName, k = self.checkKey(k, optionName)
                                    self.homesPossibleCombinations[k][optionName].append(optionValue)



    def checkIfContainsList(self, constraintsArray):
        listNr = 0
        for key, element in constraintsArray.items():
            if isinstance(element, list):
                listNr = listNr + 1
                return True
        return False
    

    def isComplete(self,homesDict):
        isEmpty = []
        for home, homeArr in homesDict.items():
            for variant, option in homeArr.items():
                if option == '':
                    return home, homeArr, variant, option
        return True


    def returnValue(self, home, variant, option):
        if option != '':
            if isinstance(option, list):
                value, name = self.findConstraint(option, home) 
                if   value  != False :
                    return option, value
            else:
                value, name = self.findConstraint(option, home) 
                if   value  != False :
                    return option, value
        return False, False


    def findConstraint(self, word, home):
        constraintName = []
        for constraint, constraintsArr in self.constraintsDict.items():
            for key, value in constraintsArr.items():
                if isinstance(word, list):
                    if word[1] in value:
                        self.alredyUsedConstraintName.append(constraint)
                        return constraintsArr,constraint
    
                elif  word in value :
                        self.alredyUsedConstraintName.append(constraint)
                        return constraintsArr,constraint
        return False, False


    def removeLastConstraint(self):
        for i in range (0, len(self.lastConstraintPlaces[len(self.lastConstraintPlaces)-1]), 2):
            homeKey = self.lastConstraintPlaces[len(self.lastConstraintPlaces)-1][i+1] 
            elementKey = self.lastConstraintPlaces[len(self.lastConstraintPlaces)-1][i]
            self.homes[homeKey][elementKey] = ''


    def printHomes(self):
        for key , value in self.homes.items():
            print(key)
            for key1, value1 in value.items():
                print(key1 , value1)       
            print("")    

    def emptyHomesPossibleCombinations(self):
        for home, homeCaracteristics in self.homesPossibleCombinations.items():
            for variant, options in homeCaracteristics.items():
                options.clear()


    def checkKey(self, home, constraintOptionName, constraintOptionValue = 0):
        keyIndex = list(self.homes).index(home)
        homeKey = list(self.homes)[keyIndex + constraintOptionValue]
        for approx in self. homes[homeKey].keys():
            if approx in constraintOptionName:
                constraintOptionName = approx
        return constraintOptionName, homeKey


    def addHomeValues(self, homeKey, constraintOptionName, constraintOptionValue):
        if self.homes[homeKey][constraintOptionName] == '': 
            self.homes[homeKey][constraintOptionName] = constraintOptionValue
            self.lastConstraintPlaces[len(self.lastConstraintPlaces)-1].append(constraintOptionName)
            self.lastConstraintPlaces[len(self.lastConstraintPlaces)-1].append(homeKey)

        
    def callMethodsToAddData(self, homeName, constraintOptionName, constraintOptionValue, keyOfHome = 1, value = ''):
        if isinstance(constraintOptionValue, list):

            for i in range(1, len(constraintOptionValue)):
                if keyOfHome == 0:                     
                    constraintOptionName, homeKey = self.checkKey(homeName, constraintOptionName, constraintOptionValue[i])
                else:
                    constraintOptionName, homeKey = self.checkKey(homeName, constraintOptionName)

                for option in self.homesPossibleCombinations[homeKey][constraintOptionName]:
                    if constraintOptionValue[0] in option or constraintOptionValue[0] == option:
                        if self.homes[homeKey][constraintOptionName] == '': 
                            self.addHomeValues(homeKey, constraintOptionName, constraintOptionValue[0])
                break
        
        else:
            if value != '':
                constraintOptionName, homeKey = self.checkKey(value, constraintOptionName)
                self.addHomeValues(value, constraintOptionName, constraintOptionValue)

            else:
                constraintOptionName, homeKey = self.checkKey(homeName, constraintOptionName)
                self.addHomeValues(homeName, constraintOptionName, constraintOptionValue)

    def reverseSteps(self, alredyUsedConstraintName):
            self.removeLastConstraint()
            self.lastConstraintPlaces.pop()
            self.alredyUsedConstraintName.pop()
            self.emptyHomesPossibleCombinations()
            self.addHomesPossibleCombinations(alredyUsedConstraintName)


    def addValuesInStart(self):
       for key , value in self.homes.items():
            for key1, value1 in value.items():
                if value1 != '':
                    if self.findConstraint(value1, key) != False :
                       self.existsFromTheStart.append(value1)




def main():
        homes = {
            'home1' : {'color':'','nationality':'Norwegian', 'cigaretteBrands':'', 'drink':'', 'pet':''},
            'home2' : {'color':'','nationality':'', 'cigaretteBrands':'', 'drink':'', 'pet':''},
            'home3' : {'color':'','nationality':'', 'cigaretteBrands':'', 'drink':'Milk', 'pet':''},
            'home4' : {'color':'','nationality':'', 'cigaretteBrands':'', 'drink':'', 'pet':'' },
            'home5' : {'color':'','nationality':'', 'cigaretteBrands':'', 'drink':'', 'pet':'' },
        }
        constraints = Constraints(homes)
        constraints.addValuesInStart()
        constraints.addHomesPossibleCombinations()
        constraints.solveEnigma()


main()