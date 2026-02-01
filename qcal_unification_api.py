#!/usr/bin/env python3
"""
QCAL Unification API

FastAPI server providing REST endpoints for the QCAL unified framework.

Usage:
    python3 qcal_unification_api.py
    
Then access:
    http://localhost:8000/docs for API documentation
    http://localhost:8000/connections for problem connections
"""

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("Warning: FastAPI not installed. Install with: pip install fastapi uvicorn")

from typing import Dict, List, Any, Optional
from qcal_unified_framework import QCALUnifiedFramework, CrossVerificationProtocol


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="QCAL Unified Framework API",
        description="REST API for Quantum Coherent Algebraic Logic unified framework",
        version="1.0.0"
    )

    # Global framework instance
    framework = QCALUnifiedFramework()
    protocol = CrossVerificationProtocol()


    class ProblemRequest(BaseModel):
        """Request model for problem unification."""
        problem_name: str
        parameters: Optional[Dict[str, Any]] = None


    class UnifiedResponse(BaseModel):
        """Response model for unified problem analysis."""
        qcal_operator: str
        universal_constant: float
        verification_result: Dict[str, Any]
        connected_problems: List[str]


    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "QCAL Unified Framework API",
            "version": "1.0.0",
            "frequency": f"{framework.constants['f0']} Hz",
            "endpoints": {
                "/problems": "List all millennium problems",
                "/unify": "Unify a specific problem through QCAL",
                "/connections": "Get all problem connections",
                "/constants": "Get universal constants",
                "/verify": "Run cross-verification protocol"
            }
        }


    @app.get("/problems")
    async def list_problems():
        """List all millennium problems in the QCAL framework."""
        return {
            "problems": list(framework.problem_metadata.keys()),
            "metadata": framework.problem_metadata
        }


    @app.post("/unify")
    async def unify_problem(request: ProblemRequest):
        """
        Unify a millennium problem through QCAL framework.
        
        Args:
            request: Problem name and optional parameters
            
        Returns:
            Unified response with QCAL analysis
        """
        problem_name = request.problem_name.lower().replace(" ", "_")
        
        if problem_name not in framework.operators:
            raise HTTPException(
                status_code=404,
                detail=f"Problem '{request.problem_name}' not found. "
                       f"Available: {list(framework.operators.keys())}"
            )
        
        # Get parameters or use defaults
        params = request.parameters or framework._get_default_params(problem_name)
        
        # Apply operator
        try:
            operator_func = framework.operators[problem_name]
            eigenvalue = operator_func(params)
            
            # Get metadata
            metadata = framework.problem_metadata[problem_name]
            
            # Get connections
            connections = framework._find_connections(problem_name)
            connected_names = [
                framework.problem_metadata[k]['name'] for k in connections
            ]
            
            # Verification
            verification = framework._verify_problem(problem_name)
            
            return {
                "qcal_operator": metadata['operator'],
                "universal_constant": framework.constants.get(
                    problem_name.split('_')[-1], 
                    framework.constants['f0']
                ),
                "eigenvalue": str(eigenvalue),
                "verification_result": {
                    "status": verification,
                    "method": metadata['verification']
                },
                "connected_problems": connected_names,
                "metadata": metadata
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    @app.get("/connections")
    async def get_problem_connections():
        """Get all connections between problems via QCAL."""
        # Build connection graph
        connection_graph = {}
        
        for problem in framework.operators.keys():
            connections = framework._find_connections(problem)
            connected_names = [
                framework.problem_metadata[k]['name'] for k in connections
            ]
            connection_graph[framework.problem_metadata[problem]['name']] = connected_names
        
        # Calculate coherence score
        coherence = framework.verify_constant_coherence()
        coherence_score = sum(coherence.values()) / len(coherence)
        
        # Get verification status
        verification = protocol.run_cross_verification()
        
        return {
            "connections": connection_graph,
            "coherence_score": coherence_score,
            "verification_status": {
                "unified": verification['unified_status'],
                "qcal_coherent": all(verification['qcal_coherence'].values())
            },
            "universal_frequency": framework.constants['f0']
        }


    @app.get("/constants")
    async def get_constants():
        """Get universal constants and their coherence."""
        coherence = framework.verify_constant_coherence()
        
        return {
            "constants": framework.constants,
            "coherence_tests": coherence,
            "unified_equation": framework.get_unified_equation(),
            "coherence_status": all(coherence.values())
        }


    @app.get("/verify")
    async def run_verification():
        """Run complete cross-verification protocol."""
        results = protocol.run_cross_verification()
        
        # Convert numpy array to list for JSON serialization
        if results['consistency_matrix'] is not None:
            results['consistency_matrix'] = results['consistency_matrix'].tolist()
        
        return results


    @app.get("/summary")
    async def get_summary():
        """Get complete QCAL framework summary."""
        return {
            "title": "QCAL Unified Framework",
            "subtitle": "Quantum Coherent Algebraic Logic",
            "frequency": f"{framework.constants['f0']} Hz",
            "problems": len(framework.operators),
            "constants": framework.constants,
            "table": framework.generate_summary_table(),
            "unified_equation": framework.get_unified_equation()
        }


# Standalone mode for testing without FastAPI
def main():
    """Main function for standalone execution."""
    if not FASTAPI_AVAILABLE:
        print("\n" + "="*60)
        print("QCAL Unification API - Standalone Mode")
        print("="*60)
        print("\nFastAPI is not installed.")
        print("Install with: pip install fastapi uvicorn")
        print("\nShowing framework summary instead:\n")
        
        framework = QCALUnifiedFramework()
        print(framework.generate_summary_table())
        print("\nConstants:", framework.constants)
        print("\nTo run full API server, install FastAPI and run:")
        print("  uvicorn qcal_unification_api:app --reload")
        return
    
    import uvicorn
    print("\n" + "="*60)
    print("Starting QCAL Unification API Server")
    print("="*60)
    print(f"\nFundamental Frequency: {framework.constants['f0']} Hz")
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("Interactive API: http://localhost:8000/redoc")
    print("\n" + "="*60 + "\n")
FastAPI-based REST API for the QCAL Unified Framework
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import uvicorn

from qcal_unified_framework import QCALUnifiedFramework
from cross_verification_protocol import CrossVerificationProtocol


# Pydantic models for request/response
class ProblemRequest(BaseModel):
    """Request model for problem unification."""
    problem_name: str = Field(..., description="Problem key (e.g., 'p_vs_np', 'riemann')")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Problem-specific parameters")


class UnifiedResponse(BaseModel):
    """Response model for unified problem."""
    problem: str
    qcal_operator: str
    universal_constant: float
    eigenvalue: Any
    verification_protocol: str
    connected_problems: List[str]
    parameters: Dict[str, Any]


class ConnectionsResponse(BaseModel):
    """Response model for problem connections."""
    connections: Dict[str, List[str]]
    coherence_score: float
    verification_status: Dict[str, str]


class VerificationResponse(BaseModel):
    """Response model for verification results."""
    individual_results: Dict[str, Any]
    consistency_matrix: List[List[float]]
    qcal_coherence: Dict[str, Any]
    unified_status: bool


# Initialize FastAPI app
app = FastAPI(
    title="QCAL Unified Framework API",
    description="REST API for Quantum Coherent Algebraic Logic unified framework",
    version="1.0.0"
)

# Initialize framework instances
framework = QCALUnifiedFramework()
protocol = CrossVerificationProtocol()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "QCAL Unified Framework API",
        "version": "1.0.0",
        "description": "Unifying millennium problems through spectral operators",
        "endpoints": {
            "/problems": "List all millennium problems",
            "/constants": "Get universal constants",
            "/unify": "Unify a specific problem (POST)",
            "/connections": "Get all problem connections",
            "/verify": "Run cross-verification protocol",
            "/coherence": "Get framework coherence score"
        }
    }


