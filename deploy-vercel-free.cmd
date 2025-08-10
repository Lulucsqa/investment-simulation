@echo off
REM Deploy gratuito no Vercel

echo 🚀 Deploy GRATUITO no Vercel - Investment Simulation System
echo ===========================================================

echo.
echo ✅ Vercel oferece:
echo    - Plano gratuito generoso
echo    - Deploy ultra-rápido
echo    - CDN global
echo    - Domínio personalizado gratuito
echo.

echo 📋 Passos para deploy:
echo.
echo 1. Instale Node.js se não tiver: https://nodejs.org/
echo 2. Instale Vercel CLI: npm install -g vercel
echo 3. Execute: vercel login
echo 4. Execute: vercel --prod
echo 5. Siga as instruções no terminal
echo.

echo 🌐 Sua aplicação estará disponível em:
echo    https://investment-simulation.vercel.app
echo.

echo 💰 Custo: GRATUITO
echo.

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado
    echo 📥 Instale Node.js primeiro: https://nodejs.org/
    set /p choice="Pressione Enter para abrir Node.js no navegador..."
    start https://nodejs.org/
) else (
    echo ✅ Node.js encontrado
    echo.
    echo Instalando Vercel CLI...
    npm install -g vercel
    echo.
    echo Execute agora: vercel login
    echo Depois: vercel --prod
)

pause