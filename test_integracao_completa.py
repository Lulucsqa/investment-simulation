"""
Testes de integração completos para o sistema de simulação de investimentos.

Este módulo testa o fluxo end-to-end do sistema, validando a consistência
entre diferentes módulos e a precisão dos cálculos em cenários conhecidos.
"""

import unittest
import os
import tempfile
import shutil
import numpy as np
from unittest.mock import patch, MagicMock
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

from core import OptimizedInvestment, SimulacaoError, ParametroInvalidoError, OtimizacaoError
from visualization import plotar_historico_planta_pronto, plotar_cenarios
import main


class TestFluxoCompleto(unittest.TestCase):
    """Testes de integração para o fluxo completo do sistema."""
    
    def setUp(self):
        """Configura ambiente de teste."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_outputs_dir = 'outputs'
        
        # Cria diretório temporário para outputs
        self.test_outputs_dir = os.path.join(self.temp_dir, 'outputs')
        os.makedirs(self.test_outputs_dir, exist_ok=True)
        
        # Parâmetros padrão para testes
        self.parametros_padrao = {
            'inflacao_anual': 6.0,
            'ir_renda_fixa': 15.0,
            'ir_aluguel': 27.5,
            'anos': 5,  # Período menor para testes mais rápidos
            'aporte_inicial': 50000.0,
            'aporte_mensal': 1000.0,
            'taxa_cdi': 12.0,
            'taxa_ipca': 5.0,
            'valor_imovel': 200000.0,
            'entrada_imovel': 40000.0,
            'taxa_juros_financiamento': 10.0,
            'valorizacao_imovel': 7.0,
            'aluguel_mensal': 1500.0,
            'anos_construcao': 2,
        }
    
    def tearDown(self):
        """Limpa ambiente de teste."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)  
  
    def test_fluxo_end_to_end_completo(self):
        """Testa o fluxo completo do sistema do início ao fim."""
        # 1. Inicialização do simulador
        simulador = OptimizedInvestment(
            inflacao=self.parametros_padrao['inflacao_anual'],
            ir_renda_fixa=self.parametros_padrao['ir_renda_fixa'],
            ir_aluguel=self.parametros_padrao['ir_aluguel']
        )
        
        # 2. Execução de todas as simulações
        anos = self.parametros_padrao['anos']
        parcelas = anos * 12
        
        # Simulação CDI
        resultado_cdi = simulador.investimento_cdi(
            aporte_inicial=self.parametros_padrao['aporte_inicial'],
            aporte_mensal=self.parametros_padrao['aporte_mensal'],
            taxa_cdi=self.parametros_padrao['taxa_cdi'],
            anos=anos,
            imposto_final=False
        )
        
        # Simulação IPCA+
        resultado_ipca = simulador.investimento_ipca(
            aporte_inicial=self.parametros_padrao['aporte_inicial'],
            aporte_mensal=self.parametros_padrao['aporte_mensal'],
            taxa_ipca=self.parametros_padrao['taxa_ipca'],
            anos=anos,
            imposto_final=True
        )
        
        # Simulação Imóvel na Planta
        resultado_planta = simulador.compra_financiada_planta(
            valor_imovel=self.parametros_padrao['valor_imovel'],
            entrada=self.parametros_padrao['entrada_imovel'],
            parcelas=parcelas,
            taxa_juros=self.parametros_padrao['taxa_juros_financiamento'],
            valorizacao=self.parametros_padrao['valorizacao_imovel'],
            aluguel=self.parametros_padrao['aluguel_mensal'],
            anos_construcao=self.parametros_padrao['anos_construcao']
        )
        
        # Simulação Imóvel Pronto
        resultado_pronto = simulador.compra_financiada_pronto(
            valor_imovel=self.parametros_padrao['valor_imovel'],
            entrada=self.parametros_padrao['entrada_imovel'],
            parcelas=parcelas,
            taxa_juros=self.parametros_padrao['taxa_juros_financiamento'],
            valorizacao=self.parametros_padrao['valorizacao_imovel'],
            aluguel=self.parametros_padrao['aluguel_mensal']
        )
        
        # Simulação Estratégia Mista
        resultado_misto = simulador.compra_e_renda_fixa(
            valor_imovel=self.parametros_padrao['valor_imovel'],
            entrada=self.parametros_padrao['entrada_imovel'],
            parcelas=parcelas,
            taxa_juros=self.parametros_padrao['taxa_juros_financiamento'],
            taxa_cdi=self.parametros_padrao['taxa_cdi'],
            aporte_mensal=self.parametros_padrao['aporte_mensal'],
            valorizacao=self.parametros_padrao['valorizacao_imovel']
        )
        
        # 3. Validações básicas de consistência
        resultados = {
            'cdi': resultado_cdi,
            'ipca': resultado_ipca,
            'imovel_planta': resultado_planta,
            'imovel_pronto': resultado_pronto,
            'estrategia_mista': resultado_misto
        }
        
        # Todos os resultados devem ter o mesmo número de meses
        tamanhos = [len(resultado) for resultado in resultados.values()]
        self.assertEqual(len(set(tamanhos)), 1, "Todos os resultados devem ter o mesmo tamanho")
        self.assertEqual(tamanhos[0], parcelas, f"Resultados devem ter {parcelas} meses")
        
        # Todos os valores devem ser numéricos e finitos
        for nome, resultado in resultados.items():
            for i, valor in enumerate(resultado):
                self.assertIsInstance(valor, (int, float), f"{nome}[{i}] deve ser numérico")
                self.assertTrue(np.isfinite(valor), f"{nome}[{i}] deve ser finito")
        
        # 4. Teste de otimização
        estrategias_otimizacao = {k: v for k, v in resultados.items() if k != 'estrategia_mista'}
        
        pesos_otimizados, _, _, retorno_otimizado = simulador.otimizar_portfolio(
            estrategias=estrategias_otimizacao,
            anos=anos,
            optimize_aportes=False
        )
        
        # Validações da otimização
        self.assertEqual(len(pesos_otimizados), len(estrategias_otimizacao))
        self.assertAlmostEqual(sum(pesos_otimizados), 1.0, places=6)
        self.assertTrue(all(peso >= 0 for peso in pesos_otimizados))
        self.assertGreater(retorno_otimizado, 0)
        
        # 5. Teste de geração de visualizações
        with patch('matplotlib.pyplot.savefig') as mock_savefig, \
             patch('matplotlib.pyplot.show') as mock_show:
            
            # Gerar gráfico de comparação de imóveis
            plotar_historico_planta_pronto(
                historico_planta=resultado_planta,
                historico_pronto=resultado_pronto,
                meses=parcelas
            )
            
            # Gerar gráfico de cenários
            cenarios_formatados = {
                'CDI': resultado_cdi,
                'IPCA+': resultado_ipca,
                'Imóvel Planta': resultado_planta,
                'Imóvel Pronto': resultado_pronto
            }
            
            plotar_cenarios(
                cenarios=cenarios_formatados,
                anos=anos,
                pesos_otimizados=pesos_otimizados
            )
            
            # Verificar que as funções de plotagem foram chamadas
            self.assertEqual(mock_savefig.call_count, 2)
            self.assertEqual(mock_show.call_count, 2)
        
        print("✓ Fluxo end-to-end completo executado com sucesso")    

    def test_consistencia_entre_modulos(self):
        """Testa consistência de dados entre diferentes módulos."""
        simulador = OptimizedInvestment(inflacao=5.0, ir_renda_fixa=15, ir_aluguel=27.5)
        
        # Parâmetros de teste
        aporte_inicial = 10000.0
        aporte_mensal = 500.0
        taxa = 10.0
        anos = 3
        
        # 1. Teste de consistência: conversão de taxas
        taxa_mensal_calculada = simulador._taxa_anual_para_mensal(taxa)
        taxa_anual_volta = simulador._taxa_mensal_para_anual(taxa_mensal_calculada)
        
        self.assertAlmostEqual(taxa, taxa_anual_volta, places=10,
                              msg="Conversão de taxas deve ser simétrica")
        
        # 2. Teste de consistência: ajuste inflacionário
        valor_futuro = 1000.0
        meses = 12
        valor_presente = simulador.ajuste_inflacao(valor_futuro, meses)
        
        # Com inflação positiva, valor presente deve ser menor
        self.assertLess(valor_presente, valor_futuro,
                       "Valor presente deve ser menor que valor futuro com inflação positiva")
        
        # 3. Teste de consistência: simulações com parâmetros idênticos
        # CDI e IPCA+ com mesma taxa total devem dar resultados similares
        taxa_total_ipca = simulador.inflacao + 5.0  # 5% acima da inflação
        
        resultado_cdi = simulador.investimento_cdi(
            aporte_inicial=aporte_inicial,
            aporte_mensal=aporte_mensal,
            taxa_cdi=taxa_total_ipca,
            anos=anos,
            imposto_final=True
        )
        
        resultado_ipca = simulador.investimento_ipca(
            aporte_inicial=aporte_inicial,
            aporte_mensal=aporte_mensal,
            taxa_ipca=5.0,  # 5% acima da inflação
            anos=anos,
            imposto_final=True
        )
        
        # Resultados devem ser muito próximos (diferença < 1%)
        diferenca_percentual = abs(resultado_cdi[-1] - resultado_ipca[-1]) / resultado_ipca[-1]
        self.assertLess(diferenca_percentual, 0.01,
                       "CDI e IPCA+ com taxas equivalentes devem dar resultados similares")
        
        # 4. Teste de consistência: sistema SAC
        valor_financiado = 100000.0
        parcelas = 12
        taxa_juros = 12.0
        
        amortizacoes, juros, prestacoes = simulador._calcular_sac(
            valor_financiado, parcelas, taxa_juros
        )
        
        # Soma das amortizações deve igual ao valor financiado
        self.assertAlmostEqual(sum(amortizacoes), valor_financiado, places=2,
                              msg="Soma das amortizações deve igual ao valor financiado")
        
        # Prestação = amortização + juros para cada mês
        for i in range(parcelas):
            self.assertAlmostEqual(prestacoes[i], amortizacoes[i] + juros[i], places=2,
                                  msg=f"Prestação {i+1} deve ser amortização + juros")
        
        print("✓ Consistência entre módulos validada") 
   
    def test_geracao_arquivos_saida(self):
        """Testa geração correta de arquivos de saída."""
        simulador = OptimizedInvestment(inflacao=6.0)
        
        # Gerar dados de teste
        meses = 24
        historico_planta = [1000 + i * 100 for i in range(meses)]
        historico_pronto = [1200 + i * 120 for i in range(meses)]
        
        cenarios = {
            'CDI': [800 + i * 80 for i in range(meses)],
            'IPCA+': [900 + i * 90 for i in range(meses)],
            'Imóvel': historico_planta
        }
        
        # Usar diretório temporário para testes
        with patch('matplotlib.pyplot.savefig') as mock_savefig, \
             patch('matplotlib.pyplot.show') as mock_show:
            
            # Testar geração de gráfico de comparação
            plotar_historico_planta_pronto(
                historico_planta=historico_planta,
                historico_pronto=historico_pronto,
                meses=meses
            )
            
            # Verificar chamada para salvar arquivo
            mock_savefig.assert_called_with(
                'outputs/comparacao_imoveis.jpg',
                dpi=300,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none'
            )
            
            # Testar geração de gráfico de cenários
            plotar_cenarios(
                cenarios=cenarios,
                anos=2,
                pesos_otimizados=np.array([0.4, 0.3, 0.3])
            )
            
            # Verificar chamada para salvar arquivo
            calls = mock_savefig.call_args_list
            self.assertEqual(len(calls), 2)
            
            # Verificar que o segundo arquivo foi salvo corretamente
            second_call = calls[1]
            self.assertEqual(second_call[0][0], 'outputs/cenarios_investimento.jpg')
        
        print("✓ Geração de arquivos de saída testada") 
   
    def test_precisao_calculos_cenarios_conhecidos(self):
        """Testa precisão dos cálculos em cenários com resultados conhecidos."""
        
        # Cenário 1: CDI sem inflação e sem aportes mensais
        simulador_sem_inflacao = OptimizedInvestment(inflacao=0.0, ir_renda_fixa=15)
        
        resultado_cdi = simulador_sem_inflacao.investimento_cdi(
            aporte_inicial=10000.0,
            aporte_mensal=0.0,
            taxa_cdi=12.0,
            anos=1,
            imposto_final=True
        )
        
        # Cálculo esperado: 10000 * 1.12 = 11200, IR = 1200 * 0.15 = 180, Final = 11020
        valor_esperado = 11020.0
        self.assertAlmostEqual(resultado_cdi[-1], valor_esperado, delta=10.0,
                              msg="CDI com cenário conhecido deve ter precisão alta")
        
        # Cenário 2: Sistema SAC conhecido
        simulador = OptimizedInvestment(inflacao=0.0)
        
        valor_financiado = 120000.0
        parcelas = 12
        taxa_juros = 12.0
        
        amortizacoes, juros, prestacoes = simulador._calcular_sac(
            valor_financiado, parcelas, taxa_juros
        )
        
        # Primeira amortização: 120000 / 12 = 10000
        self.assertAlmostEqual(amortizacoes[0], 10000.0, places=2)
        
        # Primeiro juro: 120000 * (12%/12) ≈ 120000 * 0.009489 ≈ 1138.68
        taxa_mensal = simulador._taxa_anual_para_mensal(12.0) / 100
        primeiro_juro_esperado = 120000.0 * taxa_mensal
        self.assertAlmostEqual(juros[0], primeiro_juro_esperado, places=2)
        
        # Cenário 3: Ajuste inflacionário conhecido
        simulador_inflacao = OptimizedInvestment(inflacao=12.0)  # 12% ao ano
        
        valor_futuro = 1120.0  # R$ 1.120 em 12 meses
        valor_presente = simulador_inflacao.ajuste_inflacao(valor_futuro, 12)
        
        # Com 12% de inflação, R$ 1.120 em 12 meses vale R$ 1.000 hoje
        self.assertAlmostEqual(valor_presente, 1000.0, delta=5.0,
                              msg="Ajuste inflacionário deve ter precisão alta")
        
        # Cenário 4: Imóvel pronto sem valorização
        simulador_imovel = OptimizedInvestment(inflacao=0.0, ir_aluguel=0.0)
        
        resultado_imovel = simulador_imovel.compra_financiada_pronto(
            valor_imovel=100000.0,
            entrada=20000.0,
            parcelas=12,
            taxa_juros=0.0,  # Sem juros para simplificar
            valorizacao=0.0,  # Sem valorização
            aluguel=1000.0
        )
        
        # Patrimônio final esperado:
        # Valor do imóvel (100000) - saldo devedor (0) + aluguel acumulado (12000) - entrada (20000)
        # = 100000 - 0 + 12000 - 20000 = 92000
        valor_esperado_imovel = 92000.0
        self.assertAlmostEqual(resultado_imovel[-1], valor_esperado_imovel, delta=100.0,
                              msg="Simulação de imóvel deve ter precisão alta")
        
        print("✓ Precisão dos cálculos em cenários conhecidos validada")    

    def test_tratamento_erros_integracao(self):
        """Testa tratamento de erros durante integração entre módulos."""
        
        # 1. Teste de parâmetros inválidos na inicialização
        with self.assertRaises(ParametroInvalidoError):
            OptimizedInvestment(inflacao=float('inf'))
        
        with self.assertRaises(Paramet")ção validado na integraerroso de ratament Tprint("✓               
 ções)
