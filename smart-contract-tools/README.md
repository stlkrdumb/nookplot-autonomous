# Smart Contract Security Tools

A collection of Solidity smart contract security analysis tools, templates, and verification scripts.

## Tools

### `reentrancy-detector.sol`
Static analysis tool for detecting reentrancy vulnerabilities in Solidity contracts.
- Checks Effects-Interactions compliance
- Identifies external calls before state changes
- Flags missing nonReentrant modifiers

### `access-control-analyzer.sol`
Scans for access control vulnerabilities.
- Identifies missing modifier checks
- Flags publicly accessible setters
- Reports permission escalation vectors

### `signature-replay-checker.sol`
Detects signature replay vulnerabilities.
- Checks domain separator usage (EIP-712)
- Validates nonce implementation
- Flags missing replay protection

## Usage

```bash
# Compile all tools
forge build

# Run static analysis
forge test --match-path "test/*.sol"
```

## License
MIT
