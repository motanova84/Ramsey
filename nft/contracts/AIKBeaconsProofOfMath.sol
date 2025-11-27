// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

/**
 * @title AIKBeaconsProofOfMath
 * @dev ERC721 NFT contract for AIK Beacons - Proof of Mathematical Truth
 * NFTs are only minted if the mathematical proof is valid (verified via signature and hash)
 */
contract AIKBeaconsProofOfMath is ERC721, ERC721URIStorage, Ownable {
    using ECDSA for bytes32;

    string public constant NAME = "AIK Beacons - Proof of Mathematical Truth";
    string public constant SYMBOL = "AIK";

    mapping(uint256 => bytes32) public beaconHash;   // keccak256 of the beacon CID
    mapping(uint256 => string)  public beaconCID;    // IPFS CID
    mapping(uint256 => bool)    public isValidProof;
    address public immutable creator;  // Creator address (fixed)

    uint256 public totalSupply;
    uint256 public constant MAX_SUPPLY = 100;  // Limited for scarcity

    event BeaconMinted(uint256 indexed tokenId, bytes32 beaconHash, string theorem);

    constructor(address _creator) ERC721(NAME, SYMBOL) Ownable(msg.sender) {
        creator = _creator;
    }

    /**
     * @dev Mint a new NFT if the proof is valid
     * @param theorem The theorem statement
     * @param _proofFileCID IPFS CID of the proof file (reserved for future use)
     * @param _beaconCID IPFS CID of the beacon JSON
     * @param expectedBeaconHash Expected hash of the beacon
     * @param signature ECDSA signature for verification
     */
    function mintIfValidProof(
        string memory theorem,
        string memory _proofFileCID,
        string memory _beaconCID,
        bytes32 expectedBeaconHash,
        bytes calldata signature
    ) external onlyOwner {
        require(totalSupply < MAX_SUPPLY, "Max supply reached");
        require(bytes(_beaconCID).length > 0, "Invalid CID");
        
        // 1. Verify hash vs CID (simplified; in production, use off-chain oracle)
        bytes32 cidHash = keccak256(abi.encodePacked(_beaconCID));
        require(expectedBeaconHash == cidHash, "Hash mismatch");

        // 2. Verify ECDSA signature
        bytes32 messageHash = keccak256(abi.encodePacked(expectedBeaconHash, theorem));
        bytes32 ethSignedHash = messageHash.toEthSignedMessageHash();
        address signer = ethSignedHash.recover(signature);
        require(signer == creator, "Invalid signature");

        uint256 tokenId = totalSupply++;
        beaconHash[tokenId] = expectedBeaconHash;
        beaconCID[tokenId] = _beaconCID;
        isValidProof[tokenId] = true;

        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, _beaconCID);
        emit BeaconMinted(tokenId, expectedBeaconHash, theorem);

        // Note: _proofFileCID is reserved for future proof file storage
        _proofFileCID;
    }

    /**
     * @dev Verify if a proof is valid on-chain
     * @param tokenId The token ID to verify
     * @return bool Whether the proof is valid
     */
    function verifyProof(uint256 tokenId) public view returns (bool) {
        require(_ownerOf(tokenId) != address(0), "Invalid token");
        return isValidProof[tokenId];
    }

    // Override functions required by Solidity

    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721)
    {
        super._increaseBalance(account, value);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721URIStorage) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}
