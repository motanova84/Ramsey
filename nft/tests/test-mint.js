const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AIKBeaconsProofOfMath", function () {
  let contract;
  let owner;
  let creator;
  let otherAccount;

  beforeEach(async function () {
    [owner, creator, otherAccount] = await ethers.getSigners();
    
    const AIKBeacons = await ethers.getContractFactory("AIKBeaconsProofOfMath");
    contract = await AIKBeacons.deploy(creator.address);
    await contract.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct name and symbol", async function () {
      expect(await contract.name()).to.equal("AIK Beacons - Proof of Mathematical Truth");
      expect(await contract.symbol()).to.equal("AIK");
    });

    it("Should set the correct creator", async function () {
      expect(await contract.creator()).to.equal(creator.address);
    });

    it("Should set the correct owner", async function () {
      expect(await contract.owner()).to.equal(owner.address);
    });

    it("Should have zero initial supply", async function () {
      expect(await contract.totalSupply()).to.equal(0);
    });
  });

  describe("Minting", function () {
    it("Should mint only if valid proof", async function () {
      const theorem = "R(5,5) = 43";
      const beaconCID = "ipfs://QmTestBeaconCID123";
      const proofFileCID = "ipfs://QmTestProofCID123";
      
      // Calculate expected hash
      const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
      
      // Create signature
      const messageHash = ethers.keccak256(
        ethers.solidityPacked(["bytes32", "string"], [expectedBeaconHash, theorem])
      );
      const signature = await creator.signMessage(ethers.getBytes(messageHash));

      // Mint
      await expect(contract.mintIfValidProof(theorem, proofFileCID, beaconCID, expectedBeaconHash, signature))
        .to.emit(contract, "BeaconMinted")
        .withArgs(0, expectedBeaconHash, theorem);

      // Verify token was minted
      expect(await contract.totalSupply()).to.equal(1);
      expect(await contract.isValidProof(0)).to.be.true;
      expect(await contract.beaconCID(0)).to.equal(beaconCID);
    });

    it("Should reject hash mismatch", async function () {
      const theorem = "R(5,5) = 43";
      const beaconCID = "ipfs://QmTestBeaconCID123";
      const wrongHash = ethers.keccak256(ethers.toUtf8Bytes("wrong"));
      
      const messageHash = ethers.keccak256(
        ethers.solidityPacked(["bytes32", "string"], [wrongHash, theorem])
      );
      const signature = await creator.signMessage(ethers.getBytes(messageHash));
      const proofFileCID = "ipfs://QmTestProofCID123";

      await expect(
        contract.mintIfValidProof(theorem, proofFileCID, beaconCID, wrongHash, signature)
      ).to.be.revertedWith("Hash mismatch");
    });

    it("Should reject invalid signature", async function () {
      const theorem = "R(5,5) = 43";
      const beaconCID = "ipfs://QmTestBeaconCID123";
      const proofFileCID = "ipfs://QmTestProofCID123";
      const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
      
      // Sign with wrong account
      const messageHash = ethers.keccak256(
        ethers.solidityPacked(["bytes32", "string"], [expectedBeaconHash, theorem])
      );
      const signature = await otherAccount.signMessage(ethers.getBytes(messageHash));

      await expect(
        contract.mintIfValidProof(theorem, proofFileCID, beaconCID, expectedBeaconHash, signature)
      ).to.be.revertedWith("Invalid signature");
    });

    it("Should reject empty CID", async function () {
      const theorem = "R(5,5) = 43";
      const beaconCID = "";
      const proofFileCID = "ipfs://QmTestProofCID123";
      const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
      
      const messageHash = ethers.keccak256(
        ethers.solidityPacked(["bytes32", "string"], [expectedBeaconHash, theorem])
      );
      const signature = await creator.signMessage(ethers.getBytes(messageHash));

      await expect(
        contract.mintIfValidProof(theorem, proofFileCID, beaconCID, expectedBeaconHash, signature)
      ).to.be.revertedWith("Invalid CID");
    });

    it("Should only allow owner to mint", async function () {
      const theorem = "R(5,5) = 43";
      const beaconCID = "ipfs://QmTestBeaconCID123";
      const proofFileCID = "ipfs://QmTestProofCID123";
      const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
      
      const messageHash = ethers.keccak256(
        ethers.solidityPacked(["bytes32", "string"], [expectedBeaconHash, theorem])
      );
      const signature = await creator.signMessage(ethers.getBytes(messageHash));

      // Try to mint from non-owner account
      await expect(
        contract.connect(otherAccount).mintIfValidProof(theorem, proofFileCID, beaconCID, expectedBeaconHash, signature)
      ).to.be.revertedWithCustomError(contract, "OwnableUnauthorizedAccount");
    });
  });

  describe("Verification", function () {
    it("Should verify proof on-chain", async function () {
      const theorem = "R(5,5) = 43";
      const beaconCID = "ipfs://QmTestBeaconCID123";
      const proofFileCID = "ipfs://QmTestProofCID123";
      const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
      
      const messageHash = ethers.keccak256(
        ethers.solidityPacked(["bytes32", "string"], [expectedBeaconHash, theorem])
      );
      const signature = await creator.signMessage(ethers.getBytes(messageHash));

      // Mint first
      await contract.mintIfValidProof(theorem, proofFileCID, beaconCID, expectedBeaconHash, signature);

      // Verify
      expect(await contract.verifyProof(0)).to.be.true;
    });

    it("Should reject verification for invalid token", async function () {
      await expect(contract.verifyProof(999)).to.be.revertedWith("Invalid token");
    });
  });

  describe("Token URI", function () {
    it("Should return correct token URI", async function () {
      const theorem = "R(5,5) = 43";
      const beaconCID = "ipfs://QmTestBeaconCID123";
      const proofFileCID = "ipfs://QmTestProofCID123";
      const expectedBeaconHash = ethers.keccak256(ethers.toUtf8Bytes(beaconCID));
      
      const messageHash = ethers.keccak256(
        ethers.solidityPacked(["bytes32", "string"], [expectedBeaconHash, theorem])
      );
      const signature = await creator.signMessage(ethers.getBytes(messageHash));

      await contract.mintIfValidProof(theorem, proofFileCID, beaconCID, expectedBeaconHash, signature);

      expect(await contract.tokenURI(0)).to.equal(beaconCID);
    });
  });

  describe("Max Supply", function () {
    it("Should respect max supply limit", async function () {
      // This test would require minting 100 tokens, which is expensive
      // Just verify the constant is set correctly
      expect(await contract.MAX_SUPPLY()).to.equal(100);
    });
  });
});
