const { ethers } = require("ethers");
require('dotenv').config();
const fs = require('fs');
const path = require('path');

// ABI for the AIKBeaconsProofOfMath contract
const CONTRACT_ABI = [
  "function mintIfValidProof(string theorem, string proofFileCID, string beaconCID, bytes32 expectedBeaconHash, bytes signature) external",
  "function totalSupply() view returns (uint256)",
  "function verifyProof(uint256 tokenId) view returns (bool)",
  "event BeaconMinted(uint256 indexed tokenId, bytes32 beaconHash, string theorem)"
];

// List of beacons to mint
const BEACONS = [
  {
    name: "Rpsi55",
    theorem: "R(5,5) = 43",
    beaconFile: "data/verified_bound_R55.json",
    description: "Vibrational proof of R(5,5) = 43 using QCAL framework"
  },
  {
    name: "RpsiModel",
    theorem: "Rψ(5,5; f₀=141.7001 Hz) ≤ 16",
    beaconFile: "data/rpsi_vibration_model.json",
    description: "Vibrational Ramsey model with f₀ = 141.7001 Hz"
  },
  {
    name: "QCALBeacon",
    theorem: "QCAL ∞³ Framework Certification",
    beaconFile: ".qcal_beacon",
    description: "QCAL framework beacon for Ramsey theory"
  },
  {
    name: "Rpsi33",
    theorem: "Rψ(3,3) Certification",
    beaconFile: ".qcal_beacon_r33",
    description: "Vibrational certification for R(3,3)"
  },
  {
    name: "Rpsi44",
    theorem: "Rψ(4,4) Certification",
    beaconFile: ".qcal_beacon_r44",
    description: "Vibrational certification for R(4,4)"
  }
];

/**
 * Sign a beacon for minting
 */
async function signBeacon(wallet, beaconCID, theorem) {
  const beaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
  const messageHash = ethers.keccak256(
    ethers.solidityPacked(["bytes32", "string"], [beaconHash, theorem])
  );
  return wallet.signMessage(ethers.getBytes(messageHash));
}

/**
 * Mint a single beacon NFT
 */
async function mintSingleBeacon(contract, wallet, beacon) {
  console.log(`\n--- Minting: ${beacon.name} ---`);
  console.log(`Theorem: ${beacon.theorem}`);
  
  // Generate placeholder CID (in production, use actual IPFS CIDs)
  const beaconCID = `ipfs://Qm${beacon.name}${Date.now().toString(36)}`;
  const proofFileCID = beaconCID;
  
  // Calculate hash and sign
  const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
  const signature = await signBeacon(wallet, beaconCID, beacon.theorem);
  
  console.log(`Beacon CID: ${beaconCID}`);
  console.log(`Hash: ${expectedBeaconHash}`);
  
  try {
    const tx = await contract.mintIfValidProof(
      beacon.theorem,
      proofFileCID,
      beaconCID,
      expectedBeaconHash,
      signature
    );
    
    console.log(`Transaction: ${tx.hash}`);
    const receipt = await tx.wait();
    console.log(`✓ Minted in block ${receipt.blockNumber}`);
    
    return {
      name: beacon.name,
      theorem: beacon.theorem,
      txHash: tx.hash,
      blockNumber: receipt.blockNumber,
      beaconCID,
      success: true
    };
  } catch (error) {
    console.error(`✗ Failed to mint ${beacon.name}:`, error.message);
    return {
      name: beacon.name,
      theorem: beacon.theorem,
      error: error.message,
      success: false
    };
  }
}

/**
 * Batch mint all beacons
 */
async function batchMint(contractAddress) {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║     AIK Beacons - Batch Minting                            ║");
  console.log("║     Proof of Mathematical Truth NFTs                       ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  
  // Connect to network
  const rpcUrl = process.env.BASE_RPC_URL || "https://sepolia.base.org";
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  
  if (!process.env.PRIVATE_KEY) {
    throw new Error("PRIVATE_KEY not set in .env file");
  }
  
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
  console.log("Minting wallet:", wallet.address);
  
  const contract = new ethers.Contract(contractAddress, CONTRACT_ABI, wallet);
  
  // Get initial supply
  const initialSupply = await contract.totalSupply();
  console.log("Initial supply:", initialSupply.toString());
  console.log("Beacons to mint:", BEACONS.length);
  
  const results = [];
  
  // Mint each beacon
  for (const beacon of BEACONS) {
    const result = await mintSingleBeacon(contract, wallet, beacon);
    results.push(result);
    
    // Small delay between mints
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Summary
  console.log("\n═══════════════════════════════════════════════════════════════");
  console.log("                    BATCH MINT SUMMARY                          ");
  console.log("═══════════════════════════════════════════════════════════════\n");
  
  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);
  
  console.log(`Successful: ${successful.length}/${BEACONS.length}`);
  console.log(`Failed: ${failed.length}/${BEACONS.length}`);
  
  if (successful.length > 0) {
    console.log("\nMinted NFTs:");
    successful.forEach(r => {
      console.log(`  ✓ ${r.name}: ${r.theorem}`);
      console.log(`    TX: ${r.txHash}`);
    });
  }
  
  if (failed.length > 0) {
    console.log("\nFailed mints:");
    failed.forEach(r => {
      console.log(`  ✗ ${r.name}: ${r.error}`);
    });
  }
  
  // Save results
  const resultsPath = "nft/metadata/batch_mint_results.json";
  fs.writeFileSync(resultsPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    contractAddress,
    initialSupply: initialSupply.toString(),
    results
  }, null, 2));
  console.log(`\nResults saved to: ${resultsPath}`);
  
  return results;
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log("Usage: node batch-mint.js <contract-address>");
    console.log("Example: node batch-mint.js 0x123...");
    console.log("\nMake sure to set PRIVATE_KEY and BASE_RPC_URL in .env");
    process.exit(1);
  }
  
  batchMint(args[0])
    .then(() => {
      console.log("\n✓ Batch minting complete!");
      process.exit(0);
    })
    .catch(error => {
      console.error("\n✗ Batch minting failed:", error.message);
      process.exit(1);
    });
}

module.exports = { batchMint, BEACONS };
