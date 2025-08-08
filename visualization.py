"""
Módulo de visualização para gráficos de investimentos.

Este módulo contém funções para criar visualizações profissionais
dos resultados das simulações de investimento.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional


def plotar_historico_planta_pronto(historico_planta: List[float], 
                                  historico_pronto: List[float], 
                                  meses: int) -> None:
    """
    Plota comparação entre investimento em imóvel na planta vs pronto.
    
    Args:
        historico_planta: Lista com histórico de patrimônio do imóvel na planta
        historico_pronto: Lista com histórico de patrimônio do imóvel pronto
        meses: Número de meses da simulação
    """
    # Configuração da figura com tamanho profissional
    plt.figure(figsize=(12, 8))
    
    # Cria array de meses para o eixo X
    meses_array = np.arange(1, meses + 1)
    
    # Plota as duas estratégias com cores distintas
    plt.plot(meses_array, historico_planta, 
             color='#2E8B57', linewidth=2.5, label='Imóvel na Planta', alpha=0.9)
    plt.plot(meses_array, historico_pronto, 
             color='#4169E1', linewidth=2.5, label='Imóvel Pronto', alpha=0.9)
    
    # Configuração dos eixos
    plt.xlabel('Meses', fontsize=12, fontweight='bold')
    plt.ylabel('Patrimônio Líquido (R$)', fontsize=12, fontweight='bold')
    plt.title('Comparação: Imóvel na Planta vs Imóvel Pronto\n(Valores Ajustados pela Inflação)', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Formatação do eixo Y para valores monetários
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
    
    # Grid profissional
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Legenda com formatação profissional
    plt.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, 
               fontsize=11, framealpha=0.9)
    
    # Ajuste automático do layout
    plt.tight_layout()
    
    # Salva em alta resolução
    plt.savefig('outputs/comparacao_imoveis.jpg', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Exibe o gráfico
    plt.show()
    
    print("Gráfico salvo em: outputs/comparacao_imoveis.jpg")


def plotar_cenarios(cenarios: Dict[str, List[float]], 
                   anos: int, 
                   pesos_otimizados: Optional[np.ndarray] = None) -> None:
    """
    Plota múltiplos cenários de investimento em um único gráfico.
    
    Args:
        cenarios: Dicionário com nome do cenário e histórico de valores
        anos: Número de anos da simulação
        pesos_otimizados: Array com pesos otimizados (opcional)
    """
    # Configuração da figura com tamanho profissional
    plt.figure(figsize=(14, 10))
    
    # Calcula número de meses
    meses = anos * 12
    meses_array = np.arange(1, meses + 1)
    
    # Cores e estilos para diferentes cenários
    cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    estilos = ['-', '--', '-.', ':', '-', '--', '-.']
    
    # Plota cada cenário com estilo único
    for i, (nome, historico) in enumerate(cenarios.items()):
        cor = cores[i % len(cores)]
        estilo = estilos[i % len(estilos)]
        
        plt.plot(meses_array, historico, 
                color=cor, linestyle=estilo, linewidth=2.5, 
                label=nome, alpha=0.9, marker='o' if i < 3 else None, 
                markersize=3, markevery=max(1, meses//20))
    
    # Configuração dos eixos
    plt.xlabel('Meses', fontsize=12, fontweight='bold')
    plt.ylabel('Patrimônio Acumulado (R$)', fontsize=12, fontweight='bold')
    
    # Título com pesos otimizados se fornecidos
    titulo = 'Comparação de Cenários de Investimento\n(Valores Ajustados pela Inflação)'
    if pesos_otimizados is not None:
        nomes_cenarios = list(cenarios.keys())
        pesos_texto = ', '.join([f'{nome}: {peso:.1%}' 
                                for nome, peso in zip(nomes_cenarios, pesos_otimizados)])
        titulo += f'\nAlocação Otimizada: {pesos_texto}'
    
    plt.title(titulo, fontsize=14, fontweight='bold', pad=20)
    
    # Formatação do eixo Y para valores monetários
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
    
    # Grid profissional
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Legenda com formatação profissional
    plt.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, 
               fontsize=10, framealpha=0.9, ncol=1 if len(cenarios) <= 4 else 2)
    
    # Ajuste automático do layout
    plt.tight_layout()
    
    # Salva em alta resolução
    plt.savefig('outputs/cenarios_investimento.jpg', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Exibe o gráfico
    plt.show()
    
    print("Gráfico salvo em: outputs/cenarios_investimento.jpg")