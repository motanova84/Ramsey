const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString());

  const AIKBeacons = await hre.ethers.getContractFactory("AIKBeaconsProofOfMath");
  const contract = await AIKBeacons.deploy(deployer.address);

  await contract.waitForDeployment();
  const contractAddress = await contract.getAddress();
  
  console.log("AIKBeacons deployed to:", contractAddress);
  console.log("Creator address:", deployer.address);
  
  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    contract: "AIKBeaconsProofOfMath",
    address: contractAddress,
    creator: deployer.address,
    network: hre.network.name,
    timestamp: new Date().toISOString()
  };
  
  fs.writeFileSync(
    "nft/metadata/deployment.json",
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("Deployment info saved to nft/metadata/deployment.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
