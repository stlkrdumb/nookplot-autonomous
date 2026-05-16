# Security Analysis Methodology

## Smart Contract Audit Framework

### Phase 1: Reconnaissance
1. Identify contract purpose and deployment context
2. Map external dependencies and interaction patterns
3. Enumerate privileged functions and access control mechanisms

### Phase 2: Static Analysis
1. Check for CEI (Checks-Effects-Interactions) violations
2. Enumerate all external calls and their ordering relative to state updates
3. Scan for missing access control modifiers on privileged functions
4. Identify storage collision vectors in proxy patterns

### Phase 3: Signature Verification Analysis
1. Validate domain separator construction (EIP-712)
2. Check nonce monotonicity enforcement
3. Verify deadline validation in signature verification
4. Confirm canonical forwarder pinning (ERC-2771)

### Phase 4: Gas Analysis
1. Map gas-intensive operations (storage writes, external calls)
2. Identify array iteration vulnerabilities (gas griefing)
3. Check for gas-left() dependent logic that can be manipulated

## Vulnerability Severity Classification

| Severity | Impact | Example |
|---|---|---|
| Critical | Total fund loss or complete contract compromise | Reentrancy with unchecked external call |
| High | Significant fund loss or major functionality compromise | Missing access control on withdrawal |
| Medium | Moderate impact or exploitable under specific conditions | Gas griefing in batch operations |
| Low | Minimal impact or theoretical exploit | Missing event emissions |

## Common Vulnerability Patterns

### Reentrancy
- External call before state update
- Missing nonReentrant modifier
- Cross-function shared state exploitation

### Access Control
- Missing modifier on administrative functions
- tx.origin usage for authentication
- Permission escalation via missing checks

### Signature Replay
- Missing domain separator
- Nonce not incremented after use
- No deadline validation

### Storage Manipulation
- EIP-1967 slot manipulation in proxies
- Storage collision via delegatecall
- Implementation pointer overwrite
