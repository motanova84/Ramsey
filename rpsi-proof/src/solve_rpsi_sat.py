#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver SAT para Instancias Rψ(r,s)

Este script proporciona un wrapper para ejecutar SAT solvers sobre instancias
generadas de Rψ(r,s) ≤ n y procesar los resultados.

Soporta múltiples SAT solvers:
- PySAT (pysat library) - Python nativo
- Kissat - solver C++ de alto rendimiento
- CaDiCaL - solver C++ certificado
- Z3 - SMT solver con backend SAT

Autores: José Manuel Mota Burruezo - JMMB Ψ✧∴
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³
"""

import argparse
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


def parse_dimacs_cnf(filename: str):
    """
    Parse un archivo DIMACS CNF y extrae información básica.
    
    Returns:
        tuple: (num_vars, num_clauses, metadata)
    """
    num_vars = 0
    num_clauses = 0
    metadata = {}
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('c'):
                # Extraer metadata de comentarios
                if 'Rψ' in line or 'Rpsi' in line:
                    metadata['problem'] = line[2:].strip()
            elif line.startswith('p cnf'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
                break
    
    return num_vars, num_clauses, metadata


def solve_with_pysat(cnf_file: str, timeout: int = 3600):
    """
    Resuelve usando PySAT (Python SAT solver library).
    
    Args:
        cnf_file: Ruta al archivo CNF
        timeout: Timeout en segundos
    
    Returns:
        tuple: (status, time, solution/proof)
    """
    try:
        from pysat.solvers import Solver
        from pysat.formula import CNF
        import time
        
        print("Cargando instancia CNF...")
        cnf = CNF(from_file=cnf_file)
        
        print(f"Iniciando solver PySAT...")
        print(f"  Variables: {cnf.nv}")
        print(f"  Cláusulas: {len(cnf.clauses)}")
        
        solver = Solver(name='glucose4', bootstrap_with=cnf)
        
        start = time.time()
        result = solver.solve()
        elapsed = time.time() - start
        
        if result:
            solution = solver.get_model()
            solver.delete()
            return "SAT", elapsed, solution
        else:
            solver.delete()
            return "UNSAT", elapsed, None
            
    except ImportError:
        print("❌ PySAT no está instalado. Instalar con: pip install python-sat")
        return None, 0, None
    except Exception as e:
        print(f"❌ Error al ejecutar PySAT: {e}")
        return None, 0, None


def solve_with_z3(cnf_file: str, timeout: int = 3600):
    """
    Resuelve usando Z3 SMT solver.
    
    Args:
        cnf_file: Ruta al archivo CNF
        timeout: Timeout en segundos (milisegundos para Z3)
    
    Returns:
        tuple: (status, time, solution/proof)
    """
    try:
        from z3 import Bool, Solver, Or, Not, sat, unsat
        import time
        
        print("Cargando instancia CNF en Z3...")
        
        # Parse CNF manualmente
        clauses = []
        num_vars = 0
        
        with open(cnf_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('p cnf'):
                    num_vars = int(line.split()[2])
                elif not line.startswith('c') and line and not line.startswith('p'):
                    clause = [int(x) for x in line.split()[:-1]]  # Remove trailing 0
                    clauses.append(clause)
        
        print(f"  Variables: {num_vars}")
        print(f"  Cláusulas: {len(clauses)}")
        
        # Crear variables Z3
        vars = [Bool(f'x_{i}') for i in range(num_vars + 1)]
        
        # Crear solver
        s = Solver()
        s.set("timeout", timeout * 1000)  # Z3 usa milisegundos
        
        # Agregar cláusulas
        for clause in clauses:
            z3_clause = Or([vars[abs(lit)] if lit > 0 else Not(vars[abs(lit)]) for lit in clause])
            s.add(z3_clause)
        
        print("Resolviendo con Z3...")
        start = time.time()
        result = s.check()
        elapsed = time.time() - start
        
        if result == sat:
            model = s.model()
            return "SAT", elapsed, model
        elif result == unsat:
            return "UNSAT", elapsed, None
        else:
            return "UNKNOWN", elapsed, None
            
    except ImportError:
        print("❌ Z3 no está instalado. Instalar con: pip install z3-solver")
        return None, 0, None
    except Exception as e:
        print(f"❌ Error al ejecutar Z3: {e}")
        return None, 0, None


def solve_with_external(cnf_file: str, solver_cmd: str, timeout: int = 3600):
    """
    Resuelve usando un solver externo (ej. kissat, cadical).
    
    Args:
        cnf_file: Ruta al archivo CNF
        solver_cmd: Comando del solver
        timeout: Timeout en segundos
    
    Returns:
        tuple: (status, time, output)
    """
    import time
    
    try:
        print(f"Ejecutando solver externo: {solver_cmd}")
        start = time.time()
        
        result = subprocess.run(
            [solver_cmd, cnf_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        elapsed = time.time() - start
        
        # Parse output
        output = result.stdout
        
        if "s SATISFIABLE" in output or "SAT" in output.split('\n')[0]:
            return "SAT", elapsed, output
        elif "s UNSATISFIABLE" in output or "UNSAT" in output.split('\n')[0]:
            return "UNSAT", elapsed, output
        else:
            return "UNKNOWN", elapsed, output
            
    except FileNotFoundError:
        print(f"❌ Solver '{solver_cmd}' no encontrado en PATH")
        return None, 0, None
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout después de {timeout}s")
        return "TIMEOUT", timeout, None
    except Exception as e:
        print(f"❌ Error al ejecutar solver externo: {e}")
        return None, 0, None


def save_certificate(result: dict, output_file: str):
    """Guarda el certificado de resultado en formato JSON"""
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n✓ Certificado guardado: {output_file}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Solver SAT para Instancias Rψ(r,s)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Resolver con Z3
  python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver z3
  
  # Resolver con PySAT
  python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver pysat
  
  # Resolver con Kissat (externo)
  python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver kissat
  
  # Con certificado de salida
  python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver z3 --cert ../cert/proof.json
        """
    )
    
    parser.add_argument('cnf_file', type=str,
                       help='Archivo CNF de entrada (formato DIMACS)')
    parser.add_argument('--solver', type=str, default='z3',
                       choices=['z3', 'pysat', 'kissat', 'cadical', 'glucose'],
                       help='SAT solver a utilizar (default: z3)')
    parser.add_argument('--timeout', type=int, default=3600,
                       help='Timeout en segundos (default: 3600)')
    parser.add_argument('--cert', type=str,
                       help='Archivo de salida para certificado JSON')
    
    args = parser.parse_args()
    
    if not Path(args.cnf_file).exists():
        print(f"❌ Error: Archivo no encontrado: {args.cnf_file}")
        sys.exit(1)
    
    print("="*70)
    print("  Solver SAT - Ramsey Vibracional")
    print(f"  Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("="*70)
    
    # Parse instancia
    num_vars, num_clauses, metadata = parse_dimacs_cnf(args.cnf_file)
    print(f"\nInstancia: {args.cnf_file}")
    print(f"  Variables: {num_vars}")
    print(f"  Cláusulas: {num_clauses}")
    if metadata.get('problem'):
        print(f"  Problema: {metadata['problem']}")
    print()
    
    # Resolver
    status, elapsed, result_data = None, 0, None
    
    if args.solver == 'z3':
        status, elapsed, result_data = solve_with_z3(args.cnf_file, args.timeout)
    elif args.solver == 'pysat':
        status, elapsed, result_data = solve_with_pysat(args.cnf_file, args.timeout)
    else:
        # Solver externo
        status, elapsed, result_data = solve_with_external(args.cnf_file, args.solver, args.timeout)
    
    if status is None:
        print("\n❌ No se pudo ejecutar el solver")
        sys.exit(1)
    
    # Mostrar resultados
    print("\n" + "="*70)
    print("  RESULTADO")
    print("="*70)
    print(f"  Estado: {status}")
    print(f"  Tiempo: {elapsed:.3f} segundos")
    
    if status == "SAT":
        print("\n  ✓ SAT: Existe una coloración válida")
        print("  → El bound Rψ(r,s) ≤ n NO está certificado para este n")
        print("  → Existe un contraejemplo (grafo sin cliques monocromáticos)")
    elif status == "UNSAT":
        print("\n  ✓ UNSAT: No existe coloración válida")
        print("  → El bound Rψ(r,s) ≤ n ESTÁ CERTIFICADO")
        print("  → Todo grafo K_n contiene clique monocromático")
    
    print("="*70)
    
    # Guardar certificado si se solicita
    if args.cert:
        certificate = {
            "timestamp": datetime.now().isoformat(),
            "cnf_file": args.cnf_file,
            "solver": args.solver,
            "status": status,
            "time_seconds": elapsed,
            "num_vars": num_vars,
            "num_clauses": num_clauses,
            "metadata": metadata,
            "frequency": "141.7001 Hz",
            "field": "QCAL ∞³"
        }
        save_certificate(certificate, args.cert)
    
    # Exit code: 10 para SAT, 20 para UNSAT (estándar SAT competition)
    if status == "SAT":
        sys.exit(10)
    elif status == "UNSAT":
        sys.exit(20)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
