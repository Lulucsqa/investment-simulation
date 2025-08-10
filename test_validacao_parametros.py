"""
Testes específicos para validação de parâmetros de entrada.

Este módulo testa todas as validações implementadas na classe OptimizedInvestment
para garantir que parâmetros inválidos são rejeitados com mensagens apropriadas.
"""

import unittest
import numpy as np
from core import OptimizedInvestment, ParametroInvalidoError, SimulacaoError


class TestValidacaoParametrosInicializacao(unittest.TestCase):
    """Testes para validação de parâmetros na inicialização."""
    
    def test_inflacao_valida(self):
        """Testa inicialização com inflação válida."""
        # Valores válidos devem funcionar
        investment = OptimizedInvestment(inflacao=6.0)
        self.assertEqual(investment.inflacao, 6.0)
        
        # Valores extremos válidos
        OptimizedInvestment(inflacao=-50.0)  # Deflação extrema
        OptimizedInvestment(inflacao=100.0)  # Hiperinflação
        OptimizedInvestment(inflacao=0.0)    # Inflação zero
    
    def test_inflacao_invalida(self):
        """Testa rejeição de inflação inválida."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao="6%")
        self.assertIn("Inflação deve ser um número", str(context.exception))
        
        # Valores infinitos
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=float('inf'))
        self.assertIn("Inflação deve ser um valor finito", str(context.exception))
        
        # Valores NaN
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=float('nan'))
        self.assertIn("Inflação deve ser um valor finito", str(context.exception))
        
        # Valores fora do range
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=-60.0)
        self.assertIn("Inflação deve estar entre -50% e 100%", str(context.exception))
        
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=150.0)
        self.assertIn("Inflação deve estar entre -50% e 100%", str(context.exception))
    
    def test_ir_renda_fixa_invalido(self):
        """Testa rejeição de IR de renda fixa inválido."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=6.0, ir_renda_fixa="15%")
        self.assertIn("Imposto de renda fixa deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=6.0, ir_renda_fixa=-5.0)
        self.assertIn("Imposto de renda fixa deve estar entre 0% e 100%", str(context.exception))
        
        # Valores acima de 100%
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=6.0, ir_renda_fixa=150.0)
        self.assertIn("Imposto de renda fixa deve estar entre 0% e 100%", str(context.exception))
    
    def test_ir_aluguel_invalido(self):
        """Testa rejeição de IR de aluguel inválido."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=6.0, ir_aluguel="27.5%")
        self.assertIn("Imposto de aluguel deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=6.0, ir_aluguel=-10.0)
        self.assertIn("Imposto de aluguel deve estar entre 0% e 100%", str(context.exception))
        
        # Valores acima de 100%
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=6.0, ir_aluguel=120.0)
        self.assertIn("Imposto de aluguel deve estar entre 0% e 100%", str(context.exception))


class TestValidacaoParametrosInvestimento(unittest.TestCase):
    """Testes para validação de parâmetros de investimento."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_aporte_inicial_invalido(self):
        """Testa rejeição de aporte inicial inválido."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi("1000", 100, 12.0, 1)
        self.assertIn("Aporte inicial do CDI deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(-1000.0, 100, 12.0, 1)
        self.assertIn("Aporte inicial do CDI não pode ser negativo", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(2e12, 100, 12.0, 1)
        self.assertIn("Aporte inicial do CDI é muito alto", str(context.exception))
        
        # Valores infinitos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(float('inf'), 100, 12.0, 1)
        self.assertIn("Aporte inicial do CDI deve ser um valor finito", str(context.exception))
    
    def test_aporte_mensal_invalido(self):
        """Testa rejeição de aporte mensal inválido."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, "100", 12.0, 1)
        self.assertIn("Aporte mensal do CDI deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, -100.0, 12.0, 1)
        self.assertIn("Aporte mensal do CDI não pode ser negativo", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 2e9, 12.0, 1)
        self.assertIn("Aporte mensal do CDI é muito alto", str(context.exception))
    
    def test_taxa_invalida(self):
        """Testa rejeição de taxa inválida."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, "12%", 1)
        self.assertIn("Taxa do CDI deve ser um número", str(context.exception))
        
        # Valores fora do range
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, -60.0, 1)
        self.assertIn("Taxa do CDI deve estar entre -50% e 200%", str(context.exception))
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, 250.0, 1)
        self.assertIn("Taxa do CDI deve estar entre -50% e 200%", str(context.exception))
    
    def test_anos_invalido(self):
        """Testa rejeição de período inválido."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, 12.0, "1 ano")
        self.assertIn("Período do CDI deve ser um número", str(context.exception))
        
        # Valores zero ou negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, 12.0, 0)
        self.assertIn("Período do CDI deve ser maior que zero", str(context.exception))
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, 12.0, -1)
        self.assertIn("Período do CDI deve ser maior que zero", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, 12.0, 150)
        self.assertIn("Período do CDI é muito longo", str(context.exception))


