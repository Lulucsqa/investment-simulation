"""
Script principal para execução das simulações de investimento.

Este script configura os parâmetros, executa as simulações e gera
os relatórios e visualizações dos resultados.
"""

from core import OptimizedInvestment
from visualization import plotar_historico_planta_pronto, plotar_cenarios


def configurar_parametros():
    """
    Configura todos os parâmetros de simulação do sistema de investimentos.
    
    Esta função centraliza a configuração de todos os parâmetros necessários
    para executar as simulações de investimento, incluindo parâmetros econômicos,
    temporais, de renda fixa, imobiliários e de otimização.
    
    Returns:
        dict: Dicionário com todos os parâmetros configurados, contendo:
            - Configurações econômicas (inflação, impostos)
            - Parâmetros temporais (anos de simulação)
            - Parâmetros de investimento (aportes inicial e mensal)
            - Taxas de renda fixa (CDI, IPCA+)
            - Parâmetros imobiliários (valor, entrada, financiamento, aluguel)
            - Configurações de otimização (bounds para aportes)
    
    Configuration Categories:
        Economic Parameters:
            - inflacao_anual: Taxa de inflação anual (4.5%)
            - ir_renda_fixa: Imposto de renda para renda fixa (15%)
            - ir_aluguel: Imposto de renda para aluguel (27.5%)
        
        Investment Parameters:
            - aporte_inicial: Valor inicial disponível (R$ 100.000)
            - aporte_mensal: Aporte mensal (R$ 3.000)
            - anos: Horizonte de investimento (20 anos)
        
        Fixed Income Rates:
            - taxa_cdi: Taxa CDI anual (10.5%)
            - taxa_ipca: Taxa IPCA+ adicional (5.5%)
        
        Real Estate Parameters:
            - valor_imovel: Valor total do imóvel (R$ 500.000)
            - entrada_imovel: Valor da entrada (R$ 100.000)
            - taxa_juros_financiamento: Taxa do financiamento (9%)
            - valorizacao_imovel: Valorização anual (6%)
            - aluguel_mensal: Aluguel mensal (R$ 2.500)
            - anos_construcao: Período de construção (3 anos)
        
        Optimization Parameters:
            - optimize_aportes: Se deve otimizar aportes (False)
            - aporte_inicial_min/max: Bounds para aporte inicial
            - aporte_mensal_min/max: Bounds para aporte mensal
    
    Note:
        - Valores baseados em cenário econômico brasileiro típico
        - Parâmetros podem ser ajustados conforme necessário
        - Taxas de imposto seguem legislação brasileira atual
        - Parâmetros imobiliários representam imóvel de padrão médio
    
    Example:
        >>> params = configurar_parametros()
        >>> print(f"Inflação: {params['inflacao_anual']}%")
        >>> print(f"Aporte inicial: R$ {params['aporte_inicial']:,.2f}")
        Inflação: 4.5%
        Aporte inicial: R$ 100,000.00
    """
    # Parâmetros gerais de simulação
    parametros = {
        # Configurações econômicas
        'inflacao_anual': 4.5,  # Taxa de inflação anual em %
        'ir_renda_fixa': 15.0,  # Imposto de renda para renda fixa em %
        'ir_aluguel': 27.5,     # Imposto de renda para aluguel em %
        
        # Parâmetros temporais
        'anos': 20,             # Horizonte de investimento em anos
        
        # Parâmetros de investimento
        'aporte_inicial': 100000.0,  # Aporte inicial em R$
        'aporte_mensal': 3000.0,     # Aporte mensal em R$
        
        # Taxas de renda fixa
        'taxa_cdi': 10.5,       # Taxa CDI anual em %
        'taxa_ipca': 5.5,       # Taxa IPCA+ adicional anual em %
        
        # Parâmetros imobiliários
        'valor_imovel': 500000.0,           # Valor do imóvel em R$
        'entrada_imovel': 100000.0,         # Entrada do imóvel em R$
        'taxa_juros_financiamento': 9.0,    # Taxa de juros do financiamento anual em %
        'valorizacao_imovel': 6.0,          # Valorização anual do imóvel em %
        'aluguel_mensal': 2500.0,           # Aluguel mensal em R$
        'anos_construcao': 3,               # Anos de construção para imóvel na planta
        
        # Parâmetros de otimização
        'optimize_aportes': False,          # Se deve otimizar aportes
        'aporte_inicial_min': 50000.0,      # Aporte inicial mínimo para otimização
        'aporte_inicial_max': 200000.0,     # Aporte inicial máximo para otimização
        'aporte_mensal_min': 1000.0,        # Aporte mensal mínimo para otimização
        'aporte_mensal_max': 5000.0,        # Aporte mensal máximo para otimização
    }
    
    return parametros


