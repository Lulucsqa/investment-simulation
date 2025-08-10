"""
Testes unitários para funcionalidades de otimização de portfólio.

Testa as funcionalidades de otimização da classe OptimizedInvestment,
incluindo função objetivo, restrições, bounds e algoritmo de otimização.
"""

import unittest
import numpy as np
from core import OptimizedInvestment


class TestOtimizacaoPortfolio(unittest.TestCase):
    """Testes para otimização de portfólio."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_calcular_portfolio_ponderado_basico(self):
        """Testa cálculo básico de portfólio ponderado."""
        estrategias = {
            'CDI': [1000.0, 1100.0, 1200.0],
            'IPCA': [1000.0, 1050.0, 1150.0]
        }
        pesos = np.array([0.6, 0.4])
        
        portfolio = self.investment._calcular_portfolio_ponderado(estrategias, pesos)
        
        # Deve ter 3 meses
        self.assertEqual(len(portfolio), 3)
        
        # Primeiro mês: 0.6 * 1000 + 0.4 * 1000 = 1000
        self.assertAlmostEqual(portfolio[0], 1000.0, places=2)
        
        # Segundo mês: 0.6 * 1100 + 0.4 * 1050 = 1080
        self.assertAlmostEqual(portfolio[1], 1080.0, places=2)
        
        # Terceiro mês: 0.6 * 1200 + 0.4 * 1150 = 1180
        self.assertAlmostEqual(portfolio[2], 1180.0, places=2)
    
    def test_calcular_portfolio_ponderado_pesos_iguais(self):
        """Testa portfólio ponderado com pesos iguais."""
        estrategias = {
            'A': [100.0, 200.0],
            'B': [300.0, 400.0]
        }
        pesos = np.array([0.5, 0.5])
        
        portfolio = self.investment._calcular_portfolio_ponderado(estrategias, pesos)
        
        # Primeiro mês: 0.5 * 100 + 0.5 * 300 = 200
        self.assertAlmostEqual(portfolio[0], 200.0, places=2)
        
        # Segundo mês: 0.5 * 200 + 0.5 * 400 = 300
        self.assertAlmostEqual(portfolio[1], 300.0, places=2)
    
    def test_calcular_portfolio_ponderado_erro_tamanhos(self):
        """Testa erro quando número de pesos difere do número de estratégias."""
        estrategias = {
            'A': [100.0, 200.0],
            'B': [300.0, 400.0]
        }
        pesos = np.array([0.5, 0.3, 0.2])  # 3 pesos para 2 estratégias
        
        with self.assertRaises(ValueError):
            self.investment._calcular_portfolio_ponderado(estrategias, pesos)
    
    def test_calcular_portfolio_ponderado_erro_historicos_diferentes(self):
        """Testa erro quando estratégias têm históricos de tamanhos diferentes."""
        estrategias = {
            'A': [100.0, 200.0],
            'B': [300.0, 400.0, 500.0]  # Tamanho diferente
        }
        pesos = np.array([0.5, 0.5])
        
        with self.assertRaises(ValueError):
            self.investment._calcular_portfolio_ponderado(estrategias, pesos)
    
    def test_funcao_objetivo_portfolio_maximizacao(self):
        """Testa função objetivo para maximização."""
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        pesos = np.array([0.7, 0.3])
        
        # Maximização (retorna valor negativo)
        resultado = self.investment._funcao_objetivo_portfolio(pesos, estrategias, maximize=True)
        
        # Valor final esperado: 0.7 * 1200 + 0.3 * 1100 = 1170
        # Para maximização, retorna negativo
        self.assertAlmostEqual(resultado, -1170.0, places=2)
    
    def test_funcao_objetivo_portfolio_minimizacao(self):
        """Testa função objetivo para minimização."""
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        pesos = np.array([0.4, 0.6])
        
        # Minimização (retorna valor positivo)
        resultado = self.investment._funcao_objetivo_portfolio(pesos, estrategias, maximize=False)
        
        # Valor final esperado: 0.4 * 1200 + 0.6 * 1100 = 1140
        self.assertAlmostEqual(resultado, 1140.0, places=2)
    
    def test_funcao_objetivo_portfolio_erro(self):
        """Testa função objetivo com erro (estratégias inválidas)."""
        estrategias = {
            'A': [1000.0, 1100.0],
            'B': [1000.0, 1050.0, 1100.0]  # Tamanho diferente
        }
        pesos = np.array([0.5, 0.5])
        
        # Deve retornar valor muito ruim em caso de erro
        resultado = self.investment._funcao_objetivo_portfolio(pesos, estrategias, maximize=True)
        self.assertEqual(resultado, 1e10)
    
    def test_criar_restricoes_portfolio(self):
        """Testa criação de restrições para otimização."""
        restricoes = self.investment._criar_restricoes_portfolio(3)
        
        # Deve ter uma restrição (soma dos pesos = 1)
        self.assertEqual(len(restricoes), 1)
        
        # Restrição deve ser de igualdade
        self.assertEqual(restricoes[0]['type'], 'eq')
        
        # Testa a função de restrição
        pesos_validos = np.array([0.3, 0.4, 0.3])
        resultado = restricoes[0]['fun'](pesos_validos)
        self.assertAlmostEqual(resultado, 0.0, places=6)
        
        pesos_invalidos = np.array([0.3, 0.4, 0.4])
        resultado_invalido = restricoes[0]['fun'](pesos_invalidos)
        self.assertAlmostEqual(resultado_invalido, 0.1, places=6)
    
    def test_criar_bounds_portfolio(self):
        """Testa criação de bounds para pesos."""
        bounds = self.investment._criar_bounds_portfolio(3)
        
        # Deve ter 3 bounds (um para cada peso)
        self.assertEqual(len(bounds), 3)
        
        # Todos os bounds devem ser (0.0, 1.0)
        for bound in bounds:
            self.assertEqual(bound, (0.0, 1.0))
    
    def test_criar_restricoes_com_aportes(self):
        """Testa criação de restrições incluindo aportes."""
        restricoes = self.investment._criar_restricoes_com_aportes(2)
        
        # Deve ter uma restrição (soma dos pesos = 1)
        self.assertEqual(len(restricoes), 1)
        
        # Testa a função de restrição com parâmetros [peso1, peso2, aporte_inicial, aporte_mensal]
        params_validos = np.array([0.6, 0.4, 10000.0, 1000.0])
        resultado = restricoes[0]['fun'](params_validos)
        self.assertAlmostEqual(resultado, 0.0, places=6)
        
        params_invalidos = np.array([0.7, 0.4, 10000.0, 1000.0])
        resultado_invalido = restricoes[0]['fun'](params_invalidos)
        self.assertAlmostEqual(resultado_invalido, 0.1, places=6)
    
    def test_criar_bounds_com_aportes(self):
        """Testa criação de bounds incluindo aportes."""
        aporte_bounds = (1000.0, 50000.0)
        bounds = self.investment._criar_bounds_com_aportes(2, aporte_bounds)
        
        # Deve ter 4 bounds: 2 pesos + aporte inicial + aporte mensal
        self.assertEqual(len(bounds), 4)
        
        # Primeiros 2 bounds são para pesos (0.0, 1.0)
        self.assertEqual(bounds[0], (0.0, 1.0))
        self.assertEqual(bounds[1], (0.0, 1.0))
        
        # Últimos 2 bounds são para aportes
        self.assertEqual(bounds[2], aporte_bounds)
        self.assertEqual(bounds[3], aporte_bounds)
    
    def test_validar_parametros_otimizacao_validos(self):
        """Testa validação com parâmetros válidos."""
        estrategias = {
            'CDI': [1000.0, 1100.0, 1200.0],
            'IPCA': [1000.0, 1050.0, 1150.0]
        }
        
        # Não deve lançar exceção
        try:
            self.investment._validar_parametros_otimizacao(estrategias, 1)
        except ValueError:
            self.fail("Validação falhou com parâmetros válidos")
    
    def test_validar_parametros_otimizacao_estrategias_vazias(self):
        """Testa validação com estratégias vazias."""
        estrategias = {}
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 1)
        
        self.assertIn("pelo menos uma estratégia", str(context.exception))
    
    def test_validar_parametros_otimizacao_anos_invalidos(self):
        """Testa validação com anos inválidos."""
        estrategias = {'A': [1000.0, 1100.0]}
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 0)
        
        self.assertIn("maior que zero", str(context.exception))
    
    def test_validar_parametros_otimizacao_historico_vazio(self):
        """Testa validação com histórico vazio."""
        estrategias = {'A': []}
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 1)
        
        self.assertIn("histórico vazio", str(context.exception))
    
    def test_validar_parametros_otimizacao_valores_nao_numericos(self):
        """Testa validação com valores não numéricos."""
        estrategias = {'A': [1000.0, 'invalid', 1200.0]}
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 1)
        
        self.assertIn("valores não numéricos", str(context.exception))
    
    def test_validar_parametros_otimizacao_tamanhos_diferentes(self):
        """Testa validação com históricos de tamanhos diferentes."""
        estrategias = {
            'A': [1000.0, 1100.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 1)
        
        self.assertIn("mesmo período", str(context.exception))
    
    def test_validar_parametros_otimizacao_aportes_sem_bounds(self):
        """Testa validação de aportes sem bounds."""
        estrategias = {'A': [1000.0, 1100.0]}
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 1, optimize_aportes=True)
        
        self.assertIn("aporte_bounds é obrigatório", str(context.exception))
    
    def test_validar_parametros_otimizacao_aporte_minimo_negativo(self):
        """Testa validação com aporte mínimo negativo."""
        estrategias = {'A': [1000.0, 1100.0]}
        aporte_bounds = (-1000.0, 50000.0)
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 1, optimize_aportes=True, aporte_bounds=aporte_bounds)
        
        self.assertIn("não pode ser negativo", str(context.exception))
    
    def test_validar_parametros_otimizacao_aporte_maximo_menor(self):
        """Testa validação com aporte máximo menor que mínimo."""
        estrategias = {'A': [1000.0, 1100.0]}
        aporte_bounds = (50000.0, 10000.0)
        
        with self.assertRaises(ValueError) as context:
            self.investment._validar_parametros_otimizacao(estrategias, 1, optimize_aportes=True, aporte_bounds=aporte_bounds)
        
        self.assertIn("maior que o mínimo", str(context.exception))
    
    def test_normalizar_pesos_normais(self):
        """Testa normalização de pesos normais."""
        pesos = np.array([0.3, 0.5, 0.4])  # Soma = 1.2
        pesos_normalizados = self.investment._normalizar_pesos(pesos)
        
        # Soma deve ser 1
        self.assertAlmostEqual(np.sum(pesos_normalizados), 1.0, places=6)
        
        # Proporções devem ser mantidas
        self.assertAlmostEqual(pesos_normalizados[0], 0.25, places=6)  # 0.3/1.2
        self.assertAlmostEqual(pesos_normalizados[1], 0.4167, places=3)  # 0.5/1.2
        self.assertAlmostEqual(pesos_normalizados[2], 0.3333, places=3)  # 0.4/1.2
    
    def test_normalizar_pesos_zeros(self):
        """Testa normalização de pesos todos zero."""
        pesos = np.array([0.0, 0.0, 0.0])
        pesos_normalizados = self.investment._normalizar_pesos(pesos)
        
        # Deve distribuir igualmente
        self.assertAlmostEqual(np.sum(pesos_normalizados), 1.0, places=6)
        for peso in pesos_normalizados:
            self.assertAlmostEqual(peso, 1.0/3.0, places=6)


class TestOtimizacaoIntegracao(unittest.TestCase):
    """Testes de integração para otimização de portfólio."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_otimizar_portfolio_apenas_pesos_simples(self):
        """Testa otimização simples apenas dos pesos."""
        # Cria estratégias simples onde uma é claramente melhor
        estrategias = {
            'Ruim': [1000.0, 1000.0, 1000.0],  # Sem crescimento
            'Boa': [1000.0, 1100.0, 1200.0]   # Crescimento linear
        }
        
        pesos, aporte_inicial, aporte_mensal, retorno = self.investment.otimizar_portfolio(
            estrategias, anos=1
        )
        
        # Deve ter 2 pesos
        self.assertEqual(len(pesos), 2)
        
        # Soma dos pesos deve ser 1
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        
        # Aportes devem ser None (não otimizados)
        self.assertIsNone(aporte_inicial)
        self.assertIsNone(aporte_mensal)
        
        # Peso da estratégia boa deve ser maior
        self.assertGreater(pesos[1], pesos[0])
        
        # Retorno deve ser positivo
        self.assertGreater(retorno, 1000.0)
    
    def test_otimizar_portfolio_tres_estrategias(self):
        """Testa otimização com três estratégias."""
        estrategias = {
            'A': [1000.0, 1050.0, 1100.0],
            'B': [1000.0, 1100.0, 1200.0],
            'C': [1000.0, 1080.0, 1160.0]
        }
        
        pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias, anos=1)
        
        # Deve ter 3 pesos
        self.assertEqual(len(pesos), 3)
        
        # Soma dos pesos deve ser 1
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        
        # Todos os pesos devem estar entre 0 e 1
        for peso in pesos:
            self.assertGreaterEqual(peso, 0.0)
            self.assertLessEqual(peso, 1.0)
        
        # Retorno deve ser razoável (pode ser igual ao máximo se otimização escolher 100% da melhor estratégia)
        self.assertGreater(retorno, 1100.0)
        self.assertLessEqual(retorno, 1200.0)
    
    def test_otimizar_portfolio_estrategias_identicas(self):
        """Testa otimização com estratégias idênticas."""
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1100.0, 1200.0]
        }
        
        pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias, anos=1)
        
        # Com estratégias idênticas, pesos podem ser qualquer combinação que some 1
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        
        # Retorno deve ser igual ao retorno das estratégias individuais
        self.assertAlmostEqual(retorno, 1200.0, places=2)
    
    def test_otimizar_portfolio_erro_convergencia(self):
        """Testa tratamento de erro de convergência."""
        # Cria cenário que pode causar problemas de convergência
        estrategias = {
            'A': [float('inf'), 1100.0, 1200.0],  # Valor infinito
            'B': [1000.0, 1100.0, 1200.0]
        }
        
        with self.assertRaises(RuntimeError) as context:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        self.assertIn("Falha na otimização", str(context.exception))


