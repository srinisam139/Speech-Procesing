#!/usr/bin/python

import random
import sys
from statistics import mode

# set this to 1 if you want to see more output
verbose = 0

#################################
#### LETTER-to-PHONEME RULES ####
#################################

# These are some very likely letter-to-phoneme mappings.
## TO DO ##
## You can add additional likely letter-to-phoneme correspondences here
## to improve the alignments from which you derive your mapping rules.

baserules = {'F':'F', 'K':'K', 'L':'L', 'M':'M', 'T':'T', 'N':'N', 'P':'P', 'C':'K',
                 'D':'D', 'B':'B', 'G':'G', 'R':'R','S':'S','V':'V','Y':'Y', 'Z':'Z','AT': 'AE', 
                 'AC':'AE','UT': 'AH', 'OU': 'AO', 'CO': 'K', 'OW': 'AW', 'AB': 'AH', 
                 'EE':'IY', 'ED':'EH','H':'HH', 'UR':'ER', 'AT':'AE',
                'E':{'H':'IY','R':'IY', 'M':'IY', 'W':'IY', 'I':'IY'}, 'EM':'EH', 'A':{'T':'AH'},
                'Y':{'T':'IY'}, 'IC':'K', 'S':'S', 'S':'Z', 'LL':'L', 'SS':'S', 'ON':'AH',
                'TI':'SH', 'EA': 'ER','ER':'ER','OO':{'F':'UW','M':'UW','R':'UW','T':'UW',
                'L':'AH'}, 'YM':'IH', 'OL':'AA', 'OP':'AA', 'SO':'OW', 'SU':'AH', 
                'AD':'AE', 'EN':'EH', 'GE':'JH', 'EY':'IY', 'CH': 'CH', 'OD': 'AA', 
                'IN':'IH', 'NG':'NG','OA': 'OW', 'DI':'IH', 'EP':'EH', 'EM':'EH', 'OS':'AO', 'OY':'OY',
                'SE':'IY', 'SH':'SH', 'TE':'IY', 'TH':'TH', 'ET':'EH', 'AL':'AH', 'EU':'UH', 'IN':'AY',
                'EI':'IY', 'ZU': 'ZH', 'ER':'RE', 'AN':'AE', 'CA': 'K', 'AP':'AE', 'OR':'AO'}

## TO DO ##
## Other ideas:
## set up some rules that allow a letter to map to one of several phones
## set up some conditional rules, e.g., C-> CH before H
## To implement these ideas, you will also need to update the calc_distance function!



# the dict newrules stores the new mappings that your alignment will produce.
# This will be a dictionary mapping a letter to  a list of possible phonemes.
# Keys will be single letters, values will be lists of possible phonemes.
# We will use this set of new mapping rules to
# to guess the pronunciations of words we haven't seen.
newrules = {}

 
# A set of vowels is created
vowels = ('A', 'E', 'I', 'O', 'U')
#A set of consonants is created
consonants = ('B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z')
##################
### FUNCTIONS ####
##################

# This function compares a letter and phoneme to see how well they match

## TO DO ##
## You can change the way the distance is calculated when performing
## the alignment. 
## Ideas: 
## * assign different values (e.g., 2 instead of 1, .5 for matches
## that are possible but not super likely, etc.).
## * implement something to allow for conditional distances (e.g., 
## C:CH only before H, S:Z at the end of a word after a vowel)
## * add functionality to encourage vowel letters to align to vowel phonemes

