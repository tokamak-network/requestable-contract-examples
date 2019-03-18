# for checking global counting state(number),
# you should check whether ancestor(or ascendent) counter contract is initialized or not.
contract IncreaseDecreaseCounter is Requestable:

    uint currentNumber # counter's number state

    # constructer function
    def InitializableCounter():
        currentNumber = 0

    # It manipulates root chain's state(state transition in root chain)
    def applyRequestInRootChain(isExit, exchangingNumber):
        # state transition of root chain for exit
        if !isExit:
            require(currentNumber >= exchangingNumber)
            currentNumber -= exchangingNumber
        # state transition of root chain for enter
        else:
            currentNnumber += exchangingNumber

    # It manipulates child chain's state(state transition in child chain)
    # null-account executes this function
    def applyRequestInChildChain(isExit, exchangingNumber):
        # state transition of child chain for exit
        if !isExit:
            currentNnumber += exchangingNumber
        # state transition of child chain for enter
        else:
            require(currentNumber >= exchangingNumber)
            currentNumber -= exchangingNumber

    # main counting function for user
    def count():
        currentNumber += 1

    def isInitialized():
        if currentNumber == 0:
            return True
        else:
            return false
