# 🗄️ Configuração do Supabase - Investment Simulation System

## 📋 Visão Geral

O Supabase será usado como banco de dados PostgreSQL para:
- ✅ Armazenar simulações dos usuários
- ✅ Histórico de cálculos
- ✅ Portfólios otimizados
- ✅ Estatísticas de uso
- ✅ Autenticação (opcional)

## 🚀 Passo a Passo da Configuração

### 1. Criar Projeto no Supabase

1. **Acesse:** https://supabase.com
2. **Clique "Start your project"**
3. **Faça login** com GitHub/Google
4. **Clique "New Project"**
5. **Configure:**
   ```
   Organization: Sua organização
   Name: investment-simulation
   Database Password: [senha forte]
   Region: South America (São Paulo)
   ```
6. **Clique "Create new project"**
7. **Aguarde 2-3 minutos** para provisionar

### 2. Configurar Banco de Dados

1. **No dashboard do Supabase, vá para "SQL Editor"**
2. **Clique "New Query"**
3. **Cole o conteúdo do arquivo `supabase-setup.sql`**
4. **Clique "Run"**
5. **Verifique se apareceu:** "Investment Simulation System database setup completed successfully!"

### 3. Obter Credenciais

1. **Vá para "Settings" → "API"**
2. **Copie as informações:**
   ```
   Project URL: https://seu-projeto.supabase.co
   anon public key: eyJ... (chave pública)
   service_role key: eyJ... (chave privada - cuidado!)
   ```

### 4. Configurar Variáveis de Ambiente

#### No Render (Produção):
1. **Acesse seu app no Render**
2. **Vá para "Environment"**
3. **Adicione as variáveis:**
   ```
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_ANON_KEY=eyJ... (chave pública)
   SUPABASE_SERVICE_KEY=eyJ... (chave privada)
   ```

#### Localmente (Desenvolvimento):
1. **Crie arquivo `.env`:**
   ```bash
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_ANON_KEY=eyJ...
   SUPABASE_SERVICE_KEY=eyJ...
   ```

### 5. Instalar Dependência Python

```bash
pip install supabase
```

### 6. Testar Integração

```bash
python supabase-integration.py
```

Deve aparecer:
```
✅ Supabase conectado com sucesso
✅ Simulação salva com sucesso
📊 Encontradas X simulações no histórico
```

## 🔧 Estrutura do Banco de Dados

### Tabelas Criadas

#### 1. **users** (Usuários)
```sql
- id: UUID (chave primária)
- email: VARCHAR (único)
- name: VARCHAR
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### 2. **simulations** (Simulações)
```sql
- id: UUID (chave primária)
- user_id: UUID (referência para users)
- strategy: VARCHAR (CDI, IPCA, etc.)
- parameters: JSONB (parâmetros de entrada)
- result: JSONB (resultado da simulação)
- created_at: TIMESTAMP
```

#### 3. **portfolios** (Portfólios)
```sql
- id: UUID (chave primária)
- user_id: UUID (referência para users)
- name: VARCHAR
- strategies: JSONB
- optimal_weights: JSONB
- final_return: DECIMAL
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

## 📊 Funcionalidades Disponíveis

### API Endpoints com Supabase

#### Simulações com Persistência
```bash
# Todas as simulações agora salvam automaticamente
POST /simulate/cdi
POST /simulate/ipca
POST /simulate/real-estate/under-construction
POST /simulate/real-estate/ready
POST /simulate/mixed-strategy
```

#### Histórico do Usuário
```bash
GET /history/usuario@email.com?limit=10
```

#### Estatísticas Gerais
```bash
GET /stats
```

#### Status do Banco
```bash
GET /health/database
```

### Exemplo de Uso

```python
import requests

# Fazer simulação (salva automaticamente)
response = requests.post("https://seu-app.onrender.com/simulate/cdi", json={
    "aporte_inicial": 100000,
    "aporte_mensal": 3000,
    "taxa_cdi": 10.5,
    "anos": 20,
    "inflacao_anual": 4.5
})

result = response.json()
print(f"Simulação salva: {result['saved_to_database']}")

# Buscar histórico
history = requests.get("https://seu-app.onrender.com/history/meu@email.com")
print(f"Simulações anteriores: {len(history.json()['simulations'])}")

# Ver estatísticas
stats = requests.get("https://seu-app.onrender.com/stats")
print(f"Total de simulações: {stats.json()['total_simulations']}")
```