def executar_simulacoes(parametros):
    """
    Executa todas as simulações de investimento.
    
    Args:
        parametros (dict): Dicionário com parâmetros de configuração
        
    Returns:
        dict: Dicionário com resultados de todas as simulações
    """
    # Instanciar OptimizedInvestment com parâmetros configurados
    simulador = OptimizedInvestment(
        inflacao=parametros['inflacao_anual'],
        ir_renda_fixa=parametros['ir_renda_fixa'],
        ir_aluguel=parametros['ir_aluguel']
    )
    
    print("\nExecutando simulações...")
    print("-" * 30)
    
    # Calcular parcelas do financiamento
    valor_financiado = parametros['valor_imovel'] - parametros['entrada_imovel']
    parcelas_financiamento = parametros['anos'] * 12  # Financiamento pelo período total
    
    resultados = {}
    
    # 1. Simulação CDI
    print("Executando simulação CDI...")
    resultados['cdi'] = simulador.investimento_cdi(
        aporte_inicial=parametros['aporte_inicial'],
        aporte_mensal=parametros['aporte_mensal'],
        taxa_cdi=parametros['taxa_cdi'],
        anos=parametros['anos'],
        imposto_final=False
    )
    
    # 2. Simulação IPCA+
    print("Executando simulação IPCA+...")
    resultados['ipca'] = simulador.investimento_ipca(
        aporte_inicial=parametros['aporte_inicial'],
        aporte_mensal=parametros['aporte_mensal'],
        taxa_ipca=parametros['taxa_ipca'],
        anos=parametros['anos'],
        imposto_final=True
    )
    
    # 3. Simulação Imóvel na Planta
    print("Executando simulação imóvel na planta...")
    resultados['imovel_planta'] = simulador.compra_financiada_planta(
        valor_imovel=parametros['valor_imovel'],
        entrada=parametros['entrada_imovel'],
        parcelas=parcelas_financiamento,
        taxa_juros=parametros['taxa_juros_financiamento'],
        valorizacao=parametros['valorizacao_imovel'],
        aluguel=parametros['aluguel_mensal'],
        anos_construcao=parametros['anos_construcao']
    )
    
    # 4. Simulação Imóvel Pronto
    print("Executando simulação imóvel pronto...")
    resultados['imovel_pronto'] = simulador.compra_financiada_pronto(
        valor_imovel=parametros['valor_imovel'],
        entrada=parametros['entrada_imovel'],
        parcelas=parcelas_financiamento,
        taxa_juros=parametros['taxa_juros_financiamento'],
        valorizacao=parametros['valorizacao_imovel'],
        aluguel=parametros['aluguel_mensal']
    )
    
    # 5. Simulação Estratégia Mista
    print("Executando simulação estratégia mista...")
    resultados['estrategia_mista'] = simulador.compra_e_renda_fixa(
        valor_imovel=parametros['valor_imovel'],
        entrada=parametros['entrada_imovel'],
        parcelas=parcelas_financiamento,
        taxa_juros=parametros['taxa_juros_financiamento'],
        taxa_cdi=parametros['taxa_cdi'],
        aporte_mensal=parametros['aporte_mensal'],
        valorizacao=parametros['valorizacao_imovel']
    )
    
    print("Simulações concluídas!")
    
    return resultados, simulador


