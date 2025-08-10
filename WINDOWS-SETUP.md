# Windows Setup Guide - Investment Simulation System

## 🚀 Quick Start para Windows

### Opção 1: Script Simples (Recomendado)
```cmd
start.cmd
```
- Funciona em qualquer versão do Windows
- Abre automaticamente no navegador
- Não requer configurações especiais

### Opção 2: PowerShell (Mais Recursos)
```powershell
.\deploy.ps1
```
- Mais opções de configuração
- Melhor feedback visual
- Suporte a modo produção

### Opção 3: Batch Script
```cmd
.\deploy.bat
```
- Script tradicional do Windows
- Compatível com CMD e PowerShell

## 🔧 Pré-requisitos

### 1. Docker Desktop
- **Download**: https://www.docker.com/products/docker-desktop
- **Requisitos**: Windows 10/11 com WSL2 ou Hyper-V
- **Configuração**: Ativar "Use Docker Compose V2"

### 2. Git (Opcional)
- **Download**: https://git-scm.com/download/win
- Necessário apenas se clonar o repositório

## ⚠️ Problemas Comuns e Soluções

### Erro: "não é reconhecido como comando"

**Problema**: PowerShell não encontra o script
```
deploy.bat : O termo 'deploy.bat' não é reconhecido...
```

**Solução**: Use `.\` antes do nome do script
```powershell
.\deploy.bat
.\deploy.ps1
```

### Erro: "Política de Execução"

**Problema**: PowerShell bloqueia scripts
```
não pode ser carregado porque a execução de scripts está desabilitada
```

**Solução 1 (Temporária)**:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\deploy.ps1
```

**Solução 2 (Permanente)**:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Docker não está rodando

**Problema**: 
```
error during connect: Get "http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.24/version"
```

**Solução**:
1. Abra Docker Desktop
2. Aguarde inicializar completamente
3. Execute o script novamente

### Porta já está em uso

**Problema**:
```
bind: address already in use
```

**Solução**:
```cmd
# Parar serviços existentes
docker-compose down

# Verificar o que está usando a porta
netstat -ano | findstr :80
netstat -ano | findstr :8000

# Matar processo se necessário
taskkill /PID <PID_NUMBER> /F
```

### WSL2 não configurado

**Problema**: Docker Desktop requer WSL2

**Solução**:
1. Abra PowerShell como Administrador
2. Execute:
```powershell
wsl --install
```
3. Reinicie o computador
4. Configure WSL2 como padrão:
```powershell
wsl --set-default-version 2
```

## 🎯 Verificação de Funcionamento

### 1. Teste Rápido
```cmd
# Verificar se os containers estão rodando
docker-compose ps

# Testar conectividade
curl http://localhost:8000
```

### 2. Health Check Completo
```cmd
python health-check.py
```

### 3. Dashboard em Tempo Real
```cmd
python status.py
```

## 📊 URLs de Acesso

Após deployment bem-sucedido:

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000  
- **Documentação API**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8000/redoc

## 🔄 Comandos de Gerenciamento

### Parar o Sistema
```cmd
docker-compose down
```

### Reiniciar Serviços
```cmd
docker-compose restart
```

### Ver Logs
```cmd
# Todos os serviços
docker-compose logs -f

# Apenas backend
docker-compose logs -f backend

# Apenas frontend  
docker-compose logs -f frontend
```

### Atualizar Sistema
```cmd
# Parar, reconstruir e iniciar
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🛠️ Desenvolvimento Local

### Backend Python (Standalone)
```cmd
# Instalar dependências
pip install -r requirements.txt

# Executar simulação
python main.py

# Executar API
uvicorn backend.api:app --reload --port 8000
```

### Frontend React (Standalone)
```cmd
cd frontend
npm install
npm run dev
```

## 🔍 Debugging

### Verificar Configuração Docker
```cmd
docker version
docker-compose version
docker-compose config
```

### Verificar Recursos do Sistema
```cmd
# Uso de memória pelos containers
docker stats

# Espaço em disco
docker system df

# Limpar recursos não utilizados
docker system prune -a
```

### Logs Detalhados
```cmd
# Logs com timestamps
docker-compose logs -f -t

# Logs apenas de erros
docker-compose logs --tail=50 | findstr ERROR
```

## 📞 Suporte

Se os problemas persistirem:

1. **Verifique os logs**: `docker-compose logs -f`
2. **Teste conectividade**: `curl http://localhost:8000`
3. **Reinicie Docker Desktop**
4. **Execute health check**: `python health-check.py`
5. **Consulte documentação**: `DEPLOYMENT.md`

## 🎉 Próximos Passos

Após deployment bem-sucedido:

1. **Acesse o sistema**: http://localhost
2. **Explore a API**: http://localhost:8000/docs
3. **Execute simulações**: Use a interface web
4. **Monitore status**: `python status.py`
5. **Personalize configurações**: Edite `.env`

---

**Deployment bem-sucedido! 🚀**