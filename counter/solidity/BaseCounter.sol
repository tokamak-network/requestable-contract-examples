pragma solidity ^0.4.24;


contract BaseCounter {
  uint n;

  event Counted(uint _n);

  function count() external {
    n++;
    emit Counted(n);
  }

  function getCount() external view returns (uint) {
    return n;
  }
}