"""
param spelling:  The current letter passed from word spelling
param pronunciation: The speech pronunciation mapped for the letter
param position: Position of the letter from the spelling
param word_length: The length of the spelling word
param nextletter: By default it is null until there is a nextletter after the current letter
param previousletter: By default it is null for the first letter in the spelling and passes the previous letter
"""
def calc_distance(spelling, pronunciation, position, word_length, nextletter = "null", previousletter="null"):
    # If it's in a baserule, then the distance is 0 because they should probably match.
    # Otherwise, make the distance 2 because it's probably a very bad idea.
    string = spelling+nextletter #Combining the current Letter and next Letter
    
    # The outer if condition checks if the spelling letter is in the list of baselinerule keys
    if spelling in baserules.keys():
        #The first inner if condition checks S:Z at the end of a word after a vowel
        if baserules[spelling] == 'Z' and position == word_length and previousletter in vowels:
            return 0.0
        # the second if condition checks if S:S is in the middle of the spelling
        elif baserules[spelling] == 'S':
            return 0.0
        # the third if condition checks C:CH only before H
        elif spelling+nextletter == "CH":
            return 0.0
        # the third if condition is used to check if any spelling falls in baseline rules pronunciation value
        elif baserules[spelling] == pronunciation:
            return 0.0
        # the final if conditon is used to check the previous letter mapping (For eg: in word 'ME')
        # the baseline rule can able to map M:M but when it goes to next letter it needs to know M
        # so previous letter baseline rules are stored in dictionary of dictionary eg: for letter 'E'
        # 'E': {'H':'IY','R':'IY', 'M':'IY', 'W':'IY', 'I':'IY'}, there are 5 possible previous letters
        # H, R, M, W and I 
        elif type(baserules[spelling]) == type({}):
            for key in baserules[spelling].keys():
                if key == previousletter and baserules[spelling][key] == pronunciation:
                    return 0.0
    #The below if condition checks for (current letter+next letter) mappings. For eg: ('EA':'ER', 'DI':'IH')
    if string in baserules.keys():
        if baserules[string] == pronunciation:
            return 0.0
        #The below condition checks for the current two letters and previous letter mappings
        #For eg: 'OO':{'F':'UW','M':'UW','R':'UW','T':'UW', 'L':'AH'} The 'OO' has two chracters
        # and their previous chracters are F,M,R,T,L and their mappings. So totally three letters
        # are mapped in this pronunciation. Eg: FOO --> 'F' 'UW'
        elif type(baserules[string]) == type({}):
            for key in baserules[string].keys():
                if key == previousletter and baserules[string][key] == pronunciation:
                    return 0.0
                #If OO is present but any previous values are not matching then partial credit is given
                else:
                    return 0.5
        else:
            return 1.0
        # Otherwise, it's not clear, so assign a smaller penalty
    else:
        return 1.0


# This function performs dynamic time warping to align
# the spelling of a word with the pronunciation for that word.
def getalignment(s1, s2):

    if verbose == 1:
        print("Aligning " + s1 + " to " + s2)

    spelling = list(s1)  # word spelling (letters)
    pronunciation = s2.split()  # word pronunciation (phonemes)

    n = len(pronunciation)
    N = len(spelling)

    D = [[0 for i in range(N)] for j in range(n)]
    BT = {}
    spelling[-1] 
    # This is the same code you used for you last problem set.
    for i in range(0,n):
        for j in range(0,N):
            if j < N - 1: # This condition is used to check j is less than last chracter
                if j ==0: # If j is equal to 0. Use the below cal_distance function or else use the below one
                    mydist = calc_distance(spelling[j], pronunciation[i],j,N-1, spelling[j+1])
                else:
                    mydist = calc_distance(spelling[j], pronunciation[i],j,N-1, spelling[j+1], spelling[j-1])
            elif j == N - 1: #if j is equal to the last chracter then use the below calling function
                mydist = calc_distance(spelling[j], pronunciation[i],j,N-1, "null", spelling[j-1])
            else:
                mydist = calc_distance(spelling[j], pronunciation[i],j,N-1)
            if j==0 and i==0:
                D[0][0] = mydist
                BT[(0,0)] = (-1,-1) 
            else:
                mymin = 10000000
                if i==0:
                    mymin = D[i][j-1]
                    BT[(i,j)] = (i,j-1)
                elif j==0:
                    mymin = D[i-1][j]
                    BT[(i,j)] = (i-1,j)
                else:
                    mymin = min(D[i-1][j-1], D[i-1][j], D[i][j-1])
                    minval = D[i-1][j-1]
                    minidxs = (i-1, j-1)
                    if D[i-1][j] < minval:
                        minval = D[i-1][j]
                        minidxs = (i-1, j)
                    if D[i][j-1] < minval:
                        minval = D[i][j-1]
                        minidxs = (i, j-1)
                    BT[(i,j)] = minidxs
                D[i][j]=mydist + mymin

                            
    if verbose == 1:
        print("Overall distance is:" + str(D[n-1][N-1]))
            

    # Just a reminder...
    # spelling uses variables j,N
    # pronunciation uses variables i,n

    # This determines the alignment using the backtrace.
    # Substitutions get added to the set of "new" rules that you are learning.
    # Deletions also get as a rule X->NULL (i.e., a rule to delete X).
    startn = n-1
    startN = N-1

    while startn > -1 and startN > -1:
        backup = BT[(startn, startN)]
        if backup == (startn-1, startN-1):
            if verbose == 1:
                print("Substitution: "+ spelling[startN]+ " with "+ pronunciation[startn])
            if spelling[startN] in newrules.keys():
                newrules[spelling[startN]].append(pronunciation[startn])
            else:
                newrules[spelling[startN]] = [pronunciation[startn]]
        if backup == (startn-1, startN):
            if verbose == 1:
                print("Insert: "+ spelling[startN])
        if backup == (startn, startN-1):
            if verbose == 1:
                print("Delete: "+ spelling[startN])
            if spelling[startN] in newrules.keys():
                newrules[spelling[startN]].append("NULL")
            else:
                newrules[spelling[startN]] = ["NULL"]
        startn = backup[0]
        startN = backup[1]



