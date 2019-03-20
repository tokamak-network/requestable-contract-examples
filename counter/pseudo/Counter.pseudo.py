
### TB - ... - CB - [CB + 1]
##   ㄴ-------------- URB
## URB 가 success 되었으니 CB + 1 에서 revert 되는 경우


## TB: counter 3
## CB: counter 4

## ERU : exit 3 (succeess in URB, reverted in CB+1)
## ERO : exit 4 (succeess in CB + 2)

# for checking global counting state(number),
# you should check whether this counter contract is freezed or not.
contract Counter is Requestable:

    address owner
    uint currentNumber # counter's number state

    # constructer
    def Counter():
        currentNumber = 0
        owner = msg.sender

    # It manipulates root chain's state(state transition in root chain)
    def applyRequestInRootChain(isExit, exchangingNumber):
        # state transition of root chain for enter
        if !isExit:
            require(currentNumber >= exchangingNumber)
            currentNumber -= exchangingNumber

        # state transition of root chain for exit
        else:
            currentNumber += exchangingNumber

    # It manipulates child chain's state(state transition in child chain)
    def applyRequestInChildChain(isExit, exchangingNumber):
        # state transition of child chain for enter
        if !isExit:
            currentNumber += exchangingNumber

        # state transition of child chain for exit
        else:
            require(currentNumber == exchangingNumber)
            currentNumber -= exchangingNumber


    def count():
        require(msg.sender == owner)
        currentNumber += 1
