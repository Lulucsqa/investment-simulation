# 🚀 Deploy no Vercel - Passo a Passo

## ✅ Pré-requisitos Verificados
- ✅ Node.js instalado
- ✅ npm funcionando
- ✅ Vercel CLI instalado (v44.7.3)
- ✅ Build local funcionando
- ✅ Estrutura do projeto correta
- ✅ Variáveis de ambiente configuradas

## 📋 Passos para Deploy

### 1. Fazer Login no Vercel
```cmd
vercel login
```
- Isso abrirá seu navegador
- Faça login com GitHub, GitLab ou email
- Autorize o Vercel CLI

### 2. Fazer o Deploy
```cmd
vercel --prod
```

### 3. Configurar o Projeto (primeira vez)
O Vercel fará algumas perguntas:

**"Set up and deploy?"** → Digite `Y` e pressione Enter

**"Which scope?"** → Escolha sua conta (geralmente a primeira opção)

**"Link to existing project?"** → Digite `N` (para novo projeto)

**"What's your project's name?"** → Digite: `investment-simulation` ou outro nome

**"In which directory is your code located?"** → Pressione Enter (usa o diretório atual)

### 4. Aguardar o Deploy
- O Vercel fará o build automaticamente
- Mostrará o progresso em tempo real
- No final, fornecerá a URL da aplicação

## 🎯 Resultado Esperado

Você verá algo como:
```
✅ Production: https://investment-simulation-abc123.vercel.app [copied to clipboard] [2m 15s]
```

## 🔧 Se Houver Problemas

### Erro de Build
```cmd
# Limpe e reinstale dependências
rmdir /s /q node_modules
npm install
npm run build
vercel --prod
```

### Erro de Variáveis de Ambiente
1. Acesse: https://vercel.com/dashboard
2. Clique no seu projeto
3. Vá em Settings → Environment Variables
4. Adicione:
   - `VITE_SUPABASE_URL`: `https://kjcqoxlusfcndmdtjsks.supabase.co`
   - `VITE_SUPABASE_KEY`: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqY3FveGx1c2ZjbmRtZHRqc2tzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0OTY2MzEsImV4cCI6MjA3MDA3MjYzMX0.p77UoH_KZfaDV4AFDiRbaGELm5epLUx6HMyVpaljZJg`

### Erro de Permissão
```cmd
# Execute como administrador ou use:
npx vercel --prod
```

## 📱 Comandos Úteis Pós-Deploy

```cmd
# Ver todos os deployments
vercel ls

# Ver logs do último deploy
vercel logs

# Fazer novo deploy
vercel --prod

# Configurar domínio personalizado
vercel domains add meudominio.com
```

## 🌐 Testando a Aplicação

Após o deploy:
1. Acesse a URL fornecida
2. Teste as funcionalidades principais
3. Verifique se o Supabase está conectado
4. Teste a simulação de investimentos

## 💡 Dicas

- **Deploy automático**: Conecte seu repositório Git para deploys automáticos
- **Preview deploys**: Use `vercel` (sem --prod) para deploys de teste
- **Domínio personalizado**: Configure gratuitamente no dashboard
- **Analytics**: Ative no dashboard para ver métricas de uso

## 🆘 Suporte

Se precisar de ajuda:
1. Consulte: `VERCEL_TROUBLESHOOTING.md`
2. Logs detalhados: `vercel logs [URL]`
3. Documentação: https://vercel.com/docs