class TestValidacaoParametrosImovel(unittest.TestCase):
    """Testes para validação de parâmetros imobiliários."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_valor_imovel_invalido(self):
        """Testa rejeição de valor do imóvel inválido."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto("300000", 60000, 240, 12.0, 8.0, 2000)
        self.assertIn("Valor do imóvel deve ser um número", str(context.exception))
        
        # Valores zero ou negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(0, 60000, 240, 12.0, 8.0, 2000)
        self.assertIn("Valor do imóvel deve ser maior que zero", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(2e12, 60000, 240, 12.0, 8.0, 2000)
        self.assertIn("Valor do imóvel é muito alto", str(context.exception))
    
    def test_entrada_invalida(self):
        """Testa rejeição de entrada inválida."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, "60000", 240, 12.0, 8.0, 2000)
        self.assertIn("Entrada do imóvel deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, -10000, 240, 12.0, 8.0, 2000)
        self.assertIn("Entrada do imóvel não pode ser negativa", str(context.exception))
        
        # Entrada maior que valor do imóvel
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 350000, 240, 12.0, 8.0, 2000)
        self.assertIn("Entrada deve ser menor que o valor do imóvel", str(context.exception))
    
    def test_parcelas_invalidas(self):
        """Testa rejeição de número de parcelas inválido."""
        # Valores não inteiros
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240.5, 12.0, 8.0, 2000)
        self.assertIn("Número de parcelas deve ser um número inteiro", str(context.exception))
        
        # Valores zero ou negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 0, 12.0, 8.0, 2000)
        self.assertIn("Número de parcelas deve ser maior que zero", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 700, 12.0, 8.0, 2000)
        self.assertIn("Número de parcelas é muito alto", str(context.exception))
    
    def test_taxa_juros_invalida(self):
        """Testa rejeição de taxa de juros inválida."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, "12%", 8.0, 2000)
        self.assertIn("Taxa de juros deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, -5.0, 8.0, 2000)
        self.assertIn("Taxa de juros deve estar entre 0% e 50%", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, 60.0, 8.0, 2000)
        self.assertIn("Taxa de juros deve estar entre 0% e 50%", str(context.exception))
    
    def test_valorizacao_invalida(self):
        """Testa rejeição de taxa de valorização inválida."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, 12.0, "8%", 2000)
        self.assertIn("Taxa de valorização deve ser um número", str(context.exception))
        
        # Valores fora do range
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, 12.0, -60.0, 2000)
        self.assertIn("Taxa de valorização deve estar entre -50% e 100%", str(context.exception))
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, 12.0, 150.0, 2000)
        self.assertIn("Taxa de valorização deve estar entre -50% e 100%", str(context.exception))
    
    def test_aluguel_invalido(self):
        """Testa rejeição de valor de aluguel inválido."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, 12.0, 8.0, "2000")
        self.assertIn("Valor do aluguel deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, 12.0, 8.0, -500)
        self.assertIn("Valor do aluguel não pode ser negativo", str(context.exception))
        
        # Aluguel muito alto em relação ao valor do imóvel
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 60000, 240, 12.0, 8.0, 30000)
        self.assertIn("Valor do aluguel é muito alto em relação ao valor do imóvel", str(context.exception))
    
    def test_anos_construcao_invalido(self):
        """Testa rejeição de anos de construção inválidos."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_planta(300000, 60000, 240, 12.0, 8.0, 2000, "3 anos")
        self.assertIn("Anos de construção deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_planta(300000, 60000, 240, 12.0, 8.0, 2000, -1)
        self.assertIn("Anos de construção não pode ser negativo", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_planta(300000, 60000, 240, 12.0, 8.0, 2000, 15)
        self.assertIn("Anos de construção é muito alto", str(context.exception))


class TestValidacaoParametrosEstrategiaMista(unittest.TestCase):
    """Testes para validação de parâmetros da estratégia mista."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_taxa_cdi_invalida(self):
        """Testa rejeição de taxa CDI inválida na estratégia mista."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_e_renda_fixa(300000, 60000, 240, 12.0, "10%", 500, 8.0)
        self.assertIn("Taxa CDI deve ser um número", str(context.exception))
        
        # Valores fora do range
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_e_renda_fixa(300000, 60000, 240, 12.0, -60.0, 500, 8.0)
        self.assertIn("Taxa CDI deve estar entre -50% e 200%", str(context.exception))
    
    def test_aporte_mensal_estrategia_mista_invalido(self):
        """Testa rejeição de aporte mensal inválido na estratégia mista."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_e_renda_fixa(300000, 60000, 240, 12.0, 10.0, "500", 8.0)
        self.assertIn("Aporte mensal deve ser um número", str(context.exception))
        
        # Valores negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_e_renda_fixa(300000, 60000, 240, 12.0, 10.0, -500, 8.0)
        self.assertIn("Aporte mensal não pode ser negativo", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_e_renda_fixa(300000, 60000, 240, 12.0, 10.0, 2e9, 8.0)
        self.assertIn("Aporte mensal é muito alto", str(context.exception))


class TestValidacaoParametrosOtimizacao(unittest.TestCase):
    """Testes para validação de parâmetros de otimização."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
        # Estratégias válidas para testes
        self.estrategias_validas = {
            'CDI': [1000, 1100, 1200, 1300, 1400],
            'IPCA+': [1000, 1050, 1100, 1150, 1200]
        }
    
    def test_estrategias_vazias(self):
        """Testa rejeição de estratégias vazias."""
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio({}, 1)
        self.assertIn("Deve haver pelo menos uma estratégia", str(context.exception))
    
    def test_anos_otimizacao_invalido(self):
        """Testa rejeição de período inválido na otimização."""
        # Valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, "1 ano")
        self.assertIn("Período deve ser um número", str(context.exception))
        
        # Valores zero ou negativos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 0)
        self.assertIn("Período deve ser maior que zero", str(context.exception))
        
        # Valores muito altos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 150)
        self.assertIn("Período é muito longo", str(context.exception))
    
    def test_estrategias_com_historico_vazio(self):
        """Testa rejeição de estratégias com histórico vazio."""
        estrategias_invalidas = {
            'CDI': [1000, 1100, 1200],
            'IPCA+': []  # Histórico vazio
        }
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(estrategias_invalidas, 1)
        self.assertIn("Estratégia 'IPCA+' tem histórico vazio", str(context.exception))
    
    def test_estrategias_com_valores_nao_numericos(self):
        """Testa rejeição de estratégias com valores não numéricos."""
        estrategias_invalidas = {
            'CDI': [1000, "1100", 1200],  # Valor não numérico
            'IPCA+': [1000, 1050, 1100]
        }
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(estrategias_invalidas, 1)
        self.assertIn("Estratégia 'CDI' contém valores não numéricos", str(context.exception))
    
    def test_estrategias_com_valores_infinitos(self):
        """Testa rejeição de estratégias com valores infinitos."""
        estrategias_invalidas = {
            'CDI': [1000, float('inf'), 1200],  # Valor infinito
            'IPCA+': [1000, 1050, 1100]
        }
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(estrategias_invalidas, 1)
        self.assertIn("Estratégia 'CDI' contém valor inválido na posição 1", str(context.exception))
    
    def test_estrategias_com_tamanhos_diferentes(self):
        """Testa rejeição de estratégias com períodos diferentes."""
        estrategias_invalidas = {
            'CDI': [1000, 1100, 1200, 1300],  # 4 meses
            'IPCA+': [1000, 1050, 1100]       # 3 meses
        }
        
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(estrategias_invalidas, 1)
        self.assertIn("Todas as estratégias devem ter o mesmo período", str(context.exception))
    
    def test_aporte_bounds_invalido(self):
        """Testa rejeição de bounds de aporte inválidos."""
        # Bounds não fornecidos quando necessários
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 1, optimize_aportes=True)
        self.assertIn("aporte_bounds é obrigatório quando optimize_aportes=True", str(context.exception))
        
        # Bounds com formato inválido
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 1, optimize_aportes=True, aporte_bounds=(1000,))
        self.assertIn("aporte_bounds deve ser uma tupla com 2 elementos", str(context.exception))
        
        # Bounds com valores não numéricos
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 1, optimize_aportes=True, aporte_bounds=("1000", 5000))
        self.assertIn("Bounds de aporte devem ser números", str(context.exception))
        
        # Aporte mínimo negativo
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 1, optimize_aportes=True, aporte_bounds=(-1000, 5000))
        self.assertIn("Aporte mínimo não pode ser negativo", str(context.exception))
        
        # Aporte máximo menor que mínimo
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 1, optimize_aportes=True, aporte_bounds=(5000, 1000))
        self.assertIn("Aporte máximo deve ser maior que o mínimo", str(context.exception))
        
        # Aporte máximo muito alto
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio(self.estrategias_validas, 1, optimize_aportes=True, aporte_bounds=(1000, 2e12))
        self.assertIn("Aporte máximo é muito alto", str(context.exception))


class TestValidacaoMensagensErro(unittest.TestCase):
    """Testes para verificar se as mensagens de erro são informativas."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0)
    
    def test_mensagens_erro_especificas_por_investimento(self):
        """Testa se mensagens de erro incluem o tipo de investimento."""
        # CDI
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(-1000, 100, 12.0, 1)
        self.assertIn("CDI", str(context.exception))
        
        # IPCA+
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_ipca(-1000, 100, 6.0, 1)
        self.assertIn("IPCA+", str(context.exception))
    
    def test_mensagens_erro_incluem_valores_limites(self):
        """Testa se mensagens de erro incluem valores limites."""
        # Inflação fora do range
        with self.assertRaises(ParametroInvalidoError) as context:
            OptimizedInvestment(inflacao=150.0)
        self.assertIn("-50% e 100%", str(context.exception))
        
        # Taxa fora do range
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.investimento_cdi(1000, 100, 250.0, 1)
        self.assertIn("-50% e 200%", str(context.exception))
    
    def test_mensagens_erro_incluem_contexto(self):
        """Testa se mensagens de erro incluem contexto suficiente."""
        # Entrada maior que valor do imóvel
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.compra_financiada_pronto(300000, 350000, 240, 12.0, 8.0, 2000)
        mensagem = str(context.exception)
        self.assertIn("Entrada", mensagem)
        self.assertIn("valor do imóvel", mensagem)
        
        # Estratégia com histórico vazio
        with self.assertRaises(ParametroInvalidoError) as context:
            self.investment.otimizar_portfolio({'CDI': []}, 1)
        mensagem = str(context.exception)
        self.assertIn("CDI", mensagem)
        self.assertIn("histórico vazio", mensagem)


if __name__ == '__main__':
    unittest.main()