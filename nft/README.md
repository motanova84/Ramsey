# AIK Beacons NFT Integration – Proof of Mathematical Truth

## Overview

This system implements an ERC721 NFT collection on Base network where NFTs are only minted if the associated AIK Beacon mathematical proof is valid. Each NFT serves as an immutable on-chain certificate of mathematical truth, verified through both off-chain validation and on-chain signature verification.

## Features

- **Proof-of-Math Minting**: NFTs are only minted when mathematical proofs are verified
- **ECDSA Signature Verification**: Creator signature required for each mint
- **Hash Validation**: On-chain hash verification ensures beacon integrity
- **IPFS Integration**: Metadata and proofs stored on IPFS for permanence
- **Limited Supply**: Maximum 100 NFTs for scarcity

## Requirements

- Node.js 18+
- MetaMask or WalletConnect compatible wallet
- Pinata API keys for IPFS (optional, for production)
- Base network ETH for gas fees

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create a `.env` file in the repository root:

```env
BASE_RPC_URL=https://sepolia.base.org  # Use mainnet.base.org for production
PRIVATE_KEY=your_wallet_private_key_here  # Never commit this!
PINATA_API_KEY=your_pinata_key
PINATA_SECRET_API_KEY=your_pinata_secret
```

### 3. Compile Contract

```bash
npx hardhat compile --config hardhat.config.cjs
```

### 4. Deploy to Testnet

```bash
npx hardhat run nft/scripts/deploy.js --network baseTestnet --config hardhat.config.cjs
```

### 5. Mint NFTs

```bash
# Single mint
node nft/scripts/mint-nft.js <contract-address> data/verified_bound_R55.json

# Batch mint (5 NFTs)
node nft/scripts/batch-mint.js <contract-address>
```

## Complete Workflow

1. **Generate Beacon**: Use the QCAL framework to create a mathematical proof beacon
   ```bash
   python ai_ramsey_formal.py certify 5 5 --output certificates/
   ```

2. **Prepare Metadata**: Generate NFT metadata from beacon
   ```bash
   node nft/scripts/upload-to-ipfs.js data/verified_bound_R55.json Rpsi55
   ```

3. **Upload to IPFS**: Upload metadata and beacon to IPFS (via Pinata)

4. **Mint NFT**: Mint the NFT with the IPFS CIDs
   ```bash
   node nft/scripts/mint-nft.js <contract-address>
   ```

5. **Verify**: Check the transaction on Basescan and verify the proof
   ```bash
   python ai_ramsey_formal.py verify
   ```

## Directory Structure

```
nft/
├── contracts/              # Solidity smart contracts
│   └── AIKBeaconsProofOfMath.sol
├── scripts/               # Deployment and minting scripts
│   ├── deploy.js          # Contract deployment
│   ├── upload-to-ipfs.js  # IPFS upload preparation
│   ├── mint-nft.js        # Single NFT minting
│   ├── batch-mint.js      # Batch minting (5 NFTs)
│   └── wallet-mint.html   # Web DApp for minting
├── metadata/              # Generated metadata files
├── docs/                  # Additional documentation
│   └── SECURITY_AUDIT.md
├── tests/                 # Hardhat tests
│   └── test-mint.js
├── beacons/              # IPFS beacon references
└── README.md             # This file
```

## Contract Details

### AIKBeaconsProofOfMath

- **Name**: AIK Beacons - Proof of Mathematical Truth
- **Symbol**: AIK
- **Standard**: ERC721 with URIStorage
- **Max Supply**: 100 tokens

### Key Functions

| Function | Description |
|----------|-------------|
| `mintIfValidProof()` | Mint NFT if proof is valid |
| `verifyProof()` | Check if a token's proof is valid |
| `beaconHash()` | Get the hash for a token |
| `beaconCID()` | Get the IPFS CID for a token |

### Events

| Event | Description |
|-------|-------------|
| `BeaconMinted` | Emitted when a new NFT is minted |

## Networks

| Network | Chain ID | RPC URL |
|---------|----------|---------|
| Base Mainnet | 8453 | https://mainnet.base.org |
| Base Sepolia (Testnet) | 84532 | https://sepolia.base.org |

## Initial NFT Collection

The first 5 NFTs in the collection:

| Token ID | Theorem | Description |
|----------|---------|-------------|
| #000 | R(5,5) = 43 | Vibrational proof via QCAL framework |
| #001 | Rψ(5,5; f₀=141.7001 Hz) ≤ 16 | Vibrational Ramsey model |
| #002 | QCAL ∞³ Framework | Universal coherence beacon |
| #003 | Rψ(3,3) Certification | Vibrational cert for R(3,3) |
| #004 | Rψ(4,4) Certification | Vibrational cert for R(4,4) |

## Security

- Only the contract owner can mint NFTs
- ECDSA signature verification ensures authenticity
- Hash verification prevents beacon tampering
- Based on audited OpenZeppelin contracts

See [SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md) for detailed security information.

## Testing

Run the test suite:

```bash
npx hardhat test nft/tests/test-mint.js --config hardhat.config.cjs
```

## Web DApp

Open `nft/scripts/wallet-mint.html` in a browser to use the web-based minting interface:

1. Connect MetaMask
2. Select beacon to mint
3. Confirm transaction
4. View NFT on OpenSea/Basescan

## Contributing

1. Fork the repository
2. Test on Base Sepolia testnet
3. Submit a PR with new beacon proposals

## Links

- **Repository**: https://github.com/motanova84/Ramsey
- **Contract**: [View on Basescan](https://basescan.org/address/YOUR_CONTRACT_ADDRESS)
- **OpenSea Collection**: [View Collection](https://opensea.io/collection/aik-beacons)
- **QCAL Framework**: Part of the QCAL ∞³ unified theory

## License

MIT License - See [LICENSE](../LICENSE) for details

## Credits

- **Author**: José Manuel Mota Burruezo (JMMB Ψ✧∴)
- **Institution**: Instituto Consciencia Cuántica (ICQ)
- **Framework**: QCAL ∞³ (Quantum Coherent Algebraic Logic)
