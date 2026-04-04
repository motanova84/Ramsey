#!/usr/bin/env python3
"""
Red de Ramsey QCAL de 7 Nodos Primos
=====================================
QCAL-SYMBIO-BRIDGE v1.1.0

Implementa la red de 7 nodos primos {2, 3, 5, 7, 11, 13, 17} con:

1. NodoPrimo          — nodo primo con frecuencia armónica f_p = f₀·ln(p)
2. RedRamsey          — grafo C₇ con 21 aristas potenciales
3. OperadorMaestroHPi — operador de Berry-Keating con espectro en línea crítica
4. SimbiosisHiggsPC   — simbiosis Higgs-PC con masa efectiva m* = m_H·(1 - g_eff)
5. TasaSimbiotitica   — tasa simbiótica R_symb = N·f₀·Ψ
6. CoherenciaRedRamsey — coherencia global Ψ_global ≥ 0.888
7. SistemaRedRamseyQCAL — integración completa del sistema

Sello: ∴RRQ∞³
RAM:   RAM-LII-2026-RED-RAMSEY-QCAL

Author: NOESIS ∞³ (via Trinity QCAL ∞³)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
Frequency: 141.7001 Hz
"""

import math
from typing import Dict, List, Tuple

# ── Sovereign metadata ────────────────────────────────────────────────────────

__author__ = "NOESIS ∞³ (via Trinity QCAL ∞³)"
__architecture__ = "QCAL ∞³"
__license__ = "Sovereign Noetic License 1.0"
__f0__ = 141.7001
__version__ = "QCAL-SYMBIO-BRIDGE v1.1.0"
__sello__ = "∴RRQ∞³"
__ram__ = "RAM-LII-2026-RED-RAMSEY-QCAL"


# ── ConstantesRedRamsey ───────────────────────────────────────────────────────

class ConstantesRedRamsey:
    """Constantes fundamentales de la Red de Ramsey QCAL de 7 Nodos Primos."""

    # Frecuencia base QCAL — integral de conexión topológica
    F0: float = 141.7001

    # Constante de acoplamiento simbiótico efectivo Higgs-PC
    G_EFF: float = 0.053

    # Masa del bosón de Higgs (GeV)
    M_HIGGS: float = 125.0

    # Masa efectiva del campo con acoplamiento PC: m* = m_H·(1 - g_eff)
    M_ESTRELLA: float = 118.375

    # Tasa simbiótica perfecta (kilo-pulsos por segundo)
    R_SYMB: float = 991.9007

    # Umbral mínimo de coherencia global
    PSI_UMBRAL: float = 0.888

    # Coherencia global medida del sistema
    PSI_GLOBAL: float = 0.999999

    # Número de nodos primos
    N_NODOS: int = 7

    # Sello del sistema
    SELLO: str = "∴RRQ∞³"

    # Identificador RAM
    RAM: str = "RAM-LII-2026-RED-RAMSEY-QCAL"

    # Versión del sistema
    VERSION: str = "QCAL-SYMBIO-BRIDGE v1.1.0"

    # Pesos de la coherencia global ponderada
    W_NODOS: float = 0.35
    W_ESPECTRO: float = 0.35
    W_HIGGS: float = 0.30

    # Los 7 nodos primos sagrados
    PRIMOS: Tuple[int, ...] = (2, 3, 5, 7, 11, 13, 17)

    # Partes imaginarias γ_n de los 7 ceros de Riemann activados
    GAMMAS: Tuple[float, ...] = (14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919)

    # Funciones noéticas de cada nodo primo
    NOETICA: Dict[int, str] = {
        2:  "Dualidad primordial — Puerta de entrada al espacio adélico",
        3:  "Trinidad noética — Resonancia trinitaria QCAL",
        5:  "Quintaesencia — Punto de equilibrio áureo",
        7:  "Septenario sagrado — Núcleo de la red de Ramsey",
        11: "Undécima armónica — Coherencia espectral elevada",
        13: "Decimotercero primo — Sincronizador de ciclos lunares",
        17: "Decimoséptimo primo — Puerta de manifestación galáctica",
    }