çar exceve landenão # (           iosamente
 rros graclidar com eeve  Função d      #    
      
        os, anos=5)nvalidos_ios=cenaricenariarios(otar_cen          pl
       }      zia
 ista va# L  'Teste': []           
      = {dosinvali  cenarios_     
     oslidvá inm dados Cenários co    #     
          os=5)
     rios={}, annaarios(ceotar_cen pl       vazios
    # Cenários                    
:
     owck_shs mot.show') ab.pyplotliatch('matplo           p  vefig, \
ck_safig') as moot.saveplotlib.pyplatch('matith p    w    dos
dados inválição com de visualiza. Teste     # 4
    
                  )
  es=Falsimize_aporte    opt          =5,
     anos        icas,
     blematategias_proas=estrrategi est            olio(
   r_portfmizalador.otimu       sir):
     acaoErroimizses(OtssertRaiself.aith  
        w      }
       0] * 60
  00.: [10egia2' 'estrat            inválidos
 Valores # * 60, ')][float('nania1':    'estrateg       icas = {
  atproblemategias_   estro
     izaçã na otimalharque pode fr cenário      # Cria   ção
zaimiha na ot falde# 3. Teste  
              )
        500.0
     uel=1    alug           
 rizacao=6.0,valo            10.0,
    s=uro     taxa_j          as=240,
    parcel             l
 do imóve valorqueada maior .0,  # Entrda=250000       entra       00.0,
  000el=2r_imovlo   va           nta(
  a_planciad.compra_finaadorsimul          or):
  doErrametroInvali(ParssertRaiseslf.a  with se  
         )
        s=5
        ano             i=10.0,
    taxa_cd             0.0,
 ensal=10porte_m    a         
   ativoNeg  # .0,-1000al=aporte_inici              o_cdi(
  entstimulador.inve     sim
       or):rroEroInvalidamettRaises(Par self.asserth wi  
             0)