# Levenshtein distance
# Used to calculate quality of your guessed pronunciations.
def levenshtein(s1, s2):
    # s1: J and j
    # s2: I and i

    J = len(s1)
    I = len(s2)

    D = [[0 for j in range(J)] for i in range(I)]

    for i in range(0,I):
        for j in range(0,J):
            mydist = 0
            if s1[j] != s2[i]:
                mydist = 1

            if j==0 and i==0:
                D[0][0] = mydist
            else:
                mymin = 10000000
                if i==0:
                    mymin = D[i][j-1]
                elif j==0:
                    mymin = D[i-1][j]
                else:
                    mymin = min(D[i-1][j-1], D[i-1][j], D[i][j-1])
                D[i][j]=mydist + mymin

    return D[I-1][J-1]



###################
#### MAIN PART ####
###################

#####################################
### Train letter-to-phoneme model ###
#####################################

# Read in a training lexicon.
# f = open(sys.argv[1])
f = open('trainprons.txt')
for line in f:
    parts = line.strip().split("  ")
    w = parts[0]
    p = parts[1]

    # Align the letters to the phonemes with dtw.
    getalignment(w, p)

f.close()

# Go through list of mappings for each letter and
# calculate the probability of mapping from a letter
# to each of the possible phonemes it was aligned to
# in training.
probs = {}
for k,v in newrules.items():
    probs[k] ={}
    for i in set(v):
        iprob = v.count(i) / float(len(v))
        probs[k][i] = iprob

    if verbose == 1:
        print(k + "\t"),
        print(v)


####################################
### Test letter-to-phoneme model ###
####################################

# Use these mappings trained above to generate pronunciations for unseen words.

# Option 1: Randomly pick one of the mappings that was found
# by the aligner. Ones that were found more often will
# get picked more often. Do this ten times for every test word.

## TO DO ##
##
## If you added conditional mappings in your alignment, you 
## will need code to implement that here.
##
## You can also change the way you select the mapping, e.g.,
## * always pick the most frequent mapping
## * ignore infrequent mappings
## * ignore unlikely mappings (e.g., vowel:consonant mappings)
## * disallow sequences of more than one vowel in your output

# This stores the actual pron - guessed pron pairs to be evaluated.
# It is a list of tuples (actual pron, guessed pron)

#Fucntion to find most frequent mapping
def most_frequent(List):
    return max(set(List), key = List.count)

results = []

#f = open(sys.argv[2])
f = open('testprons.txt')
for line in f:
    counter = 0
    parts = line.strip().split("  ")
    word = parts[0]
    pron = parts[1]
    token = word.split()
    # make ten guesses for every input word
    while counter < 10:
        counter += 1
        guess = ""

        for index, lett in enumerate(word):
            possibles = newrules[lett]
            #r = random.randrange(len(possibles))
            value = most_frequent(possibles) #Find most frequent mapping for the letter
            # Conditional Mapping for S:Z if it comes at the last chracter
            if index>0 and lett == 'S' and len(word) - 1 == index and word[index-1] in vowels:
                    guess = guess + 'Z' + " "
            #IF vowel:vowel mapping is used, then use mode to pick the possible mapping
            elif lett in vowels:
                if value not in consonants:
                    if mode(possibles) != "NULL":
                        guess = guess + mode(possibles) + " "
            #Ig vowel:consonant mapping is used then skip it 
            elif lett in vowels:
                if value in consonants:
                    pass #ignoring vowel:consonant mapping
            #For other mappings just use the most frequent mapping
            elif (value != "NULL"):
                guess = guess + value + " "
    
        if verbose == 1:
            print (line),
            print ("\t"),
            print(guess + "\t")
        results.append((pron, guess))


########################
### Evaluate outoput ###
########################

# Calculate the Levenshtein distance (min edit distance)
# between each pronunciation you guessed and the correct one.

# Final output is total distance over all pairs
# divided by the total number of phones in the correct prons.

totalphones = 0
totallev = 0
for pron,guess in results:
    lev = levenshtein(pron.strip().split(), guess.strip().split())
    print(pron + "\t\t" + guess + "\t\t" + str(lev))
    totallev += lev
    totalphones += len(pron.strip().split())



totalerr = float(totallev) / float(totalphones)
print("The total error is: " + str(totalerr))

