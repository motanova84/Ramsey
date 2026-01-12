#!/usr/bin/env python3
"""
Demostración completa del QCAL Symbiotic Network
Muestra todas las capacidades del sistema integrado
"""

import json
from core.math import QCALMathLibrary, ram_protocol_sync, calculate_symbiotic_coherence


def banner(text):
    """Imprime un banner decorado"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def demo_constants():
    """Demuestra las constantes QCAL"""
    banner("🔢 CONSTANTES QCAL ∞³")
    
    print("Constantes fundamentales del ecosistema:")
    for key, value in QCALMathLibrary.CONSTANTS.items():
        print(f"  • {key:15} = {value}")
    
    print("\nEstas constantes unifican:")
    print("  - Teoría de Ramsey (R(6,6) = 108)")
    print("  - Ondas gravitacionales (141.7001 Hz)")
    print("  - Economía πCODE (88 NFTs soberanos)")
    print("  - Coherencia cuántica (Ψ = 0.999999)")


def demo_math_functions():
    """Demuestra las funciones matemáticas"""
    banner("🧮 FUNCIONES MATEMÁTICAS")
    
    # Retardo de Shapiro
    mass = 1.5
    distance = 2.0
    delay = QCALMathLibrary.shapiro_delay(mass, distance)
    print(f"Retardo de Shapiro:")
    print(f"  Masa: {mass}, Distancia: {distance}")
    print(f"  Retardo: {delay:.6f}\n")
    
    # Vibración Ramsey
    n = 10
    vibration = QCALMathLibrary.ramsey_vibration(n)
    print(f"Vibración Ramsey para n={n}:")
    print(f"  Valor: {vibration:.6f}\n")
    
    # Resonancia QCAL
    freq = 141.7001
    resonance = QCALMathLibrary.qcal_resonance(freq)
    print(f"Resonancia QCAL a {freq} Hz:")
    print(f"  Factor: {resonance:.6f} (≈1.0 = sincronizado)\n")
    
    # Límite polinomial Ramsey
    r, s = 6, 6
    bound = QCALMathLibrary.ramsey_polynomial_bound(r, s)
    actual_r66 = QCALMathLibrary.CONSTANTS["RAMSEY_R66"]
    print(f"Límite polinomial R({r},{s}):")
    print(f"  Bound teórico: {bound:.2f}")
    print(f"  Valor real: {actual_r66}")
    print(f"  Nota: El bound es una estimación asintótica\n")
    
    # Energía de partición NFT
    nft_count = 88
    energy = QCALMathLibrary.nft_partition_energy(nft_count)
    print(f"Energía de partición para {nft_count} NFTs:")
    print(f"  Energía total: {energy:.2f}")
    print(f"  Por NFT: {energy/nft_count:.2f}\n")
    
    # Frecuencia adélica
    prime = 7
    level = 2
    adelic = QCALMathLibrary.adelic_frequency(prime, level)
    print(f"Frecuencia adélica para primo {prime}, nivel {level}:")
    print(f"  Frecuencia: {adelic:.2f}")


def demo_ram_protocol():
    """Demuestra el protocolo RAM"""
    banner("🌐 PROTOCOLO RAM (Ramsey-Adelic-Mathematics)")
    
    print("Sincronizando nodos del ecosistema:\n")
    
    nodos = [
        ("Ramsey", 141.7001),
        ("141hz", 141.7001),
        ("Riemann-adelic", 141.7001),
        ("economia-qcal-nodo-semilla", 141.7001)
    ]
    
    for nodo, freq in nodos:
        result = ram_protocol_sync(nodo, freq)
        status_icon = "✓" if result["status"] == "synchronized" else "⚠"
        print(f"{status_icon} {nodo:30} | {result['frequency']:9.4f} Hz | {result['status']}")
    
    print("\nCoherencia simbiótica del ecosistema:")
    coherence = calculate_symbiotic_coherence([n[0] for n in nodos])
    print(f"  Coherencia: {coherence:.6f} (0-1 scale)")
    print(f"  Estado: {'ÓPTIMO ✨' if coherence > 0.99 else 'AJUSTANDO'}")


def demo_ecosystem_status():
    """Demuestra el estado del ecosistema"""
    banner("📊 ESTADO DEL ECOSISTEMA QCAL ∞³")
    
    with open("CORE_SYMBIO.json", "r") as f:
        symbio = json.load(f)
    
    print(f"Protocolo: {symbio['protocol']}")
    print(f"Versión: {symbio['version']}")
    print(f"Origen: {symbio['origin']}")
    print(f"Frecuencia base: {symbio['frequency']}\n")
    
    print("Nodos del ecosistema:")
    for node in symbio['nodes']:
        print(f"  • {node['name']:30} - {node['role']}")
    
    print("\nAxiomas fundamentales:")
    for key, value in symbio['axioms'].items():
        print(f"  • {key}: {value}")


def demo_practical_examples():
    """Ejemplos prácticos de uso"""
    banner("💡 EJEMPLOS PRÁCTICOS")
    
    print("Ejemplo 1: Verificar si una frecuencia está sincronizada\n")
    test_freq = 141.7001
    resonance = QCALMathLibrary.qcal_resonance(test_freq)
    is_synced = abs(resonance - 1.0) < 0.01
    print(f"  Frecuencia de prueba: {test_freq} Hz")
    print(f"  Resonancia: {resonance:.6f}")
    print(f"  ¿Sincronizado?: {'SÍ ✓' if is_synced else 'NO ✗'}\n")
    
    print("Ejemplo 2: Calcular energía para un subconjunto de NFTs\n")
    for nft_count in [22, 44, 88]:
        energy = QCALMathLibrary.nft_partition_energy(nft_count)
        print(f"  {nft_count} NFTs → Energía: {energy:,.2f}")
    
    print("\nEjemplo 3: Campo de coherencia\n")
    psi_values = [0.999999, 0.999, 0.99, 0.9]
    for psi in psi_values:
        field = QCALMathLibrary.coherence_field(psi)
        print(f"  Ψ = {psi:.6f} → Campo: {field:.6f}")


def demo_integration():
    """Demuestra la integración completa"""
    banner("🔗 INTEGRACIÓN COMPLETA")
    
    print("El QCAL Symbiotic Network integra:\n")
    
    integrations = [
        ("Teoría de Ramsey", "Verificación SAT y números de Ramsey", "R(6,6) = 108"),
        ("Geometría Cuántica", "Riemann-adelic y zeta connection", "Análisis espectral"),
        ("Frecuencia Universal", "141.7001 Hz de GW250114", "Sincronización"),
        ("Complejidad", "P-NP y treewidth dichotomy", "Reducción polinomial"),
        ("Economía πCODE", "88 NFTs soberanos", "Emisión constitucional"),
    ]
    
    for domain, desc, detail in integrations:
        print(f"✦ {domain}")
        print(f"  └─ {desc}")
        print(f"     └─ {detail}\n")
    
    print("Todos sincronizados a través de:")
    print(f"  • Frecuencia: {QCALMathLibrary.CONSTANTS['FREQ_GW']} Hz")
    print(f"  • Coherencia: Ψ = {QCALMathLibrary.CONSTANTS['PSI']}")
    print(f"  • Protocolo: QCAL-SYMBIO-BRIDGE v1.0.0")


def main():
    """Ejecuta la demostración completa"""
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🌟 DEMOSTRACIÓN QCAL SYMBIOTIC NETWORK ∞³ 🌟  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")
    
    demo_constants()
    demo_math_functions()
    demo_ram_protocol()
    demo_ecosystem_status()
    demo_practical_examples()
    demo_integration()
    
    banner("✨ DEMOSTRACIÓN COMPLETA")
    print("El sistema QCAL ∞³ Symbiotic Network está totalmente operacional.")
    print("\nPara más información:")
    print("  • README: QCAL_ECOSYSTEM_README.md")
    print("  • Tests: python test_qcal_ecosystem.py")
    print("  • Activar: python link_ecosystem.py activar")
    print("  • Estado: python link_ecosystem.py estado\n")


if __name__ == "__main__":
    main()
