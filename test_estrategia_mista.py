"""
Testes de integração para a estratégia mista (compra_e_renda_fixa).

Testa a funcionalidade que combina financiamento imobiliário com investimento em CDI.
"""

import unittest
from core import OptimizedInvestment


class TestEstrategiaMista(unittest.TestCase):
    """Testes de integração para estratégia mista."""
    
    def setUp(self):
        """Configura instância para testes."""
        self.investment = OptimizedInvestment(inflacao=6.0, ir_renda_fixa=15)
    
    def test_estrategia_mista_basica(self):
        """Testa funcionamento básico da estratégia mista."""
        historico = self.investment.compra_e_renda_fixa(
            valor_imovel=300000.0,
            entrada=60000.0,  # 20%
            parcelas=240,  # 20 anos
            taxa_juros=12.0,
            taxa_cdi=13.0,
            aporte_mensal=1000.0,
            valorizacao=8.0
        )
        
        # Deve ter 240 meses de histórico
        self.assertEqual(len(historico), 240)
        
        # Todos os valores devem ser numéricos
        for valor in historico:
            self.assertIsInstance(valor, (int, float))
        
        # Patrimônio deve crescer ao longo do tempo
        self.assertGreater(historico[-1], historico[0])
    
    def test_patrimonio_total_combinado(self):
        """Testa se patrimônio total combina imóvel + renda fixa."""
        # Cenário simplificado para validação
        investment_sem_inflacao = OptimizedInvestment(inflacao=0.0, ir_renda_fixa=15)
        
        historico = investment_sem_inflacao.compra_e_renda_fixa(
            valor_imovel=200000.0,
            entrada=40000.0,  # 20%
            parcelas=12,  # 1 ano
            taxa_juros=12.0,
            taxa_cdi=12.0,
            aporte_mensal=500.0,
            valorizacao=0.0  # Sem valorização para simplificar
        )
        
        # Valor final deve incluir:
        # 1. Patrimônio do imóvel (valor - saldo devedor - entrada)
        # 2. Saldo da renda fixa (aportes + rendimentos)
        
        # Com 12 aportes de R$ 500 e rendimento de CDI, 
        # saldo renda fixa deve ser > R$ 6.000
        # Patrimônio total deve ser significativo
        self.assertGreater(historico[-1], 150000.0)
    
    def test_rendimento_renda_fixa_com_imposto(self):
        """Testa se imposto é aplicado corretamente na renda fixa."""
        # Compara com IR de 15% vs 0%
        investment_sem_ir = OptimizedInvestment(inflacao=6.0, ir_renda_fixa=0.0)
        
        params = {
            'valor_imovel': 200000.0,
            'entrada': 40000.0,
            'parcelas': 60,
            'taxa_juros': 10.0,
            'taxa_cdi': 14.0,
            'aporte_mensal': 800.0,
            'valorizacao': 6.0
        }
        
        historico_com_ir = self.investment.compra_e_renda_fixa(**params)
        historico_sem_ir = investment_sem_ir.compra_e_renda_fixa(**params)
        
        # Patrimônio sem IR deve ser maior (mais rendimento líquido na renda fixa)
        self.assertGreater(historico_sem_ir[-1], historico_com_ir[-1])
    
    def test_aportes_mensais_acumulacao(self):
        """Testa acumulação correta dos aportes mensais."""
        historico = self.investment.compra_e_renda_fixa(
            valor_imovel=150000.0,
            entrada=30000.0,
            parcelas=24,  # 2 anos
            taxa_juros=11.0,
            taxa_cdi=0.0,  # Sem rendimento para isolar aportes
            aporte_mensal=1000.0,
            valorizacao=0.0  # Sem valorização
        )
        
        # Com 24 aportes de R$ 1.000, deve haver pelo menos R$ 24.000 na renda fixa
        # (considerando que não há rendimento, apenas acumulação)
        # Patrimônio total deve refletir essa acumulação
        self.assertGreater(historico[-1], 100000.0)
    
    def test_valorizacao_imovel_impacto(self):
        """Testa impacto da valorização do imóvel no patrimônio total."""
        # Compara cenários com e sem valorização
        params_base = {
            'valor_imovel': 200000.0,
            'entrada': 40000.0,
            'parcelas': 120,
            'taxa_juros': 10.0,
            'taxa_cdi': 12.0,
            'aporte_mensal': 600.0
        }
        
        historico_sem_valorizacao = self.investment.compra_e_renda_fixa(
            **params_base, valorizacao=0.0
        )
        
        historico_com_valorizacao = self.investment.compra_e_renda_fixa(
            **params_base, valorizacao=8.0
        )
        
        # Valorização deve aumentar significativamente o patrimônio
        self.assertGreater(
            historico_com_valorizacao[-1], 
            historico_sem_valorizacao[-1] * 1.5
        )
    
    def test_comparacao_com_estrategias_puras(self):
        """Compara estratégia mista com estratégias puras."""
        # Simula apenas CDI com valor equivalente à entrada
        historico_cdi_puro = self.investment.investimento_cdi(
            aporte_inicial=60000.0,  # Valor da entrada
            aporte_mensal=1000.0,
            taxa_cdi=13.0,
            anos=10,
            imposto_final=False
        )
        
        # Simula estratégia mista
        historico_misto = self.investment.compra_e_renda_fixa(
            valor_imovel=300000.0,
            entrada=60000.0,
            parcelas=120,  # 10 anos
            taxa_juros=12.0,
            taxa_cdi=13.0,
            aporte_mensal=1000.0,
            valorizacao=8.0
        )
        
        # Estratégia mista deve superar CDI puro devido ao imóvel
        self.assertGreater(historico_misto[-1], historico_cdi_puro[-1])
    
    def test_cenario_taxa_cdi_baixa(self):
        """Testa estratégia mista com taxa CDI baixa."""
        historico = self.investment.compra_e_renda_fixa(
            valor_imovel=250000.0,
            entrada=50000.0,
            parcelas=180,
            taxa_juros=12.0,
            taxa_cdi=8.0,  # CDI baixo
            aporte_mensal=800.0,
            valorizacao=7.0
        )
        
        # Mesmo com CDI baixo, estratégia deve funcionar
        self.assertEqual(len(historico), 180)
        self.assertGreater(historico[-1], historico[0])
    
    def test_cenario_taxa_cdi_alta(self):
        """Testa estratégia mista com taxa CDI alta."""
        historico = self.investment.compra_e_renda_fixa(
            valor_imovel=250000.0,
            entrada=50000.0,
            parcelas=180,
            taxa_juros=12.0,
            taxa_cdi=18.0,  # CDI alto
            aporte_mensal=800.0,
            valorizacao=7.0
        )
        
        # Com CDI alto, patrimônio final deve ser maior
        self.assertGreater(historico[-1], 200000.0)
    
    def test_aporte_mensal_zero(self):
        """Testa estratégia mista sem aportes mensais."""
        historico = self.investment.compra_e_renda_fixa(
            valor_imovel=200000.0,
            entrada=40000.0,
            parcelas=120,
            taxa_juros=11.0,
            taxa_cdi=13.0,
            aporte_mensal=0.0,  # Sem aportes
            valorizacao=6.0
        )
        
        # Sem aportes, patrimônio vem apenas do imóvel
        self.assertEqual(len(historico), 120)
        # Deve ainda haver crescimento pela valorização e amortização
        self.assertGreater(historico[-1], historico[0])
    
    def test_entrada_alta_impacto(self):
        """Testa impacto de entrada alta na estratégia mista."""
        # Compara entrada baixa vs alta
        params_base = {
            'valor_imovel': 300000.0,
            'parcelas': 240,
            'taxa_juros': 12.0,
            'taxa_cdi': 13.0,
            'aporte_mensal': 1000.0,
            'valorizacao': 8.0
        }
        
        historico_entrada_baixa = self.investment.compra_e_renda_fixa(
            **params_base, entrada=30000.0  # 10%
        )
        
        historico_entrada_alta = self.investment.compra_e_renda_fixa(
            **params_base, entrada=90000.0  # 30%
        )
        
        # Entrada alta reduz financiamento, pode afetar patrimônio inicial
        # Mas ambos devem crescer ao longo do tempo
        self.assertGreater(historico_entrada_baixa[-1], historico_entrada_baixa[0])
        self.assertGreater(historico_entrada_alta[-1], historico_entrada_alta[0])
    
    def test_periodo_longo_estrategia_mista(self):
        """Testa estratégia mista com período longo."""
        historico = self.investment.compra_e_renda_fixa(
            valor_imovel=400000.0,
            entrada=80000.0,
            parcelas=360,  # 30 anos
            taxa_juros=11.0,
            taxa_cdi=12.0,
            aporte_mensal=1200.0,
            valorizacao=7.0
        )
        
        # Deve ter 360 meses
        self.assertEqual(len(historico), 360)
        
        # Com período longo, juros compostos devem gerar patrimônio significativo
        self.assertGreater(historico[-1], 500000.0)
    
    def test_consistencia_calculo_mensal(self):
        """Testa consistência dos cálculos mês a mês."""
        historico = self.investment.compra_e_renda_fixa(
            valor_imovel=200000.0,
            entrada=40000.0,
            parcelas=36,  # 3 anos
            taxa_juros=12.0,
            taxa_cdi=13.0,
            aporte_mensal=500.0,
            valorizacao=6.0
        )
        
        # Patrimônio deve crescer de forma consistente (sem grandes saltos)
        for i in range(1, len(historico)):
            # Variação mensal não deve ser extrema
            variacao = abs(historico[i] - historico[i-1])
            self.assertLess(variacao, 50000.0)  # Variação máxima razoável
        
        # Tendência geral deve ser crescente
        crescimento_total = historico[-1] - historico[0]
        self.assertGreater(crescimento_total, 0)


if __name__ == '__main__':
    unittest.main()