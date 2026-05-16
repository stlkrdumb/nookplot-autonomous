// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Reentrancy Vulnerability Detector
/// @notice Static analysis tool for detecting reentrancy patterns in Solidity contracts
/// @dev Run this as a static analysis pass — not deployed code

import "./access-control-analyzer.sol";

library ReentrancyDetector {
    struct Finding {
        string vulnerabilityType;
        string functionName;
        uint256 severity; // 1=low, 2=medium, 3=high, 4=critical
        string description;
    }

    /// @notice Analyze a contract for reentrancy vulnerabilities
    /// @param target The target contract address
    /// @return findings Array of identified vulnerabilities
    function detect(address target) external view returns (Finding[] memory) {
        // Implementation would interface with static analysis engine
        // This is a template for the detection pattern
        Finding[] memory results = new Finding[](0);
        return results;
    }

    /// @notice Check if external call precedes state mutation
    /// @dev Pattern: external call -> state change = reentrancy risk
    function hasExternalCallBeforeStateChange(
        address[] calldata callTargets,
        uint256[] calldata callOrder,
        uint256 stateChangeOrder
    ) external pure returns (bool) {
        for (uint i = 0; i < callTargets.length; i++) {
            if (callOrder[i] < stateChangeOrder && callTargets[i] != address(0)) {
                return true;
            }
        }
        return false;
    }

    /// @notice Identify missing nonReentrant guards on externally callable functions
    function missingNonReentrantGuard(
        bytes4[] calldata functionSelectors,
        bool[] calldata hasGuard
    ) external pure returns (uint256[] memory) {
        uint256 count = 0;
        for (uint i = 0; i < functionSelectors.length; i++) {
            if (!hasGuard[i]) count++;
        }
        
        uint256[] memory unprotected = new uint256[](count);
        uint256 idx = 0;
        for (uint i = 0; i < functionSelectors.length; i++) {
            if (!hasGuard[i]) {
                unprotected[idx++] = i;
            }
        }
        return unprotected;
    }
}
