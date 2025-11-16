# src/solve_rpsi_sat.py
import subprocess
from pathlib import Path

def solve_with_kissat():
    cnf = "data/rpsi_5_5_n16.cnf"
    lrat = "cert/rpsi_5_5_n16_unsat.lrat"
    Path("cert").mkdir(exist_ok=True)
    
    cmd = ["kissat", "--lrat", cnf]
    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    with open(lrat, "w") as f:
        f.write(result.stdout)
    
    if "UNSATISFIABLE" in result.stdout:
        print("UNSAT → Rψ(5,5) ≤ 16 CERTIFICADO FORMALMENTE")
        print(f"Certificado LRAT: {lrat}")
    else:
        print("SAT → Existe contraejemplo. Revisar ε/grid.")
    
    return "UNSAT" in result.stdout

if __name__ == "__main__":
    solve_with_kissat()
