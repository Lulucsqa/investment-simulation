"""
Testes específicos para a tarefa 10.2: Implementar tratamento de erros de otimização.

Este módulo testa:
- Captura de falhas na convergência do algoritmo
- Implementação de fallback para casos de não convergência
- Logging detalhado de erros
- Cenários de erro específicos
"""

import unittest
import numpy as np
import logging
from unittest.mock import patch, MagicMock
from scipy.optimize import OptimizeResult

from core import OptimizedInvestment, OtimizacaoError, ParametroInvalidoError


class TestTratamentoErrosOtimizacao(unittest.TestCase):
    """Testes para tratamento avançado de erros na otimização."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
        
        # Estratégias válidas para testes
        self.estrategias_validas = {
            'CDI': [1000.0, 1100.0, 1200.0],
            'IPCA': [1000.0, 1080.0, 1160.0],
            'Imovel': [1000.0, 1120.0, 1250.0]
        }
    
    def test_analise_falha_convergencia_maxiter(self):
        """Testa análise de falha por máximo de iterações."""
        # Simula resultado com falha por máximo de iterações
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = "Maximum number of iterations reached"
        resultado.fun = -1000.0
        resultado.nit = 1000
        resultado.nfev = 5000
        
        detalhes = self.investment._analisar_falha_convergencia(resultado, 'SLSQP', 1)
        
        self.assertEqual(detalhes['erro_tipo'], 'CONVERGENCIA_MAXITER')
        self.assertEqual(detalhes['tentativa'], 1)
        self.assertEqual(detalhes['metodo'], 'SLSQP')
        self.assertFalse(detalhes['success'])
        self.assertEqual(detalhes['nit'], 1000)
        self.assertEqual(detalhes['nfev'], 5000)
        self.assertIn('Máximo de iterações', detalhes['descricao'])
    
    def test_analise_falha_convergencia_tolerancia(self):
        """Testa análise de falha por tolerância."""
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = "Tolerance not achieved"
        resultado.fun = -1000.0
        resultado.nit = 500
        resultado.nfev = 2500
        
        detalhes = self.investment._analisar_falha_convergencia(resultado, 'SLSQP', 2)
        
        self.assertEqual(detalhes['erro_tipo'], 'CONVERGENCIA_TOLERANCIA')
        self.assertEqual(detalhes['tentativa'], 2)
        self.assertIn('Tolerância', detalhes['descricao'])
    
    def test_analise_falha_convergencia_singular(self):
        """Testa análise de falha por matriz singular."""
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = "Singular matrix encountered"
        resultado.fun = None
        resultado.nit = 10
        resultado.nfev = 50
        
        detalhes = self.investment._analisar_falha_convergencia(resultado, 'trust-constr', 3)
        
        self.assertEqual(detalhes['erro_tipo'], 'CONVERGENCIA_SINGULAR')
        self.assertEqual(detalhes['tentativa'], 3)
        self.assertIn('singular', detalhes['descricao'].lower())
    
    def test_analise_falha_convergencia_linesearch(self):
        """Testa análise de falha na busca linear."""
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = "Line search failed"
        resultado.fun = -1000.0
        resultado.nit = 100
        resultado.nfev = 500
        
        detalhes = self.investment._analisar_falha_convergencia(resultado, 'L-BFGS-B', 4)
        
        self.assertEqual(detalhes['erro_tipo'], 'CONVERGENCIA_LINESEARCH')
        self.assertEqual(detalhes['tentativa'], 4)
        self.assertIn('busca linear', detalhes['descricao'])
    
    def test_analise_falha_convergencia_restricoes(self):
        """Testa análise de falha por restrições."""
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = "Constraint violation detected"
        resultado.fun = -1000.0
        resultado.nit = 200
        resultado.nfev = 1000
        
        detalhes = self.investment._analisar_falha_convergencia(resultado, 'SLSQP', 5)
        
        self.assertEqual(detalhes['erro_tipo'], 'CONVERGENCIA_RESTRICOES')
        self.assertEqual(detalhes['tentativa'], 5)
        self.assertIn('restrições', detalhes['descricao'])
    
    def test_analise_falha_convergencia_numerica(self):
        """Testa análise de falha por problemas numéricos."""
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = "Numerical precision issues"
        resultado.fun = -1000.0
        resultado.nit = 50
        resultado.nfev = 250
        
        detalhes = self.investment._analisar_falha_convergencia(resultado, 'SLSQP', 6)
        
        self.assertEqual(detalhes['erro_tipo'], 'CONVERGENCIA_NUMERICA')
        self.assertEqual(detalhes['tentativa'], 6)
        self.assertIn('precisão numérica', detalhes['descricao'])
    
    def test_analise_falha_convergencia_outros(self):
        """Testa análise de falha genérica."""
        resultado = OptimizeResult()
        resultado.success = False
        resultado.message = "Unknown optimization failure"
        resultado.fun = -1000.0
        resultado.nit = 75
        resultado.nfev = 375
        
        detalhes = self.investment._analisar_falha_convergencia(resultado, 'SLSQP', 7)
        
        self.assertEqual(detalhes['erro_tipo'], 'CONVERGENCIA_OUTROS')
        self.assertEqual(detalhes['tentativa'], 7)
        self.assertIn('genérica', detalhes['descricao'])
    
    @patch('core.minimize')
    def test_fallback_melhor_estrategia_com_logging_detalhado(self, mock_minimize):
        """Testa fallback com logging detalhado quando otimização falha."""
        # Simula múltiplas falhas de otimização
        mock_result = OptimizeResult()
        mock_result.success = False
        mock_result.message = "Maximum iterations reached"
        mock_result.fun = -1000.0
        mock_result.nit = 1000
        mock_result.nfev = 5000
        mock_minimize.return_value = mock_result
        
        with self.assertLogs('core', level='INFO') as log:
            pesos, aporte_inicial, aporte_mensal, retorno = self.investment.otimizar_portfolio(
                self.estrategias_validas, anos=1
            )
        
        # Verifica se fallback foi executado
        self.assertEqual(len(pesos), 3)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertIsNone(aporte_inicial)
        self.assertIsNone(aporte_mensal)
        
        # Verifica logging detalhado
        log_messages = ' '.join(log.output)
        self.assertIn('EXECUTANDO FALLBACK', log_messages)
        self.assertIn('melhor estratégia individual', log_messages)
        self.assertIn('Imovel', log_messages)  # Deve ser a melhor estratégia
        self.assertIn('1250.0', log_messages)  # Melhor retorno
    
    @patch('core.minimize')
    def test_fallback_distribuicao_igual_quando_melhor_estrategia_falha(self, mock_minimize):
        """Testa fallback para distribuição igual quando seleção da melhor estratégia falha."""
        # Simula falha na otimização
        mock_minimize.side_effect = RuntimeError("Optimization crashed")
        
        # Estratégias válidas mas que forçarão uso do fallback devido à falha do mock
        estrategias_para_fallback = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        with self.assertLogs('core', level='WARNING') as log:
            pesos, aporte_inicial, aporte_mensal, retorno = self.investment.otimizar_portfolio(
                estrategias_para_fallback, anos=1
            )
        
        # Verifica se fallback foi usado (pode ser melhor estratégia ou distribuição igual)
        self.assertEqual(len(pesos), 2)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertIsNone(aporte_inicial)
        self.assertIsNone(aporte_mensal)
        
        # Verifica logging de fallback
        log_messages = ' '.join(log.output)
        self.assertIn('fallback', log_messages.lower())
    
    @patch('core.minimize')
    def test_otimizacao_com_aportes_fallback_detalhado(self, mock_minimize):
        """Testa fallback detalhado para otimização com aportes."""
        # Simula falha na otimização com aportes
        mock_result = OptimizeResult()
        mock_result.success = False
        mock_result.message = "Constraint violation in aporte optimization"
        mock_result.fun = -1000.0
        mock_result.nit = 500
        mock_result.nfev = 2500
        mock_minimize.return_value = mock_result
        
        # Funções mock para estratégias
        def mock_cdi(aporte_inicial, aporte_mensal):
            return [aporte_inicial + i * aporte_mensal * 1.01 for i in range(12)]
        
        def mock_ipca(aporte_inicial, aporte_mensal):
            return [aporte_inicial + i * aporte_mensal * 1.008 for i in range(12)]
        
        estrategias_base = {
            'CDI': mock_cdi,
            'IPCA': mock_ipca
        }
        
        aporte_bounds = (1000.0, 5000.0)
        
        with self.assertLogs('core', level='INFO') as log:
            pesos, aporte_inicial, aporte_mensal, retorno = self.investment._otimizar_com_aportes(
                estrategias_base, 2, aporte_bounds
            )
        
        # Verifica se fallback foi executado
        self.assertEqual(len(pesos), 2)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertIsNotNone(aporte_inicial)
        self.assertIsNotNone(aporte_mensal)
        self.assertTrue(aporte_bounds[0] <= aporte_inicial <= aporte_bounds[1])
        self.assertTrue(aporte_bounds[0] <= aporte_mensal <= aporte_bounds[1])
        
        # Verifica logging detalhado
        log_messages = ' '.join(log.output)
        self.assertIn('FALLBACK PARA OTIMIZAÇÃO COM APORTES', log_messages)
        self.assertIn('Constraint violation', log_messages)
    
    @patch('core.minimize')
    def test_logging_detalhado_multiplas_tentativas(self, mock_minimize):
        """Testa se múltiplas tentativas são logadas adequadamente."""
        # Simula falha nas primeiras tentativas e sucesso na última
        results = []
        for i in range(3):
            result = OptimizeResult()
            result.success = False
            result.message = f"Failure attempt {i+1}"
            result.fun = -1000.0
            result.nit = 100
            result.nfev = 500
            results.append(result)
        
        # Última tentativa com sucesso
        success_result = OptimizeResult()
        success_result.success = True
        success_result.x = np.array([0.6, 0.4])
        success_result.fun = -1200.0
        results.append(success_result)
        
        mock_minimize.side_effect = results
        
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        with self.assertLogs('core', level='DEBUG') as log:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        # Verifica se múltiplas tentativas foram logadas
        log_messages = ' '.join(log.output)
        self.assertIn('Tentativa', log_messages)
        
        # Conta quantas tentativas foram logadas
        tentativas_count = log_messages.count('Tentativa')
        self.assertGreaterEqual(tentativas_count, 3)  # Deve ter pelo menos 3 tentativas
    
    def test_validacao_pesos_com_casos_extremos(self):
        """Testa validação de pesos com casos extremos."""
        # Teste com array vazio
        pesos_vazios = np.array([])
        self.assertFalse(self.investment._validar_pesos_otimizados(pesos_vazios))
        
        # Teste com valores muito pequenos
        pesos_pequenos = np.array([1e-10, 1.0 - 1e-10])
        self.assertTrue(self.investment._validar_pesos_otimizados(pesos_pequenos))
        
        # Teste com soma ligeiramente fora da tolerância
        pesos_fora_tolerancia = np.array([0.5, 0.48])  # Soma = 0.98
        self.assertFalse(self.investment._validar_pesos_otimizados(pesos_fora_tolerancia))
        
        # Teste com valores na borda da tolerância
        pesos_borda_tolerancia = np.array([0.495, 0.495])  # Soma = 0.99
        self.assertTrue(self.investment._validar_pesos_otimizados(pesos_borda_tolerancia))


class TestCenariosErroEspecificos(unittest.TestCase):
    """Testes para cenários específicos de erro."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_estrategias_com_retornos_identicos(self):
        """Testa otimização com estratégias de retornos idênticos."""
        estrategias_identicas = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1100.0, 1200.0],
            'C': [1000.0, 1100.0, 1200.0]
        }
        
        with self.assertLogs('core', level='WARNING') as log:
            pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias_identicas, anos=1)
        
        # Deve funcionar mas com warning
        self.assertEqual(len(pesos), 3)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertEqual(retorno, 1200.0)
        
        # Verifica se warning foi emitido
        log_messages = ' '.join(log.output)
        self.assertIn('similares', log_messages)
    
    def test_estrategias_com_volatilidade_extrema(self):
        """Testa otimização com estratégias de alta volatilidade."""
        estrategias_volateis = {
            'Volatil1': [1000.0, 500.0, 2000.0, 100.0, 3000.0],
            'Volatil2': [1000.0, 3000.0, 200.0, 2500.0, 150.0],
            'Estavel': [1000.0, 1050.0, 1100.0, 1150.0, 1200.0]
        }
        
        # Deve conseguir otimizar mesmo com alta volatilidade
        pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias_volateis, anos=1)
        
        self.assertEqual(len(pesos), 3)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertIsInstance(retorno, (int, float))
        self.assertTrue(np.isfinite(retorno))
    
    def test_estrategias_com_crescimento_exponencial(self):
        """Testa otimização com estratégias de crescimento exponencial."""
        estrategias_exponenciais = {
            'Exponencial': [1000.0 * (1.1 ** i) for i in range(12)],
            'Linear': [1000.0 + i * 100 for i in range(12)],
            'Constante': [1000.0] * 12
        }
        
        pesos, _, _, retorno = self.investment.otimizar_portfolio(estrategias_exponenciais, anos=1)
        
        self.assertEqual(len(pesos), 3)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        # Estratégia exponencial deve ter maior peso
        self.assertGreater(pesos[0], 0.5)  # Primeira estratégia (exponencial)


