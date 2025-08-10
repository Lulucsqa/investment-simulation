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

REM Instalar Vercel CLI
echo [INFO] Instalando Vercel CLI...
npm install -g vercel

REM Login no Vercel
echo.
echo [INFO] Fazendo login no Vercel...
vercel login

REM Deploy
echo.
echo [INFO] Fazendo deploy para o Vercel...
vercel --prod

echo.
echo 🎉 Deploy concluído!
echo.
echo 📊 Sua aplicação estará disponível na URL fornecida pelo Vercel
echo.
echo 📝 Comandos úteis:
echo    Ver deployments: vercel ls
echo    Ver logs: vercel logs
echo    Configurar domínio: vercel domains
echo.
pause