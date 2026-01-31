#!/usr/bin/env python3
"""
QCAL Unification API
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