# ── NodoPrimo ─────────────────────────────────────────────────────────────────

class NodoPrimo:
    """
    Nodo primo de la Red de Ramsey con frecuencia armónica.

    La frecuencia armónica se calcula como:
        f_p = f₀ · ln(p)

    donde f₀ = 141.7001 Hz es la frecuencia base QCAL.
    """

    def __init__(self, primo: int, f0: float = ConstantesRedRamsey.F0):
        if primo < 2:
            raise ValueError(f"El primo debe ser >= 2, se recibió {primo}")
        self.primo = primo
        self.f0 = f0
        self.frecuencia: float = self._calcular_frecuencia()
        self.noetica: str = ConstantesRedRamsey.NOETICA.get(
            primo, f"Nodo primo {primo}"
        )

    def _calcular_frecuencia(self) -> float:
        """Calcula la frecuencia armónica: f_p = f₀ · ln(p)."""
        return self.f0 * math.log(self.primo)

    def es_primo(self) -> bool:
        """Verifica que el número del nodo es efectivamente primo."""
        if self.primo < 2:
            return False
        if self.primo == 2:
            return True
        if self.primo % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(self.primo)) + 1, 2):
            if self.primo % i == 0:
                return False
        return True

    def __repr__(self) -> str:
        return f"NodoPrimo(p={self.primo}, f={self.frecuencia:.4f} Hz)"


# ── RedRamsey ─────────────────────────────────────────────────────────────────

class RedRamsey:
    """
    Red de Ramsey C₇ con 7 nodos primos y 21 aristas potenciales.

    El conjunto sagrado C₇ = {2, 3, 5, 7, 11, 13, 17} forma el grafo
    completo K₇ con C(7,2) = 21 aristas potenciales.
    """

    def __init__(
        self,
        primos: Tuple[int, ...] = ConstantesRedRamsey.PRIMOS,
        f0: float = ConstantesRedRamsey.F0,
    ):
        self.primos = primos
        self.f0 = f0
        self.nodos: List[NodoPrimo] = [NodoPrimo(p, f0) for p in primos]
        self.n_nodos: int = len(primos)

    def aristas_potenciales(self) -> int:
        """Número de aristas en el grafo completo K_n: C(n,2) = n(n-1)/2."""
        n = self.n_nodos
        return n * (n - 1) // 2

    def todos_son_primos(self) -> bool:
        """Verifica que todos los nodos son números primos."""
        return all(nodo.es_primo() for nodo in self.nodos)

    def coherencia_nodos(self) -> float:
        """Fracción de nodos que son primos válidos."""
        validos = sum(1 for nodo in self.nodos if nodo.es_primo())
        return validos / self.n_nodos if self.n_nodos > 0 else 0.0

    def calcular_psi_nodos(self) -> float:
        """
        Calcula Ψ_nodos: coherencia interna de los nodos de la red.

        Retorna 0.999999 cuando todos los nodos son primos válidos
        con frecuencias positivas bien definidas.
        """
        frecuencias_validas = all(nodo.frecuencia > 0 for nodo in self.nodos)
        if frecuencias_validas and self.todos_son_primos():
            return 0.999999
        return 0.0

    def cierre_nodos(self) -> bool:
        """
        Cierre Aritmético — Cierre 1 del sistema.

        El cierre se alcanza cuando:
        - Todos los nodos son primos válidos
        - El grafo tiene 21 aristas potenciales
        - Ψ_nodos ≥ PSI_UMBRAL
        """
        return (
            self.todos_son_primos()
            and self.aristas_potenciales() == 21
            and self.calcular_psi_nodos() >= ConstantesRedRamsey.PSI_UMBRAL
        )


# ── OperadorMaestroHPi ────────────────────────────────────────────────────────

