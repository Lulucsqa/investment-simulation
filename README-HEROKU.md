# Investment Simulation System - Heroku Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## 🚀 Deploy Rápido no Heroku

### Opção 1: Deploy com Um Clique
1. Clique no botão "Deploy to Heroku" acima
2. Escolha um nome para sua aplicação
3. Clique em "Deploy app"
4. Aguarde o deploy completar
5. Clique em "View" para acessar sua aplicação

### Opção 2: Deploy via Heroku CLI

**Pré-requisitos:**
- Conta no Heroku (gratuita): https://signup.heroku.com/
- Heroku CLI instalado: https://devcenter.heroku.com/articles/heroku-cli

**Comandos:**
```bash
# 1. Login no Heroku
heroku login

# 2. Criar aplicação
heroku create seu-app-name

# 3. Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 4. Abrir aplicação
heroku open
```

### Opção 3: Deploy via GitHub Integration

1. **Faça push do código para GitHub**
2. **Acesse:** https://dashboard.heroku.com/new-app
3. **Crie uma nova app**
4. **Em "Deployment method":** Escolha "GitHub"
5. **Conecte seu repositório**
6. **Enable "Automatic deploys"**
7. **Clique "Deploy Branch"**

## 🌐 URLs da Aplicação

Após o deploy, sua aplicação estará disponível em:

- **Frontend/API:** `https://seu-app-name.herokuapp.com`
- **Documentação da API:** `https://seu-app-name.herokuapp.com/docs`
- **Especificação OpenAPI:** `https://seu-app-name.herokuapp.com/openapi.json`

## 📊 Endpoints da API

### Simulações de Investimento
- `POST /simulate/cdi` - Simulação CDI
- `POST /simulate/ipca` - Simulação IPCA+
- `POST /simulate/real-estate/under-construction` - Imóvel na planta
- `POST /simulate/real-estate/ready` - Imóvel pronto
- `POST /simulate/mixed-strategy` - Estratégia mista

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

## 🔧 Configurações do Heroku

### Variáveis de Ambiente
```bash
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=false
```

### Scaling
```bash
# Verificar dynos
heroku ps

# Escalar aplicação
heroku ps:scale web=1
```

### Logs
```bash
# Ver logs em tempo real
heroku logs --tail

# Ver logs específicos
heroku logs --source app
```

## 💰 Custos

**Tier Gratuito (Eco Dynos):**
- 550-1000 horas gratuitas por mês
- Aplicação "dorme" após 30 minutos de inatividade
- Perfeito para desenvolvimento e testes

**Tier Pago (Basic Dynos - $7/mês):**
- Aplicação sempre ativa
- Melhor performance
- Recomendado para produção

## 🔒 Segurança

### Configurações de Produção
- CORS configurado para domínios específicos
- Variáveis de ambiente para configurações sensíveis
- HTTPS habilitado automaticamente

### Monitoramento
```bash
# Métricas da aplicação
heroku logs --tail

# Status da aplicação
heroku ps:scale
```

## 🚨 Troubleshooting

### Problemas Comuns

**1. Build Failed:**
```bash
# Verificar logs de build
heroku logs --tail

# Verificar dependências
cat requirements.txt
```

**2. Application Error:**
```bash
# Verificar logs da aplicação
heroku logs --source app

# Reiniciar aplicação
heroku restart
```

**3. Timeout Errors:**
```bash
# Verificar se a aplicação está respondendo
curl https://seu-app-name.herokuapp.com/

# Verificar configuração do Procfile
cat Procfile
```

### Comandos Úteis

```bash
# Informações da aplicação
heroku apps:info

# Configurações
heroku config

# Reiniciar aplicação
heroku restart

# Abrir aplicação no browser
heroku open

# Conectar ao bash da aplicação
heroku run bash
```

## 📈 Próximos Passos

1. **Configurar domínio customizado** (opcional)
2. **Adicionar monitoramento** com add-ons
3. **Configurar CI/CD** com GitHub Actions
4. **Adicionar banco de dados** se necessário
5. **Configurar SSL customizado** (opcional)

## 🆘 Suporte

- **Documentação Heroku:** https://devcenter.heroku.com/
- **Status do Heroku:** https://status.heroku.com/
- **Suporte:** https://help.heroku.com/

---

**Sua aplicação de simulação de investimentos agora está na nuvem! 🚀📈**