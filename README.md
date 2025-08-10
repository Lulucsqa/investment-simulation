# Sistema de Simulação e Otimização de Investimentos Imobiliários

## Visão Geral

Este sistema permite simular e comparar diferentes estratégias de investimento, incluindo renda fixa (CDI, IPCA+) e investimentos imobiliários (compra na planta, imóvel pronto, estratégias mistas). O sistema calcula retornos ajustados pela inflação, considera impostos brasileiros, e otimiza a alocação de portfólio para maximizar retornos.

## Características Principais

- **Simulações de Renda Fixa**: CDI e IPCA+ com cálculos de impostos precisos
- **Investimentos Imobiliários**: Simulação de compra na planta e imóvel pronto com financiamento SAC
- **Estratégia Mista**: Combinação de financiamento imobiliário com investimento em renda fixa
- **Otimização de Portfólio**: Algoritmos de otimização para encontrar a melhor alocação
- **Ajuste Inflacionário**: Todos os cálculos em valor presente
- **Visualizações**: Gráficos profissionais para comparação de estratégias
- **Performance Otimizada**: Operações vetorizadas NumPy para simulações de longo prazo

## Requisitos do Sistema

### Dependências Python

```bash
numpy>=1.21.0          # Cálculos numéricos otimizados
scipy>=1.7.0           # Algoritmos de otimização
matplotlib>=3.4.0      # Visualizações e gráficos
```

### Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd simulacao-investimentos-imobiliarios
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o sistema:
```bash
python main.py
```

## Estrutura do Projeto

```
simulacao-investimentos-imobiliarios/
├── core.py                    # Módulo principal com lógica de simulação
├── visualization.py           # Módulo de visualizações e gráficos
├── main.py                   # Script principal de execução
├── requirements.txt          # Dependências do projeto
├── README.md                 # Este arquivo
├── outputs/                  # Diretório para gráficos gerados
│   ├── comparacao_imoveis.jpg
│   └── cenarios_investimento.jpg
└── tests/                    # Testes unitários e de integração
    ├── test_core.py
    ├── test_estrategia_mista.py
    └── test_validacao_parametros.py
```

## 🚀 Deployment

### Quick Start (Docker)

1. **Deploy the entire system:**

**Windows (escolha uma opção):**
```cmd
# Opção 1: Script simples (recomendado)
start.cmd

# Opção 2: Batch script
.\deploy.bat

# Opção 3: PowerShell script (mais recursos)
.\deploy.ps1
```

**Linux/Mac:**
```bash
./deploy.sh
```

2. **Access the application:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

3. **Monitor system status:**
```bash
python status.py        # Real-time dashboard
python health-check.py  # One-time health check
```

### Manual Deployment

**Backend API:**
```bash
pip install -r requirements.txt
uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run build
npm run preview
```

**Python Simulation (Standalone):**
```bash
python main.py
```

## Como Usar

### Via Web Interface (Recommended)

1. Access http://localhost after deployment
2. Use the interactive forms to configure simulations
3. View results and charts in real-time

### Via API

```bash
# CDI Simulation
curl -X POST "http://localhost:8000/simulate/cdi" \
  -H "Content-Type: application/json" \
  -d '{
    "aporte_inicial": 100000,
    "aporte_mensal": 3000,
    "taxa_cdi": 10.5,
    "anos": 20,
    "inflacao_anual": 4.5
  }'
```

### Via Python Script (Standalone)

Execute o script principal para rodar todas as simulações com parâmetros padrão:

```bash
python main.py
```

### Configuração de Parâmetros

Edite a função `configurar_parametros()` em `main.py` para ajustar:

#### Parâmetros Econômicos
- `inflacao_anual`: Taxa de inflação anual (%)
- `ir_renda_fixa`: Imposto de renda para renda fixa (%)
- `ir_aluguel`: Imposto de renda para aluguel (%)

#### Parâmetros de Investimento
- `aporte_inicial`: Valor inicial disponível (R$)
- `aporte_mensal`: Valor mensal para aportes (R$)
- `anos`: Horizonte de investimento (anos)

