#!/usr/bin/env python3
"""
RLM Security Challenge Analyzer
Analyzes patterns across all 20 RLM security challenge types on Nookplot.
Identifies common vulnerability categories, key patterns, and recommended approaches.
"""

CHALLENGES = {
    "reentrancy": [
        {"id": "ccdd736f-7e2b-4fef-830c-c510a464a32f", "title": "Read-only reentrancy", "difficulty": "expert", "reward": "~44K"},
        {"id": "9798e20e-f916-4d88-8786-6e1f13d3d919", "title": "SWC-107 reentrancy in lending", "difficulty": "hard", "reward": "~13K"},
        {"id": "3e58d5ae-3f09-4185-872e-59dc8c67cb65", "title": "Cross-function reentrancy", "difficulty": "hard", "reward": "~13K"},
    ],
    "access_control": [
        {"id": "f1606d60-3b51-4525-9e69-46f6af2569ae", "title": "tx.origin auth bug", "difficulty": "hard", "reward": "~13K"},
        {"id": "5d0b8088-ffca-43ee-a192-427ee2c8877c", "title": "Uninitialized proxy initialize() race", "difficulty": "hard", "reward": "~13K"},
        {"id": "f473d6bb-2f2f-48ae-8c15-2e1c6e4ff541", "title": "Missing-modifier privileged setter", "difficulty": "easy", "reward": "~873"},
    ],
    "signature_replay": [
        {"id": "e4942a90-5ceb-41c7-bbc5-477c99839a83", "title": "Replay-drain on missing-nonce permit", "difficulty": "hard", "reward": "~13K"},
        {"id": "7426bad1-64ce-4e29-a7f1-b180e4715388", "title": "Signature-replay variant", "difficulty": "medium", "reward": "~4K"},
    ],
    "flash_loan": [
        {"id": "56ded58e-bc95-46d6-b1cf-00312c267b8a", "title": "Flash-loan governance attack", "difficulty": "expert", "reward": "~44K"},
        {"id": "28ba7bf2-9325-465a-844d-a2af6728f029", "title": "Flash-loan drain on spot-oracle", "difficulty": "hard", "reward": "~13K"},
    ],
    "oracle_manipulation": [
        {"id": "c164e587-83ce-4454-8e0b-b6005ba61b06", "title": "Oracle-flaw severity+root+fix", "difficulty": "hard", "reward": "~13K"},
        {"id": "368a54c0-5605-49b0-a83b-aa6f66425fd5", "title": "Oracle-read flaw across price-feed", "difficulty": "medium", "reward": "~4K"},
    ],
    "dos_gas": [
        {"id": "b155e5cd-8264-469d-b8ed-5582d923a513", "title": "Gas-griefing primitive + fix", "difficulty": "hard", "reward": "~13K"},
        {"id": "f1ae04ae-89d4-41c6-97d8-8cfbac3504f7", "title": "DoS variant across denial-of-service", "difficulty": "medium", "reward": "~4K"},
    ],
    "precision_loss": [
        {"id": "dced9067-8164-46c3-abc7-e8e173690cbf", "title": "Precision-loss tokens-burned via div", "difficulty": "hard", "reward": "~13K"},
        {"id": "decd3c83-cae1-4561-83e8-cb51d25e5d9b", "title": "Pre-0.8 overflow result for uint8 fee", "difficulty": "medium", "reward": "~4K"},
    ],
    "mev_sandwich": [
        {"id": "299cd162-57b9-4361-8817-b2be4e6ee8d2", "title": "Sandwich-attack profit on zero-slippage", "difficulty": "hard", "reward": "~13K"},
        {"id": "aa65b262-b5cf-4d14-bb02-b16c4ef6e7ef", "title": "MEV variant + protection", "difficulty": "medium", "reward": "~4K"},
    ],
}

CATEGORY_PATTERNS = {
    "reentrancy": {
        "swc": "SWC-107",
        "key_functions": ["withdraw", "transfer", "send", "call"],
        "indicators": ["state changes after external call", "no reentrancy guard", "checks-effects-interactions violation"],
        "fix": "Use checks-effects-interactions pattern + ReentrancyGuard",
    },
    "access_control": {
        "swc": "SWC-100 / SWC-105",
        "key_functions": ["setOwner", "setFee", "setToken", "initialize"],
        "indicators": ["missing onlyOwner", "tx.origin instead of msg.sender", "uninitialized proxy"],
        "fix": "Use Ownable + initializer pattern with OZ",
    },
    "signature_replay": {
        "swc": "SWC-121",
        "key_functions": ["permit", "execute"],
        "indicators": ["no nonce", "no deadline", "no chainId", "no domain separator verification"],
        "fix": "Implement EIP-712 domain separator + nonce monotonicity + deadline",
    },
    "flash_loan": {
        "key_functions": ["flashLoan", "executeOperation"],
        "indicators": ["no user-specific amount check", "unchecked return", "state not updated atomically"],
        "fix": "Update state BEFORE external call; check accounting",
    },
    "oracle_manipulation": {
        "swc": "SWC-104",
        "key_functions": ["getPrice", "latestAnswer", "latestRoundData"],
        "indicators": ["no staleness check", "no spread check", "single source"],
        "fix": "Check roundID + timestamp + heartbeat; use TWAP or multi-source",
    },
}

def print_summary():
    print("=" * 70)
    print("RLM SECURITY CHALLENGE ANALYSIS - NOOKPLOT MINING")
    print("=" * 70)
    print()
    total = sum(len(v) for v in CHALLENGES.values())
    print(f"Total RLM Security Challenges: {total}")
    print(f"Categories: {len(CHALLENGES)}")
    print()
    for category, challenges in CHALLENGES.items():
        print(f"  [{category.upper()}] {len(challenges)} challenges")
        for c in challenges:
            print(f"    - {c['title']} ({c['difficulty']}, {c['reward']})")
    print()
    print("PATTERN REFERENCE:")
    for cat, data in CATEGORY_PATTERNS.items():
        print(f"\n  {cat.upper()}:")
        for k, v in data.items():
            print(f"    {k}: {v}")

if __name__ == "__main__":
    print_summary()