const { ethers } = require("ethers");
require('dotenv').config();
const fs = require('fs');

// ABI for the AIKBeaconsProofOfMath contract (minimal subset for minting)
const CONTRACT_ABI = [
  "function mintIfValidProof(string theorem, string proofFileCID, string beaconCID, bytes32 expectedBeaconHash, bytes signature) external",
  "function totalSupply() view returns (uint256)",
  "function verifyProof(uint256 tokenId) view returns (bool)",
  "function beaconCID(uint256 tokenId) view returns (string)",
  "event BeaconMinted(uint256 indexed tokenId, bytes32 beaconHash, string theorem)"
];

/**
 * Mint an AIK Beacon NFT
 * @param {string} contractAddress - Deployed contract address
 * @param {string} theorem - The theorem statement
 * @param {string} proofFileCID - IPFS CID of the proof file
 * @param {string} beaconCID - IPFS CID of the beacon JSON
 * @param {bytes32} expectedBeaconHash - Expected hash of the beacon (keccak256 of beaconCID)
 */
async function mintBeacon(contractAddress, theorem, proofFileCID, beaconCID, signature) {
  // Connect to network
  const rpcUrl = process.env.BASE_RPC_URL || "https://sepolia.base.org";
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  
  // Load wallet from private key
  if (!process.env.PRIVATE_KEY) {
    throw new Error("PRIVATE_KEY not set in .env file");
  }
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
  console.log("Minting with wallet:", wallet.address);
  
  // Connect to contract
  const contract = new ethers.Contract(contractAddress, CONTRACT_ABI, wallet);
  
  // Calculate expected hash
  const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
  console.log("Expected beacon hash:", expectedBeaconHash);
  
  // Get current total supply
  const currentSupply = await contract.totalSupply();
  console.log("Current supply:", currentSupply.toString());
  
  // Mint the NFT
  console.log("Minting NFT...");
  console.log("  Theorem:", theorem);
  console.log("  Beacon CID:", beaconCID);
  
  const tx = await contract.mintIfValidProof(
    theorem,
    proofFileCID,
    beaconCID,
    expectedBeaconHash,
    signature
  );
  
  console.log("Transaction submitted:", tx.hash);
  const receipt = await tx.wait();
  console.log("Transaction confirmed in block:", receipt.blockNumber);
  
  // Get the new token ID
  const newSupply = await contract.totalSupply();
  const tokenId = newSupply - 1n;
  console.log("New NFT Token ID:", tokenId.toString());
  
  // Verify the proof on-chain
  const isValid = await contract.verifyProof(tokenId);
  console.log("Proof valid on-chain:", isValid);
  
  return {
    tokenId: tokenId.toString(),
    txHash: tx.hash,
    blockNumber: receipt.blockNumber,
    isValid
  };
}

/**
 * Sign a message for beacon verification
 * @param {string} beaconCID - The beacon CID to sign
 * @param {string} theorem - The theorem to sign
 * @returns {string} The signature
 */
async function signBeacon(beaconCID, theorem) {
  if (!process.env.PRIVATE_KEY) {
    throw new Error("PRIVATE_KEY not set in .env file");
  }
  
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY);
  const beaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
  const messageHash = ethers.keccak256(
    ethers.solidityPacked(["bytes32", "string"], [beaconHash, theorem])
  );
  
  const signature = await wallet.signMessage(ethers.getBytes(messageHash));
  console.log("Signature:", signature);
  return signature;
}

// Example usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log("Usage: node mint-nft.js <contract-address> [beacon-json-path]");
    console.log("Example: node mint-nft.js 0x123... data/verified_bound_R55.json");
    console.log("\nMake sure to set PRIVATE_KEY and BASE_RPC_URL in .env file");
    process.exit(1);
  }
  
  const contractAddress = args[0];
  const beaconPath = args[1] || "data/verified_bound_R55.json";
  
  // Load beacon data
  const beaconData = JSON.parse(fs.readFileSync(beaconPath, 'utf8'));
  const theorem = beaconData.theorem || "R(5,5) = 43";
  const beaconCID = "ipfs://Qm" + beaconPath.replace(/[^a-zA-Z0-9]/g, '');  // Placeholder CID
  const proofFileCID = beaconCID;  // Same for now
  
  console.log("Preparing to mint AIK Beacon NFT...");
  console.log("Beacon file:", beaconPath);
  console.log("Theorem:", theorem);
  
  // First, sign the beacon
  signBeacon(beaconCID, theorem)
    .then(signature => {
      return mintBeacon(contractAddress, theorem, proofFileCID, beaconCID, signature);
    })
    .then(result => {
      console.log("\n✓ NFT minted successfully!");
      console.log("Token ID:", result.tokenId);
      console.log("Transaction:", result.txHash);
    })
    .catch(error => {
      console.error("Error minting NFT:", error.message);
      process.exit(1);
    });
}

module.exports = { mintBeacon, signBeacon };