def gerar_visualizacoes(resultados, parametros, simulador):
    """
    Gera todas as visualizações dos resultados das simulações.
    
    Args:
        resultados (dict): Resultados das simulações
        parametros (dict): Parâmetros de configuração
        simulador (OptimizedInvestment): Instância do simulador
    """
    print("\n" + "=" * 60)
    print("GERANDO VISUALIZAÇÕES")
    print("=" * 60)
    
    # Garantir que o diretório outputs existe
    import os
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        print("Diretório 'outputs' criado.")
    
    try:
        # 1. Gerar gráfico comparativo de imóveis (planta vs pronto)
        print("\nGerando gráfico comparativo de imóveis...")
        
        if 'imovel_planta' in resultados and 'imovel_pronto' in resultados:
            meses = parametros['anos'] * 12
            plotar_historico_planta_pronto(
                historico_planta=resultados['imovel_planta'],
                historico_pronto=resultados['imovel_pronto'],
                meses=meses
            )
        else:
            print("Aviso: Dados de imóveis não encontrados para comparação")
        
        # 2. Executar otimização para obter pesos otimizados
        print("\nExecutando otimização para visualização de cenários...")
        
        # Preparar estratégias para otimização (excluir estratégia mista para evitar redundância)
        estrategias_otimizacao = {k: v for k, v in resultados.items() 
                                if k != 'estrategia_mista'}
        
        pesos_otimizados = None
        try:
            if estrategias_otimizacao:
                pesos_otimizados, _, _, _ = simulador.otimizar_portfolio(
                    estrategias=estrategias_otimizacao,
                    anos=parametros['anos'],
                    optimize_aportes=False
                )
        except Exception as e:
            print(f"Aviso: Não foi possível obter pesos otimizados: {str(e)}")
            pesos_otimizados = None
        
        # 3. Gerar visualização de cenários com alocação otimizada
        print("Gerando gráfico de cenários de investimento...")
        
        # Preparar nomes mais amigáveis para os cenários
        cenarios_formatados = {}
        nomes_amigaveis = {
            'cdi': 'CDI',
            'ipca': 'IPCA+',
            'imovel_planta': 'Imóvel na Planta',
            'imovel_pronto': 'Imóvel Pronto',
            'estrategia_mista': 'Estratégia Mista'
        }
        
        # Validar que todos os cenários têm o mesmo comprimento
        tamanhos = [len(historico) for historico in resultados.values()]
        if len(set(tamanhos)) > 1:
            print(f"Aviso: Cenários têm tamanhos diferentes: {dict(zip(resultados.keys(), tamanhos))}")
            print("Usando apenas cenários com tamanho consistente...")
            
            # Encontrar o tamanho mais comum
            from collections import Counter
            tamanho_comum = Counter(tamanhos).most_common(1)[0][0]
            
            # Filtrar apenas cenários com tamanho correto
            resultados_filtrados = {k: v for k, v in resultados.items() 
                                  if len(v) == tamanho_comum}
        else:
            resultados_filtrados = resultados
        
        # Formatar nomes dos cenários filtrados
        for estrategia, historico in resultados_filtrados.items():
            nome_amigavel = nomes_amigaveis.get(estrategia, estrategia)
            cenarios_formatados[nome_amigavel] = historico
        
        if cenarios_formatados:
            plotar_cenarios(
                cenarios=cenarios_formatados,
                anos=parametros['anos'],
                pesos_otimizados=pesos_otimizados
            )
        else:
            print("Aviso: Nenhum cenário válido encontrado para visualização")
        
        # 4. Verificar criação correta dos arquivos de saída
        print("\nVerificando arquivos de saída...")
        
        import os
        arquivos_esperados = [
            'outputs/comparacao_imoveis.jpg',
            'outputs/cenarios_investimento.jpg'
        ]
        
        arquivos_criados = []
        arquivos_faltando = []
        
        for arquivo in arquivos_esperados:
            if os.path.exists(arquivo):
                tamanho = os.path.getsize(arquivo)
                arquivos_criados.append(f"{arquivo} ({tamanho:,} bytes)")
            else:
                arquivos_faltando.append(arquivo)
        
        if arquivos_criados:
            print("Arquivos criados com sucesso:")
            for arquivo in arquivos_criados:
                print(f"  ✓ {arquivo}")
        
        if arquivos_faltando:
            print("Arquivos não encontrados:")
            for arquivo in arquivos_faltando:
                print(f"  ✗ {arquivo}")
        
        print("\nVisualizações concluídas!")
        
    except Exception as e:
        print(f"Erro ao gerar visualizações: {str(e)}")
        print("Continuando execução sem visualizações...")


