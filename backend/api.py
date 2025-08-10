"""
FastAPI backend for Investment Simulation System
Provides REST API endpoints for the investment simulation engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import os
import sys
import json
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import OptimizedInvestment
from visualization import plotar_historico_planta_pronto, plotar_cenarios

app = FastAPI(
    title="Investment Simulation API",
    description="API for real estate and fixed income investment simulations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will be configured for Heroku
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class SimulationParams(BaseModel):
    """Base parameters for investment simulations"""
    aporte_inicial: float = Field(..., gt=0, description="Initial investment amount")
    aporte_mensal: float = Field(..., ge=0, description="Monthly contribution amount")
    anos: int = Field(..., gt=0, le=100, description="Investment period in years")
    inflacao_anual: float = Field(4.5, ge=0, le=50, description="Annual inflation rate (%)")
    ir_renda_fixa: float = Field(15.0, ge=0, le=50, description="Fixed income tax rate (%)")
    ir_aluguel: float = Field(27.5, ge=0, le=50, description="Rental income tax rate (%)")

class CDIParams(SimulationParams):
    """Parameters for CDI investment simulation"""
    taxa_cdi: float = Field(..., gt=0, le=50, description="CDI annual rate (%)")

class IPCAParams(SimulationParams):
    """Parameters for IPCA+ investment simulation"""
    taxa_ipca: float = Field(..., gt=0, le=50, description="IPCA+ additional rate (%)")

class RealEstateParams(SimulationParams):
    """Parameters for real estate investment simulation"""
    valor_imovel: float = Field(..., gt=0, description="Property value")
    entrada: float = Field(..., gt=0, description="Down payment amount")
    parcelas: int = Field(..., gt=0, le=600, description="Number of financing installments")
    taxa_juros: float = Field(..., gt=0, le=50, description="Financing interest rate (%)")
    valorizacao: float = Field(..., ge=0, le=50, description="Property appreciation rate (%)")
    aluguel_mensal: float = Field(..., gt=0, description="Monthly rental income")
    anos_construcao: Optional[int] = Field(0, ge=0, le=10, description="Construction period (years)")

class MixedStrategyParams(RealEstateParams):
    """Parameters for mixed strategy (real estate + CDI)"""
    taxa_cdi: float = Field(..., gt=0, le=50, description="CDI annual rate (%)")

class OptimizationParams(BaseModel):
    """Parameters for portfolio optimization"""
    estrategias: Dict[str, Any] = Field(..., description="Investment strategies to optimize")
    anos: int = Field(..., gt=0, le=100, description="Investment period in years")
    optimize_aportes: bool = Field(False, description="Whether to optimize contribution amounts")
    aporte_bounds: Optional[List[tuple]] = Field(None, description="Bounds for contribution optimization")

class SimulationResult(BaseModel):
    """Result of an investment simulation"""
    historico: List[float]
    patrimonio_final: float
    rentabilidade_total: float
    rentabilidade_anual: float

class OptimizationResult(BaseModel):
    """Result of portfolio optimization"""
    pesos_otimos: List[float]
    aporte_inicial_otimo: Optional[float]
    aporte_mensal_otimo: Optional[float]
    retorno_final: float

# Global simulator instance
simulator = None

def get_simulator(params: SimulationParams) -> OptimizedInvestment:
    """Get or create simulator instance with given parameters"""
    return OptimizedInvestment(
        inflacao=params.inflacao_anual,
        ir_renda_fixa=params.ir_renda_fixa,
        ir_aluguel=params.ir_aluguel
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Investment Simulation API is running"}

@app.post("/simulate/cdi", response_model=SimulationResult)
async def simulate_cdi(params: CDIParams):
    """Simulate CDI investment"""
    try:
        simulator = get_simulator(params)
        historico = simulator.investimento_cdi(
            aporte_inicial=params.aporte_inicial,
            aporte_mensal=params.aporte_mensal,
            taxa_cdi=params.taxa_cdi,
            anos=params.anos
        )
        
        patrimonio_final = historico[-1]
        total_investido = params.aporte_inicial + (params.aporte_mensal * params.anos * 12)
        rentabilidade_total = ((patrimonio_final / total_investido) - 1) * 100
        rentabilidade_anual = ((patrimonio_final / total_investido) ** (1/params.anos) - 1) * 100
        
        return SimulationResult(
            historico=historico,
            patrimonio_final=patrimonio_final,
            rentabilidade_total=rentabilidade_total,
            rentabilidade_anual=rentabilidade_anual
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simulate/ipca", response_model=SimulationResult)
async def simulate_ipca(params: IPCAParams):
    """Simulate IPCA+ investment"""
    try:
        simulator = get_simulator(params)
        historico = simulator.investimento_ipca(
            aporte_inicial=params.aporte_inicial,
            aporte_mensal=params.aporte_mensal,
            taxa_ipca=params.taxa_ipca,
            anos=params.anos
        )
        
        patrimonio_final = historico[-1]
        total_investido = params.aporte_inicial + (params.aporte_mensal * params.anos * 12)
        rentabilidade_total = ((patrimonio_final / total_investido) - 1) * 100
        rentabilidade_anual = ((patrimonio_final / total_investido) ** (1/params.anos) - 1) * 100
        
        return SimulationResult(
            historico=historico,
            patrimonio_final=patrimonio_final,
            rentabilidade_total=rentabilidade_total,
            rentabilidade_anual=rentabilidade_anual
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simulate/real-estate/under-construction", response_model=SimulationResult)
async def simulate_real_estate_under_construction(params: RealEstateParams):
    """Simulate real estate investment (under construction)"""
    try:
        simulator = get_simulator(params)
        historico = simulator.compra_financiada_planta(
            valor_imovel=params.valor_imovel,
            entrada=params.entrada,
            parcelas=params.parcelas,
            taxa_juros=params.taxa_juros,
            valorizacao=params.valorizacao,
            aluguel=params.aluguel_mensal,
            anos_construcao=params.anos_construcao or 3
        )
        
        patrimonio_final = historico[-1]
        total_investido = params.entrada + (params.aporte_mensal * params.anos * 12)
        rentabilidade_total = ((patrimonio_final / total_investido) - 1) * 100 if total_investido > 0 else 0
        rentabilidade_anual = ((patrimonio_final / total_investido) ** (1/params.anos) - 1) * 100 if total_investido > 0 else 0
        
        return SimulationResult(
            historico=historico,
            patrimonio_final=patrimonio_final,
            rentabilidade_total=rentabilidade_total,
            rentabilidade_anual=rentabilidade_anual
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simulate/real-estate/ready", response_model=SimulationResult)
async def simulate_real_estate_ready(params: RealEstateParams):
    """Simulate real estate investment (ready property)"""
    try:
        simulator = get_simulator(params)
        historico = simulator.compra_financiada_pronto(
            valor_imovel=params.valor_imovel,
            entrada=params.entrada,
            parcelas=params.parcelas,
            taxa_juros=params.taxa_juros,
            valorizacao=params.valorizacao,
            aluguel=params.aluguel_mensal
        )
        
        patrimonio_final = historico[-1]
        total_investido = params.entrada + (params.aporte_mensal * params.anos * 12)
        rentabilidade_total = ((patrimonio_final / total_investido) - 1) * 100 if total_investido > 0 else 0
        rentabilidade_anual = ((patrimonio_final / total_investido) ** (1/params.anos) - 1) * 100 if total_investido > 0 else 0
        
        return SimulationResult(
            historico=historico,
            patrimonio_final=patrimonio_final,
            rentabilidade_total=rentabilidade_total,
            rentabilidade_anual=rentabilidade_anual
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simulate/mixed-strategy", response_model=SimulationResult)
async def simulate_mixed_strategy(params: MixedStrategyParams):
    """Simulate mixed strategy (real estate + CDI)"""
    try:
        simulator = get_simulator(params)
        historico = simulator.compra_e_renda_fixa(
            valor_imovel=params.valor_imovel,
            entrada=params.entrada,
            parcelas=params.parcelas,
            taxa_juros=params.taxa_juros,
            valorizacao=params.valorizacao,
            aluguel=params.aluguel_mensal,
            aporte_mensal=params.aporte_mensal,
            taxa_cdi=params.taxa_cdi,
            anos_construcao=params.anos_construcao or 0
        )
        
        patrimonio_final = historico[-1]
        total_investido = params.entrada + (params.aporte_mensal * params.anos * 12)
        rentabilidade_total = ((patrimonio_final / total_investido) - 1) * 100 if total_investido > 0 else 0
        rentabilidade_anual = ((patrimonio_final / total_investido) ** (1/params.anos) - 1) * 100 if total_investido > 0 else 0
        
        return SimulationResult(
            historico=historico,
            patrimonio_final=patrimonio_final,
            rentabilidade_total=rentabilidade_total,
            rentabilidade_anual=rentabilidade_anual
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/optimize", response_model=OptimizationResult)
async def optimize_portfolio(params: OptimizationParams):
    """Optimize portfolio allocation"""
    try:
        # This would need to be implemented based on your optimization logic
        # For now, returning a placeholder
        raise HTTPException(status_code=501, detail="Portfolio optimization endpoint not yet implemented")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/charts/{chart_name}")
async def get_chart(chart_name: str):
    """Get generated chart file"""
    chart_path = Path("outputs") / f"{chart_name}.jpg"
    if not chart_path.exists():
        raise HTTPException(status_code=404, detail="Chart not found")
    
    return FileResponse(
        path=chart_path,
        media_type="image/jpeg",
        filename=f"{chart_name}.jpg"
    )

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)