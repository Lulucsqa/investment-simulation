# Investment Simulation System - Render Deployment

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Lulucsqa/investment-simulation)

## 🚀 Deploy no Render

### ⚡ Deploy Automático (Recomendado)

1. **Clique no botão "Deploy to Render" acima** ⬆️
2. **Conecte sua conta GitHub**
3. **Confirme as configurações**
4. **Clique "Create Web Service"**
5. **Aguarde o deploy (2-3 minutos)**

### 🔧 Deploy Manual

1. **Acesse:** https://render.com
2. **Crie uma conta gratuita**
3. **Clique "New +" → "Web Service"**
4. **Conecte o repositório:** `https://github.com/Lulucsqa/investment-simulation`

**Configurações:**
```
Name: investment-simulation-api
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
Plan: Free
```

**Variáveis de Ambiente:**
```
ENVIRONMENT = production
DEBUG = false
PYTHONPATH = .
```

## 🌐 URLs da Aplicação

Após o deploy:

- **API Principal:** `https://investment-simulation-api.onrender.com`
- **Documentação:** `https://investment-simulation-api.onrender.com/docs`
- **Health Check:** `https://investment-simulation-api.onrender.com/`

## 📊 Endpoints da API

### Simulações de Investimento
- `POST /simulate/cdi` - Simulação CDI
- `POST /simulate/ipca` - Simulação IPCA+
- `POST /simulate/real-estate/under-construction` - Imóvel na planta
- `POST /simulate/real-estate/ready` - Imóvel pronto
- `POST /simulate/mixed-strategy` - Estratégia mista

### Exemplo de Uso

```bash
curl -X POST "https://investment-simulation-api.onrender.com/simulate/cdi" \
  -H "Content-Type: application/json" \
  -d '{
    "aporte_inicial": 100000,
    "aporte_mensal": 3000,
    "taxa_cdi": 10.5,
    "anos": 20,
    "inflacao_anual": 4.5
  }'
```

## 💰 Planos do Render

### Free Tier (Gratuito)
- ✅ 750 horas/mês
- ✅ HTTPS automático
- ✅ Deploy automático do GitHub
- ✅ Logs em tempo real
- ⚠️ App "dorme" após 15 min de inatividade

### Starter ($7/mês)
- ✅ Sempre ativo
- ✅ Melhor performance
- ✅ Métricas avançadas
- ✅ Recomendado para produção

## 🔧 Configurações Avançadas

### Deploy Automático via render.yaml

O arquivo `render.yaml` já está configurado no projeto:

```yaml
services:
  - type: web
    name: investment-simulation-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
    healthCheckPath: /
    autoDeploy: true
```

### Monitoramento

**Logs em Tempo Real:**
- Acesse o dashboard do Render
- Clique no seu serviço
- Vá para a aba "Logs"

**Métricas:**
- CPU e memória disponíveis no dashboard
- Tempo de resposta das requisições
- Status de saúde da aplicação

## 🔒 Segurança

### HTTPS Automático
- Certificado SSL gratuito
- Renovação automática
- Redirecionamento HTTP → HTTPS

### Variáveis de Ambiente
```bash
# Configurar no dashboard do Render
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=sua-chave-secreta
CORS_ORIGINS=https://seu-dominio.com
```

## 🚨 Troubleshooting

### Problemas Comuns

**1. Build Failed:**
- Verifique `requirements.txt`
- Confira logs de build no dashboard

**2. App não responde:**
- Verifique se está usando `$PORT` no start command
- Confirme que o health check path está correto

**3. Timeout na inicialização:**
- Render tem timeout de 10 minutos para build
- Otimize dependências se necessário

### Comandos Úteis

**Verificar status:**
```bash
curl https://seu-app.onrender.com/
```

**Testar API:**
```bash
curl https://seu-app.onrender.com/docs
```

## 📈 Vantagens do Render

### ✅ Facilidade de Uso
- Interface intuitiva
- Deploy automático do GitHub
- Configuração simples

### ✅ Performance
- CDN global
- Auto-scaling
- Infraestrutura moderna

### ✅ Recursos Gratuitos
- 750 horas/mês gratuitas
- HTTPS incluído
- Logs e métricas básicas

### ✅ Integração
- GitHub/GitLab integration
- Webhooks automáticos
- Environment variables

## 🔄 CI/CD Automático

O Render faz deploy automático quando você faz push para o GitHub:

```bash
# Fazer mudanças no código
git add .
git commit -m "Update investment calculations"
git push origin master

# Deploy automático será iniciado
# Acompanhe no dashboard do Render
```

## 🌍 Domínio Personalizado

### Configurar Domínio Próprio

1. **No dashboard do Render:**
   - Vá para Settings
   - Clique "Custom Domains"
   - Adicione seu domínio

2. **Configure DNS:**
   ```
   CNAME: seu-dominio.com → seu-app.onrender.com
   ```

3. **SSL automático** será configurado

## 📊 Monitoramento de Performance

### Métricas Disponíveis
- Tempo de resposta
- Uso de CPU/Memória
- Número de requisições
- Taxa de erro

### Alertas
- Configure notificações por email
- Webhooks para Slack/Discord
- Monitoramento de uptime

## 🆘 Suporte

**Documentação Render:**
- https://render.com/docs

**Status do Render:**
- https://status.render.com

**Comunidade:**
- Discord: https://discord.gg/render

---

## 🎯 Deploy Agora!

**Clique no botão abaixo para deploy automático:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Lulucsqa/investment-simulation)

**Sua aplicação estará online em 3 minutos! 🚀📈**