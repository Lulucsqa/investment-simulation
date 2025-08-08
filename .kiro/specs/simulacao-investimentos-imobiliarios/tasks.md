# Plano de Implementação

- [x] 1. Configurar estrutura do projeto e dependências





  - Criar arquivo requirements.txt com NumPy, SciPy e Matplotlib
  - Criar estrutura de diretórios do projeto
  - Configurar imports e estrutura básica dos módulos
  - _Requisitos: 6.1, 6.2_

- [x] 2. Implementar classe base e utilitários financeiros





  - Criar classe OptimizedInvestment com construtor e parâmetros de configuração
  - Implementar método ajuste_inflacao para cálculos de valor presente
  - Criar funções auxiliares para conversão de taxas anuais para mensais
  - Escrever testes unitários para utilitários básicos
  - _Requisitos: 1.4, 7.1, 7.4_

- [x] 3. Implementar simulações de renda fixa





- [x] 3.1 Implementar simulação de investimento em CDI


  - Codificar método investimento_cdi com cálculo de juros compostos
  - Implementar aplicação de imposto de renda mensal e final
  - Adicionar acumulação de aportes mensais
  - Criar testes para cenários conhecidos de CDI
  - _Requisitos: 1.1, 1.2, 1.4_

- [x] 3.2 Implementar simulação de investimento em IPCA+


  - Codificar método investimento_ipca com lógica similar ao CDI
  - Implementar aplicação de imposto apenas no vencimento
  - Validar cálculos com casos de teste específicos
  - _Requisitos: 1.1, 1.3, 1.4_

- [x] 4. Implementar simulações imobiliárias




- [x] 4.1 Implementar financiamento com sistema SAC


  - Codificar cálculo de amortização constante (SAC)
  - Implementar cálculo de juros sobre saldo devedor
  - Criar função para cálculo de prestações mensais
  - Escrever testes para validar sistema SAC
  - _Requisitos: 2.2, 2.5_

- [x] 4.2 Implementar simulação de imóvel na planta


  - Codificar método compra_financiada_planta
  - Implementar período de construção sem aluguel
  - Adicionar valorização mensal do imóvel
  - Calcular patrimônio líquido (valor - saldo devedor + aluguel)
  - _Requisitos: 2.1, 2.4, 2.5_

- [x] 4.3 Implementar simulação de imóvel pronto


  - Codificar método compra_financiada_pronto
  - Implementar recebimento imediato de aluguel
  - Aplicar imposto de renda sobre aluguel (27,5%)
  - Validar diferenças com imóvel na planta
  - _Requisitos: 2.3, 2.4, 2.5_

- [x] 5. Implementar estratégia mista


















  - Codificar método compra_e_renda_fixa
  - Combinar simulação de financiamento imobiliário com investimento em CDI
  - Calcular patrimônio total (imóvel + renda fixa)
  - Implementar direcionamento de aportes mensais para renda fixa
  - Escrever testes de integração para estratégia mista
  - _Requisitos: 3.1, 3.2, 3.3_

- [ ] 6. Implementar otimização de portfólio
- [ ] 6.1 Implementar função objetivo para otimização
  - Codificar função que maximiza retorno final do portfólio
  - Implementar cálculo de portfólio ponderado
  - Adicionar suporte para otimização de aportes
  - _Requisitos: 4.1, 4.2_

- [ ] 6.2 Implementar restrições e bounds da otimização
  - Codificar restrição de soma dos pesos igual a 1
  - Implementar bounds para pesos (0 a 1) e aportes
  - Adicionar validação de parâmetros de entrada
  - _Requisitos: 4.3_

- [ ] 6.3 Integrar algoritmo de otimização SciPy
  - Implementar chamada para scipy.optimize.minimize com SLSQP
  - Adicionar tratamento de erros de convergência
  - Normalizar pesos otimizados automaticamente
  - Escrever testes para casos de otimização simples
  - _Requisitos: 4.1, 4.4_

- [ ] 7. Implementar módulo de visualização
- [ ] 7.1 Criar função de comparação imóvel planta vs pronto
  - Codificar plotar_historico_planta_pronto com matplotlib
  - Implementar formatação profissional (labels, grid, cores)
  - Adicionar salvamento em arquivo JPG de alta resolução
  - _Requisitos: 5.1, 5.2, 5.5_

- [ ] 7.2 Criar função de visualização de cenários múltiplos
  - Codificar plotar_cenarios para múltiplas estratégias
  - Implementar diferentes estilos de linha para cada cenário
  - Adicionar exibição de pesos otimizados no título
  - Configurar legendas e formatação adequada
  - _Requisitos: 5.1, 5.3, 5.4, 5.5_

- [ ] 8. Implementar script principal de execução
- [ ] 8.1 Criar configuração de parâmetros
  - Definir todos os parâmetros de simulação no main.py
  - Implementar configuração de inflação, impostos e taxas
  - Adicionar parâmetros imobiliários e de investimento
  - _Requisitos: 7.1, 7.2, 7.3_

- [ ] 8.2 Executar todas as simulações
  - Instanciar OptimizedInvestment com parâmetros configurados
  - Executar simulações de CDI, IPCA+, imóveis e estratégia mista
  - Coletar resultados em estrutura de dados organizada
  - _Requisitos: 7.4_

- [ ] 8.3 Implementar relatório de resultados
  - Codificar exibição formatada de resultados no console
  - Adicionar comparação entre estratégias
  - Implementar chamada para otimização de portfólio
  - Exibir pesos otimizados e aportes recomendados
  - _Requisitos: 6.4_

- [ ] 9. Integrar visualizações no fluxo principal
  - Chamar funções de plotagem após simulações
  - Gerar gráfico comparativo de imóveis
  - Criar visualização de cenários com alocação otimizada
  - Verificar criação correta dos arquivos de saída
  - _Requisitos: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 10. Implementar tratamento de erros e validações
- [ ] 10.1 Adicionar validação de parâmetros de entrada
  - Implementar verificações para valores negativos ou inválidos
  - Adicionar validação de ranges para taxas e prazos
  - Criar mensagens de erro informativas
  - _Requisitos: 6.3_

- [ ] 10.2 Implementar tratamento de erros de otimização
  - Capturar falhas na convergência do algoritmo
  - Implementar fallback para casos de não convergência
  - Adicionar logging detalhado de erros
  - Escrever testes para cenários de erro
  - _Requisitos: 4.4, 6.3_

- [ ] 11. Criar testes de integração completos
  - Escrever teste end-to-end do fluxo completo
  - Validar consistência entre diferentes módulos
  - Testar geração correta de arquivos de saída
  - Verificar precisão dos cálculos em cenários conhecidos
  - _Requisitos: 6.1, 6.2, 6.3, 6.4_

- [ ] 12. Otimizar performance e finalizar documentação
  - Implementar otimizações com operações vetorizadas NumPy
  - Adicionar docstrings detalhadas em todas as funções
  - Criar arquivo README com instruções de uso
  - Validar que todos os requisitos foram atendidos
  - _Requisitos: 6.2, 6.4_