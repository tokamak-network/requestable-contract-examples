pragma solidity ^0.4.24;

import {SimpleDecode} from "../lib/SimpleDecode.sol";
import {RequestableI} from "../lib/RequestableI.sol";
import {BaseCounter} from "./BaseCounter.sol";
import {SafeMath} from "openzeppelin-solidity/contracts/math/SafeMath.sol";


contract TrackableCounter is BaseCounter, RequestableI {
  // SimpleDecode library to decode trieValue.
  using SimpleDecode for bytes;
  using SafeMath for *;

  // trie key for state variable `n`.
  bytes32 constant public TRIE_KEY_N = 0x00;

  // previous count before enter request in root chain and exit request in child chain.
  uint public requestableN;

  // address of RootChain contract.
  address public rootchain;

  mapping (uint => bool) appliedRequests;

  constructor(address _rootchain) {
    rootchain = _rootchain;
  }

  /// @dev override BaseCounter.count function.
  function count() external {
    requestableN++;
    n++;
    emit Counted(n);
  }

  function applyRequestInRootChain(
    bool isExit,
    uint256 requestId,
    address requestor,
    bytes32 trieKey,
    bytes trieValue
  ) external returns (bool success) {
    require(!appliedRequests[requestId]);
    require(msg.sender == rootchain);

    // only accept request for `n`.
    require(trieKey == TRIE_KEY_N);
    uint _n = trieValue.toUint()
    if (isExit) {
      n = n.add(_n);
    } else {
      requestableN = requestableN.sub(_n);
    }

    appliedRequests[requestId] = true;
  }

  function applyRequestInChildChain(
    bool isExit,
    uint256 requestId,
    address requestor,
    bytes32 trieKey,
    bytes trieValue
  ) external returns (bool success) {
    require(!appliedRequests[requestId]);
    require(msg.sender == address(0));

    // only accept request for `n`.
    require(trieKey == TRIE_KEY_N);

    if (isExit) {
      requestableN = requestableN.sub(_n);
    } else {
      n = n.add(_n);
    }

    appliedRequests[requestId] = true;
  }
}