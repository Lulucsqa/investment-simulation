# Documento de Requisitos

## Introdução

O Sistema de Simulação e Otimização de Investimentos Imobiliários é uma aplicação Python que permite comparar diferentes estratégias de investimento, incluindo renda fixa (CDI, IPCA+) e investimentos imobiliários (compra na planta, imóvel pronto, estratégias mistas). O sistema deve calcular retornos ajustados pela inflação, considerar impostos brasileiros, e otimizar a alocação de portfólio para maximizar retornos.

## Requisitos

### Requisito 1

**História do Usuário:** Como um investidor, eu quero simular investimentos em renda fixa (CDI e IPCA+), para que eu possa comparar diferentes opções de investimento conservador.

#### Critérios de Aceitação

1. QUANDO o usuário fornecer aporte inicial, aporte mensal, taxa e prazo ENTÃO o sistema DEVE calcular o patrimônio acumulado mês a mês
2. QUANDO calcular rendimentos de CDI ENTÃO o sistema DEVE aplicar imposto de renda de 15% (mensal ou final)
3. QUANDO calcular rendimentos de IPCA+ ENTÃO o sistema DEVE aplicar imposto de renda apenas no vencimento
4. QUANDO apresentar resultados ENTÃO o sistema DEVE ajustar todos os valores pela inflação (valor presente)

### Requisito 2

**História do Usuário:** Como um investidor imobiliário, eu quero simular a compra de imóveis na planta e prontos com financiamento, para que eu possa avaliar qual estratégia é mais rentável.

#### Critérios de Aceitação

1. QUANDO simular imóvel na planta ENTÃO o sistema DEVE considerar período de construção sem aluguel
2. QUANDO calcular financiamento ENTÃO o sistema DEVE usar o sistema SAC (amortização constante)
3. QUANDO calcular aluguel ENTÃO o sistema DEVE aplicar imposto de renda de 27,5%
4. QUANDO valorizar o imóvel ENTÃO o sistema DEVE aplicar taxa de valorização mensal composta
5. QUANDO apresentar patrimônio ENTÃO o sistema DEVE calcular valor do imóvel menos saldo devedor mais aluguel acumulado

### Requisito 3

**História do Usuário:** Como um investidor diversificado, eu quero combinar investimento imobiliário com renda fixa, para que eu possa ter uma estratégia mista de investimentos.

#### Critérios de Aceitação

1. QUANDO executar estratégia mista ENTÃO o sistema DEVE simular financiamento imobiliário simultaneamente com investimento em CDI
2. QUANDO calcular patrimônio total ENTÃO o sistema DEVE somar valor líquido do imóvel com saldo da renda fixa
3. QUANDO aplicar aportes mensais ENTÃO o sistema DEVE direcionar recursos para renda fixa após pagamento do financiamento

### Requisito 4

**História do Usuário:** Como um investidor estratégico, eu quero otimizar a alocação entre diferentes estratégias de investimento, para que eu possa maximizar meu retorno esperado.

#### Critérios de Aceitação

1. QUANDO executar otimização ENTÃO o sistema DEVE encontrar pesos ótimos para cada estratégia
2. QUANDO otimizar aportes ENTÃO o sistema DEVE permitir otimização de aporte inicial e mensal dentro de limites definidos
3. QUANDO calcular alocação ENTÃO o sistema DEVE garantir que a soma dos pesos seja igual a 1
4. QUANDO falhar na otimização ENTÃO o sistema DEVE retornar erro informativo

### Requisito 5

**História do Usuário:** Como um usuário do sistema, eu quero visualizar comparações gráficas entre estratégias, para que eu possa entender melhor os resultados das simulações.

#### Critérios de Aceitação

1. QUANDO gerar gráficos ENTÃO o sistema DEVE criar visualizações profissionais com labels e formatação adequada
2. QUANDO comparar imóveis ENTÃO o sistema DEVE gerar gráfico específico para planta vs. pronto
3. QUANDO mostrar cenários ENTÃO o sistema DEVE incluir todos os cenários simulados em um único gráfico
4. QUANDO exibir alocação otimizada ENTÃO o sistema DEVE mostrar os pesos no título do gráfico
5. QUANDO salvar gráficos ENTÃO o sistema DEVE exportar em formato JPG com alta resolução

### Requisito 6

**História do Usuário:** Como um desenvolvedor, eu quero que o sistema seja modular e bem estruturado, para que eu possa facilmente manter e expandir funcionalidades.

#### Critérios de Aceitação

1. QUANDO estruturar o código ENTÃO o sistema DEVE separar lógica de negócio, visualização e execução em módulos distintos
2. QUANDO implementar cálculos ENTÃO o sistema DEVE usar bibliotecas otimizadas (NumPy, SciPy)
3. QUANDO tratar erros ENTÃO o sistema DEVE implementar tratamento adequado de exceções
4. QUANDO executar ENTÃO o sistema DEVE fornecer saída clara no console com resultados formatados

### Requisito 7

**História do Usuário:** Como um usuário final, eu quero configurar facilmente os parâmetros de simulação, para que eu possa adaptar as análises ao meu perfil de investimento.

#### Critérios de Aceitação

1. QUANDO configurar parâmetros ENTÃO o sistema DEVE permitir ajuste de inflação, impostos e taxas
2. QUANDO definir investimentos ENTÃO o sistema DEVE aceitar diferentes valores de aporte inicial e mensal
3. QUANDO configurar imóveis ENTÃO o sistema DEVE permitir ajuste de valor, entrada, financiamento e aluguel
4. QUANDO executar simulações ENTÃO o sistema DEVE usar os parâmetros configurados consistentemente