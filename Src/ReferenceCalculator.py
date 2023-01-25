#calc(numSellers,buyers,blocks) returns marketvalue/print CSV

# Receives a number of sellers with chains of blocks of decreasing price that contain a certain amount of product per block. 
# Also receives a number of buyers with different demands for amounts of products. One has to buy the previous blocks in a chain of blocks to access the later cheaper ones.
# If only block 1 is bought then block 2 will take on the price of block 1 and 3 of 2 and so on. 
# All possible distributions of these are then tested and the one with the best Raj Jain fairness index is choosen and returned/printed.

# Note: The sellers themselves should not matter, only their blockchains. 

from itertools import combinations
from itertools import permutations
from Block import *
from Bidder import Bidder

# blocklist: All the blocks together in a list (since the linked block class is not yet finished. Either one later changes the code to use these instead or adds a funtion to convert the linked list to an ordinary one)
# buyers: A list of buyers.
def referenceCalculator(blocklist, buyers):
    bestRajJainCostFairness = -1
    bestData = []
    permNum = 0 # For testing
    permAndComb = 0
    
    
    for permutation in permutations(blocklist): # Will be performance intensive, consider more effective way if performance becomes a problem
        for combination in splitfinder(permutation, len(buyers)):
            if(validCombination(combination, buyers)):
                averageCostsForBuyers = []
                i = 0
                while i < len(combination)-1: # Runs through what the buyers have bought (the last index is the "unboughts")
                    averageCostsForBuyers.append(averageCost(combination[i]))
                    i = i + 1
                    
                RajJainCostFairness = rajJainFairness(averageCostsForBuyers)
                if (RajJainCostFairness > bestRajJainCostFairness):
                    bestRajJainCostFairness = RajJainCostFairness
                    bestData.append(averageCostsForBuyers)
                    i = 0
                    while i < len(combination):
                        bestData.append(combination[i])
                        i = i + 1
            permAndComb = permAndComb + 1
        permNum = permNum + 1  # For testing
        print("Permutation number ", permNum, "Combination number ", permAndComb)
        
    print(bestData)    # For testing 
    return bestRajJainCostFairness
        
    #splitfinder to find all combinations of all permutations 
    
    #test the validity of all the combinations (not buying a block with a previous block unbought, demand fullfilled
    
    #for the valid combinations: calculate the average price each buyer paid and place these in a list
    
    #feed this list to the Raj Jain Fairness method and place the result in a big list together with other relevant data for each tried combination
    
    #after every combination: sort the list and return the highest fairness index
    
    #Make all of this modular so that the Fairness Index is easily switched to something else.
    

# Find all possible ways to split the blocks between the buyers (including one "buyer" for unbought blocks)
# Assumes that only the "unbought" blocks can be empty since every buyer should have a demand
def splitfinder(blocklist, numBuyers):
    
    possibleSplits = []
    for breakpoints in combinations(range(1, len(blocklist)+1), numBuyers):  # Combinatorics: find all places to place splitpoints between groups
        possibilityN = []
        
        possibilityN.append(list(blocklist[0:breakpoints[0]]))
        for i in range(0, numBuyers-1):
            possibilityN.append(list(blocklist[breakpoints[i]:breakpoints[i+1]]))
        possibilityN.append(list(blocklist[breakpoints[(len(breakpoints)-1)]:(len(blocklist))]))
        
        possibleSplits.append(list(possibilityN))
    return possibleSplits

# Takes in a way to split the blocks between the buyers and returns whether what they have bought is allowed and whether their demand is fullfilled
def validCombination(Combination, buyers):
    possibleCombination = Combination.copy() # To prevent the original list from being changed through references
    unboughts = possibleCombination.pop()
    for unboughtBlock in unboughts:
        if(checkIfPreviousBlockUnbought(unboughtBlock, possibleCombination) == False):
            return False
    
    buyerIndex = 0
    for buyerBoughts in possibleCombination:
        demand = buyers[buyerIndex].needs
        for block in buyerBoughts:
            demand = demand - block.get_amount()
        if(demand > 0):
            return False
    buyerIndex = buyerIndex + 1
            
    return True
    
# Recursively check if a block that has to be bought after another block has been bought without this being the case
def checkIfPreviousBlockUnbought(unboughtBlock, boughtBlocks):    
    if(unboughtBlock.next() != None):
        for blockset in boughtBlocks:
            if(unboughtBlock.next() in blockset):
                return False
            else:
                return checkIfPreviousBlockUnbought(unboughtBlock.next(), boughtBlocks)
    else:
        return True
    