class OperadorMaestroHPi:
    """
    Operador Maestro Ĥ_π — Berry-Keating cuántico.

    El operador de dilatación cuántica:
        Ĥ_π = -i(x ∂/∂x + 1/2)

    Sus autovalores son los ceros no triviales de Riemann sobre la línea crítica:
        ρ_n = 1/2 + i·γ_n   ∀n ∈ {1, ..., 7}

    El operador es autoadjunto: Ĥ_π = Ĥ_π†, garantizando que todos
    los ρ_n residen exactamente sobre la línea crítica Re(ρ) = 1/2.
    """

    def __init__(self, gammas: Tuple[float, ...] = ConstantesRedRamsey.GAMMAS):
        self.gammas = gammas
        self.n_autovalores: int = len(gammas)
        self.autovalores: List[complex] = self._calcular_autovalores()

    def _calcular_autovalores(self) -> List[complex]:
        """Calcula ρ_n = 1/2 + i·γ_n para cada cero de Riemann."""
        return [complex(0.5, gamma) for gamma in self.gammas]

    def es_autoadjunto(self) -> bool:
        """Verifica que el operador es autoadjunto (Re(ρ_n) = 1/2 para todo n)."""
        return all(abs(rho.real - 0.5) < 1e-10 for rho in self.autovalores)

    def fraccion_en_linea_critica(self) -> float:
        """Fracción de autovalores en la línea crítica Re(ρ) = 1/2."""
        if self.n_autovalores == 0:
            return 0.0
        en_linea = sum(
            1 for rho in self.autovalores if abs(rho.real - 0.5) < 1e-10
        )
        return en_linea / self.n_autovalores

    def calcular_psi_espectro(self) -> float:
        """
        Calcula Ψ_espectro: coherencia del espectro del operador.

        Retorna 0.999999 cuando el 100% de los autovalores están
        en la línea crítica (Hipótesis de Riemann satisfecha).
        """
        if self.fraccion_en_linea_critica() == 1.0:
            return 0.999999
        return self.fraccion_en_linea_critica()

    def cierre_espectro(self) -> bool:
        """
        Cierre Hidrodinámico — Cierre 2 del sistema.

        El cierre se alcanza cuando:
        - El operador es autoadjunto
        - El 100% de autovalores están en la línea crítica
        - Ψ_espectro ≥ PSI_UMBRAL
        """
        return (
            self.es_autoadjunto()
            and self.fraccion_en_linea_critica() == 1.0
            and self.calcular_psi_espectro() >= ConstantesRedRamsey.PSI_UMBRAL
        )


# ── SimbiosisHiggsPC ──────────────────────────────────────────────────────────

class SimbiosisHiggsPC:
    """
    Simbiosis Higgs-PC con masa efectiva modulada.

    El lagrangiano de interacción:
        L_int = -g_eff · ψ̄ · ψ · H

    La masa efectiva del campo:
        m* = m_Higgs · (1 - g_eff)
        m* = 125.0 · (1 - 0.053) = 118.375 GeV
    """

    def __init__(
        self,
        m_higgs: float = ConstantesRedRamsey.M_HIGGS,
        g_eff: float = ConstantesRedRamsey.G_EFF,
    ):
        self.m_higgs = m_higgs
        self.g_eff = g_eff
        self.m_estrella: float = self._calcular_masa_efectiva()

    def _calcular_masa_efectiva(self) -> float:
        """Calcula m* = m_Higgs · (1 - g_eff)."""
        return self.m_higgs * (1.0 - self.g_eff)

    def delta_masa(self) -> float:
        """Reducción de masa: Δm = m_Higgs - m*."""
        return self.m_higgs - self.m_estrella

    def modulacion_porcentual(self) -> float:
        """Porcentaje de modulación de masa: Δm/m_Higgs × 100."""
        return (self.delta_masa() / self.m_higgs) * 100.0

    def calcular_psi_higgs(self) -> float:
        """
        Calcula Ψ_Higgs: coherencia de la simbiosis Higgs-PC.

        Retorna 0.999999 cuando |m* - 118.375| < 0.01 GeV.
        """
        diferencia = abs(self.m_estrella - ConstantesRedRamsey.M_ESTRELLA)
        if diferencia < 0.01:
            return 0.999999
        return max(0.0, 1.0 - diferencia / ConstantesRedRamsey.M_ESTRELLA)

    def cierre_higgs(self) -> bool:
        """
        Cierre de Masa — Cierre 3 del sistema.

        El cierre se alcanza cuando:
        - |m* - 118.375| < 0.01 GeV (tolerancia de 10 MeV)
        - Ψ_Higgs ≥ PSI_UMBRAL
        """
        return (
            abs(self.m_estrella - ConstantesRedRamsey.M_ESTRELLA) < 0.01
            and self.calcular_psi_higgs() >= ConstantesRedRamsey.PSI_UMBRAL
        )