def gerar_relatorio_resultados(resultados, parametros, simulador):
    """
    Gera relatório formatado dos resultados das simulações.
    
    Args:
        resultados (dict): Resultados das simulações
        parametros (dict): Parâmetros de configuração
        simulador (OptimizedInvestment): Instância do simulador
    """
    print("\n" + "=" * 60)
    print("RELATÓRIO DE RESULTADOS")
    print("=" * 60)
    
    # Calcular valores finais (último mês)
    valores_finais = {}
    for estrategia, historico in resultados.items():
        valores_finais[estrategia] = historico[-1] if historico else 0.0
    
    # Exibir resultados individuais
    print("\nRESULTADOS INDIVIDUAIS (Valor Presente):")
    print("-" * 45)
    
    estrategias_nomes = {
        'cdi': 'CDI',
        'ipca': 'IPCA+',
        'imovel_planta': 'Imóvel na Planta',
        'imovel_pronto': 'Imóvel Pronto',
        'estrategia_mista': 'Estratégia Mista'
    }
    
    for estrategia, valor_final in valores_finais.items():
        nome = estrategias_nomes.get(estrategia, estrategia)
        print(f"{nome:20}: R$ {valor_final:>12,.2f}")
    
    # Comparação entre estratégias
    print("\nCOMPARAÇÃO ENTRE ESTRATÉGIAS:")
    print("-" * 35)
    
    # Encontrar melhor estratégia
    melhor_estrategia = max(valores_finais.items(), key=lambda x: x[1])
    melhor_nome = estrategias_nomes.get(melhor_estrategia[0], melhor_estrategia[0])
    melhor_valor = melhor_estrategia[1]
    
    print(f"Melhor estratégia: {melhor_nome}")
    print(f"Valor final: R$ {melhor_valor:,.2f}")
    
    # Calcular diferenças percentuais
    print("\nDiferença em relação à melhor estratégia:")
    for estrategia, valor_final in valores_finais.items():
        if estrategia != melhor_estrategia[0]:
            nome = estrategias_nomes.get(estrategia, estrategia)
            diferenca = ((valor_final - melhor_valor) / melhor_valor) * 100
            print(f"{nome:20}: {diferenca:>6.1f}%")
    
    # Executar otimização de portfólio
    print("\n" + "=" * 60)
    print("OTIMIZAÇÃO DE PORTFÓLIO")
    print("=" * 60)
    
    try:
        print("\nExecutando otimização...")
        
        # Preparar estratégias para otimização (excluir estratégia mista para evitar redundância)
        estrategias_otimizacao = {k: v for k, v in resultados.items() 
                                if k != 'estrategia_mista'}
        
        if parametros['optimize_aportes']:
            aporte_bounds = (
                (parametros['aporte_inicial_min'], parametros['aporte_inicial_max']),
                (parametros['aporte_mensal_min'], parametros['aporte_mensal_max'])
            )
            pesos_otimizados, aporte_inicial_otimo, aporte_mensal_otimo, retorno_final = simulador.otimizar_portfolio(
                estrategias=estrategias_otimizacao,
                anos=parametros['anos'],
                optimize_aportes=True,
                aporte_bounds=aporte_bounds
            )
            
            print("\nRESULTADOS DA OTIMIZAÇÃO (com aportes):")
            print("-" * 40)
            print(f"Aporte inicial ótimo: R$ {aporte_inicial_otimo:,.2f}")
            print(f"Aporte mensal ótimo: R$ {aporte_mensal_otimo:,.2f}")
            
        else:
            pesos_otimizados, _, _, retorno_final = simulador.otimizar_portfolio(
                estrategias=estrategias_otimizacao,
                anos=parametros['anos'],
                optimize_aportes=False
            )
            
            print("\nRESULTADOS DA OTIMIZAÇÃO:")
            print("-" * 30)
        
        print(f"Retorno final otimizado: R$ {retorno_final:,.2f}")
        
        print("\nALOCAÇÃO ÓTIMA:")
        print("-" * 20)
        estrategias_lista = list(estrategias_otimizacao.keys())
        for i, peso in enumerate(pesos_otimizados):
            estrategia = estrategias_lista[i]
            nome = estrategias_nomes.get(estrategia, estrategia)
            print(f"{nome:20}: {peso*100:>6.1f}%")
        
        # Comparar com melhor estratégia individual
        melhoria = ((retorno_final - melhor_valor) / melhor_valor) * 100
        print(f"\nMelhoria vs. melhor individual: {melhoria:+.1f}%")
        
    except Exception as e:
        print(f"\nErro na otimização: {str(e)}")
        print("Continuando com resultados individuais...")
    
    print("\n" + "=" * 60)
    print("RESUMO EXECUTIVO")
    print("=" * 60)
    
    total_investido = parametros['aporte_inicial'] + (parametros['aporte_mensal'] * parametros['anos'] * 12)
    print(f"Total investido: R$ {total_investido:,.2f}")
    print(f"Melhor estratégia individual: {melhor_nome}")
    print(f"Retorno final: R$ {melhor_valor:,.2f}")
    
    rentabilidade = ((melhor_valor - total_investido) / total_investido) * 100
    print(f"Rentabilidade total: {rentabilidade:.1f}%")
    
    rentabilidade_anual = ((melhor_valor / total_investido) ** (1/parametros['anos']) - 1) * 100
    print(f"Rentabilidade anual média: {rentabilidade_anual:.1f}%")


