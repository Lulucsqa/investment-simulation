# Guia de Troubleshooting - Deploy Vercel

## Problemas Comuns e Soluções

### 1. "Cannot find package.json"
**Problema**: Vercel não encontra o package.json no diretório correto.

**Solução**:
```cmd
# Execute o script de preparação
prepare-vercel.cmd
```

### 2. "Build failed"
**Problema**: Falha durante o processo de build.

**Soluções**:
- Verifique se todas as dependências estão instaladas:
  ```cmd
  npm install
  ```
- Teste o build localmente:
  ```cmd
  npm run build
  ```
- Verifique se as variáveis de ambiente estão configuradas no Vercel

### 3. "Environment variables not found"
**Problema**: Variáveis de ambiente do Supabase não estão configuradas.

**Solução**:
1. Acesse o dashboard do Vercel
2. Vá em Settings > Environment Variables
3. Adicione:
   - `VITE_SUPABASE_URL`: https://kjcqoxlusfcndmdtjsks.supabase.co
   - `VITE_SUPABASE_KEY`: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

### 4. "Vercel CLI not found"
**Problema**: Comando vercel não é reconhecido.

**Solução**:
```cmd
# Instalar Vercel CLI globalmente
npm install -g vercel@latest

# Verificar instalação
vercel --version
```

### 5. "Login failed"
**Problema**: Não consegue fazer login no Vercel.

**Soluções**:
- Use o navegador para login:
  ```cmd
  vercel login
  ```
- Ou use token de acesso:
  ```cmd
  vercel --token YOUR_TOKEN
  ```

### 6. "Deployment timeout"
**Problema**: Deploy demora muito ou falha por timeout.

**Soluções**:
- Verifique o tamanho do projeto (limite: 100MB)
- Remova node_modules antes do deploy:
  ```cmd
  rmdir /s /q node_modules
  vercel --prod
  ```

## Scripts de Deploy Disponíveis

### Deploy Completo
```cmd
deploy-vercel.cmd
```

### Deploy Gratuito (com instruções)
```cmd
deploy-vercel-free.cmd
```

### Preparação do Projeto
```cmd
prepare-vercel.cmd
```

## Comandos Úteis do Vercel

```cmd
# Login
vercel login

# Deploy de produção
vercel --prod

# Deploy de preview
vercel

# Listar deployments
vercel ls

# Ver logs
vercel logs [URL]

# Remover deployment
vercel rm [URL]

# Configurar domínio
vercel domains

# Ver informações do projeto
vercel inspect [URL]
```

## Estrutura de Arquivos para Vercel

O projeto deve ter esta estrutura no root:
```
├── package.json          # Dependências e scripts
├── vite.config.ts        # Configuração do Vite
├── tsconfig.json         # Configuração TypeScript
├── index.html            # HTML principal
├── vercel.json           # Configuração do Vercel
├── .env                  # Variáveis de ambiente
├── src/                  # Código fonte React
├── public/               # Arquivos estáticos
└── dist/                 # Build output (gerado)
```

## Verificação Pré-Deploy

Antes de fazer deploy, execute:

1. **Teste local**:
   ```cmd
   npm run build
   npm run preview
   ```

2. **Verificar arquivos**:
   - ✅ package.json existe
   - ✅ vite.config.ts existe
   - ✅ src/ existe
   - ✅ public/ existe
   - ✅ index.html existe

3. **Verificar variáveis de ambiente**:
   - ✅ .env existe com VITE_SUPABASE_URL
   - ✅ .env existe com VITE_SUPABASE_KEY

## Contato e Suporte

Se os problemas persistirem:
1. Verifique os logs do Vercel: `vercel logs [URL]`
2. Consulte a documentação: https://vercel.com/docs
3. Execute `prepare-vercel.cmd` para reconfigurar o projeto