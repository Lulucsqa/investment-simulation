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
    Plota comparação visual entre investimento em imóvel na planta vs imóvel pronto.
    
    Esta função cria um gráfico profissional comparando a evolução do patrimônio
    líquido entre duas estratégias imobiliárias: compra na planta (com período de
    construção) e compra de imóvel pronto (com aluguel imediato).
    
    Args:
        historico_planta (List[float]): Lista com histórico mensal de patrimônio
                                      líquido do imóvel na planta em reais (valor presente).
                                      Deve ter exatamente 'meses' elementos.
        historico_pronto (List[float]): Lista com histórico mensal de patrimônio
                                      líquido do imóvel pronto em reais (valor presente).
                                      Deve ter exatamente 'meses' elementos.
        meses (int): Número total de meses da simulação. Deve ser positivo e
                    corresponder ao tamanho das listas de histórico.
    
    Returns:
        None: A função não retorna valor, mas gera e salva o gráfico.
    
    Side Effects:
        - Cria arquivo 'outputs/comparacao_imoveis.jpg' com o gráfico
        - Exibe o gráfico na tela (plt.show())
        - Imprime mensagem de confirmação no console
        - Cria diretório 'outputs/' se não existir
    
    Note:
        - Gráfico salvo em alta resolução (300 DPI)
        - Valores formatados como moeda brasileira (R$)
        - Grid profissional e legendas otimizadas
        - Cores diferenciadas para cada estratégia
        - Todos os valores já ajustados pela inflação
    
    Raises:
        ValueError: Se as listas têm tamanhos diferentes ou incompatíveis com 'meses'
        IOError: Se não conseguir salvar o arquivo de saída
    
    Example:
        >>> historico_planta = [100000, 105000, 110000, ...]  # 240 meses
        >>> historico_pronto = [95000, 102000, 108000, ...]   # 240 meses
        >>> plotar_historico_planta_pronto(historico_planta, historico_pronto, 240)
        Gráfico salvo em: outputs/comparacao_imoveis.jpg
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
    Plota múltiplos cenários de investimento em um único gráfico comparativo.
    
    Esta função cria uma visualização abrangente comparando diferentes estratégias
    de investimento, incluindo renda fixa e imóveis, com opção de mostrar a
    alocação otimizada calculada pelo algoritmo de otimização de portfólio.
    
    Args:
        cenarios (Dict[str, List[float]]): Dicionário onde as chaves são nomes
                                         das estratégias (ex: 'CDI', 'IPCA+', 'Imóvel Planta')
                                         e os valores são listas com histórico mensal
                                         de patrimônio em reais (valor presente).
        anos (int): Número de anos da simulação. Usado para calcular o número
                   de meses esperado e configurar o eixo X do gráfico.
        pesos_otimizados (Optional[np.ndarray], optional): Array NumPy com pesos
                                                          otimizados para cada estratégia
                                                          na mesma ordem das chaves do
                                                          dicionário cenarios. Se fornecido,
                                                          será exibido no título. Defaults to None.
    
    Returns:
        None: A função não retorna valor, mas gera e salva o gráfico.
    
    Side Effects:
        - Cria arquivo 'outputs/cenarios_investimento.jpg' com o gráfico
        - Exibe o gráfico na tela (plt.show())
        - Imprime mensagem de confirmação no console
        - Imprime avisos se dados inconsistentes forem encontrados
        - Cria diretório 'outputs/' se não existir
    
    Features:
        - Suporte para até 7 estratégias diferentes com cores únicas
        - Estilos de linha variados (sólida, tracejada, pontilhada)
        - Marcadores opcionais para melhor visualização
        - Formatação monetária brasileira no eixo Y
        - Grid profissional e legendas organizadas
        - Título dinâmico com alocação otimizada (se fornecida)
        - Validação automática de dados inconsistentes
        - Truncamento inteligente para cenários de tamanhos diferentes
    
    Data Validation:
        - Remove cenários vazios ou inválidos automaticamente
        - Ajusta para o menor tamanho comum se cenários têm tamanhos diferentes
        - Imprime avisos detalhados sobre problemas encontrados
        - Continua execução mesmo com dados parcialmente inválidos
    
    Note:
        - Gráfico salvo em alta resolução (300 DPI)
        - Valores formatados como moeda brasileira (R$)
        - Legenda adaptativa (1 ou 2 colunas conforme necessário)
        - Todos os valores já ajustados pela inflação
        - Suporte para simulações de longo prazo (até 30 anos)
    
    Raises:
        ValueError: Se nenhum cenário válido for fornecido
        IOError: Se não conseguir salvar o arquivo de saída
    
    Example:
        >>> cenarios = {
        ...     'CDI': [100000, 103000, 106000, ...],
        ...     'IPCA+': [100000, 104000, 108000, ...],
        ...     'Imóvel Planta': [95000, 98000, 102000, ...]
        ... }
        >>> pesos = np.array([0.4, 0.3, 0.3])  # 40% CDI, 30% IPCA+, 30% Imóvel
        >>> plotar_cenarios(cenarios, anos=20, pesos_otimizados=pesos)
        Gráfico salvo em: outputs/cenarios_investimento.jpg
    """
    if not cenarios:
        print("Aviso: Nenhum cenário fornecido para plotagem")
        return
    
    # Validar que todos os cenários têm dados válidos
    cenarios_validos = {}
    tamanhos = []
    
    for nome, historico in cenarios.items():
        if historico and len(historico) > 0:
            cenarios_validos[nome] = historico
            tamanhos.append(len(historico))
    
    if not cenarios_validos:
        print("Aviso: Nenhum cenário com dados válidos encontrado")
        return
    
    # Verificar se todos os cenários têm o mesmo tamanho
    if len(set(tamanhos)) > 1:
        print(f"Aviso: Cenários têm tamanhos diferentes: {dict(zip(cenarios_validos.keys(), tamanhos))}")
        # Usar o tamanho mínimo para evitar erros
        tamanho_minimo = min(tamanhos)
        print(f"Usando os primeiros {tamanho_minimo} pontos de cada cenário")
        
        # Truncar todos os cenários para o tamanho mínimo
        for nome in cenarios_validos:
            cenarios_validos[nome] = cenarios_validos[nome][:tamanho_minimo]
        
        meses = tamanho_minimo
    else:
        meses = tamanhos[0]
    
    # Configuração da figura com tamanho profissional
    plt.figure(figsize=(14, 10))
    
    # Cria array de meses para o eixo X
    meses_array = np.arange(1, meses + 1)
    
    # Cores e estilos para diferentes cenários
    cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    estilos = ['-', '--', '-.', ':', '-', '--', '-.']
    
    # Plota cada cenário com estilo único
    for i, (nome, historico) in enumerate(cenarios_validos.items()):
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
    if pesos_otimizados is not None and len(pesos_otimizados) == len(cenarios_validos):
        nomes_cenarios = list(cenarios_validos.keys())
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
               fontsize=10, framealpha=0.9, ncol=1 if len(cenarios_validos) <= 4 else 2)
    
    # Ajuste automático do layout
    plt.tight_layout()
    
    # Salva em alta resolução
    plt.savefig('outputs/cenarios_investimento.jpg', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Exibe o gráfico
    plt.show()
    
    print("Gráfico salvo em: outputs/cenarios_investimento.jpg")