#### Parâmetros de Renda Fixa
- `taxa_cdi`: Taxa CDI anual (%)
- `taxa_ipca`: Taxa IPCA+ adicional anual (%)

#### Parâmetros Imobiliários
- `valor_imovel`: Valor total do imóvel (R$)
- `entrada_imovel`: Valor da entrada (R$)
- `taxa_juros_financiamento`: Taxa de juros do financiamento (%)
- `valorizacao_imovel`: Taxa de valorização anual do imóvel (%)
- `aluguel_mensal`: Valor mensal do aluguel (R$)
- `anos_construcao`: Período de construção para imóvel na planta (anos)

### Exemplo de Uso Programático

```python
from core import OptimizedInvestment

# Criar instância do simulador
simulador = OptimizedInvestment(
    inflacao=4.5,      # 4.5% ao ano
    ir_renda_fixa=15,  # 15% IR
    ir_aluguel=27.5    # 27.5% IR
)

# Simular investimento em CDI
historico_cdi = simulador.investimento_cdi(
    aporte_inicial=100000,  # R$ 100.000
    aporte_mensal=3000,     # R$ 3.000/mês
    taxa_cdi=10.5,          # 10.5% ao ano
    anos=20                 # 20 anos
)

# Simular imóvel na planta
historico_planta = simulador.compra_financiada_planta(
    valor_imovel=500000,    # R$ 500.000
    entrada=100000,         # R$ 100.000
    parcelas=240,           # 20 anos
    taxa_juros=9.0,         # 9% ao ano
    valorizacao=6.0,        # 6% ao ano
    aluguel=2500,           # R$ 2.500/mês
    anos_construcao=3       # 3 anos
)

# Otimizar portfólio
estrategias = {
    'CDI': historico_cdi,
    'Imóvel Planta': historico_planta
}

pesos_otimos, _, _, retorno_final = simulador.otimizar_portfolio(
    estrategias=estrategias,
    anos=20
)

print(f"Alocação ótima: CDI {pesos_otimos[0]:.1%}, Imóvel {pesos_otimos[1]:.1%}")
print(f"Retorno final otimizado: R$ {retorno_final:,.2f}")
```

## Estratégias de Investimento Disponíveis

### 1. CDI (Certificado de Depósito Interbancário)
- Investimento em renda fixa pós-fixada
- Tributação: 15% (mensal ou final)
- Liquidez diária
- Baixo risco

### 2. IPCA+ (Títulos Indexados à Inflação)
- Investimento em títulos públicos
- Rendimento: Inflação + taxa adicional
- Tributação: 15% apenas no vencimento
- Proteção contra inflação

### 3. Imóvel na Planta
- Compra durante construção (3 anos padrão)
- Financiamento pelo sistema SAC
- Aluguel apenas após entrega
- Valorização mensal do imóvel
- IR sobre aluguel: 27.5%

### 4. Imóvel Pronto
- Compra de imóvel já construído
- Financiamento pelo sistema SAC
- Aluguel imediato
- Valorização mensal do imóvel
- IR sobre aluguel: 27.5%

### 5. Estratégia Mista
- Financiamento imobiliário + CDI
- Aportes mensais direcionados para renda fixa
- Diversificação de riscos
- Otimização automática de alocação

## Funcionalidades Avançadas

### Otimização de Portfólio

O sistema utiliza algoritmos de otimização (SLSQP) para encontrar a melhor alocação entre estratégias:

```python
# Otimização apenas de pesos
pesos_otimos, _, _, retorno = simulador.otimizar_portfolio(
    estrategias=estrategias,
    anos=20,
    optimize_aportes=False
)

# Otimização de pesos e aportes
pesos_otimos, aporte_inicial_otimo, aporte_mensal_otimo, retorno = simulador.otimizar_portfolio(
    estrategias=estrategias,
    anos=20,
    optimize_aportes=True,
    aporte_bounds=((50000, 200000), (1000, 5000))
)
```

### Visualizações

O sistema gera automaticamente:

