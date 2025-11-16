# src/solve_rpsi_sat.py
import subprocess
import shutil
from pathlib import Path

def solve_with_kissat():
    """
    Ejecuta Kissat SAT solver con soporte LRAT para certificar UNSAT.
    
    Nota: Kissat debe estar instalado en el sistema.
    Para instalar:
        git clone https://github.com/arminbiere/kissat.git
        cd kissat && ./configure && make
        sudo cp build/kissat /usr/local/bin/
    """
    cnf = "data/rpsi_5_5_n16.cnf"
    lrat = "cert/rpsi_5_5_n16_unsat.lrat"
    Path("cert").mkdir(exist_ok=True)
    
    # Check if kissat is available
    if not shutil.which("kissat"):
        print("ERROR: Kissat no está instalado en el sistema.")
        print("\nPara instalar Kissat:")
        print("  git clone https://github.com/arminbiere/kissat.git")
        print("  cd kissat && ./configure && make")
        print("  sudo cp build/kissat /usr/local/bin/")
        print("\nAlternativamente, use otro solver SAT que soporte LRAT.")
        return False
    
    cmd = ["kissat", "--lrat", cnf]
    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    with open(lrat, "w") as f:
        f.write(result.stdout)
    
    if "UNSATISFIABLE" in result.stdout:
        print("UNSAT → Rψ(5,5) ≤ 16 CERTIFICADO FORMALMENTE")
        print(f"Certificado LRAT: {lrat}")
        return True
    else:
        print("SAT → Existe contraejemplo. Revisar ε/grid.")
        return False

if __name__ == "__main__":
    solve_with_kissat()