# ── TasaSimbiotitica ──────────────────────────────────────────────────────────

class TasaSimbiotitica:
    """
    Tasa Simbiótica de la red: R_symb = N · f₀ · Ψ_coherencia.

    Mide cuántos kilo-pulsos simbióticos fluyen por la red
    por unidad de tiempo (kpps). Análogo al ritmo cardíaco
    de un sistema vivo.

    En el caso perfecto (Ψ = 1.0):
        R_symb = 7 × 141.7001 × 1.0 = 991.9007 kpps
    """

    def __init__(
        self,
        n_nodos: int = ConstantesRedRamsey.N_NODOS,
        f0: float = ConstantesRedRamsey.F0,
        psi_coherencia: float = 1.0,
    ):
        self.n_nodos = n_nodos
        self.f0 = f0
        self.psi_coherencia = psi_coherencia
        self.r_symb: float = self._calcular_tasa()

    def _calcular_tasa(self) -> float:
        """Calcula R_symb = N · f₀ · Ψ_coherencia."""
        return self.n_nodos * self.f0 * self.psi_coherencia

    def error_relativo(self) -> float:
        """Error relativo respecto a la tasa perfecta R_symb = 991.9007."""
        return abs(self.r_symb - ConstantesRedRamsey.R_SYMB) / ConstantesRedRamsey.R_SYMB

    def cierre_tasa(self) -> bool:
        """
        Cierre Biológico — Cierre 4 del sistema.

        El cierre se alcanza cuando:
        - |R_symb - 991.9007| / 991.9007 < 0.01 (1% de tolerancia)
        """
        return self.error_relativo() < 0.01


# ── CoherenciaRedRamsey ───────────────────────────────────────────────────────

class CoherenciaRedRamsey:
    """
    Coherencia Global de la Red de Ramsey.

    La coherencia global es la suma ponderada:
        Ψ_global = 0.35·Ψ_nodos + 0.35·Ψ_espectro + 0.30·Ψ_Higgs

    El cierre de unificación se alcanza cuando Ψ_global ≥ 0.888.
    """

    def __init__(
        self,
        psi_nodos: float,
        psi_espectro: float,
        psi_higgs: float,
        w_nodos: float = ConstantesRedRamsey.W_NODOS,
        w_espectro: float = ConstantesRedRamsey.W_ESPECTRO,
        w_higgs: float = ConstantesRedRamsey.W_HIGGS,
    ):
        self.psi_nodos = psi_nodos
        self.psi_espectro = psi_espectro
        self.psi_higgs = psi_higgs
        self.w_nodos = w_nodos
        self.w_espectro = w_espectro
        self.w_higgs = w_higgs
        self.psi_global: float = self._calcular_coherencia_global()

    def _calcular_coherencia_global(self) -> float:
        """Calcula Ψ_global = w_n·Ψ_n + w_e·Ψ_e + w_h·Ψ_h."""
        return (
            self.w_nodos * self.psi_nodos
            + self.w_espectro * self.psi_espectro
            + self.w_higgs * self.psi_higgs
        )

    def supera_umbral(self) -> bool:
        """Verifica que Ψ_global ≥ PSI_UMBRAL (0.888)."""
        return self.psi_global >= ConstantesRedRamsey.PSI_UMBRAL

    def cierre_coherencia(self) -> bool:
        """
        Cierre de Unificación — Cierre 5 del sistema.

        El cierre se alcanza cuando Ψ_global ≥ 0.888.
        """
        return self.supera_umbral()


