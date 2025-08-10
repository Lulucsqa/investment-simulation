"""
Testes específicos para tratamento de erros na otimização de portfólio.
"""

import unittest
import numpy as np
from unittest.mock import patch
from scipy.optimize import OptimizeResult

from core import OptimizedInvestment, OtimizacaoError, ParametroInvalidoError


class TestOtimizacaoErros(unittest.TestCase):
    """Testes para tratamento de erros na otimização."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_otimizacao_estrategias_valores_infinitos(self):
        """Testa tratamento de estratégias com valores infinitos."""
        estrategias = {
            'A': [1000.0, float('inf'), 1200.0],
            'B': [1000.0, 1100.0, 1200.0]
        }
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        self.assertIn("valor inválido", str(context.exception))
    
    def test_otimizacao_estrategias_valores_nan(self):
        """Testa tratamento de estratégias com valores NaN."""
        estrategias = {
            'A': [1000.0, float('nan'), 1200.0],
            'B': [1000.0, 1100.0, 1200.0]
        }
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        self.assertIn("valor inválido", str(context.exception))
    
    @patch('core.minimize')
    def test_otimizacao_falha_convergencia_com_fallback(self, mock_minimize):
        """Testa fallback quando otimização falha na convergência."""
        # Simula falha na otimização
        mock_result = OptimizeResult()
        mock_result.success = False
        mock_result.message = "Optimization failed"
        mock_minimize.return_value = mock_result
        
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        # Deve usar fallback (melhor estratégia individual)
        pesos, aporte_inicial, aporte_mensal, retorno = self.investment.otimizar_portfolio(
            estrategias, anos=1
        )
        
        # Verifica se fallback foi usado (100% na melhor estratégia)
        self.assertEqual(len(pesos), 2)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertTrue(np.max(pesos) == 1.0)  # Uma estratégia com 100%
        self.assertIsNone(aporte_inicial)
        self.assertIsNone(aporte_mensal)
        self.assertEqual(retorno, 1200.0)  # Melhor estratégia (A)
    
    @patch('core.minimize')
    def test_otimizacao_excecao_com_fallback(self, mock_minimize):
        """Testa fallback quando otimização gera exceção."""
        # Simula exceção na otimização
        mock_minimize.side_effect = RuntimeError("Optimization crashed")
        
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        # Deve usar fallback
        pesos, aporte_inicial, aporte_mensal, retorno = self.investment.otimizar_portfolio(
            estrategias, anos=1
        )
        
        # Verifica se fallback foi usado
        self.assertEqual(len(pesos), 2)
        self.assertAlmostEqual(np.sum(pesos), 1.0, places=6)
        self.assertIsNone(aporte_inicial)
        self.assertIsNone(aporte_mensal)
    
    def test_verificar_condicoes_convergencia_estrategias_similares(self):
        """Testa detecção de estratégias com retornos muito similares."""
        # Estratégias com retornos quase idênticos
        estrategias = {
            'A': [1000.0, 1100.0, 1200.000001],
            'B': [1000.0, 1100.0, 1200.000002]
        }
        
        # Não deve gerar erro, mas deve logar warning
        with self.assertLogs('core', level='WARNING') as log:
            self.investment._verificar_condicoes_convergencia(estrategias)
        
        # Verifica se warning foi logado
        warning_found = any("retornos muito similares" in message for message in log.output)
        self.assertTrue(warning_found)
    
    def test_validar_pesos_otimizados_valores_infinitos(self):
        """Testa validação de pesos com valores infinitos."""
        pesos_invalidos = np.array([0.5, float('inf')])
        
        resultado = self.investment._validar_pesos_otimizados(pesos_invalidos)
        self.assertFalse(resultado)
    
    def test_validar_pesos_otimizados_valores_negativos(self):
        """Testa validação de pesos com valores negativos."""
        pesos_invalidos = np.array([0.5, -0.5])
        
        resultado = self.investment._validar_pesos_otimizados(pesos_invalidos)
        self.assertFalse(resultado)
    
    def test_validar_pesos_otimizados_soma_incorreta(self):
        """Testa validação de pesos com soma incorreta."""
        pesos_invalidos = np.array([0.3, 0.3])  # Soma = 0.6, deveria ser ~1.0
        
        resultado = self.investment._validar_pesos_otimizados(pesos_invalidos)
        self.assertFalse(resultado)
    
    def test_validar_pesos_otimizados_validos(self):
        """Testa validação de pesos válidos."""
        pesos_validos = np.array([0.6, 0.4])
        
        resultado = self.investment._validar_pesos_otimizados(pesos_validos)
        self.assertTrue(resultado)


class TestOtimizacaoLogging(unittest.TestCase):
    """Testes para verificar logging detalhado de erros."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_logging_tentativas_otimizacao(self):
        """Testa se tentativas de otimização são logadas adequadamente."""
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        with self.assertLogs('core', level='DEBUG') as log:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        # Verifica se logs de debug estão presentes
        debug_messages = [msg for msg in log.output if 'DEBUG' in msg]
        self.assertTrue(len(debug_messages) > 0)
        
        # Verifica se informações específicas estão sendo logadas
        tentativa_found = any("Tentativa" in message for message in log.output)
        self.assertTrue(tentativa_found)
    
    @patch('core.minimize')
    def test_logging_fallback_detalhado(self, mock_minimize):
        """Testa se fallback é logado com detalhes adequados."""
        # Simula falha na otimização com resultado completo
        mock_result = OptimizeResult()
        mock_result.success = False
        mock_result.message = "Test failure"
        mock_result.fun = -1000.0  # Add the fun attribute
        mock_result.nit = 100
        mock_result.nfev = 500
        mock_minimize.return_value = mock_result
        
        estrategias = {
            'A': [1000.0, 1100.0, 1200.0],
            'B': [1000.0, 1050.0, 1100.0]
        }
        
        with self.assertLogs('core', level='INFO') as log:
            self.investment.otimizar_portfolio(estrategias, anos=1)
        
        # Verifica se fallback foi logado
        fallback_found = any("fallback" in message.lower() for message in log.output)
        self.assertTrue(fallback_found)
        
        # Verifica se erro original foi logado
        erro_found = any("Test failure" in message for message in log.output)
        self.assertTrue(erro_found)


if __name__ == '__main__':
    unittest.main()