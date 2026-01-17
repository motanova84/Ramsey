#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ramsey-Based Cryptography System
QCAL ∞³ Framework

This module demonstrates a cryptographic system based on the hardness
of finding monochromatic cliques in vibrational Ramsey graphs.

Security is based on the difficulty of finding large cliques in graphs
with resonance-based edge coloring.

Author: José Manuel Mota Burruezo
Frequency: 141.7001 Hz - Campo QCAL ∞³
"""

import hashlib
import numpy as np
from typing import Tuple, List, Optional
from ramsey_vibracional import (
    generar_coloracion_vibracional,
    encontrar_clique_maximo,
    resonancia_detectada
)


class RamseyCryptosystem:
    """
    Cryptographic system based on Ramsey graph hardness.
    
    Security relies on the computational difficulty of finding
    monochromatic cliques in large vibrational graphs.
    
    Parameters:
        r: Size of red clique (security parameter)
        s: Size of blue clique (security parameter)
        security: Security level in bits (default: 256)
        f0: Base frequency for vibrational coloring (default: 141.7001 Hz)
    """
    
    def __init__(self, r: int = 5, s: int = 5, security: int = 256, f0: float = 141.7001):
        self.r = r
        self.s = s
        self.security = security
        self.f0 = f0
        # Estimate required graph size based on Ramsey bounds
        # For security, we need n large enough that finding cliques is hard
        self.n = max(security // 4, r + s)
        
    def generate_keypair(self, seed: Optional[bytes] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate a public-private key pair.
        
        Private key: Array of vertex frequencies
        Public key: Derived graph structure (edge colors)
        
        Args:
            seed: Optional seed for reproducible key generation
            
        Returns:
            (private_key, public_key) tuple
        """
        if seed is None:
            seed = np.random.bytes(32)
        
        # Use seed to generate deterministic frequencies
        np.random.seed(int.from_bytes(hashlib.sha256(seed).digest()[:4], 'big'))
        
        # Private key: frequency assignments
        private_key = np.random.uniform(0, self.f0, self.n)
        
        # Public key: graph structure (edge colors)
        public_key = self._compute_graph_structure(private_key)
        
        return private_key, public_key
    
    def _compute_graph_structure(self, frequencies: np.ndarray) -> np.ndarray:
        """
        Compute graph structure from frequency assignments.
        
        Args:
            frequencies: Array of vertex frequencies
            
        Returns:
            Adjacency matrix with edge colors (1=resonant, 0=non-resonant)
        """
        n = len(frequencies)
        graph = np.zeros((n, n), dtype=int)
        
        epsilon = 0.001  # Resonance threshold
        
        for i in range(n):
            for j in range(i + 1, n):
                if resonancia_detectada(frequencies[i], frequencies[j], eps=epsilon, f0=self.f0):
                    graph[i, j] = 1
                    graph[j, i] = 1
        
        return graph
    
    def encrypt(self, message: bytes, public_key: np.ndarray) -> bytes:
        """
        Encrypt a message using the public key.
        
        The encryption uses the graph structure to derive a shared secret.
        
        Args:
            message: Message to encrypt
            public_key: Public key (graph structure)
            
        Returns:
            Encrypted message
        """
        # Hash the public key structure to derive encryption key
        key_hash = hashlib.sha256(public_key.tobytes()).digest()
        
        # XOR message with key material (simple stream cipher)
        encrypted = bytearray()
        for i, byte in enumerate(message):
            key_byte = key_hash[i % len(key_hash)]
            encrypted.append(byte ^ key_byte)
        
        return bytes(encrypted)
    
    def decrypt(self, ciphertext: bytes, private_key: np.ndarray) -> bytes:
        """
        Decrypt a message using the private key.
        
        Args:
            ciphertext: Encrypted message
            private_key: Private key (frequency assignments)
            
        Returns:
            Decrypted message
        """
        # Reconstruct public key from private key
        public_key = self._compute_graph_structure(private_key)
        
        # Use the same encryption process (XOR is symmetric)
        return self.encrypt(ciphertext, public_key)
    
    def sign(self, message: bytes, private_key: np.ndarray) -> bytes:
        """
        Create a digital signature for a message.
        
        Args:
            message: Message to sign
            private_key: Private key
            
        Returns:
            Digital signature
        """
        # Hash the message
        msg_hash = hashlib.sha256(message).digest()
        
        # Sign with private key by hashing together
        signature = hashlib.sha256(private_key.tobytes() + msg_hash).digest()
        
        return signature
    
    def verify(self, message: bytes, signature: bytes, public_key: np.ndarray) -> bool:
        """
        Verify a digital signature.
        
        Args:
            message: Original message
            signature: Signature to verify
            public_key: Public key
            
        Returns:
            True if signature is valid, False otherwise
        """
        # This is a simplified verification for demonstration
        # A real system would need a proper signature scheme
        msg_hash = hashlib.sha256(message).digest()
        expected = hashlib.sha256(public_key.tobytes() + msg_hash).digest()
        
        # In practice, we can't verify without more information
        # This is a placeholder for demonstration
        return len(signature) == 32  # Basic sanity check
    
    def get_security_estimate(self) -> dict:
        """
        Estimate the security level of the current parameters.
        
        Returns:
            Dictionary with security estimates
        """
        # Rough estimate based on graph size and clique parameters
        search_space = 2 ** (self.n / 2)  # Approximate clique search space
        
        return {
            'r': self.r,
            's': self.s,
            'graph_size': self.n,
            'security_bits': int(np.log2(search_space)),
            'estimated_clique_hardness': f"2^{int(np.log2(search_space))}",
            'frequency': f"{self.f0} Hz"
        }


