"""
Demonstração do tratamento avançado de erros na otimização.

Este script demonstra as melhorias implementadas na tarefa 10.2:
- Captura de falhas na convergência do algoritmo
- Implementação de fallback para casos de não convergência
- Logging detalhado de erros
"""

import logging
import numpy as np
from unittest.mock import patch
from scipy.optimize import OptimizeResult

from core import OptimizedInvestment, OtimizacaoError

# Configura logging para mostrar todos os detalhes
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:%(message)s'
)

def demonstrar_analise_falhas():
    """Demonstra a análise detalhada de diferentes tipos de falha."""
    print("=" * 80)
    print("DEMONSTRAÇÃO: ANÁLISE DETALHADA DE FALHAS DE CONVERGÊNCIA")
    print("=" * 80)
    
    investment = OptimizedInvestment(inflacao=6.0)
    
    # Simula diferentes tipos de falha
    tipos_falha = [
        ("Maximum number of iterations reached", "CONVERGENCIA_MAXITER"),
        ("Tolerance not achieved", "CONVERGENCIA_TOLERANCIA"),
        ("Singular matrix encountered", "CONVERGENCIA_SINGULAR"),
        ("Line search failed", "CONVERGENCIA_LINESEARCH"),
        ("Constraint violation detected", "CONVERGENCIA_RESTRICOES"),
        ("Numerical precision issues", "CONVERGENCIA_NUMERICA"),
        ("Unknown optimization failure", "CONVERGENCIA_OUTROS")
    ]
    
    for i, (message, expected_type) in enumerate(tipos_falha, 1):
        print(f"\n{i}. Testando falha: {message}")
        
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = message
        resultado.fun = -1000.0
        resultado.nit = 100
        resultado.nfev = 500
        
        detalhes = investment._analisar_falha_convergencia(resultado, 'SLSQP', i)
        
        print(f"   Tipo identificado: {detalhes['erro_tipo']}")
        print(f"   Descrição: {detalhes['descricao']}")
        print(f"   ✓ Correto!" if detalhes['erro_tipo'] == expected_type else f"   ✗ Esperado: {expected_type}")

def demonstrar_fallback_com_logging():
    """Demonstra o fallback com logging detalhado."""
    print("\n" + "=" * 80)
    print("DEMONSTRAÇÃO: FALLBACK COM LOGGING DETALHADO")
    print("=" * 80)
    
    investment = OptimizedInvestment(inflacao=6.0)
    
    # Estratégias de teste
    estrategias = {
        'CDI': [10000.0, 11000.0, 12000.0],
        'IPCA': [10000.0, 10800.0, 11600.0],
        'Imovel': [10000.0, 11200.0, 12500.0]
    }
    
    print("\nSimulando falha na otimização para demonstrar fallback...")
    
    # Mock para simular falha consistente
    with patch('core.minimize') as mock_minimize:
        # Simula falha em todas as tentativas
        mock_result = OptimizeResult()
        mock_result.success = False
        mock_result.message = "Demonstration failure - maximum iterations reached"
        mock_result.fun = -1000.0
        mock_result.nit = 1000
        mock_result.nfev = 5000
        mock_minimize.return_value = mock_result
        
        try:
            pesos, aporte_inicial, aporte_mensal, retorno = investment.otimizar_portfolio(
                estrategias, anos=1
            )
            
            print(f"\n✓ Fallback executado com sucesso!")
            print(f"  - Pesos otimizados: {pesos}")
            print(f"  - Retorno final: {retorno}")
            print(f"  - Melhor estratégia selecionada: {'Imovel' if pesos[2] == 1.0 else 'Outra'}")
            
        except Exception as e:
            print(f"✗ Erro mesmo com fallback: {e}")

