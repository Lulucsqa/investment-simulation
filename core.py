"""
Módulo principal para simulação e otimização de investimentos imobiliários.

Este módulo contém a classe OptimizedInvestment que implementa simulações
de diferentes estratégias de investimento incluindo renda fixa e imóveis.
"""

import numpy as np
from scipy.optimize import minimize
from typing import List, Dict, Tuple, Optional


class OptimizedInvestment:
    """
    Classe principal para simulação e otimização de investimentos.
    
    Attributes:
        inflacao (float): Taxa de inflação anual em percentual
        ir_renda_fixa (float): Taxa de imposto de renda para renda fixa
        ir_aluguel (float): Taxa de imposto de renda para aluguel
    """
    
    def __init__(self, inflacao: float, ir_renda_fixa: float = 15, ir_aluguel: float = 27.5):
        """
        Inicializa a classe com parâmetros de configuração.
        
        Args:
            inflacao: Taxa de inflação anual em percentual
            ir_renda_fixa: Taxa de IR para renda fixa (padrão 15%)
            ir_aluguel: Taxa de IR para aluguel (padrão 27.5%)
        """
        self.inflacao = inflacao
        self.ir_renda_fixa = ir_renda_fixa
        self.ir_aluguel = ir_aluguel
        # Pré-calcula taxa mensal de inflação para otimização
        self.inflacao_mensal = self._taxa_anual_para_mensal(inflacao)
    
    def _taxa_anual_para_mensal(self, taxa_anual: float) -> float:
        """
        Converte taxa anual para taxa mensal equivalente.
        
        Args:
            taxa_anual: Taxa anual em percentual
            
        Returns:
            Taxa mensal equivalente em percentual
        """
        return ((1 + taxa_anual / 100) ** (1/12) - 1) * 100
    
    def _taxa_mensal_para_anual(self, taxa_mensal: float) -> float:
        """
        Converte taxa mensal para taxa anual equivalente.
        
        Args:
            taxa_mensal: Taxa mensal em percentual
            
        Returns:
            Taxa anual equivalente em percentual
        """
        return ((1 + taxa_mensal / 100) ** 12 - 1) * 100
    
    def ajuste_inflacao(self, valor: float, meses: int) -> float:
        """
        Ajusta um valor futuro para valor presente considerando a inflação.
        
        Args:
            valor: Valor futuro a ser ajustado
            meses: Número de meses no futuro
            
        Returns:
            Valor presente ajustado pela inflação
        """
        if meses == 0:
            return valor
        
        # Calcula o fator de desconto inflacionário
        fator_desconto = (1 + self.inflacao_mensal / 100) ** meses
        return valor / fator_desconto
    
    def investimento_cdi(self, aporte_inicial: float, aporte_mensal: float, 
                        taxa_cdi: float, anos: int, imposto_final: bool = False) -> List[float]:
        """
        Simula investimento em CDI com juros compostos e impostos.
        
        Args:
            aporte_inicial: Valor inicial investido
            aporte_mensal: Valor mensal de aporte
            taxa_cdi: Taxa CDI anual em percentual
            anos: Período de investimento em anos
            imposto_final: Se True, aplica IR apenas no final; se False, aplica mensalmente
            
        Returns:
            Lista com patrimônio acumulado mês a mês ajustado pela inflação
        """
        meses = anos * 12
        taxa_cdi_mensal = self._taxa_anual_para_mensal(taxa_cdi)
        historico = []
        
        # Valor atual do investimento (sem ajuste inflacionário)
        valor_atual = aporte_inicial
        
        for mes in range(meses):
            # Aplica rendimento do CDI
            rendimento_bruto = valor_atual * (taxa_cdi_mensal / 100)
            
            if imposto_final:
                # Se imposto final, acumula rendimento bruto
                valor_atual += rendimento_bruto
            else:
                # Se imposto mensal, aplica IR sobre o rendimento
                imposto = rendimento_bruto * (self.ir_renda_fixa / 100)
                rendimento_liquido = rendimento_bruto - imposto
                valor_atual += rendimento_liquido
            
            # Adiciona aporte mensal
            valor_atual += aporte_mensal
            
            # Ajusta pela inflação para valor presente e adiciona ao histórico
            valor_presente = self.ajuste_inflacao(valor_atual, mes + 1)
            historico.append(valor_presente)
        
        # Se imposto final, aplica IR sobre todo o ganho no último mês
        if imposto_final and historico:
            # Calcula ganho total (valor final - aportes totais)
            aportes_totais = aporte_inicial + (aporte_mensal * meses)
            ganho_total = valor_atual - aportes_totais
            imposto_total = ganho_total * (self.ir_renda_fixa / 100)
            
            # Ajusta o valor final
            valor_final_liquido = valor_atual - imposto_total
            valor_presente_final = self.ajuste_inflacao(valor_final_liquido, meses)
            historico[-1] = valor_presente_final
        
        return historico
    
    def investimento_ipca(self, aporte_inicial: float, aporte_mensal: float,
                         taxa_ipca: float, anos: int, imposto_final: bool = True) -> List[float]:
        """
        Simula investimento em IPCA+ com juros compostos e imposto apenas no vencimento.
        
        Args:
            aporte_inicial: Valor inicial investido
            aporte_mensal: Valor mensal de aporte
            taxa_ipca: Taxa IPCA+ anual em percentual (acima da inflação)
            anos: Período de investimento em anos
            imposto_final: Se True, aplica IR apenas no final (padrão para IPCA+)
            
        Returns:
            Lista com patrimônio acumulado mês a mês ajustado pela inflação
        """
        meses = anos * 12
        # IPCA+ rende inflação + taxa adicional
        taxa_total_anual = self.inflacao + taxa_ipca
        taxa_total_mensal = self._taxa_anual_para_mensal(taxa_total_anual)
        historico = []
        
        # Valor atual do investimento (sem ajuste inflacionário)
        valor_atual = aporte_inicial
        
        for mes in range(meses):
            # Aplica rendimento do IPCA+ (inflação + taxa adicional)
            rendimento_bruto = valor_atual * (taxa_total_mensal / 100)
            
            if imposto_final:
                # IPCA+ normalmente tem imposto apenas no final
                valor_atual += rendimento_bruto
            else:
                # Caso especial: imposto mensal (não comum para IPCA+)
                imposto = rendimento_bruto * (self.ir_renda_fixa / 100)
                rendimento_liquido = rendimento_bruto - imposto
                valor_atual += rendimento_liquido
            
            # Adiciona aporte mensal
            valor_atual += aporte_mensal
            
            # Ajusta pela inflação para valor presente e adiciona ao histórico
            valor_presente = self.ajuste_inflacao(valor_atual, mes + 1)
            historico.append(valor_presente)
        
        # Se imposto final, aplica IR sobre todo o ganho no último mês
        if imposto_final and historico:
            # Calcula ganho total (valor final - aportes totais)
            aportes_totais = aporte_inicial + (aporte_mensal * meses)
            ganho_total = valor_atual - aportes_totais
            imposto_total = ganho_total * (self.ir_renda_fixa / 100)
            
            # Ajusta o valor final
            valor_final_liquido = valor_atual - imposto_total
            valor_presente_final = self.ajuste_inflacao(valor_final_liquido, meses)
            historico[-1] = valor_presente_final
        
        return historico
    
    def _calcular_sac(self, valor_financiado: float, parcelas: int, taxa_juros_anual: float) -> Tuple[List[float], List[float], List[float]]:
        """
        Calcula financiamento pelo sistema SAC (Sistema de Amortização Constante).
        
        Args:
            valor_financiado: Valor total a ser financiado
            parcelas: Número de parcelas mensais
            taxa_juros_anual: Taxa de juros anual em percentual
            
        Returns:
            Tupla contendo (amortizações, juros, prestações) mensais
        """
        taxa_juros_mensal = self._taxa_anual_para_mensal(taxa_juros_anual) / 100
        
        # No SAC, a amortização é constante
        amortizacao_constante = valor_financiado / parcelas
        
        amortizacoes = []
        juros = []
        prestacoes = []
        saldo_devedor = valor_financiado
        
        for parcela in range(parcelas):
            # Juros sobre o saldo devedor atual
            juros_mes = saldo_devedor * taxa_juros_mensal
            
            # Prestação = amortização constante + juros do mês
            prestacao_mes = amortizacao_constante + juros_mes
            
            # Atualiza saldo devedor
            saldo_devedor -= amortizacao_constante
            
            amortizacoes.append(amortizacao_constante)
            juros.append(juros_mes)
            prestacoes.append(prestacao_mes)
        
        return amortizacoes, juros, prestacoes
    
    def _calcular_saldo_devedor_sac(self, valor_financiado: float, parcelas_pagas: int, total_parcelas: int) -> float:
        """
        Calcula o saldo devedor restante no sistema SAC.
        
        Args:
            valor_financiado: Valor original financiado
            parcelas_pagas: Número de parcelas já pagas
            total_parcelas: Número total de parcelas
            
        Returns:
            Saldo devedor restante
        """
        if parcelas_pagas >= total_parcelas:
            return 0.0
        
        amortizacao_constante = valor_financiado / total_parcelas
        saldo_restante = valor_financiado - (amortizacao_constante * parcelas_pagas)
        
        return max(0.0, saldo_restante)
    
    def compra_financiada_planta(self, valor_imovel: float, entrada: float, parcelas: int, 
                                taxa_juros: float, valorizacao: float, aluguel: float, 
                                anos_construcao: int = 3) -> List[float]:
        """
        Simula compra de imóvel na planta com financiamento SAC.
        
        Args:
            valor_imovel: Valor total do imóvel
            entrada: Valor da entrada
            parcelas: Número de parcelas do financiamento
            taxa_juros: Taxa de juros anual do financiamento
            valorizacao: Taxa de valorização anual do imóvel
            aluguel: Valor mensal do aluguel (quando disponível)
            anos_construcao: Período de construção em anos (padrão 3)
            
        Returns:
            Lista com patrimônio líquido mês a mês ajustado pela inflação
        """
        valor_financiado = valor_imovel - entrada
        meses_construcao = anos_construcao * 12
        meses_total = parcelas
        
        # Calcula financiamento SAC
        amortizacoes, juros_financiamento, prestacoes = self._calcular_sac(
            valor_financiado, parcelas, taxa_juros
        )
        
        # Taxa mensal de valorização do imóvel
        valorizacao_mensal = self._taxa_anual_para_mensal(valorizacao) / 100
        
        historico = []
        valor_imovel_atual = valor_imovel
        aluguel_acumulado = 0.0
        
        for mes in range(meses_total):
            # Valorização mensal do imóvel
            valor_imovel_atual *= (1 + valorizacao_mensal)
            
            # Saldo devedor atual
            saldo_devedor = self._calcular_saldo_devedor_sac(valor_financiado, mes, parcelas)
            
            # Aluguel só começa após período de construção
            if mes >= meses_construcao:
                # Aplica imposto de renda sobre aluguel
                aluguel_liquido = aluguel * (1 - self.ir_aluguel / 100)
                aluguel_acumulado += aluguel_liquido
            
            # Patrimônio líquido = valor do imóvel - saldo devedor + aluguel acumulado - entrada
            patrimonio_liquido = valor_imovel_atual - saldo_devedor + aluguel_acumulado - entrada
            
            # Ajusta pela inflação para valor presente
            patrimonio_presente = self.ajuste_inflacao(patrimonio_liquido, mes + 1)
            historico.append(patrimonio_presente)
        
        return historico
    
    def compra_financiada_pronto(self, valor_imovel: float, entrada: float, parcelas: int,
                                taxa_juros: float, valorizacao: float, aluguel: float) -> List[float]:
        """
        Simula compra de imóvel pronto com financiamento SAC.
        
        Args:
            valor_imovel: Valor total do imóvel
            entrada: Valor da entrada
            parcelas: Número de parcelas do financiamento
            taxa_juros: Taxa de juros anual do financiamento
            valorizacao: Taxa de valorização anual do imóvel
            aluguel: Valor mensal do aluguel
            
        Returns:
            Lista com patrimônio líquido mês a mês ajustado pela inflação
        """
        valor_financiado = valor_imovel - entrada
        
        # Calcula financiamento SAC
        amortizacoes, juros_financiamento, prestacoes = self._calcular_sac(
            valor_financiado, parcelas, taxa_juros
        )
        
        # Taxa mensal de valorização do imóvel
        valorizacao_mensal = self._taxa_anual_para_mensal(valorizacao) / 100
        
        historico = []
        valor_imovel_atual = valor_imovel
        aluguel_acumulado = 0.0
        
        for mes in range(parcelas):
            # Valorização mensal do imóvel
            valor_imovel_atual *= (1 + valorizacao_mensal)
            
            # Saldo devedor atual
            saldo_devedor = self._calcular_saldo_devedor_sac(valor_financiado, mes, parcelas)
            
            # Aluguel começa imediatamente (imóvel pronto)
            # Aplica imposto de renda sobre aluguel
            aluguel_liquido = aluguel * (1 - self.ir_aluguel / 100)
            aluguel_acumulado += aluguel_liquido
            
            # Patrimônio líquido = valor do imóvel - saldo devedor + aluguel acumulado - entrada
            patrimonio_liquido = valor_imovel_atual - saldo_devedor + aluguel_acumulado - entrada
            
            # Ajusta pela inflação para valor presente
            patrimonio_presente = self.ajuste_inflacao(patrimonio_liquido, mes + 1)
            historico.append(patrimonio_presente)
        
        return historico    

    def compra_e_renda_fixa(self, valor_imovel: float, entrada: float, parcelas: int,
                           taxa_juros: float, taxa_cdi: float, aporte_mensal: float,
                           valorizacao: float) -> List[float]:
        """
        Simula estratégia mista: financiamento imobiliário + investimento em CDI.
        
        Args:
            valor_imovel: Valor total do imóvel
            entrada: Valor da entrada do imóvel
            parcelas: Número de parcelas do financiamento
            taxa_juros: Taxa de juros anual do financiamento
            taxa_cdi: Taxa CDI anual para investimento
            aporte_mensal: Valor mensal disponível para investimento em renda fixa
            valorizacao: Taxa de valorização anual do imóvel
            
        Returns:
            Lista com patrimônio total mês a mês ajustado pela inflação
        """
        valor_financiado = valor_imovel - entrada
        
        # Calcula financiamento SAC
        amortizacoes, juros_financiamento, prestacoes = self._calcular_sac(
            valor_financiado, parcelas, taxa_juros
        )
        
        # Taxa mensal de valorização do imóvel e CDI
        valorizacao_mensal = self._taxa_anual_para_mensal(valorizacao) / 100
        taxa_cdi_mensal = self._taxa_anual_para_mensal(taxa_cdi) / 100
        
        historico = []
        valor_imovel_atual = valor_imovel
        saldo_renda_fixa = 0.0
        
        for mes in range(parcelas):
            # Valorização mensal do imóvel
            valor_imovel_atual *= (1 + valorizacao_mensal)
            
            # Saldo devedor atual do imóvel
            saldo_devedor = self._calcular_saldo_devedor_sac(valor_financiado, mes, parcelas)
            
            # Rendimento da renda fixa (CDI com imposto mensal)
            if saldo_renda_fixa > 0:
                rendimento_bruto = saldo_renda_fixa * taxa_cdi_mensal
                imposto = rendimento_bruto * (self.ir_renda_fixa / 100)
                rendimento_liquido = rendimento_bruto - imposto
                saldo_renda_fixa += rendimento_liquido
            
            # Adiciona aporte mensal à renda fixa
            saldo_renda_fixa += aporte_mensal
            
            # Patrimônio do imóvel (valor - saldo devedor - entrada)
            patrimonio_imovel = valor_imovel_atual - saldo_devedor - entrada
            
            # Patrimônio total = patrimônio imóvel + saldo renda fixa
            patrimonio_total = patrimonio_imovel + saldo_renda_fixa
            
            # Ajusta pela inflação para valor presente
            patrimonio_presente = self.ajuste_inflacao(patrimonio_total, mes + 1)
            historico.append(patrimonio_presente)
        
        return historico
    
    def _calcular_portfolio_ponderado(self, estrategias: Dict[str, List[float]], pesos: np.ndarray) -> List[float]:
        """
        Calcula o patrimônio de um portfólio ponderado de estratégias.
        
        Args:
            estrategias: Dicionário com nome da estratégia e histórico de patrimônio
            pesos: Array com pesos de cada estratégia (devem somar 1)
            
        Returns:
            Lista com patrimônio total ponderado mês a mês
        """
        if len(pesos) != len(estrategias):
            raise ValueError("Número de pesos deve ser igual ao número de estratégias")
        
        # Converte estratégias para arrays numpy para operações vetorizadas
        nomes_estrategias = list(estrategias.keys())
        historicos = [np.array(estrategias[nome]) for nome in nomes_estrategias]
        
        # Verifica se todos os históricos têm o mesmo tamanho
        tamanhos = [len(hist) for hist in historicos]
        if len(set(tamanhos)) > 1:
            raise ValueError("Todas as estratégias devem ter o mesmo período")
        
        # Calcula portfólio ponderado
        portfolio_ponderado = np.zeros(tamanhos[0])
        for i, (peso, historico) in enumerate(zip(pesos, historicos)):
            portfolio_ponderado += peso * historico
        
        return portfolio_ponderado.tolist()
    
    def _funcao_objetivo_portfolio(self, pesos: np.ndarray, estrategias: Dict[str, List[float]], 
                                  maximize: bool = True) -> float:
        """
        Função objetivo para otimização de portfólio.
        
        Args:
            pesos: Array com pesos de cada estratégia
            estrategias: Dicionário com estratégias e seus históricos
            maximize: Se True, maximiza retorno (retorna valor negativo para minimização)
            
        Returns:
            Valor da função objetivo (retorno final do portfólio)
        """
        try:
            # Calcula portfólio ponderado
            portfolio = self._calcular_portfolio_ponderado(estrategias, pesos)
            
            # Retorno final é o último valor do portfólio
            retorno_final = portfolio[-1] if portfolio else 0.0
            
            # Para maximização, retorna valor negativo (scipy.minimize minimiza)
            return -retorno_final if maximize else retorno_final
            
        except Exception:
            # Em caso de erro, retorna valor muito ruim
            return 1e10 if maximize else -1e10
    
    def _funcao_objetivo_com_aportes(self, params: np.ndarray, estrategias_base: Dict[str, callable],
                                   anos: int, aporte_bounds: Tuple[float, float],
                                   maximize: bool = True) -> float:
        """
        Função objetivo para otimização incluindo aportes inicial e mensal.
        
        Args:
            params: Array com [pesos..., aporte_inicial, aporte_mensal]
            estrategias_base: Dicionário com funções que geram estratégias
            anos: Período de investimento em anos
            aporte_bounds: Tupla com (min_aporte, max_aporte)
            maximize: Se True, maximiza retorno
            
        Returns:
            Valor da função objetivo
        """
        try:
            # Separa pesos dos aportes
            num_estrategias = len(estrategias_base)
            pesos = params[:num_estrategias]
            aporte_inicial = params[num_estrategias]
            aporte_mensal = params[num_estrategias + 1]
            
            # Valida bounds dos aportes
            min_aporte, max_aporte = aporte_bounds
            if aporte_inicial < min_aporte or aporte_inicial > max_aporte:
                return 1e10 if maximize else -1e10
            if aporte_mensal < min_aporte or aporte_mensal > max_aporte:
                return 1e10 if maximize else -1e10
            
            # Gera estratégias com os aportes otimizados
            estrategias = {}
            for nome, func_estrategia in estrategias_base.items():
                estrategias[nome] = func_estrategia(aporte_inicial, aporte_mensal, anos)
            
            # Calcula função objetivo
            return self._funcao_objetivo_portfolio(pesos, estrategias, maximize)
            
        except Exception:
            return 1e10 if maximize else -1e10
    
    def _criar_restricoes_portfolio(self, num_estrategias: int) -> List[Dict]:
        """
        Cria restrições para otimização de portfólio.
        
        Args:
            num_estrategias: Número de estratégias no portfólio
            
        Returns:
            Lista de dicionários com restrições para scipy.optimize
        """
        # Restrição: soma dos pesos deve ser igual a 1
        def restricao_soma_pesos(pesos):
            return np.sum(pesos) - 1.0
        
        restricoes = [
            {
                'type': 'eq',
                'fun': restricao_soma_pesos
            }
        ]
        
        return restricoes
    
    def _criar_restricoes_com_aportes(self, num_estrategias: int) -> List[Dict]:
        """
        Cria restrições para otimização incluindo aportes.
        
        Args:
            num_estrategias: Número de estratégias no portfólio
            
        Returns:
            Lista de dicionários com restrições para scipy.optimize
        """
        # Restrição: soma dos pesos deve ser igual a 1 (apenas os primeiros num_estrategias parâmetros)
        def restricao_soma_pesos(params):
            pesos = params[:num_estrategias]
            return np.sum(pesos) - 1.0
        
        restricoes = [
            {
                'type': 'eq',
                'fun': restricao_soma_pesos
            }
        ]
        
        return restricoes
    
    def _criar_bounds_portfolio(self, num_estrategias: int) -> List[Tuple[float, float]]:
        """
        Cria bounds (limites) para pesos do portfólio.
        
        Args:
            num_estrategias: Número de estratégias no portfólio
            
        Returns:
            Lista de tuplas com (min, max) para cada peso
        """
        # Cada peso deve estar entre 0 e 1
        bounds = [(0.0, 1.0) for _ in range(num_estrategias)]
        return bounds
    
    def _criar_bounds_com_aportes(self, num_estrategias: int, 
                                 aporte_bounds: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Cria bounds para otimização incluindo aportes.
        
        Args:
            num_estrategias: Número de estratégias no portfólio
            aporte_bounds: Tupla com (min_aporte, max_aporte)
            
        Returns:
            Lista de tuplas com bounds para [pesos..., aporte_inicial, aporte_mensal]
        """
        # Bounds para pesos (0 a 1)
        bounds = [(0.0, 1.0) for _ in range(num_estrategias)]
        
        # Bounds para aporte inicial e mensal
        min_aporte, max_aporte = aporte_bounds
        bounds.extend([(min_aporte, max_aporte), (min_aporte, max_aporte)])
        
        return bounds
    
    def _validar_parametros_otimizacao(self, estrategias: Dict[str, List[float]], 
                                      anos: int, optimize_aportes: bool = False,
                                      aporte_bounds: Optional[Tuple[float, float]] = None) -> None:
        """
        Valida parâmetros de entrada para otimização.
        
        Args:
            estrategias: Dicionário com estratégias e históricos
            anos: Período de investimento em anos
            optimize_aportes: Se True, otimiza também aportes
            aporte_bounds: Bounds para aportes (obrigatório se optimize_aportes=True)
            
        Raises:
            ValueError: Se parâmetros são inválidos
        """
        if not estrategias:
            raise ValueError("Deve haver pelo menos uma estratégia")
        
        if anos <= 0:
            raise ValueError("Período deve ser maior que zero")
        
        # Verifica se todas as estratégias têm históricos válidos
        tamanhos = []
        for nome, historico in estrategias.items():
            if not historico:
                raise ValueError(f"Estratégia '{nome}' tem histórico vazio")
            if not all(isinstance(x, (int, float)) for x in historico):
                raise ValueError(f"Estratégia '{nome}' contém valores não numéricos")
            tamanhos.append(len(historico))
        
        # Verifica se todos os históricos têm o mesmo tamanho
        if len(set(tamanhos)) > 1:
            raise ValueError("Todas as estratégias devem ter o mesmo período")
        
        # Validações específicas para otimização de aportes
        if optimize_aportes:
            if aporte_bounds is None:
                raise ValueError("aporte_bounds é obrigatório quando optimize_aportes=True")
            
            min_aporte, max_aporte = aporte_bounds
            if min_aporte < 0:
                raise ValueError("Aporte mínimo não pode ser negativo")
            if max_aporte <= min_aporte:
                raise ValueError("Aporte máximo deve ser maior que o mínimo")
    
    def _normalizar_pesos(self, pesos: np.ndarray) -> np.ndarray:
        """
        Normaliza pesos para que somem exatamente 1.
        
        Args:
            pesos: Array com pesos a serem normalizados
            
        Returns:
            Array com pesos normalizados
        """
        soma_pesos = np.sum(pesos)
        if soma_pesos == 0:
            # Se todos os pesos são zero, distribui igualmente
            return np.ones(len(pesos)) / len(pesos)
        
        return pesos / soma_pesos
    
    def otimizar_portfolio(self, estrategias: Dict[str, List[float]], anos: int,
                          optimize_aportes: bool = False, 
                          aporte_bounds: Optional[Tuple[float, float]] = None) -> Tuple[np.ndarray, Optional[float], Optional[float], float]:
        """
        Otimiza alocação de portfólio para maximizar retorno final.
        
        Args:
            estrategias: Dicionário com nome da estratégia e histórico de patrimônio
            anos: Período de investimento em anos (usado para validação)
            optimize_aportes: Se True, otimiza também aporte inicial e mensal
            aporte_bounds: Tupla com (min_aporte, max_aporte) para otimização de aportes
            
        Returns:
            Tupla com (pesos_otimizados, aporte_inicial_otimo, aporte_mensal_otimo, retorno_final)
            
        Raises:
            ValueError: Se parâmetros são inválidos
            RuntimeError: Se otimização falha na convergência
        """
        # Valida parâmetros de entrada
        self._validar_parametros_otimizacao(estrategias, anos, optimize_aportes, aporte_bounds)
        
        num_estrategias = len(estrategias)
        
        try:
            if optimize_aportes:
                # Otimização incluindo aportes
                return self._otimizar_com_aportes(estrategias, num_estrategias, aporte_bounds)
            else:
                # Otimização apenas dos pesos
                return self._otimizar_apenas_pesos(estrategias, num_estrategias)
                
        except Exception as e:
            raise RuntimeError(f"Falha na otimização: {str(e)}")
    
    def _otimizar_apenas_pesos(self, estrategias: Dict[str, List[float]], 
                              num_estrategias: int) -> Tuple[np.ndarray, None, None, float]:
        """
        Otimiza apenas os pesos do portfólio.
        
        Args:
            estrategias: Dicionário com estratégias e históricos
            num_estrategias: Número de estratégias
            
        Returns:
            Tupla com (pesos_otimizados, None, None, retorno_final)
        """
        # Pesos iniciais (distribuição igual)
        pesos_iniciais = np.ones(num_estrategias) / num_estrategias
        
        # Cria restrições e bounds
        restricoes = self._criar_restricoes_portfolio(num_estrategias)
        bounds = self._criar_bounds_portfolio(num_estrategias)
        
        # Executa otimização
        resultado = minimize(
            fun=self._funcao_objetivo_portfolio,
            x0=pesos_iniciais,
            args=(estrategias, True),  # True para maximizar
            method='SLSQP',
            bounds=bounds,
            constraints=restricoes,
            options={'ftol': 1e-9, 'disp': False}
        )
        
        if not resultado.success:
            raise RuntimeError(f"Otimização não convergiu: {resultado.message}")
        
        # Normaliza pesos para garantir soma = 1
        pesos_otimizados = self._normalizar_pesos(resultado.x)
        
        # Calcula retorno final
        portfolio_otimo = self._calcular_portfolio_ponderado(estrategias, pesos_otimizados)
        retorno_final = portfolio_otimo[-1] if portfolio_otimo else 0.0
        
        return pesos_otimizados, None, None, retorno_final
    
    def _otimizar_com_aportes(self, estrategias_base: Dict[str, callable], 
                             num_estrategias: int, 
                             aporte_bounds: Tuple[float, float]) -> Tuple[np.ndarray, float, float, float]:
        """
        Otimiza pesos e aportes simultaneamente.
        
        Args:
            estrategias_base: Dicionário com funções que geram estratégias
            num_estrategias: Número de estratégias
            aporte_bounds: Bounds para aportes
            
        Returns:
            Tupla com (pesos_otimizados, aporte_inicial_otimo, aporte_mensal_otimo, retorno_final)
        """
        min_aporte, max_aporte = aporte_bounds
        
        # Parâmetros iniciais: [pesos..., aporte_inicial, aporte_mensal]
        pesos_iniciais = np.ones(num_estrategias) / num_estrategias
        aporte_inicial_inicial = (min_aporte + max_aporte) / 2
        aporte_mensal_inicial = (min_aporte + max_aporte) / 2
        
        params_iniciais = np.concatenate([
            pesos_iniciais, 
            [aporte_inicial_inicial, aporte_mensal_inicial]
        ])
        
        # Cria restrições e bounds
        restricoes = self._criar_restricoes_com_aportes(num_estrategias)
        bounds = self._criar_bounds_com_aportes(num_estrategias, aporte_bounds)
        
        # Executa otimização
        resultado = minimize(
            fun=self._funcao_objetivo_com_aportes,
            x0=params_iniciais,
            args=(estrategias_base, 10, aporte_bounds, True),  # 10 anos padrão, True para maximizar
            method='SLSQP',
            bounds=bounds,
            constraints=restricoes,
            options={'ftol': 1e-9, 'disp': False}
        )
        
        if not resultado.success:
            raise RuntimeError(f"Otimização não convergiu: {resultado.message}")
        
        # Extrai resultados
        pesos_otimizados = self._normalizar_pesos(resultado.x[:num_estrategias])
        aporte_inicial_otimo = resultado.x[num_estrategias]
        aporte_mensal_otimo = resultado.x[num_estrategias + 1]
        
        # Calcula retorno final com parâmetros otimizados
        retorno_final = -resultado.fun  # Converte de volta (estava negativo para maximização)
        
        return pesos_otimizados, aporte_inicial_otimo, aporte_mensal_otimo, retorno_final