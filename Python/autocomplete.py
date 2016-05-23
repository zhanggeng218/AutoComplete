########################################################################################################################
# Auto-Complete
#
# Method 1:
# Brute Force search.
# The entries in the data file is searched one by one to compare to the prefix.
#
# Method 2:
# Fast Tree search.
# First the data file is converted to a tree. Each letter corresponds to a tree node.
# For example, if the data file contains three words - soccer, cat and canada - then the tree looks like:
# {'c': {'a': {'n': {'a': {'d': {'a': {'END': True}}}},
#              't': {'END': True}}},
#  's': {'o': {'c': {'c': {'e': {'r': {'END': True}}}}}}}
# Each letter takes a level. The END key indicates that an end of the word is reached
########################################################################################################################

import sys
import time

# set a larger limit for recursion
sys.setrecursionlimit(10000)

# global variables
METHODS  = ['brute force', 'fast tree']              # two methods used in this task
FILENAME = 'data.txt'                                # file name of the data
DICTTREE = {}

def main() :
    # make selection of the method used
    print("Please select the method of autocomplete (type 1 or 2):")
    print("1. Brute force")
    print("2. Fast Tree")
    methodSelection = int(raw_input())

    print('\nUse %s!\n' % METHODS[methodSelection - 1])

    if methodSelection == 2: getTree(DICTTREE)

    print("Pick an option (type 1 or 2): ")
    print("1. Try a new prefix")
    print("2. Quit")
    option = int(raw_input())
    while option != 2 : # last choice is to quit
        if option == 1 :
            recommendations = set()                         # the set of qualifying words
            if methodSelection == 1: completeTime = bruteForce(recommendations)
            elif methodSelection == 2: completeTime = fastTree(recommendations)

            # output final results
            result = list(recommendations)
            result.sort()
            print("\nSuggestions:")
            for w in result: print w

            # the total time used for search words
            # note that this time does not include the time for preparing the tree in the fast tree method
            print("\nTime for auto-complete: %f" % completeTime)

        elif option == 3 :
            pass
        else :
            print('Invalid response;try again')

        print("Pick an option: ")
        print("1. Try a new prefix")
        print("2. Quit")
        option = int(raw_input())

    return

def bruteForce(recommendations):

    prefix = getPrefix()

    start_time = time.time()                            # for performance analysis
    with open(FILENAME, 'rb') as f:
        for line in f:
            tmp = line.strip('\n\t\r ').lower()
            if tmp.startswith(prefix):
                if tmp not in recommendations: recommendations.add(tmp)
    end_time = time.time()                              # for performance analysis
    elapsed_time = end_time - start_time

    return elapsed_time

def fastTree(recommendations):
    # print("Preparing dictionary tree from data file..........")
    #
    # # construct the dictionary tree first
    # # this step takes some time, but it is a one-time job.
    # dictTree = {}
    # with open('data.txt', 'rb') as f:
    #     for line in f:
    #         tmp = line.strip('\n\t\r ').lower()
    #         populateTree(dictTree, tmp, 0)
    # print("Preperation done!\n")

    prefix = getPrefix()

    start_time = time.time()                            # for performance analysis
    depthSearch(DICTTREE, prefix, 0, recommendations)   # search for qualifying words
    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

########################################################################################################################
# Helper Functions
########################################################################################################################
# prepare the dictionary tree for the fast tree method
def getTree(dict):
    print("Preparing dictionary tree from data file..........")

    # construct the dictionary tree first
    # this step takes some time, but it is a one-time job.

    with open('data.txt', 'rb') as f:
        for line in f:
            tmp = line.strip('\n\t\r ').lower()
            populateTree(dict, tmp, 0)
    print("Preperation done!\n")

# get user input for the prefix
def getPrefix():
    print("\nPlease type the prefix of a word:")
    prefix = raw_input()
    return prefix

# populate the dictionary tree with all the entries in the data file
def populateTree(treenode, word, i):
    # if the end of word is reached, add the END key to the tree
    if (i > len(word) - 1): return {'END': True}
    # continue to populate the tree
    else:
        if (word[i] not in treenode): treenode[word[i]] = populateTree({}, word, i + 1)
        else: populateTree(treenode[word[i]], word, i + 1)

    return treenode

# if there exits words starting with the prefix, populate the recommendation set
def getRecommendations(treenode, prefix, reco):
    for key in treenode:
        # if an END key is reached, a complete word is found
        if key == 'END': reco.add(prefix)
        # the word has not be completed, continue to the next depth of the tree
        else: getRecommendations(treenode[key], prefix + key, reco)

# run a depth search with in the dictionary tree
def depthSearch(dictTree, pre, depth, wordList):
    # when the entire prefix exists in the tree, continue to populate the recommendation set
    if (depth == len(pre) - 1) and (pre[depth] in dictTree): getRecommendations(dictTree[pre[depth]], pre, wordList)
    # search within the tree for every character in the prefix
    elif (pre[depth] in dictTree):
        depthSearch(dictTree[pre[depth]], pre, depth + 1, wordList)


main()