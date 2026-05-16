// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Access Control Vulnerability Analyzer
/// @notice Detects missing modifier checks and permission escalation vectors

library AccessControlAnalyzer {
    enum PrivilegeLevel {
        None,
        Owner,
        Admin,
        User,
        Guest
    }

    struct AccessFinding {
        string functionName;
        PrivilegeLevel requiredLevel;
        PrivilegeLevel actualLevel;
        uint256 severity;
        string recommendation;
    }

    /// @notice Scan for publicly accessible state-changing functions
    /// @dev Functions without modifiers that write to state
    function scanPublicSetters(
        string[] calldata functionNames,
        bool[] calldata hasAccessControl,
        bool[] calldata isExternal
    ) external pure returns (uint256[] memory) {
        uint256 count = 0;
        for (uint i = 0; i < functionNames.length; i++) {
            if (!hasAccessControl[i] && isExternal[i]) {
                count++;
            }
        }
        
        uint256[] memory unprotected = new uint256[](count);
        uint256 idx = 0;
        for (uint i = 0; i < functionNames.length; i++) {
            if (!hasAccessControl[i] && isExternal[i]) {
                unprotected[idx++] = i;
            }
        }
        return unprotected;
    }

    /// @notice Check for missing onlyOwner on administrative functions
    /// @param functionSelectors Array of function selectors to check
    /// @param hasOnlyOwner Array of booleans indicating if each has onlyOwner
    function checkOwnerGating(
        bytes4[] calldata functionSelectors,
        bool[] calldata hasOnlyOwner
    ) external pure returns (bytes4[] memory) {
        uint256 count = 0;
        for (uint i = 0; i < functionSelectors.length; i++) {
            if (!hasOnlyOwner[i]) count++;
        }
        
        bytes4[] memory unguarded = new bytes4[](count);
        uint256 idx = 0;
        for (uint i = 0; i < functionSelectors.length; i++) {
            if (!hasOnlyOwner[i]) unguarded[idx++] = functionSelectors[i];
        }
        return unguarded;
    }
}