class TestLoggingDetalhado(unittest.TestCase):
    """Testes específicos para logging detalhado de erros."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_logging_nivel_debug_ativado(self):
        """Testa se logging de debug está funcionando adequadamente."""
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        # Configura logging para capturar DEBUG
        with self.assertLogs('core', level='DEBUG') as log:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        # Verifica se informações de debug estão presentes
        debug_messages = [msg for msg in log.output if 'DEBUG' in msg]
        self.assertGreater(len(debug_messages), 0)
        
        # Verifica conteúdo específico do debug
        log_content = ' '.join(log.output)
        self.assertIn('Pesos iniciais', log_content)
        self.assertIn('Tentativa', log_content)
    
    @patch('core.minimize')
    def test_logging_resumo_erros_completo(self, mock_minimize):
        """Testa se resumo completo de erros é logado."""
        # Simula falha consistente
        mock_result = OptimizeResult()
        mock_result.success = False
        mock_result.message = "Test failure for logging"
        mock_result.fun = -1000.0
        mock_result.nit = 100
        mock_result.nfev = 500
        mock_minimize.return_value = mock_result
        
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        with self.assertLogs('core', level='ERROR') as log:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        # Verifica se resumo detalhado foi logado
        log_content = ' '.join(log.output)
        self.assertIn('Resumo detalhado', log_content)
        self.assertIn('Test failure for logging', log_content)
        self.assertIn('Iterações', log_content)
        self.assertIn('Avaliações', log_content)


if __name__ == '__main__':
    # Configura logging para os testes
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()