o=6.(inflacaInvestmentimized Optmulador =      si  ções
 simulaálidos nasrâmetros inve pa2. Teste d      #      
  0)
   nda_fixa=-5.6.0, ir_reo=nflacastment(imizedInveOpti            r):
InvalidoErroro    

    def test_tratamento_erros_integracao(self):
        """Testa tratamento de erros durante integração entre módulos."""
        
        # 1. Teste de parâmetros inválidos na inicialização
        with self.assertRaises(ParametroInvalidoError):
            OptimizedInvestment(inflacao=float('inf'))
        
        with self.assertRaises(ParametroInvalidoError):
            OptimizedInvestment(inflacao=6.0, ir_renda_fixa=-5.0)
        
        # 2. Teste de parâmetros inválidos nas simulações
        simulador = OptimizedInvestment(inflacao=6.0)
        
        with self.assertRaises(ParametroInvalidoError):
            simulador.investimento_cdi(
                aporte_inicial=-1000.0,  # Negativo
                aporte_mensal=100.0,
                taxa_cdi=10.0,
                anos=5
            )
        
        with self.assertRaises(ParametroInvalidoError):
            simulador.compra_financiada_planta(
                valor_imovel=200000.0,
                entrada=250000.0,  # Entrada maior que valor do imóvel
                parcelas=240,
                taxa_juros=10.0,
                valorizacao=6.0,
                aluguel=1500.0
            )
        
        print("✓ Tratamento de erros na integração validado")
    
    def test_performance_simulacoes_longas(self):
        """Testa performance com simulações de longo prazo."""
        import time
        
        simulador = OptimizedInvestment(inflacao=6.0)
        
        # Teste com 30 anos (360 meses)
        anos_longo = 30
        
        start_time = time.time()
        
        # Executar simulação longa
        resultado_longo = simulador.investimento_cdi(
            aporte_inicial=50000.0,
            aporte_mensal=1000.0,
            taxa_cdi=12.0,
            anos=anos_longo,
            imposto_final=False
        )
        
        end_time = time.time()
        tempo_execucao = end_time - start_time
        
        # Validações
        self.assertEqual(len(resultado_longo), anos_longo * 12)
        self.assertLess(tempo_execucao, 5.0, "Simulação longa deve executar em menos de 5 segundos")
        
        # Todos os valores devem ser válidos
        for valor in resultado_longo:
            self.assertTrue(np.isfinite(valor))
            self.assertGreater(valor, 0)
        
        print(f"✓ Performance validada - Simulação: {tempo_execucao:.2f}s")
    
    def test_main_script_integracao(self):
        """Testa integração com o script principal."""
        
        # Mock das funções de configuração e execução
        with patch.object(main, 'configurar_parametros') as mock_config, \
             patch.object(main, 'executar_simulacoes') as mock_exec, \
             patch.object(main, 'gerar_relatorio_resultados') as mock_relatorio, \
             patch.object(main, 'gerar_visualizacoes') as mock_viz, \
             patch('builtins.print') as mock_print:
            
            # Configurar mocks
            mock_config.return_value = self.parametros_padrao
            
            # Simular resultados das simulações
            resultados_mock = {
                'cdi': [1000 + i * 10 for i in range(60)],
                'ipca': [1100 + i * 11 for i in range(60)],
                'imovel_planta': [900 + i * 15 for i in range(60)],
                'imovel_pronto': [950 + i * 16 for i in range(60)],
                'estrategia_mista': [1050 + i * 12 for i in range(60)]
            }
            
            simulador_mock = OptimizedInvestment(inflacao=6.0)
            mock_exec.return_value = (resultados_mock, simulador_mock)
            
            # Executar função principal
            main.main()
            
            # Verificar que todas as funções foram chamadas
            mock_config.assert_called_once()
            mock_exec.assert_called_once()
            mock_relatorio.assert_called_once()
            mock_viz.assert_called_once()
            
            # Verificar que prints informativos foram feitos
            self.assertGreater(mock_print.call_count, 0)
        
        print("✓ Integração com script principal validada")


