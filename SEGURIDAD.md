# 🔒 Política de Seguridad

## Visión General

Este documento describe las políticas y procedimientos de seguridad para el proyecto Ramsey Formal Verification. Dado que este proyecto involucra verificación matemática formal y certificación criptográfica, la seguridad e integridad de los datos son fundamentales.

## 📋 Tabla de Contenidos

1. [Versiones Soportadas](#versiones-soportadas)
2. [Reporte de Vulnerabilidades](#reporte-de-vulnerabilidades)
3. [Integridad de Datos](#integridad-de-datos)
4. [Gestión de Dependencias](#gestión-de-dependencias)
5. [Reproducibilidad](#reproducibilidad)
6. [Verificación Criptográfica](#verificación-criptográfica)
7. [Mejores Prácticas](#mejores-prácticas)

## 🛡️ Versiones Soportadas

Actualmente se proporciona soporte de seguridad para las siguientes versiones:

| Versión | Soportada          | Notas                                    |
| ------- | ------------------ | ---------------------------------------- |
| main    | ✅ Sí             | Rama principal con últimas correcciones  |
| 1.0.x   | ✅ Sí             | Versión estable con soporte completo     |
| < 1.0   | ❌ No             | Versiones de desarrollo no soportadas    |

## 🚨 Reporte de Vulnerabilidades

### Cómo Reportar

Si descubres una vulnerabilidad de seguridad, por favor **NO** la reportes públicamente a través de GitHub Issues. En su lugar:

1. **Envía un email a**: [Crear email de contacto de seguridad]
2. **Incluye**:
   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducir el problema
   - Impacto potencial
   - Cualquier solución o mitigación propuesta

3. **Tiempo de respuesta esperado**:
   - Acuse de recibo: 48 horas
   - Evaluación inicial: 7 días
   - Resolución planificada: 30 días (dependiendo de la severidad)

### Proceso de Divulgación Responsable

1. **Reporte confidencial** → Evaluación del equipo de seguridad
2. **Desarrollo de parche** → Prueba en entorno privado
3. **Coordinación de divulgación** → Notificación a usuarios afectados
4. **Publicación pública** → Después de que el parche esté disponible

## 🔐 Integridad de Datos

### Archivos Críticos

Los siguientes archivos son críticos para la verificación matemática y **DEBEN** mantener su integridad:

#### 1. Datos de Verificación
- `data/rpsi_vibration_model.json` - Parámetros del modelo vibracional
- `data/verified_bound_R55.json` - Resultados verificados de R(5,5)
- `data/coloring_sat_r55.cnf` - Instancia SAT para verificación
- `data/rpsi_5_5_n16.cnf` - Instancia SAT completa

#### 2. Beacons Criptográficos
- `.qcal_beacon` - Firma criptográfica principal
- `.qcal_beacon_r33`, `.qcal_beacon_r44`, `.qcal_beacon_r66`, `.qcal_beacon_r88` - Beacons específicos

#### 3. Certificados
- `certificates/*.smt2` - Instancias SMT2 para verificación
- `Rpsi_*_certification.json` - Certificados de resultados

### Verificación de Checksums

Todos los archivos críticos tienen checksums SHA-256 documentados en `ENV.lock`. Para verificar la integridad:

```bash
# Verificar todos los archivos de datos
python scripts/verify_integrity.py

# Verificar un archivo específico
sha256sum data/rpsi_vibration_model.json
# Debe coincidir con: 539f00a7d61c9c589d1b7adeb4c9856c8de00122c98a764fe7bc3ff47eff93bb
```

### Protección de Modificaciones

- ✅ **PERMITIDO**: Agregar nuevos archivos de datos con documentación
- ⚠️ **REQUIERE REVISIÓN**: Modificar archivos de datos existentes
- ❌ **PROHIBIDO**: Modificar archivos críticos sin actualizar checksums y documentación

## 📦 Gestión de Dependencias

### Principio de Mínimo Privilegio

- Solo se incluyen dependencias estrictamente necesarias
- Todas las dependencias están fijadas a versiones específicas
- Se realiza auditoría de seguridad regularmente

### Python Dependencies

```bash
# Verificar vulnerabilidades conocidas
pip install pip-audit
pip-audit -r requirements-lock.txt

# Actualizar dependencias (con cuidado)
pip-compile requirements.in --upgrade
# Revisar cambios antes de aplicar
```

### Node.js Dependencies

```bash
# Auditoría de seguridad
npm audit

# Reparar vulnerabilidades automáticamente (revisar cambios)
npm audit fix

# Actualizar package-lock.json
npm install
```

### Lean Dependencies

```bash
# Actualizar mathlib (verificar compatibilidad)
lake update

# Las dependencias de Lean están controladas por:
# - lean-toolchain (versión de Lean)
# - lakefile.lean (dependencias de paquetes)
```

## 🔄 Reproducibilidad

### Garantías de Reproducibilidad

El proyecto garantiza que los resultados son reproducibles si:

1. **Entorno coincide con ENV.lock**
   - Versiones de Python, Lean, Node.js
   - Versiones exactas de dependencias
   - Versiones de solucionadores SAT/SMT

2. **Datos íntegros**
   - Checksums verificados
   - Archivos beacon sin modificar
   - Parámetros f₀ y ε constantes

3. **Procedimiento estandarizado**
   - Seguir WORKFLOW.md
   - Usar scripts de verificación oficiales
   - Documentar cualquier desviación

### Script de Verificación de Entorno

```bash
# Verificar que el entorno cumple con ENV.lock
python scripts/verify_environment.py

# Salida esperada:
# ✓ Python version: 3.12.3 (>= 3.10)
# ✓ Lean version: 4.3.0
# ✓ All dependencies match ENV.lock
# ✓ All data checksums valid
# ✓ Environment is reproducible
```

### Contenedores Docker (Recomendado)

Para máxima reproducibilidad, se recomienda usar contenedores:

```bash
# Construir imagen Docker
docker build -t ramsey-verification .

# Ejecutar verificación completa
docker run --rm ramsey-verification python run_tests.py

# Ejecutar Lean verification
docker run --rm ramsey-verification lake build
```

## 🔏 Verificación Criptográfica

### QCAL Beacon

El archivo `.qcal_beacon` contiene una firma criptográfica que certifica:

- Frecuencia fundamental f₀ = 141.7001 Hz
- Parámetros del modelo vibracional
- Resultados de verificación R(5,5) = 43

**Estructura del beacon:**

```json
{
  "framework": "QCAL ∞³",
  "frequency_hz": 141.7001,
  "theorem": "R(5,5) = 43",
  "timestamp": "ISO-8601",
  "signature": "cryptographic_seal"
}
```

### Validación del Beacon

```bash
# Verificar beacon principal
python display_seal.py

# Validación en CI/CD
# Ver: .github/workflows/ci.yml - validate-qcal job
```

### Protección contra Falsificación

- Los beacons son inmutables una vez generados
- Cualquier modificación invalida la firma
- CI/CD verifica automáticamente la validez del beacon
- Timestamp proporciona prueba temporal

## 🛠️ Mejores Prácticas

### Para Desarrolladores

1. **Nunca commitear secretos**
   ```bash
   # Usar .gitignore para archivos sensibles
   # Ejemplo: .env, *.key, *.pem
   ```

2. **Revisar dependencias antes de agregar**
   ```bash
   # Verificar licencia y seguridad
   pip show package-name
   npm info package-name
   ```

3. **Actualizar ENV.lock al cambiar dependencias**
   ```bash
   # Después de modificar requirements.in o package.json
   # 1. Regenerar lock file
   # 2. Actualizar checksums en ENV.lock
   # 3. Documentar cambios en commit
   ```

4. **Ejecutar verificación local antes de push**
   ```bash
   # Suite completa de verificación
   ./build_and_verify.sh
   python run_tests.py
   python scripts/verify_integrity.py
   ```

### Para Usuarios

1. **Verificar integridad después de clonar**
   ```bash
   git clone https://github.com/motanova84/Ramsey.git
   cd Ramsey
   python scripts/verify_integrity.py
   ```

2. **Usar entornos virtuales**
   ```bash
   # Python
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install -r requirements-lock.txt
   ```

3. **Reportar discrepancias**
   - Si checksums no coinciden → Reportar issue
   - Si resultados difieren → Documentar diferencias
   - Si tests fallan → Verificar entorno primero

## 🔍 Auditoría y Monitoreo

### Revisiones de Seguridad

- **Mensual**: Auditoría de dependencias
- **Trimestral**: Revisión de políticas de seguridad
- **Anual**: Auditoría completa de código y procesos

### Herramientas Automatizadas

- GitHub Dependabot: Alertas de vulnerabilidades
- GitHub Code Scanning: Análisis estático de código
- GitHub Secret Scanning: Detección de secretos
- CI/CD Security Checks: Verificación continua

### Métricas de Seguridad

- Tiempo medio de resolución de vulnerabilidades: < 30 días
- Cobertura de tests de seguridad: > 80%
- Actualizaciones de dependencias: Mensual
- Revisiones de código: 100% de PRs

## 📚 Referencias y Recursos

### Documentación Relacionada

- [ENV.lock](ENV.lock) - Especificación completa del entorno
- [RESUMEN_DE_SEGURIDAD.md](RESUMEN_DE_SEGURIDAD.md) - Resumen ejecutivo
- [WORKFLOW.md](WORKFLOW.md) - Flujo de trabajo de verificación
- [TESTING.md](TESTING.md) - Documentación de testing

### Estándares Seguidos

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Reproducible Builds](https://reproducible-builds.org/)

### Herramientas Recomendadas

- `pip-audit` - Auditoría de paquetes Python
- `npm audit` - Auditoría de paquetes Node.js
- `bandit` - Análisis de seguridad para Python
- `safety` - Verificación de vulnerabilidades conocidas

## 📞 Contacto

Para preguntas sobre seguridad:

- **Email de seguridad**: [A definir]
- **Mantenedor del proyecto**: José Manuel Mota Burruezo (JMMB Ψ✧∴)
- **Repositorio**: https://github.com/motanova84/Ramsey
- **Issues públicos** (no sensibles): GitHub Issues

---

**Última actualización**: 2026-01-06  
**Versión del documento**: 1.0  
**Responsable**: Equipo de Desarrollo Ramsey