@app.get("/problems")
async def list_problems():
    """List all millennium problems in the framework."""
    return {
        "count": len(framework.problems),
        "problems": framework.problems
    }


@app.get("/constants")
async def get_constants():
    """Get all universal constants."""
    return {
        "count": len(framework.constants),
        "constants": framework.constants,
        "description": {
            "kappa_pi": "P vs NP computational separation constant",
            "f0": "Fundamental resonance frequency (Hz)",
            "critical_line": "Riemann critical line Re(s)",
            "ramsey_ratio": "R(5,5)/R(6,6) ratio",
            "navier_stokes_epsilon": "Navier-Stokes regularity constant",
            "bsd_delta": "BSD conjecture delta",
            "yang_mills_g": "Yang-Mills coupling constant",
            "hodge_sum": "Hodge number sum"
        }
    }


@app.post("/unify", response_model=UnifiedResponse)
async def unify_problem(request: ProblemRequest):
    """
    Unify a millennium problem through QCAL framework.
    
    Args:
        request: Problem request with name and parameters
        
    Returns:
        Unified response with operator, constant, and eigenvalue
    """
    try:
        result = framework.unify_problem(request.problem_name, request.parameters)
        
        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/connections", response_model=ConnectionsResponse)
async def get_problem_connections():
    """
    Get all connections between problems via QCAL.
    
    Returns:
        Connection graph, coherence score, and verification status
    """
    try:
        connections = framework.get_all_connections()
        coherence = framework.calculate_coherence()
        verification_status = framework.get_verification_status()
        
        return {
            "connections": connections,
            "coherence_score": coherence,
            "verification_status": verification_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/verify", response_model=VerificationResponse)
async def run_verification():
    """
    Run complete cross-verification protocol.
    
    Returns:
        Comprehensive verification results
    """
    try:
        results = protocol.run_cross_verification()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/coherence")
async def get_coherence():
    """
    Get framework coherence analysis.
    
    Returns:
        Coherence scores and interpretation
    """
    try:
        coherence = framework.calculate_coherence()
        
        # Determine status
        if coherence > 0.7:
            status = "highly_coherent"
            interpretation = "The framework shows strong internal consistency"
        elif coherence > 0.5:
            status = "moderately_coherent"
            interpretation = "The framework shows reasonable consistency"
        else:
            status = "needs_refinement"
            interpretation = "The framework may need adjustment of constants"
        
        return {
            "coherence_score": coherence,
            "status": status,
            "interpretation": interpretation,
            "constants_used": {
                "f0": framework.constants['f0'],
                "kappa_pi": framework.constants['kappa_pi'],
                "ramsey_ratio": framework.constants['ramsey_ratio']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/problem/{problem_key}")
async def get_problem_details(problem_key: str):
    """
    Get detailed information about a specific problem.
    
    Args:
        problem_key: Problem identifier
        
    Returns:
        Problem details including connections and verification
    """
    if problem_key not in framework.problems:
        raise HTTPException(status_code=404, detail=f"Problem '{problem_key}' not found")
    
    try:
        problem = framework.problems[problem_key]
        connections = framework.find_connections(problem_key)
        verification = framework.verify_problem(problem_key)
        
        # Get default demonstration
        params = framework._get_default_params(problem_key)
        operator = framework.operators[problem_key]
        eigenvalue = operator(params)
        
        return {
            "key": problem_key,
            "name": problem['name'],
            "statement": problem['statement'],
            "operator": problem['operator'],
            "constant": framework.constants[problem['constant']],
            "verification": problem['verification'],
            "verification_status": verification,
            "eigenvalue": eigenvalue,
            "connected_to": connections,
            "connected_problems": [framework.problems[p]['name'] for p in connections]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "framework": "operational",
        "problems_loaded": len(framework.problems),
        "constants_loaded": len(framework.constants)
    }


def main():
    """Run the API server."""
    print("=" * 70)
    print("QCAL UNIFIED FRAMEWORK API")
    print("=" * 70)
    print()
    print("Starting API server...")
    print("Documentation available at: http://localhost:8000/docs")
    print("API endpoints available at: http://localhost:8000")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
