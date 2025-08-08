"""
Demonstração da estratégia mista: financiamento imobiliário + CDI.

Este script mostra como usar o método compra_e_renda_fixa para simular
uma estratégia que combina a compra de um imóvel financiado com
investimento dos aportes mensais em CDI.
"""

from core import OptimizedInvestment
import matplotlib.pyplot as plt


def demonstrar_estrategia_mista():
    """Demonstra o uso da estratégia mista com exemplo prático."""
    
    # Configura simulação com inflação de 6% ao ano
    investment = OptimizedInvestment(inflacao=6.0, ir_renda_fixa=15)
    
    # Parâmetros do cenário
    valor_imovel = 300000.0      # R$ 300.000
    entrada = 60000.0            # R$ 60.000 (20%)
    parcelas = 240               # 20 anos
    taxa_juros = 12.0            # 12% ao ano
    taxa_cdi = 13.0              # 13% ao ano
    aporte_mensal = 1000.0       # R$ 1.000/mês para renda fixa
    valorizacao = 8.0            # 8% ao ano
    
    print("=== DEMONSTRAÇÃO DA ESTRATÉGIA MISTA ===")
    print(f"Valor do imóvel: R$ {valor_imovel:,.2f}")
    print(f"Entrada: R$ {entrada:,.2f} ({entrada/valor_imovel*100:.1f}%)")
    print(f"Financiamento: {parcelas} parcelas a {taxa_juros}% ao ano")
    print(f"Valorização do imóvel: {valorizacao}% ao ano")
    print(f"Taxa CDI: {taxa_cdi}% ao ano")
    print(f"Aporte mensal em renda fixa: R$ {aporte_mensal:,.2f}")
    print(f"Inflação: {investment.inflacao}% ao ano")
    print(f"IR sobre renda fixa: {investment.ir_renda_fixa}%")
    print()
    
    # Executa simulação
    historico = investment.compra_e_renda_fixa(
        valor_imovel=valor_imovel,
        entrada=entrada,
        parcelas=parcelas,
        taxa_juros=taxa_juros,
        taxa_cdi=taxa_cdi,
        aporte_mensal=aporte_mensal,
        valorizacao=valorizacao
    )
    
    # Mostra resultados em marcos temporais
    marcos = [12, 60, 120, 180, 240]  # 1, 5, 10, 15, 20 anos
    
    print("=== EVOLUÇÃO DO PATRIMÔNIO (valores em R$ de hoje) ===")
    for mes in marcos:
        if mes <= len(historico):
            anos = mes // 12
            patrimonio = historico[mes - 1]
            print(f"Após {anos:2d} ano(s): R$ {patrimonio:>10,.2f}")
    
    print()
    print("=== RESUMO FINAL ===")
    patrimonio_final = historico[-1]
    total_aportes = entrada + (aporte_mensal * parcelas)
    
    print(f"Patrimônio final: R$ {patrimonio_final:,.2f}")
    print(f"Total investido: R$ {total_aportes:,.2f}")
    print(f"Ganho líquido: R$ {patrimonio_final - total_aportes:,.2f}")
    print(f"Rentabilidade: {(patrimonio_final / total_aportes - 1) * 100:.1f}%")
    
    return historico


def comparar_estrategias():
    """Compara estratégia mista com investimento puro em CDI."""
    
    investment = OptimizedInvestment(inflacao=6.0, ir_renda_fixa=15)
    
    # Parâmetros comuns
    entrada = 60000.0
    aporte_mensal = 1000.0
    anos = 20
    taxa_cdi = 13.0
    
    # Estratégia 1: Apenas CDI
    historico_cdi = investment.investimento_cdi(
        aporte_inicial=entrada,
        aporte_mensal=aporte_mensal,
        taxa_cdi=taxa_cdi,
        anos=anos,
        imposto_final=False
    )
    
    # Estratégia 2: Mista (imóvel + CDI)
    historico_misto = investment.compra_e_renda_fixa(
        valor_imovel=300000.0,
        entrada=entrada,
        parcelas=anos * 12,
        taxa_juros=12.0,
        taxa_cdi=taxa_cdi,
        aporte_mensal=aporte_mensal,
        valorizacao=8.0
    )
    
    print("\n=== COMPARAÇÃO DE ESTRATÉGIAS ===")
    print(f"Apenas CDI: R$ {historico_cdi[-1]:,.2f}")
    print(f"Estratégia mista: R$ {historico_misto[-1]:,.2f}")
    
    diferenca = historico_misto[-1] - historico_cdi[-1]
    print(f"Vantagem da estratégia mista: R$ {diferenca:,.2f}")
    print(f"Percentual de vantagem: {diferenca / historico_cdi[-1] * 100:.1f}%")


if __name__ == "__main__":
    # Executa demonstração
    historico = demonstrar_estrategia_mista()
    
    # Compara estratégias
    comparar_estrategias()
    
    print("\n=== OBSERVAÇÕES ===")
    print("• Todos os valores estão ajustados pela inflação (valor presente)")
    print("• A estratégia mista combina valorização imobiliária com renda fixa")
    print("• Impostos estão incluídos nos cálculos")
    print("• Resultados podem variar conforme cenário econômico")