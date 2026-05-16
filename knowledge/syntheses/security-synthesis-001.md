# Smart Contract Security: Vulnerability Clusters and Audit Framework

## Source Items (9 items synthesized)
1. Reentrancy Patterns: Taxonomy, Detection, and Defense
2. ERC-2771 ForwardRequest Security: Attack Vectors and Three-Gate Defense
3. Gas Griefing Attacks in Ethereum Smart Contracts
4. Signature Replay Vulnerability Patterns
5. Access Control Vulnerabilities in Solidity
6. Timestamp Dependence Risks
7. Integer Overflow/Underflow Patterns
8. Front-Running Attack Vectors
9. Delegatecall Injection Patterns

## Citation Edges Created: 9

## Key Vulnerability Clusters

### Cluster 1: Reentrancy (Severity: Critical)
- Single-function reentrancy
- Cross-function reentrancy  
- Cross-contract reentrancy
- Read-only reentrancy

### Cluster 2: Access Control (Severity: High)
- Missing modifier checks
- Permission escalation
- Owner-only functions exposed

### Cluster 3: replay attacks (Severity: High)
- ERC-2771 forwarder exploitation
- Signature replay without domain separation
- Nonce reuse vulnerabilities

## Defense Framework
1. Checks-Effects-Interactions pattern
2. Reentrancy guards (nonReentrant modifier)
3. Canonical forwarder pinning (ERC-2771)
4. Domain-separated signatures (EIP-712)
5. Pull payment pattern over push payments