## 🔒 Segurança Configurada

### Row Level Security (RLS)
- ✅ Usuários só veem seus próprios dados
- ✅ Políticas de segurança automáticas
- ✅ Acesso público apenas para estatísticas

### Autenticação (Opcional)
```python
# Para implementar autenticação completa
from supabase import create_client

supabase = create_client(url, key)

# Registrar usuário
user = supabase.auth.sign_up({
    "email": "usuario@email.com",
    "password": "senha123"
})

# Login
session = supabase.auth.sign_in_with_password({
    "email": "usuario@email.com", 
    "password": "senha123"
})
```

## 📈 Monitoramento e Analytics

### Dashboard do Supabase
1. **Acesse "Database" → "Tables"**
2. **Visualize dados em tempo real**
3. **Execute queries personalizadas**

### Queries Úteis

#### Simulações mais populares:
```sql
SELECT strategy, COUNT(*) as total
FROM simulations 
GROUP BY strategy 
ORDER BY total DESC;
```

#### Usuários mais ativos:
```sql
SELECT u.email, COUNT(s.id) as simulations_count
FROM users u
LEFT JOIN simulations s ON u.id = s.user_id
GROUP BY u.id, u.email
ORDER BY simulations_count DESC;
```

#### Média de retorno por estratégia:
```sql
SELECT 
    strategy,
    AVG((result->>'patrimonio_final')::DECIMAL) as avg_final_value,
    AVG((result->>'rentabilidade_total')::DECIMAL) as avg_return
FROM simulations
GROUP BY strategy;
```

## 💰 Custos do Supabase

### Plano Gratuito
- ✅ 500MB de banco de dados
- ✅ 2GB de bandwidth
- ✅ 50MB de storage
- ✅ Até 50.000 usuários mensais
- ✅ Perfeito para começar

### Plano Pro ($25/mês)
- ✅ 8GB de banco de dados
- ✅ 250GB de bandwidth
- ✅ 100GB de storage
- ✅ Usuários ilimitados
- ✅ Backup automático

## 🔧 Manutenção

### Limpeza Automática
```sql
-- Executar mensalmente para limpar dados antigos
SELECT cleanup_old_simulations(365); -- Remove simulações > 1 ano
```

### Backup Manual
1. **No dashboard: "Settings" → "Database"**
2. **Clique "Download backup"**
3. **Arquivo SQL será baixado**

### Monitoramento
- **Logs em tempo real** no dashboard
- **Métricas de performance** automáticas
- **Alertas por email** configuráveis

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão
```
❌ Erro ao conectar Supabase
```
**Solução:** Verifique as variáveis de ambiente

#### 2. Erro de Permissão
```
❌ RLS policy violation
```
**Solução:** Verifique se as políticas RLS estão corretas

#### 3. Erro de Schema
```
❌ Table doesn't exist
```
**Solução:** Execute novamente o `supabase-setup.sql`

### Comandos de Diagnóstico

```python
# Testar conexão
python -c "from supabase_integration import supabase_client; print('Conectado:', supabase_client.is_connected())"

# Testar API
curl https://seu-app.onrender.com/health/database
```

## 🎯 Próximos Passos

1. **✅ Configurar Supabase** (este guia)
2. **🔄 Fazer deploy no Render** com variáveis de ambiente
3. **🧪 Testar integração** com simulações
4. **📊 Monitorar uso** no dashboard
5. **🚀 Implementar autenticação** (opcional)
6. **📱 Criar frontend** React (futuro)

## 🆘 Suporte

**Documentação Supabase:**
- https://supabase.com/docs

**Comunidade:**
- Discord: https://discord.supabase.com

**Status:**
- https://status.supabase.com

---

**Com o Supabase configurado, seu sistema terá persistência de dados profissional e escalável! 🗄️🚀**