# Calculation of Raj Jain's fairness index following Wikipedia equation
def rajJainFairness(metricList):
    numerator = 0
    denominator = 0
    for metric in metricList:
        numerator = numerator + metric
        denominator = denominator + (metric**2)
        
    numerator = numerator**2
    denominator = denominator * len(metricList)
    
    fairnessIndex = numerator / denominator
    return fairnessIndex

# Feed this function a valid set of blocks for a seller to buy and it will return the average cost paid
def averageCost(boughtBlocks):
    sum = 0
    totAmount = 0
    for block in boughtBlocks:
        discount = findDiscount(block,boughtBlocks)
        sum = sum + (block.get_amount() * (block.get_price() - discount))
        totAmount = totAmount + block.get_amount()
    return sum / totAmount

# Finds the discount that should be applied to a given block recursivly under the assumption that block.discount is the cumulative discount on a base price given all previous blocks are bought 
# Block = Block discount is sought for, boughtBlocks = The blocks bought by a buyer, foundPrevBlocks = recursion variable, init at 0
# Goes back to the beginning of the sellers blockchain, finding how many blocks in that chain have been purchased. Then goes to the "index" in that blockchain that 
# corresponds to the number of blocks found, there finding the discount of if the block had been moved to that place in the chain.
def findDiscount(block, boughtBlocks, foundPrevBlocks = 0):
    if (block.prev() != None):
        if(block.prev() in boughtBlocks):
            foundPrevBlocks = foundPrevBlocks + 1
        return findDiscount(block.prev(), boughtBlocks, foundPrevBlocks)
    else:
        discount = 0
        while foundPrevBlocks > 0:
            discount = block.next().get_discount()
            block = block.next()
            foundPrevBlocks = foundPrevBlocks - 1
        return discount
            

def demo():

    # blocklist = ["block11", "block12", "block21", "block31"]
    # buyers = 2
    # blocklist = ["block11", "block12", "block13", "block21", "block22", "block31"]
    # buyers = 3
    
    # splits = splitfinder(blocklist, buyers)
    # print("\nPossible combinations:")
    # for split in splits:
    #      print(split)
    
    
    # demoMetrics = [10, 10, 10, 10, 10]    
    # #demoMetrics = [5.5, 10, 7.6, 3]
    # #demoMetrics = [121, 220, 150, 89, 95, 140, 190]
    
    # print("\n Rai Jain's fairness index given the input", demoMetrics, "\n", rajJainFairness(demoMetrics), "\n")
    
    # Demo 2:
    
    block1 = AuctionBlock("block1")
    block2 = AuctionBlock("block2")
    block3 = AuctionBlock("block3")
    block4 = AuctionBlock("block4")
    block5 = AuctionBlock("block5")
    
    block1.set_amount(1)
    block2.set_amount(2)
    block3.set_amount(3)
    block4.set_amount(4)
    block5.set_amount(5)
    
    block1.set_price(5)
    block2.set_price(5)
    block3.set_price(5)
    block4.set_price(5)
    block5.set_price(5)
    
    block1.set_discount(0)
    block2.set_discount(1)
    block3.set_discount(2)
    block4.set_discount(3)
    block5.set_discount(4)
    
    block1.set_nextBlock(block2)
    block2.set_nextBlock(block3)
    block3.set_nextBlock(block4)
    block4.set_nextBlock(block5)
    
    
    block2.set_prevBlock(block1)
    block3.set_prevBlock(block2)
    block4.set_prevBlock(block3)
    block5.set_prevBlock(block4)
    
    buyer1 = Bidder(0,"Buyer",0,3,0,0)
    buyer2 = Bidder(0,"Buyer",0,5,0,0)
    buyer3 = Bidder(0,"Buyer",0,8,0,0)
    
    blocklist = [block1,block2,block3,block4,block5]
    buyerlist = [buyer1, buyer2]
    #buyerlist = [buyer1, buyer2, buyer3] # Show returning -1 when no solution can be found
    
    print(referenceCalculator(blocklist, buyerlist))
    
    
demo()
    
# TODO: Firstly fix checkIfPreviousBlockUnbought not working properly, then do the rest