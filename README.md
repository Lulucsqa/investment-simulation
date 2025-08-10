# Investment Simulation System 🚀📈

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Lulucsqa/investment-simulation)

## 🌟 Sistema de Simulação e Otimização de Investimentos Imobiliários

Este sistema permite simular e comparar diferentes estratégias de investimento, incluindo renda fixa (CDI, IPCA+) e investimentos imobiliários (compra na planta, imóvel pronto, estratégias mistas). O sistema calcula retornos ajustados pela inflação, considera impostos brasileiros, e otimiza a alocação de portfólio para maximizar retornos.

## 🚀 Deploy Rápido no Heroku

### ⚡ Deploy com Um Clique (Mais Fácil)

1. **Clique no botão "Deploy to Heroku" acima** ⬆️
2. **Escolha um nome para sua aplicação**
3. **Clique em "Deploy app"**
4. **Aguarde o deploy completar (2-3 minutos)**
5. **Clique em "View" para acessar sua aplicação**

### 🌐 Sua Aplicação Estará Disponível Em:

- **API Principal:** `https://seu-app-name.herokuapp.com/`
- **Documentação Interativa:** `https://seu-app-name.herokuapp.com/docs`
- **Especificação OpenAPI:** `https://seu-app-name.herokuapp.com/openapi.json`

## 📊 Características Principais

- **✅ Simulações de Renda Fixa**: CDI e IPCA+ com cálculos de impostos precisos
- **✅ Investimentos Imobiliários**: Simulação de compra na planta e imóvel pronto com financiamento SAC
- **✅ Estratégia Mista**: Combinação de financiamento imobiliário com investimento em renda fixa
- **✅ Otimização de Portfólio**: Algoritmos de otimização para encontrar a melhor alocação
- **✅ API REST Completa**: Todos os cálculos disponíveis via HTTP
- **✅ Documentação Automática**: Interface Swagger integrada
- **✅ Ajuste Inflacionário**: Todos os cálculos em valor presente
- **✅ Visualizações**: Gráficos profissionais para comparação de estratégias

## 🔧 Endpoints da API

### Simulações de Investimento
- `POST /simulate/cdi` - Simulação de investimento em CDI
- `POST /simulate/ipca` - Simulação de investimento em IPCA+
- `POST /simulate/real-estate/under-construction` - Imóvel na planta
- `POST /simulate/real-estate/ready` - Imóvel pronto
- `POST /simulate/mixed-strategy` - Estratégia mista (imóvel + CDI)

### Exemplo de Uso da API

```bash
curl -X POST "https://seu-app-name.herokuapp.com/simulate/cdi" \
  -H "Content-Type: application/json" \
  -d '{
    "aporte_inicial": 100000,
    "aporte_mensal": 3000,
    "taxa_cdi": 10.5,
    "anos": 20,
    "inflacao_anual": 4.5
  }'
```

## 💻 Executar Localmente

### Opção 1: Python Direto (Simulação Original)
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar simulação
python main.py

# Ou iniciar API server
python -m uvicorn backend.api:app --reload
```

### Opção 2: Docker (Completo)
```bash
# Iniciar sistema completo
docker-compose up -d

# Acessar em http://localhost
```

## 📈 Estratégias de Investimento Disponíveis

### 1. **CDI** (Certificado de Depósito Interbancário)
- Investimento em renda fixa pós-fixada
- Tributação: 15% (mensal ou final)
- Liquidez diária
- Baixo risco

### 2. **IPCA+** (Títulos Indexados à Inflação)
- Investimento em títulos públicos
- Rendimento: Inflação + taxa adicional
- Tributação: 15% apenas no vencimento
- Proteção contra inflação

### 3. **Imóvel na Planta**
- Compra durante construção (3 anos padrão)
- Financiamento pelo sistema SAC
- Aluguel apenas após entrega
- Valorização mensal do imóvel
- IR sobre aluguel: 27.5%

### 4. **Imóvel Pronto**
- Compra de imóvel já construído
- Financiamento pelo sistema SAC
- Aluguel imediato
- Valorização mensal do imóvel
- IR sobre aluguel: 27.5%

### 5. **Estratégia Mista**
- Financiamento imobiliário + CDI
- Aportes mensais direcionados para renda fixa
- Diversificação de riscos
- Otimização automática de alocação

## 🎯 Exemplo de Resultados

Com os parâmetros padrão (20 anos, R$ 100k inicial, R$ 3k/mês):

| Estratégia | Valor Final | Rentabilidade |
|------------|-------------|---------------|
| **Estratégia Mista** | **R$ 1.404.879** | **71.3%** |
| CDI | R$ 1.008.743 | 23.0% |
| IPCA+ | R$ 1.047.553 | 27.7% |
| Imóvel Planta | R$ 776.066 | -5.4% |
| Imóvel Pronto | R$ 803.122 | -2.1% |

## 🔒 Segurança e Validação

- **✅ Validação de entrada** com Pydantic
- **✅ Tratamento de erros** robusto
- **✅ CORS configurado** para produção
- **✅ Rate limiting** disponível
- **✅ HTTPS automático** no Heroku

## 📚 Documentação Completa

- **[SETUP.md](SETUP.md)** - Guia de instalação local
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guia avançado de deploy
- **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** - Configurações de produção

## 🛠️ Tecnologias Utilizadas

**Backend:**
- Python 3.10+
- FastAPI (API REST)
- NumPy (Cálculos financeiros)
- SciPy (Otimização)
- Matplotlib (Visualizações)
- Pydantic (Validação)

**Deploy:**
- Heroku (Cloud Platform)
- Docker (Containerização)
- GitHub Actions (CI/CD)

## 📊 Funcionalidades Avançadas

### Otimização de Portfólio
O sistema utiliza algoritmos de otimização (SLSQP) para encontrar a melhor alocação entre estratégias, maximizando o retorno final ajustado pela inflação.

### Visualizações Automáticas
Gera automaticamente gráficos comparativos salvos em formato JPG de alta resolução.

### Cálculos Precisos
- Todos os valores em valor presente (ajustados pela inflação)
- Sistema SAC para financiamentos
- Impostos brasileiros aplicados corretamente
- Operações vetorizadas NumPy para performance

## 🆘 Suporte

Para dúvidas ou problemas:

1. **Consulte a documentação da API:** `https://seu-app.herokuapp.com/docs`
2. **Verifique os logs:** `heroku logs --tail`
3. **Teste localmente:** `python main.py`
4. **Abra uma issue** neste repositório

## 📄 Licença

Este projeto está licenciado sob a MIT License.

---

## 🎉 Deploy Agora!

**Clique no botão abaixo para ter sua própria instância rodando em 3 minutos:**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Lulucsqa/investment-simulation)

**Sua aplicação de simulação de investimentos estará online e acessível de qualquer lugar do mundo! 🌍🚀**