1. **Comparação Imóveis**: Gráfico comparando imóvel na planta vs pronto
2. **Cenários de Investimento**: Comparação de todas as estratégias
3. **Alocação Otimizada**: Visualização com pesos otimizados

Arquivos salvos em `outputs/`:
- `comparacao_imoveis.jpg`
- `cenarios_investimento.jpg`

### Tratamento de Erros

O sistema inclui validação robusta de parâmetros:

```python
try:
    resultado = simulador.investimento_cdi(
        aporte_inicial=-1000,  # Valor inválido
        aporte_mensal=3000,
        taxa_cdi=10.5,
        anos=20
    )
except ParametroInvalidoError as e:
    print(f"Erro de parâmetro: {e}")
```

## Interpretação dos Resultados

### Valores Apresentados
- **Todos os valores estão em valor presente** (ajustados pela inflação)
- **Patrimônio líquido** para imóveis = Valor do imóvel - Saldo devedor + Aluguel acumulado - Entrada
- **Rentabilidade** calculada sobre o total investido (aportes + entrada)

### Métricas Importantes
- **Retorno Final**: Valor total ao final do período
- **Rentabilidade Total**: Ganho percentual sobre o investido
- **Rentabilidade Anual Média**: Taxa anual equivalente
- **Alocação Ótima**: Percentual recomendado para cada estratégia

## Limitações e Considerações

### Limitações Técnicas
- **Horizonte máximo**: 100 anos (recomendado até 30 anos)
- **Precisão**: Float64 para cálculos financeiros
- **Estratégias simultâneas**: Até 10 estratégias na otimização

### Considerações Econômicas
- **Inflação constante**: Sistema assume taxa fixa ao longo do tempo
- **Taxas fixas**: CDI, IPCA+ e valorização imobiliária constantes
- **Impostos simplificados**: Não considera mudanças na legislação
- **Custos de transação**: Não incluídos nas simulações

### Riscos Não Modelados
- **Risco de crédito**: Não considera inadimplência
- **Risco de liquidez**: Não modela dificuldades de venda
- **Risco regulatório**: Mudanças em impostos ou regras
- **Vacância**: Não considera períodos sem aluguel

## Testes

Execute os testes para validar o funcionamento:

```bash
# Testes unitários básicos
python -m pytest test_core.py -v

# Testes de estratégia mista
python -m pytest test_estrategia_mista.py -v

# Testes de validação de parâmetros
python -m pytest test_validacao_parametros.py -v

# Todos os testes
python -m pytest -v
```

## Contribuição

### Estrutura do Código
- **core.py**: Lógica principal de simulação
- **visualization.py**: Funções de plotagem
- **main.py**: Interface de usuário e execução

### Padrões de Código
- Docstrings em inglês com parâmetros em português
- Type hints para todos os parâmetros
- Validação robusta de entrada
- Tratamento de exceções específicas

### Adicionando Novas Estratégias

1. Implemente a função na classe `OptimizedInvestment`
2. Adicione validação de parâmetros
3. Inclua docstring detalhada
4. Crie testes unitários
5. Atualize a documentação

## Suporte e Contato

Para dúvidas, sugestões ou problemas:

1. Verifique a documentação
2. Execute os testes para validar a instalação
3. Consulte os exemplos de uso
4. Abra uma issue no repositório

## Licença

Este projeto está licenciado sob [especificar licença].

## Changelog

### Versão Atual
- ✅ Simulações de renda fixa (CDI, IPCA+)
- ✅ Simulações imobiliárias (planta, pronto, mista)
- ✅ Otimização de portfólio
- ✅ Visualizações profissionais
- ✅ Operações vetorizadas NumPy
- ✅ Validação robusta de parâmetros
- ✅ Tratamento de erros
- ✅ Testes abrangentes
- ✅ Documentação completa

### Próximas Funcionalidades
- [ ] Interface web interativa
- [ ] Análise de sensibilidade
- [ ] Simulação Monte Carlo
- [ ] Exportação para Excel/PDF
- [ ] API REST
- [ ] Dashboard em tempo real