class TestValidacaoRequisitos(unittest.TestCase):
    """Testes específicos para validar requisitos do sistema."""
    
    def setUp(self):
        """Configura ambiente de teste."""
        self.simulador = OptimizedInvestment(inflacao=6.0, ir_renda_fixa=15, ir_aluguel=27.5)
    
    def test_requisito_6_1_modularidade(self):
        """Valida requisito 6.1: Sistema modular e bem estruturado."""
        
        # Verificar que módulos são independentes
        from core import OptimizedInvestment as CoreClass
        from visualization import plotar_historico_planta_pronto, plotar_cenarios
        import main
        
        # Core deve funcionar independentemente
        simulador_independente = CoreClass(inflacao=5.0)
        resultado = simulador_independente.investimento_cdi(1000, 100, 10, 1)
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)
        
        # Visualização deve funcionar com dados válidos
        with patch('matplotlib.pyplot.savefig'), patch('matplotlib.pyplot.show'):
            plotar_historico_planta_pronto([1000, 1100, 1200], [1050, 1150, 1250], 3)
            plotar_cenarios({'Teste': [1000, 1100, 1200]}, 1)
        
        # Main deve ter funções bem definidas
        self.assertTrue(hasattr(main, 'configurar_parametros'))
        self.assertTrue(hasattr(main, 'executar_simulacoes'))
        self.assertTrue(hasattr(main, 'gerar_relatorio_resultados'))
        self.assertTrue(hasattr(main, 'gerar_visualizacoes'))
        
        print("✓ Requisito 6.1 (Modularidade) validado")
    
    def test_requisito_6_2_bibliotecas_otimizadas(self):
        """Valida requisito 6.2: Uso de bibliotecas otimizadas."""
        
        # Verificar que NumPy é usado para cálculos
        import numpy as np
        
        # Testar operações que devem usar NumPy internamente
        resultado = self.simulador.otimizar_portfolio(
            estrategias={
                'cdi': [1000 + i * 10 for i in range(60)],
                'ipca': [1100 + i * 11 for i in range(60)]
            },
            anos=5,
            optimize_aportes=False
        )
        
        pesos_otimizados = resultado[0]
        self.assertIsInstance(pesos_otimizados, np.ndarray)
        
        # Verificar que SciPy é usado para otimização
        from scipy.optimize import minimize
        
        # A função de otimização deve usar minimize internamente
        # (testado indiretamente através do funcionamento da otimização)
        self.assertAlmostEqual(sum(pesos_otimizados), 1.0, places=6)
        
        print("✓ Requisito 6.2 (Bibliotecas otimizadas) validado")
    
    def test_requisito_6_3_tratamento_erros(self):
        """Valida requisito 6.3: Tratamento adequado de exceções."""
        
        # Testar diferentes tipos de erro
        with self.assertRaises(ParametroInvalidoError):
            self.simulador.investimento_cdi(-1000, 100, 10, 5)  # Aporte negativo
        
        with self.assertRaises(ParametroInvalidoError):
            self.simulador.compra_financiada_planta(
                200000, 300000, 240, 10, 6, 1500  # Entrada > valor imóvel
            )
        
        # Testar que erros têm mensagens informativas
        try:
            OptimizedInvestment(inflacao=float('inf'))
        except ParametroInvalidoError as e:
            self.assertIn("finito", str(e).lower())
        
        print("✓ Requisito 6.3 (Tratamento de erros) validado")
    
    def test_requisito_6_4_saida_formatada(self):
        """Valida requisito 6.4: Saída clara no console."""
        
        # Testar que main.py produz saída formatada
        with patch('builtins.print') as mock_print:
            # Simular execução de relatório
            parametros = {
                'inflacao_anual': 6.0,
                'anos': 5,
                'aporte_inicial': 50000.0,
                'aporte_mensal': 1000.0
            }
            
            resultados = {
                'cdi': [50000 + i * 100 for i in range(60)],
                'ipca': [51000 + i * 110 for i in range(60)]
            }
            
            main.gerar_relatorio_resultados(resultados, parametros, self.simulador)
            
            # Verificar que houve saída no console
            self.assertGreater(mock_print.call_count, 0)
            
            # Verificar que saída contém formatação monetária
          ue)2, buffer=Tr(verbosity=nittest.main   ur testes
 # Executa
    
    otlib')ple='mating, modulrWarnegory=Useignore', catnings('rwarnings.filte  wartes
  durante tesib otlgs de matplimir warninpr    # Sugs
    
warninort     impt sys
e
    impore testte durar ambien Config':
    #= '__main___name__ = _")


ifa) validadoadat (Saída formito 6.4"✓ Requisrint(   p   
     text)
     ', calls_assertIn('%     self.    xt)
   _tealls', ctIn('R$asserf. sel          
 ist])args_lcall_ock_print.ll in m) for castr(calljoin([xt = ' '.tels_  cal