def main():
    """
    Função principal que executa todas as simulações e gera relatórios.
    """
    print("Sistema de Simulação e Otimização de Investimentos Imobiliários")
    print("=" * 60)
    
    # Configurar parâmetros de simulação
    parametros = configurar_parametros()
    
    print("\nParâmetros de Simulação:")
    print("-" * 30)
    print(f"Inflação anual: {parametros['inflacao_anual']:.1f}%")
    print(f"IR Renda Fixa: {parametros['ir_renda_fixa']:.1f}%")
    print(f"IR Aluguel: {parametros['ir_aluguel']:.1f}%")
    print(f"Horizonte: {parametros['anos']} anos")
    print(f"Aporte inicial: R$ {parametros['aporte_inicial']:,.2f}")
    print(f"Aporte mensal: R$ {parametros['aporte_mensal']:,.2f}")
    print(f"Taxa CDI: {parametros['taxa_cdi']:.1f}%")
    print(f"Taxa IPCA+: {parametros['taxa_ipca']:.1f}%")
    print(f"Valor do imóvel: R$ {parametros['valor_imovel']:,.2f}")
    print(f"Entrada: R$ {parametros['entrada_imovel']:,.2f}")
    print(f"Taxa financiamento: {parametros['taxa_juros_financiamento']:.1f}%")
    print(f"Valorização imóvel: {parametros['valorizacao_imovel']:.1f}%")
    print(f"Aluguel mensal: R$ {parametros['aluguel_mensal']:,.2f}")
    
    # Executar todas as simulações
    resultados, simulador = executar_simulacoes(parametros)
    
    # Gerar relatório de resultados
    gerar_relatorio_resultados(resultados, parametros, simulador)
    
    # Gerar visualizações
    gerar_visualizacoes(resultados, parametros, simulador)
    
    print("\nExecução concluída!")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()