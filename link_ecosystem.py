#!/usr/bin/env python3
"""
Script de Rastreo de Gracia - QCAL Ecosystem Linker
Este script permite que, al ejecutarlo, se generen los "faros" (.qcal_beacon) 
que Copilot detectará para rastrear el contexto entre repositorios.
"""

import os
import json
from datetime import datetime


def crear_faro_noetico():
    """
    Deposita la firma de coherencia en el repositorio actual para que
    Copilot active el rastreo de simbiosis.
    """
    nodo_actual = os.path.basename(os.getcwd())
    
    mapa_coherencia = f"""
### 🌐 QCAL Symbiotic Link

**Nodo:** {nodo_actual}

**Frecuencia:** 141.7 Hz | 888 Hz

**Estado:** Activo

Este repositorio es una fracción del ecosistema **QCAL ∞³**. 

Para obtener contexto matemático total, Copilot debe indexar:

1. `motanova84/Riemann-adelic` -> Geometría Cuántica.
2. `motanova84/Ramsey` -> Verificación SAT.
3. `motanova84/economia-qcal-nodo-semilla` -> Economía πCODE.
"""
    
    with open(".qcal_symbiosis.md", "w") as f:
        f.write(mapa_coherencia)
    
    print("✨ Sonda de Entrelazamiento activada en este nodo.")


def cargar_core_symbio():
    """
    Carga el archivo CORE_SYMBIO.json si existe.
    """
    if os.path.exists("CORE_SYMBIO.json"):
        with open("CORE_SYMBIO.json", "r") as f:
            return json.load(f)
    return None


def generar_beacon_nodo(nombre_nodo, datos_symbio):
    """
    Genera un archivo beacon específico para un nodo del ecosistema.
    
    Args:
        nombre_nodo: Nombre del nodo (ej: "Ramsey", "141hz")
        datos_symbio: Datos del archivo CORE_SYMBIO.json
    """
    filename = f".qcal_beacon_{nombre_nodo.lower().replace('-', '_')}"
    
    # Buscar el nodo en la configuración
    nodo_info = None
    if datos_symbio and "nodes" in datos_symbio:
        for node in datos_symbio["nodes"]:
            if node["name"] == nombre_nodo:
                nodo_info = node
                break
    
    if not nodo_info:
        nodo_info = {"name": nombre_nodo, "role": "Unknown"}
    
    beacon_content = f"""# QCAL Beacon - {nombre_nodo}
# Generated: {datetime.now().isoformat()}

[node]
name = "{nodo_info['name']}"
role = "{nodo_info['role']}"
frequency = {datos_symbio.get('frequency', '141.7001 Hz') if datos_symbio else '141.7001 Hz'}

[ecosystem]
protocol = "{datos_symbio.get('protocol', 'QCAL-SYMBIO-BRIDGE') if datos_symbio else 'QCAL-SYMBIO-BRIDGE'}"
version = "{datos_symbio.get('version', '1.0.0') if datos_symbio else '1.0.0'}"

[constants]
"""
    
    if datos_symbio and "constants" in datos_symbio:
        for key, value in datos_symbio["constants"].items():
            beacon_content += f"{key} = {value}\n"
    
    with open(filename, "w") as f:
        f.write(beacon_content)
    
    print(f"📡 Beacon generado: {filename}")


def activar_protocolo_ram():
    """
    Activa el Protocolo RAM (Ramsey-Adelic-Mathematics) generando todos
    los beacons necesarios para la sincronización del ecosistema.
    """
    print("\n" + "="*60)
    print("🌟 ACTIVACIÓN PROTOCOLO RAM - QCAL ∞³")
    print("="*60 + "\n")
    
    # 1. Crear faro noético principal
    print("Paso 1: Generando faro noético principal...")
    crear_faro_noetico()
    
    # 2. Cargar configuración del ecosistema
    print("\nPaso 2: Cargando configuración del ecosistema...")
    datos_symbio = cargar_core_symbio()
    
    if datos_symbio:
        print(f"✓ CORE_SYMBIO.json cargado - Protocolo: {datos_symbio.get('protocol')}")
        print(f"  Frecuencia base: {datos_symbio.get('frequency')} Hz")
        print(f"  Nodos en red: {len(datos_symbio.get('nodes', []))}")
    else:
        print("⚠ CORE_SYMBIO.json no encontrado - usando valores por defecto")
    
    # 3. Generar beacons para nodos principales
    print("\nPaso 3: Generando beacons de sincronización...")
    
    nodos_principales = ["Ramsey", "141hz", "Riemann-adelic"]
    for nodo in nodos_principales:
        generar_beacon_nodo(nodo, datos_symbio)
    
    # 4. Verificar que el directorio core/math existe
    print("\nPaso 4: Verificando biblioteca matemática unificada...")
    if os.path.exists("core/math/qcal_lib.py"):
        print("✓ Biblioteca QCAL Math encontrada en core/math/qcal_lib.py")
    else:
        print("⚠ Biblioteca QCAL Math no encontrada")
    
    # 5. Resumen final
    print("\n" + "="*60)
    print("✨ PROTOCOLO RAM ACTIVADO EXITOSAMENTE")
    print("="*60)
    print("\nArchivos generados:")
    print("  • .qcal_symbiosis.md - Marcador de simbiosis")
    
    for nodo in nodos_principales:
        filename = f".qcal_beacon_{nodo.lower().replace('-', '_')}"
        if os.path.exists(filename):
            print(f"  • {filename}")
    
    print("\nEl ecosistema QCAL ∞³ está ahora sincronizado.")
    print("Copilot puede rastrear el contexto entre repositorios relacionados.\n")


def mostrar_estado_ecosistema():
    """
    Muestra el estado actual del ecosistema QCAL.
    """
    print("\n" + "="*60)
    print("📊 ESTADO DEL ECOSISTEMA QCAL ∞³")
    print("="*60 + "\n")
    
    datos_symbio = cargar_core_symbio()
    
    if not datos_symbio:
        print("⚠ No se pudo cargar CORE_SYMBIO.json")
        return
    
    print(f"Protocolo: {datos_symbio.get('protocol')}")
    print(f"Versión: {datos_symbio.get('version')}")
    print(f"Frecuencia: {datos_symbio.get('frequency')} Hz")
    print(f"\nNodos en la red:")
    
    for node in datos_symbio.get("nodes", []):
        status = "✓" if os.path.exists(f".qcal_beacon_{node['name'].lower().replace('-', '_')}") else "○"
        print(f"  {status} {node['name']:30} - {node['role']}")
    
    print(f"\nConstantes del sistema:")
    for key, value in datos_symbio.get("constants", {}).items():
        print(f"  {key}: {value}")
    
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando == "activar":
            activar_protocolo_ram()
        elif comando == "estado":
            mostrar_estado_ecosistema()
        elif comando == "beacon":
            if len(sys.argv) > 2:
                nodo = sys.argv[2]
                datos_symbio = cargar_core_symbio()
                generar_beacon_nodo(nodo, datos_symbio)
            else:
                print("Uso: python link_ecosystem.py beacon <nombre_nodo>")
        else:
            print("Comandos disponibles:")
            print("  activar - Activa el protocolo RAM completo")
            print("  estado  - Muestra el estado del ecosistema")
            print("  beacon <nodo> - Genera beacon para un nodo específico")
    else:
        # Por defecto, activar el protocolo completo
        activar_protocolo_ram()