class TestOtimizacaoCenarios(unittest.TestCase):
    """Testes com cenários realistas de otimização."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_cenario_cdi_vs_ipca(self):
        """Testa otimização entre CDI e IPCA+."""
        # Simula CDI e IPCA+ com parâmetros realistas
        historico_cdi = self.investment.investimento_cdi(
            aporte_inicial=10000.0,
            aporte_mensal=1000.0,
            taxa_cdi=12.0,
            anos=2,
            imposto_final=False
        )
        
        historico_ipca = self.investment.investimento_ipca(
            aporte_inicial=10000.0,
            aporte_mensal=1000.0,
            taxa_ipca=6.0,
            anos=2,
            imposto_final=True
        )
        
        estrategias = {
            'CDI': historico_cdi,
            'IPCA+': historico_ipca
        }
        
        pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias, anos=2)
        
        # Deve otimizar corretamente
        self.assertEqual(len(pesos), 2)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertGreater(retorno, 20000.0)  # Mais que apenas os aportes
    
    def test_cenario_imovel_vs_renda_fixa(self):
        """Testa otimização entre imóvel e renda fixa."""
        # Simula imóvel pronto
        historico_imovel = self.investment.compra_financiada_pronto(
            valor_imovel=300000.0,
            entrada=60000.0,
            parcelas=120,  # 10 anos
            taxa_juros=12.0,
            valorizacao=8.0,
            aluguel=2000.0
        )
        
        # Simula CDI com mesmo aporte inicial
        historico_cdi = self.investment.investimento_cdi(
            aporte_inicial=60000.0,
            aporte_mensal=0.0,
            taxa_cdi=12.0,
            anos=10,
            imposto_final=False
        )
        
        estrategias = {
            'Imóvel': historico_imovel,
            'CDI': historico_cdi
        }
        
        pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias, anos=10)
        
        # Deve otimizar corretamente
        self.assertEqual(len(pesos), 2)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertGreater(retorno, 50000.0)
    
    def test_cenario_estrategia_mista(self):
        """Testa otimização incluindo estratégia mista."""
        # Simula diferentes estratégias
        historico_cdi = self.investment.investimento_cdi(
            aporte_inicial=50000.0,
            aporte_mensal=2000.0,
            taxa_cdi=12.0,
            anos=5,
            imposto_final=False
        )
        
        historico_mista = self.investment.compra_e_renda_fixa(
            valor_imovel=250000.0,
            entrada=50000.0,
            parcelas=60,  # 5 anos
            taxa_juros=12.0,
            taxa_cdi=12.0,
            aporte_mensal=2000.0,
            valorizacao=8.0
        )
        
        estrategias = {
            'CDI_Puro': historico_cdi,
            'Mista': historico_mista
        }
        
        pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias, anos=5)
        
        # Deve otimizar corretamente
        self.assertEqual(len(pesos), 2)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertGreater(retorno, 100000.0)


if __name__ == '__main__':
    unittest.main()