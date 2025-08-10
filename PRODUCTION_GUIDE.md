# 🚀 Guia de Deploy em Produção - Investment Simulation System

## 📋 Opções de Deploy (Sem Docker)

### 🥇 Opção 1: Heroku (Recomendado - Mais Simples)

**Vantagens:**
- ✅ Deploy com um comando
- ✅ HTTPS automático
- ✅ Domínio gratuito (.herokuapp.com)
- ✅ Logs integrados
- ✅ Fácil configuração

**Passos:**

1. **Instalar Heroku CLI:**
   - Acesse: https://devcenter.heroku.com/articles/heroku-cli
   - Baixe e instale

2. **Instalar Git (se não tiver):**
   - Acesse: https://git-scm.com/download/win
   - Baixe e instale

3. **Deploy:**
   ```cmd
   deploy-heroku.cmd
   ```

4. **Sua aplicação estará em:**
   - `https://seu-app.herokuapp.com`
   - `https://seu-app.herokuapp.com/docs`

---

### 🥈 Opção 2: Vercel (Serverless)

**Vantagens:**
- ✅ Deploy ultra-rápido
- ✅ CDN global
- ✅ Domínio personalizado gratuito
- ✅ Integração com GitHub

**Passos:**

1. **Instalar Node.js:**
   - Acesse: https://nodejs.org/
   - Baixe versão LTS

2. **Deploy:**
   ```cmd
   deploy-vercel.cmd
   ```

---

### 🥉 Opção 3: Railway (Moderno)

**Vantagens:**
- ✅ Interface moderna
- ✅ Deploy automático
- ✅ Banco de dados integrado
- ✅ Monitoramento

**Passos:**

1. **Deploy:**
   ```cmd
   deploy-railway.cmd
   ```

---

### 🐍 Opção 4: PythonAnywhere (Python Especializado)

**Vantagens:**
- ✅ Especializado em Python
- ✅ Console Python online
- ✅ Cron jobs integrados
- ✅ Plano gratuito disponível

**Passos:**

1. **Criar conta:** https://www.pythonanywhere.com/
2. **Upload dos arquivos via interface web**
3. **Configurar Web App com o arquivo `wsgi.py`**

---

## 🔧 Configurações de Produção

### Variáveis de Ambiente

Crie estas variáveis no seu provedor:

```bash
# Aplicação
ENVIRONMENT=production
DEBUG=false

# API
API_HOST=0.0.0.0
API_PORT=8000

# Segurança
SECRET_KEY=sua-chave-secreta-aqui
CORS_ORIGINS=https://seu-dominio.com

# Performance
API_WORKERS=2
```

### Configuração de CORS

Edite `backend/api.py`:

```python
# Para produção, substitua "*" pelo seu domínio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-dominio.com"],  # Seu domínio
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 🔒 Segurança em Produção

### 1. Configurar HTTPS
- Heroku: Automático
- Vercel: Automático  
- Railway: Automático
- PythonAnywhere: Disponível nos planos pagos

### 2. Rate Limiting

Adicione ao `backend/api.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/simulate/cdi")
@limiter.limit("10/minute")
async def simulate_cdi(request: Request, params: CDIParams):
    # ... código existente
```

### 3. Validação de Input

Já implementado com Pydantic nos modelos da API.

---

## 📊 Monitoramento

### Logs de Aplicação

**Heroku:**
```bash
heroku logs --tail
```

**Vercel:**
```bash
vercel logs
```

**Railway:**
```bash
railway logs
```

### Health Check

Sua API já tem endpoint de health check em `/`

### Métricas

Adicione ao `backend/api.py`:

```python
from prometheus_client import Counter, generate_latest

REQUEST_COUNT = Counter('requests_total', 'Total requests')

@app.middleware("http")
async def count_requests(request: Request, call_next):
    REQUEST_COUNT.inc()
    response = await call_next(request)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

---

## 🚀 Deploy Automatizado

### GitHub Actions (Para Heroku)

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "seu-app-name"
          heroku_email: "seu-email@example.com"
```

---

## 🔧 Troubleshooting

### Problemas Comuns

**1. Erro de Port:**
```python
# Em backend/api.py, certifique-se:
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**2. Erro de Dependências:**
```bash
# Certifique-se que requirements.txt está correto
pip freeze > requirements.txt
```

**3. Erro de CORS:**
```python
# Adicione seu domínio de produção
allow_origins=["https://seu-dominio.herokuapp.com"]
```

---

## 📈 Otimizações de Performance

### 1. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def calculate_simulation(params_hash):
    # Cache de simulações
    pass
```

### 2. Compressão

```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 3. Async Operations

```python
import asyncio

@app.post("/simulate/cdi")
async def simulate_cdi_async(params: CDIParams):
    # Operações assíncronas para melhor performance
    pass
```

---

## 💰 Custos Estimados

### Planos Gratuitos:
- **Heroku:** 550 horas/mês (suficiente para testes)
- **Vercel:** 100GB bandwidth/mês
- **Railway:** $5 crédito inicial
- **PythonAnywhere:** 1 web app gratuita

### Planos Pagos (Recomendado para produção):
- **Heroku Hobby:** $7/mês
- **Vercel Pro:** $20/mês
- **Railway:** Pay-as-you-go
- **PythonAnywhere Hacker:** $5/mês

---

## 🎯 Recomendação Final

**Para começar:** Use Heroku (mais simples)
**Para escalar:** Considere Railway ou Vercel
**Para Python puro:** PythonAnywhere

---

## 🆘 Suporte

Se encontrar problemas:

1. **Verifique os logs** do seu provedor
2. **Teste localmente** primeiro
3. **Verifique as variáveis de ambiente**
4. **Consulte a documentação** do provedor

**Seu sistema está pronto para produção! 🚀📈**