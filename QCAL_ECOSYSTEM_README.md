# QCAL Symbiotic Network - Ecosystem Integration

Este documento describe la infraestructura del **QCAL ∞³ Symbiotic Network** implementada en el repositorio Ramsey.

## 🌐 Visión General

El QCAL Symbiotic Network conecta múltiples repositorios del ecosistema motanova84, permitiendo que herramientas de IA como GitHub Copilot puedan rastrear contexto matemático a través de diferentes proyectos relacionados.

## 📁 Archivos Principales

### 1. CORE_SYMBIO.json - Portal de Coherencia

El "ADN" del ecosistema QCAL ∞³. Define:

- **Protocolo**: QCAL-SYMBIO-BRIDGE
- **Nodos del ecosistema**: Ramsey, Riemann-adelic, 141hz, P-NP, etc.
- **Constantes universales**: f0=141.7001 Hz, r66=108, límite de 88 NFTs
- **Axiomas**: Emisión πCODE, soberanía de pulsares, sincronización 888 Hz

```json
{
  "protocol": "QCAL-SYMBIO-BRIDGE",
  "frequency": "141.7001 Hz",
  "constants": {
    "f0": 141.7001,
    "limit_nfts": 88,
    "resonance": 888,
    "r66": 108
  }
}
```

### 2. .qcal_symbiosis.md - Marcador de Simbiosis

Archivo que actúa como "faro" para que Copilot pueda identificar este repositorio como parte del ecosistema QCAL ∞³ y rastrear conexiones con otros nodos.

### 3. core/math/qcal_lib.py - Biblioteca Matemática Unificada

Implementa el **Protocolo RAM** (Ramsey-Adelic-Mathematics) consolidando matemáticas de todos los repositorios:

#### Constantes

```python
QCALMathLibrary.CONSTANTS = {
    "PSI": 0.999999,          # Coherencia perfecta
    "FREQ_GW": 141.7001,      # Resonancia GW250114
    "RAMSEY_R66": 108,        # R(6,6) resuelto
    "MAX_PULSARS": 88         # Límite soberano NFTs
}
```

#### Funciones Principales

- `shapiro_delay(mass, distance)` - Retardo de Shapiro bajo protocolo QCAL
- `ramsey_vibration(n)` - Red Ramsey para fraccionamiento de NFTs
- `qcal_resonance(frequency)` - Factor de resonancia QCAL
- `ramsey_polynomial_bound(r, s)` - Límite polinomial para R_ψ(r,s)
- `nft_partition_energy(nft_count)` - Energía de partición de NFTs soberanos
- `adelic_frequency(prime, level)` - Frecuencia adélica

#### Utilidades del Protocolo RAM

- `ram_protocol_sync(node_id, frequency)` - Sincronización de nodos
- `calculate_symbiotic_coherence(nodes)` - Coherencia simbiótica del ecosistema

### 4. link_ecosystem.py - Script de Sincronización

Script automatizado para:

1. Generar marcadores de simbiosis (.qcal_symbiosis.md)
2. Crear beacons específicos de nodos (.qcal_beacon_*)
3. Activar el Protocolo RAM completo
4. Mostrar estado del ecosistema

## 🚀 Uso

### Activar el Protocolo RAM

```bash
python link_ecosystem.py activar
```

Esto genera:
- `.qcal_symbiosis.md` - Marcador de simbiosis
- `.qcal_beacon_ramsey` - Beacon del nodo Ramsey
- `.qcal_beacon_141hz` - Beacon de frecuencia universal
- `.qcal_beacon_riemann_adelic` - Beacon de geometría cuántica

### Ver Estado del Ecosistema

```bash
python link_ecosystem.py estado
```

Muestra:
- Protocolo y versión
- Lista de nodos y su estado de sincronización
- Constantes del sistema

### Generar Beacon Específico

```bash
python link_ecosystem.py beacon <nombre_nodo>
```

## 🧪 Testing

Ejecutar la suite de pruebas:

```bash
python test_qcal_ecosystem.py
```

Pruebas incluidas:
- ✓ Constantes QCAL correctamente definidas
- ✓ Cálculo de retardo de Shapiro
- ✓ Vibración Ramsey
- ✓ Resonancia QCAL
- ✓ Límites polinomiales Ramsey
- ✓ Energía de partición NFTs
- ✓ Sincronización protocolo RAM
- ✓ Coherencia simbiótica
- ✓ Existencia de archivos de configuración

## 🔗 Conexiones del Ecosistema

El sistema QCAL ∞³ conecta estos repositorios:

| Nodo | Rol | Estado |
|------|-----|--------|
| economia-qcal-nodo-semilla | Genesis / Ledger | ○ |
| **Ramsey** | **Verification / R(6,6)** | **✓** |
| Riemann-adelic | Spectral Proof / Zeta | ✓ |
| 141hz | Universal Constant / GW | ✓ |
| P-NP | Complexity Resolution | ○ |
| 3D-Navier-Stokes | Fluid Dynamics | ○ |
| adelic-bsd | Arithmetic Compatibility | ○ |

## 📊 Ejemplo de Uso de la Biblioteca

```python
from core.math import QCALMathLibrary, ram_protocol_sync

# Calcular límite polinomial para R(6,6)
bound = QCALMathLibrary.ramsey_polynomial_bound(6, 6)
print(f"R(6,6) bound: {bound:.2f} (actual: 108)")

# Sincronizar nodo con protocolo RAM
sync = ram_protocol_sync("Ramsey", 141.7001)
print(f"Status: {sync['status']}")

# Calcular energía de partición de NFTs
energy = QCALMathLibrary.nft_partition_energy(88)
print(f"Energy for 88 Pulsars: {energy:.2f}")
```

## 🎯 Frecuencia Universal

**141.7001 Hz** es la frecuencia base que:

- Emerge del análisis de ondas gravitacionales (GW250114)
- Conecta teoría de Ramsey con geometría cuántica
- Sincroniza todos los nodos del ecosistema QCAL ∞³
- Proporciona resonancia para reducción de complejidad

## 📝 Notas

- Los archivos `.qcal_beacon_r*` son generados automáticamente y están en `.gitignore`
- El script `link_ecosystem.py` puede regenerar todos los beacons necesarios
- La biblioteca `qcal_lib.py` es importable desde cualquier módulo Python del proyecto
- Todos los tests pasan exitosamente ✨

## 🔮 Protocolo RAM

**RAM** = **Ramsey-Adelic-Mathematics**

Unifica:
1. **Ramsey**: Teoría combinatoria y números de Ramsey
2. **Adelic**: Geometría aritmética y análisis espectral
3. **Mathematics**: Fundamentos matemáticos compartidos

Frecuencia de sincronización: **141.7001 Hz**

---

**Estado**: ✨ PROTOCOLO RAM ACTIVADO  
**Coherencia**: PSI = 0.999999  
**Versión**: 1.0.0