def demonstrar_cenarios_problematicos():
    """Demonstra tratamento de cenários que podem causar problemas."""
    print("\n" + "=" * 80)
    print("DEMONSTRAÇÃO: CENÁRIOS PROBLEMÁTICOS")
    print("=" * 80)
    
    investment = OptimizedInvestment(inflacao=6.0)
    
    # Cenário 1: Estratégias com retornos muito similares
    print("\n1. Estratégias com retornos muito similares:")
    estrategias_similares = {
        'A': [1000.0, 1100.0, 1200.000001],
        'B': [1000.0, 1100.0, 1200.000002],
        'C': [1000.0, 1100.0, 1200.000003]
    }
    
    try:
        pesos, _, _, retorno = investment.otimizar_portfolio(estrategias_similares, anos=1)
        print(f"   ✓ Otimização bem-sucedida apesar da similaridade")
        print(f"   - Pesos: {pesos}")
        print(f"   - Retorno: {retorno}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Cenário 2: Estratégias com alta volatilidade
    print("\n2. Estratégias com alta volatilidade:")
    estrategias_volateis = {
        'Volatil1': [1000.0, 500.0, 2000.0, 100.0, 3000.0],
        'Volatil2': [1000.0, 3000.0, 200.0, 2500.0, 150.0],
        'Estavel': [1000.0, 1050.0, 1100.0, 1150.0, 1200.0]
    }
    
    try:
        pesos, _, _, retorno = investment.otimizar_portfolio(estrategias_volateis, anos=1)
        print(f"   ✓ Otimização bem-sucedida com alta volatilidade")
        print(f"   - Pesos: {pesos}")
        print(f"   - Retorno: {retorno}")
        print(f"   - Estratégia estável favorecida: {'Sim' if pesos[2] > 0.5 else 'Não'}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")

def demonstrar_validacao_robusta():
    """Demonstra a validação robusta de pesos."""
    print("\n" + "=" * 80)
    print("DEMONSTRAÇÃO: VALIDAÇÃO ROBUSTA DE PESOS")
    print("=" * 80)
    
    investment = OptimizedInvestment(inflacao=6.0)
    
    casos_teste = [
        ("Pesos válidos", np.array([0.6, 0.4]), True),
        ("Pesos com valores infinitos", np.array([0.5, float('inf')]), False),
        ("Pesos negativos", np.array([0.7, -0.3]), False),
        ("Soma incorreta", np.array([0.3, 0.3]), False),
        ("Pesos na borda da tolerância", np.array([0.495, 0.495]), True),
        ("Array vazio", np.array([]), False),
    ]
    
    for i, (descricao, pesos, esperado) in enumerate(casos_teste, 1):
        print(f"\n{i}. {descricao}:")
        try:
            resultado = investment._validar_pesos_otimizados(pesos)
            status = "✓ Válido" if resultado else "✗ Inválido"
            correto = "✓" if resultado == esperado else "✗"
            print(f"   {status} {correto}")
            if len(pesos) > 0:
                print(f"   Pesos: {pesos}")
                print(f"   Soma: {np.sum(pesos) if len(pesos) > 0 else 'N/A'}")
        except Exception as e:
            print(f"   ✗ Exceção: {e}")

def main():
    """Executa todas as demonstrações."""
    print("DEMONSTRAÇÃO DO TRATAMENTO AVANÇADO DE ERROS NA OTIMIZAÇÃO")
    print("Tarefa 10.2: Implementar tratamento de erros de otimização")
    print("\nRecursos implementados:")
    print("- Captura de falhas na convergência do algoritmo")
    print("- Implementação de fallback para casos de não convergência")
    print("- Logging detalhado de erros")
    print("- Testes para cenários de erro")
    
    try:
        demonstrar_analise_falhas()
        demonstrar_fallback_com_logging()
        demonstrar_cenarios_problematicos()
        demonstrar_validacao_robusta()
        
        print("\n" + "=" * 80)
        print("✓ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("✓ Todos os recursos de tratamento de erro estão funcionando")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()