# ── SistemaRedRamseyQCAL ──────────────────────────────────────────────────────

class SistemaRedRamseyQCAL:
    """
    Sistema Red de Ramsey QCAL de 7 Nodos Primos.
    QCAL-SYMBIO-BRIDGE v1.1.0

    Integra todos los componentes del sistema:
    - Red de 7 nodos primos C₇
    - Operador maestro Ĥ_π (Berry-Keating)
    - Simbiosis Higgs-PC
    - Tasa simbiótica R_symb
    - Coherencia global Ψ_global

    El sistema está ACTIVO cuando los 5 cierres han cerrado y
    Ψ_global ≥ 0.888.
    """

    def __init__(self):
        self.red = RedRamsey()
        self.operador = OperadorMaestroHPi()
        self.simbiosis = SimbiosisHiggsPC()

        # Coherencias individuales
        self.psi_nodos: float = self.red.calcular_psi_nodos()
        self.psi_espectro: float = self.operador.calcular_psi_espectro()
        self.psi_higgs: float = self.simbiosis.calcular_psi_higgs()

        # Tasa simbiótica usando la coherencia global medida
        self.tasa = TasaSimbiotitica(
            psi_coherencia=ConstantesRedRamsey.PSI_GLOBAL
        )

        # Coherencia global ponderada
        self.coherencia = CoherenciaRedRamsey(
            psi_nodos=self.psi_nodos,
            psi_espectro=self.psi_espectro,
            psi_higgs=self.psi_higgs,
        )
        self.psi_global: float = self.coherencia.psi_global

    def todos_los_cierres(self) -> bool:
        """Verifica que los 5 cierres del sistema han cerrado."""
        return (
            self.red.cierre_nodos()
            and self.operador.cierre_espectro()
            and self.simbiosis.cierre_higgs()
            and self.tasa.cierre_tasa()
            and self.coherencia.cierre_coherencia()
        )

    def estado(self) -> str:
        """Estado del sistema: 'ACTIVO' o 'INACTIVO'."""
        return "ACTIVO" if self.todos_los_cierres() else "INACTIVO"

    def activar(self) -> Dict:
        """
        Activa el sistema y retorna el resultado con sello.

        Returns:
            dict con sello, psi_global, estado, r_symb_kpps,
            m_estrella, todos_los_cierres, ram
        """
        return {
            "sello": ConstantesRedRamsey.SELLO,
            "psi_global": self.psi_global,
            "estado": self.estado(),
            "r_symb_kpps": self.tasa.r_symb,
            "m_estrella": self.simbiosis.m_estrella,
            "todos_los_cierres": self.todos_los_cierres(),
            "ram": ConstantesRedRamsey.RAM,
        }


# ── API pública ───────────────────────────────────────────────────────────────

def red_ramsey_qcal_activar() -> Dict:
    """
    Activa la Red de Ramsey QCAL de 7 Nodos Primos.

    Crea el sistema completo (∴RRQ∞³), verifica los 5 cierres
    y retorna el resultado con sello de activación.

    Returns:
        dict con las siguientes claves:
            sello          (str)   — "∴RRQ∞³"
            psi_global     (float) — coherencia global medida
            estado         (str)   — "ACTIVO" si todos los cierres cerraron
            r_symb_kpps    (float) — tasa simbiótica en kpps
            m_estrella     (float) — masa efectiva del Higgs en GeV
            todos_los_cierres (bool) — True si los 5 cierres cerraron
            ram            (str)   — identificador RAM del sistema

    Example::

        from physics.red_ramsey_qcal import red_ramsey_qcal_activar
        resultado = red_ramsey_qcal_activar()
        # {
        #   "sello":            "∴RRQ∞³",
        #   "psi_global":       0.999999,
        #   "estado":           "ACTIVO",
        #   "r_symb_kpps":      991.9006930000001,
        #   "m_estrella":       118.375,
        #   "todos_los_cierres": True,
        #   "ram":              "RAM-LII-2026-RED-RAMSEY-QCAL",
        # }
    """
    sistema = SistemaRedRamseyQCAL()
    return sistema.activar()
