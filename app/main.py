from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from app.models import ConstraintsInput, AnalysisResponse, HealthResponse
from app.scoring import ScoringEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="API Gateway Referee API",
    description="Transparent comparison engine for AWS API Gateway, ALB, and NLB",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scoring engine
scoring_engine = ScoringEngine()


@app.get("/", response_model=HealthResponse)
async def root():
    return {
        "status": "healthy",
        "message": "API Gateway Referee API is running",
        "version": "1.0.0",
        "built_with": "Kiro spec-driven development"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "message": "All systems operational",
        "version": "1.0.0"
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_options(constraints: ConstraintsInput):
    try:
        logger.info(f"Analyzing options for use case: {constraints.use_case}, RPS: {constraints.rps}")
        
        # Validate constraints
        if constraints.budget < 10:
            raise HTTPException(status_code=400, detail="Budget must be at least $10/month")
        
        if constraints.rps < 1:
            raise HTTPException(status_code=400, detail="RPS must be at least 1")
        
        if constraints.latency < 1:
            raise HTTPException(status_code=400, detail="Latency target must be at least 1ms")
        
        # Calculate scores using the scoring engine
        analysis = scoring_engine.analyze(
            rps=constraints.rps,
            budget=constraints.budget,
            latency=constraints.latency,
            features=constraints.features,
            use_case=constraints.use_case,
            weights=constraints.weights
        )
        
        logger.info(f"Analysis complete. Winner: {analysis['winner']}")
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/sensitivity")
async def sensitivity_analysis(constraints: ConstraintsInput):
    try:
        sensitivity = scoring_engine.analyze_sensitivity(
            rps=constraints.rps,
            budget=constraints.budget,
            latency=constraints.latency,
            features=constraints.features,
            use_case=constraints.use_case,
            current_weights=constraints.weights
        )
        
        return sensitivity
        
    except Exception as e:
        logger.error(f"Error during sensitivity analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/pricing/{option}")
async def get_pricing_details(option: str, rps: int = 100):
    if option not in ["apigateway", "alb", "nlb"]:
        raise HTTPException(status_code=400, detail="Invalid option. Must be apigateway, alb, or nlb")
    
    try:
        pricing = scoring_engine.get_pricing_breakdown(option, rps)
        return pricing
        
    except Exception as e:
        logger.error(f"Error fetching pricing details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)