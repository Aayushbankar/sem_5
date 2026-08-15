// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SimpleStorage
/// @notice A "Hello World" of smart contracts: store and read a number.
contract SimpleStorage {
    // State variable - permanently stored on the blockchain (storage)
    uint256 public storedNumber;

    // Event emitted every time the value changes (easy to watch off-chain)
    event NumberChanged(address indexed by, uint256 oldValue, uint256 newValue);

    /// @dev Reads the current stored number (view = no gas cost to call).
    function read() public view returns (uint256) {
        return storedNumber;
    }

    /// @dev Writes a new number (state change -> costs gas).
    function store(uint256 _newNumber) public {
        uint256 oldValue = storedNumber;
        storedNumber = _newNumber;
        emit NumberChanged(msg.sender, oldValue, _newNumber);
    }

    /// @dev Example of payable function + msg.sender.
    function whoAmI() public view returns (address) {
        return msg.sender;
    }
}