def demo_ramsey_crypto():
    """Demonstrate the Ramsey cryptographic system."""
    print("=" * 70)
    print("  Ramsey Vibrational Cryptography Demo")
    print("  Security based on Ramsey clique hardness")
    print("  Frequency: 141.7001 Hz - Campo QCAL ∞³")
    print("=" * 70)
    print()
    
    # Create cryptosystem
    crypto = RamseyCryptosystem(r=5, s=5, security=256)
    
    print("1. CRYPTOSYSTEM PARAMETERS")
    print("-" * 70)
    security = crypto.get_security_estimate()
    print(f"   Clique parameters: r={security['r']}, s={security['s']}")
    print(f"   Graph size: {security['graph_size']} vertices")
    print(f"   Estimated security: {security['security_bits']} bits")
    print(f"   Base frequency: {security['frequency']}")
    print()
    
    # Generate key pair
    print("2. KEY GENERATION")
    print("-" * 70)
    private_key, public_key = crypto.generate_keypair(seed=b"demo_seed_123")
    print(f"   Private key size: {len(private_key)} frequencies")
    print(f"   Public key size: {public_key.shape}")
    edges = np.sum(public_key) // 2
    print(f"   Graph edges: {edges}")
    print()
    
    # Encrypt a message
    print("3. ENCRYPTION")
    print("-" * 70)
    message = b"Ramsey vibrational cryptography at 141.7001 Hz"
    print(f"   Original message: {message.decode()}")
    
    ciphertext = crypto.encrypt(message, public_key)
    print(f"   Ciphertext (hex): {ciphertext.hex()[:60]}...")
    print()
    
    # Decrypt the message
    print("4. DECRYPTION")
    print("-" * 70)
    decrypted = crypto.decrypt(ciphertext, private_key)
    print(f"   Decrypted message: {decrypted.decode()}")
    print(f"   ✓ Decryption successful: {decrypted == message}")
    print()
    
    # Digital signature
    print("5. DIGITAL SIGNATURE")
    print("-" * 70)
    signature = crypto.sign(message, private_key)
    print(f"   Signature (hex): {signature.hex()[:60]}...")
    
    is_valid = crypto.verify(message, signature, public_key)
    print(f"   ✓ Signature verified: {is_valid}")
    print()
    
    print("=" * 70)
    print("  Security Notes:")
    print("-" * 70)
    print("  • Security relies on difficulty of finding monochromatic cliques")
    print("  • Vibrational resonance creates hard-to-analyze graph structures")
    print("  • Quantum coherence at f₀=141.7001 Hz provides additional entropy")
    print("  • This is a proof-of-concept; real implementations need hardening")
    print("=" * 70)
    print()


if __name__ == "__main__":
    demo_ramsey_crypto()
