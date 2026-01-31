#!/usr/bin/env python3
"""
QCAL Unification API
====================

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
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
