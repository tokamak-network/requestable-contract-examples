#
# Gaussian Summation : [1,2,3, ... 100]
# Array[1,2,3, ... 100] is stored at outside of blockchain
# Let's say there is no Oracle Problem
####
#### State Description
####
# Root Chain <====================> Child Chain
# 2  + 1  = [3,  True]
# 3  + 3  = [6,  True]
# 4  + 6  = [10, True]
# 5  + 10 = [15, False] => Enter => 5  + 10 = [15, True]
#                                   6  + 15 = [21, True]
#                                   7  + 21 = [28, True]
# 8  + 28 = [36, True]  <= Exit <== 8  + 28 = [36, False]
# 9  + 36 = [45, True]
# 10 + 45 = [55, True]
#...

contract GaussianSum is Requestable:

    struct Result {
        uint resultSum;
        bool exchangeable;
    }

    # store data twice, it is inefficient. It should be optimized later.
    mapping(uint => uint) unitLeft;
    mapping(uint => mapping(uint => Result)) unitSum;


    # constructer function
    def FreezableCounter():
        currentNumber = 0

    # It manipulates root chain's state(state transition in root chain)
    def applyRequestInRootChain(isExit, exchangingIndex, exchangingAdded):
        # state transition of root chain for exit
        if isExit:
            _checkExitPossibilityInRootChain(exchangingIndex)
            __fillJustInValue(exchangingIndex, exchangingAdded)
        # state transition of root chain for enter
        else:
            _isExchangeable(exchangingIndex)
            _setUnexchangeable(exchangingIndex)

    # It manipulates child chain's state(state transition in child chain)
    def applyRequestInChildChain(isExit, exchangingIndex, exchangingAdded):
        # state transition of child chain for exit
        if isExit:
            # Should be changed.
            # current logic does not cover that no previous exit in childchain does not exist.
            _setUnexchangeable(exchangingIndex)
        # state transition of child chain for enter
        else:
            __fillJustInValue(exchangingIndex, exchangingAdded)

    # main counting function for user
    def sum(index):
        # previous
        uint memory previousAdded = uintLeft[index-1]
        uint memory previousSum = unitSum[index-1][previousSum].resultSum
        # get current
        uint memory currentSum = uintSum[index][previousSum].resultSum

        # Check if (index - 1) data exist
        require(previousAdded != False)
        # Check if current index does not exist
        require(currentSum == False)
        # Check if (index -1) data is exchangeable or not
        require(uintSum[index-1][uintLeft[index-1]].exchangeable == True)

        # insert current index data
        uintLeft[index] = index + added
        unitSum[index][added].resultSum = index + previousSum
        unitSum[index][added].exchangeable = True

    def _isExchangeable(index):
        uint memory currentSum = unitLeft[index]
        uint memory nextSum = unitLeft[index+1]
        bool memory isCurrentExchangeable = unitSum[index+1][currentSum].exchangeable
        # check if current data exist
        require(currentSum != False)
        # check if current data is exchangeable
        require(isCurrentExchangeable == True)
        # check if next data exist
        require(nextSum != False)

    def _checkExitPossibilityInRootChain(index):
        # check if previous value does not exist or
        # current exchangeable False and next value does not exist
        uint memory previousAdded = unitLeft[index-1]
        uint memory previousSum = index - 1 + previousAdded
        bool memory previousExchangeableFlag = unitSum[index-1][previousAdded].exchangeable

        bool memory currentExchangeableFlag = uintSum[index][previousSum].exchangeable
        uint memory nextAdded = unitLeft[index+1]

        require(!previousAdded or (!previousExchangeableFlag and nextAdded))

    def _setUnexchangeable(index):
        uint memory previousSum = unitLeft[index-1]
        unitSum[index][previousSum].exchangeable = False

    def _setExchangeable(index):
        uint memory previousSum = unitLeft[index-1]
        unitSum[index][previousSum].exchangeable = True

    def __fillJustInValue(index, added):
        unitLeft[index] = added
        unitSum[index][added].resultSum = index+added
        unitSum[index][added].exchangeable = True
