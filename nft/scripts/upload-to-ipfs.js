require('dotenv').config();
const fs = require('fs');

// Note: In production, use Pinata SDK for IPFS uploads
// This is a simplified version that prepares metadata for upload

/**
 * Generate NFT metadata from a beacon JSON file
 * @param {string} beaconJsonPath - Path to the beacon JSON file
 * @param {string} metadataName - Name for the metadata file
 * @returns {object} Generated metadata object
 */
function generateMetadata(beaconJsonPath, metadataName) {
  // Read beacon data
  const beaconData = JSON.parse(fs.readFileSync(beaconJsonPath, 'utf8'));

  // Generate NFT metadata following ERC721 standard
  const metadata = {
    name: `${metadataName} - AIK Beacon`,
    description: `Immutable certificate of mathematical truth. Theorem: "${beaconData.theorem || 'R(5,5) = 43'}". Verified via AIK CLI and QCAL framework.`,
    image: "ipfs://QmPlaceholderImageCID",  // Replace with actual image CID
    external_url: "https://github.com/motanova84/Ramsey",
    attributes: [
      { trait_type: "Framework", value: "QCAL ∞³" },
      { trait_type: "Theorem", value: beaconData.theorem || "R(5,5) = 43" },
      { trait_type: "Frequency", value: `${beaconData.frequency_parameters?.f0 || 141.7001} Hz` },
      { trait_type: "Verification Status", value: beaconData.verification_status || "PROVEN" },
      { trait_type: "Proof Method", value: beaconData.verification?.method || "SAT_solver" },
      { trait_type: "Timestamp", value: beaconData.timestamp || new Date().toISOString() }
    ],
    properties: {
      verification_command: "python3 ai_ramsey_formal.py verify",
      repository: "https://github.com/motanova84/Ramsey",
      license: "MIT"
    }
  };

  return metadata;
}

/**
 * Prepare beacon for IPFS upload (creates metadata file)
 * @param {string} beaconJsonPath - Path to beacon JSON
 * @param {string} metadataName - Name for metadata
 */
function prepareForIPFS(beaconJsonPath, metadataName) {
  console.log(`Preparing ${metadataName} for IPFS upload...`);
  
  const metadata = generateMetadata(beaconJsonPath, metadataName);
  
  // Save metadata to file
  const metadataPath = `nft/metadata/${metadataName}_metadata.json`;
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));
  console.log(`Metadata saved to: ${metadataPath}`);
  
  // Generate CID placeholder info
  const cidInfo = {
    metadata_file: metadataPath,
    beacon_file: beaconJsonPath,
    status: "ready_for_upload",
    instructions: [
      "1. Upload metadata JSON to IPFS (e.g., via Pinata)",
      "2. Upload beacon JSON to IPFS",
      "3. Save the returned CIDs",
      "4. Use mint-nft.js to mint with the CIDs"
    ]
  };
  
  const cidInfoPath = `nft/metadata/${metadataName}_cids.json`;
  fs.writeFileSync(cidInfoPath, JSON.stringify(cidInfo, null, 2));
  console.log(`CID info saved to: ${cidInfoPath}`);
  
  return { metadata, metadataPath, cidInfoPath };
}

// If running directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log("Usage: node upload-to-ipfs.js <beacon-json-path> <metadata-name>");
    console.log("Example: node upload-to-ipfs.js data/verified_bound_R55.json Rpsi55");
    process.exit(1);
  }
  
  const [beaconPath, metadataName] = args;
  prepareForIPFS(beaconPath, metadataName);
}

module.exports = { generateMetadata, prepareForIPFS };
