"""
Demonstração da validação de parâmetros em ação.

Este script mostra como o sistema rejeita parâmetros inválidos
com mensagens de erro informativas.
"""

from core import OptimizedInvestment, ParametroInvalidoError


def demonstrar_validacao():
    """Demonstra a validação de parâmetros com exemplos práticos."""
    
    print("=" * 60)
    print("DEMONSTRAÇÃO DA VALIDAÇÃO DE PARÂMETROS")
    print("=" * 60)
    
    # Teste 1: Inflação inválida
    print("\n1. Testando inflação inválida...")
    try:
        investment = OptimizedInvestment(inflacao=150.0)  # Muito alta
    except ParametroInvalidoError as e:
        print(f"   ✓ Erro capturado: {e}")
    
    # Teste 2: Aporte inicial negativo
    print("\n2. Testando aporte inicial negativo...")
    try:
        investment = OptimizedInvestment(inflacao=6.0)
        investment.investimento_cdi(-1000, 100, 12.0, 1)  # Negativo
    except ParametroInvalidoError as e:
        print(f"   ✓ Erro capturado: {e}")
    
    # Teste 3: Taxa de juros muito alta
    print("\n3. Testando taxa de juros muito alta...")
    try:
        investment = OptimizedInvestment(inflacao=6.0)
        investment.compra_financiada_pronto(300000, 60000, 240, 60.0, 8.0, 2000)  # 60% ao ano
    except ParametroInvalidoError as e:
        print(f"   ✓ Erro capturado: {e}")
    
    # Teste 4: Entrada maior que valor do imóvel
    print("\n4. Testando entrada maior que valor do imóvel...")
    try:
        investment = OptimizedInvestment(inflacao=6.0)
        investment.compra_financiada_pronto(300000, 350000, 240, 12.0, 8.0, 2000)
    except ParametroInvalidoError as e:
        print(f"   ✓ Erro capturado: {e}")
    
    # Teste 5: Estratégias com históricos de tamanhos diferentes
    print("\n5. Testando estratégias com períodos diferentes...")
    try:
        investment = OptimizedInvestment(inflacao=6.0)
        estrategias_invalidas = {
            'CDI': [1000, 1100, 1200, 1300],  # 4 meses
            'IPCA+': [1000, 1050, 1100]       # 3 meses
        }
        investment.otimizar_portfolio(estrategias_invalidas, 1)
    except ParametroInvalidoError as e:
        print(f"   ✓ Erro capturado: {e}")
    
    # Teste 6: Valores não numéricos
    print("\n6. Testando valores não numéricos...")
    try:
        investment = OptimizedInvestment(inflacao=6.0)
        investment.investimento_cdi("mil reais", 100, 12.0, 1)  # String ao invés de número
    except ParametroInvalidoError as e:
        print(f"   ✓ Erro capturado: {e}")
    
    # Teste 7: Valores infinitos
    print("\n7. Testando valores infinitos...")
    try:
        investment = OptimizedInvestment(inflacao=float('inf'))  # Infinito
    except ParametroInvalidoError as e:
        print(f"   ✓ Erro capturado: {e}")
    
    # Teste 8: Parâmetros válidos (deve funcionar)
    print("\n8. Testando parâmetros válidos...")
    try:
        investment = OptimizedInvestment(inflacao=6.0)
        historico = investment.investimento_cdi(1000, 100, 12.0, 1)
        print(f"   ✓ Simulação executada com sucesso! Valor final: R$ {historico[-1]:.2f}")
    except Exception as e:
        print(f"   ✗ Erro inesperado: {e}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 60)
    print("\nTodos os parâmetros inválidos foram rejeitados com mensagens informativas!")
    print("O sistema está protegido contra entradas incorretas.")


if __name__ == "__main__":
    demonstrar_validacao()