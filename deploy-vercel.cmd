@echo off
REM Deploy para Vercel - Investment Simulation System

echo 🚀 Deploy para Vercel - Investment Simulation System
echo ===================================================
echo.

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js não está instalado
    echo.
    echo 📥 Instale o Node.js:
    echo    1. Acesse: https://nodejs.org/
    echo    2. Baixe e instale a versão LTS
    echo    3. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo [INFO] Node.js encontrado ✅
echo.

REM Verificar se npm está funcionando
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm não está funcionando
    pause
    exit /b 1
)

echo [INFO] npm encontrado ✅
echo.

REM Instalar dependências se necessário
if not exist "node_modules" (
    echo [INFO] Instalando dependências...
    npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Falha ao instalar dependências
        pause
        exit /b 1
    )
)

REM Fazer build local para testar
echo [INFO] Fazendo build local para testar...
npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Falha no build local
    echo Verifique os erros acima e corrija antes de fazer deploy
    pause
    exit /b 1
)

echo [INFO] Build local bem-sucedido ✅
echo.

REM Instalar Vercel CLI
echo [INFO] Instalando/atualizando Vercel CLI...
npm install -g vercel@latest

REM Verificar se Vercel CLI foi instalado
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Falha ao instalar Vercel CLI
    pause
    exit /b 1
)

echo [INFO] Vercel CLI instalado ✅
echo.

REM Login no Vercel
echo [INFO] Fazendo login no Vercel...
echo (Se já estiver logado, isso será pulado automaticamente)
vercel login

REM Deploy
echo.
echo [INFO] Fazendo deploy para o Vercel...
echo [INFO] Configuração será detectada automaticamente do vercel.json
vercel --prod

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Deploy concluído com sucesso!
    echo.
    echo 📊 Sua aplicação estará disponível na URL fornecida pelo Vercel
    echo.
    echo 📝 Comandos úteis:
    echo    Ver deployments: vercel ls
    echo    Ver logs: vercel logs [URL]
    echo    Configurar domínio: vercel domains
    echo    Cancelar deployment: vercel rm [deployment-url]
) else (
    echo.
    echo ❌ Falha no deploy
    echo Verifique os erros acima e tente novamente
)

echo.
pause