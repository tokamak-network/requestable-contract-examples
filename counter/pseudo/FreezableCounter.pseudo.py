# for checking global counting state(number),
# you should check whether this counter contract is freezed or not.
contract FreezableCounter is Requestable:

    uint currentNumber # counter's number state
    bool isFreeze # freeze state of counter

    # constructer function
    def FreezableCounter():
        currentNumber = 0

    # It manipulates root chain's state(state transition in root chain)
    def applyRequestInRootChain(isEnter, exchangingNumber):
        # state transition of root chain for exit
        if isEnter:
            require(currentNumber == exchangingNumber)
            _freeze()
        # state transition of root chain for enter
        else:
            require(exchangingNumber >=  currentNumber)
            _unfreeze()
            currentNumber = exchangingNumber

    # It manipulates child chain's state(state transition in child chain)
    def applyRequestInChildChain(isExit, exchangingNumber):
        # state transition of child chain for exit
        if isEnter:
            # require(exchangingNumber >=  currentNumber)
            _unfreeze()
            currentNumber = exchangingNumber
        # state transition of child chain for enter
        else:
            require(currentNumber == exchangingNumber)
            _freeze()

    # main counting function for user
    def count():
        require(isFreeze == False)
        currentNumber += 1

    def _freeze():
        isFreeze = True

    def _unfreeze():
        isFreese = False
