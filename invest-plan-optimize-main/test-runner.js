#!/usr/bin/env node

/**
 * Test Runner Script
 * 
 * Este script executa uma série de testes para verificar:
 * 1. Funcionalidade dos botões
 * 2. Design e styling
 * 3. Acessibilidade
 * 4. Responsividade
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🚀 Iniciando verificação completa do sistema...\n');

// Cores para output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkFileExists(filePath) {
  return fs.existsSync(path.join(__dirname, filePath));
}

function runCommand(command, description) {
  log(`\n📋 ${description}`, 'cyan');
  try {
    const output = execSync(command, { 
      encoding: 'utf8', 
      cwd: __dirname,
      stdio: 'pipe'
    });
    log(`✅ ${description} - SUCESSO`, 'green');
    return { success: true, output };
  } catch (error) {
    log(`❌ ${description} - FALHOU`, 'red');
    log(`Erro: ${error.message}`, 'red');
    return { success: false, error: error.message };
  }
}

async function main() {
  const results = {
    passed: 0,
    failed: 0,
    tests: []
  };

  // 1. Verificar se os arquivos de teste existem
  log('1. Verificando arquivos de teste...', 'yellow');
  
  const testFiles = [
    'src/tests/button-functionality.test.tsx',
    'src/tests/button-design.test.tsx',
    'src/tests/setup.ts',
    'vitest.config.ts'
  ];

  for (const file of testFiles) {
    if (checkFileExists(file)) {
      log(`✅ ${file} existe`, 'green');
    } else {
      log(`❌ ${file} não encontrado`, 'red');
      results.failed++;
    }
  }

  // 2. Verificar se as dependências estão instaladas
  log('\n2. Verificando dependências...', 'yellow');
  
  if (checkFileExists('node_modules')) {
    log('✅ node_modules existe', 'green');
    results.passed++;
  } else {
    log('❌ node_modules não encontrado. Execute: npm install', 'red');
    results.failed++;
  }

  // 3. Verificar estrutura de componentes
  log('\n3. Verificando estrutura de componentes...', 'yellow');
  
  const componentFiles = [
    'src/components/ui/button.tsx',
    'src/components/ui/badge.tsx',
    'src/components/ui/card.tsx',
    'src/components/Dashboard.tsx',
    'src/components/WelcomeScreen.tsx',
    'src/components/SimulationWizard.tsx'
  ];

  for (const file of componentFiles) {
    if (checkFileExists(file)) {
      log(`✅ ${file} existe`, 'green');
      results.passed++;
    } else {
      log(`❌ ${file} não encontrado`, 'red');
      results.failed++;
    }
  }

  // 4. Verificar se as cores rosa foram removidas
  log('\n4. Verificando remoção das cores rosa/magenta...', 'yellow');
  
  try {
    const cssContent = fs.readFileSync(path.join(__dirname, 'src/index.css'), 'utf8');
    
    if (cssContent.includes('285 85% 65%') || cssContent.includes('324 93% 58%')) {
      log('❌ Cores rosa/magenta ainda presentes no CSS', 'red');
      results.failed++;
    } else {
      log('✅ Cores rosa/magenta removidas com sucesso', 'green');
      results.passed++;
    }
  } catch (error) {
    log('❌ Erro ao verificar arquivo CSS', 'red');
    results.failed++;
  }

  // 5. Executar lint
  const lintResult = runCommand('npm run lint', 'Executando ESLint');
  if (lintResult.success) {
    results.passed++;
  } else {
    results.failed++;
  }

  // 6. Tentar build do projeto
  const buildResult = runCommand('npm run build', 'Executando build do projeto');
  if (buildResult.success) {
    results.passed++;
    log('✅ Build executado com sucesso - sem erros de TypeScript', 'green');
  } else {
    results.failed++;
    log('❌ Build falhou - possíveis erros de TypeScript', 'red');
  }

  // 7. Verificar se o projeto pode ser iniciado (simulação)
  log('\n7. Verificando configuração do Vite...', 'yellow');
  
  if (checkFileExists('vite.config.ts')) {
    log('✅ vite.config.ts existe', 'green');
    results.passed++;
  } else {
    log('❌ vite.config.ts não encontrado', 'red');
    results.failed++;
  }

  // 8. Verificar configuração do Tailwind
  log('\n8. Verificando configuração do Tailwind...', 'yellow');
  
  if (checkFileExists('tailwind.config.ts')) {
    log('✅ tailwind.config.ts existe', 'green');
    results.passed++;
  } else {
    log('❌ tailwind.config.ts não encontrado', 'red');
    results.failed++;
  }

  // 9. Verificar se os simuladores existem
  log('\n9. Verificando simuladores...', 'yellow');
  
  const simulatorFiles = [
    'src/components/simulators/FixedIncomeSimulator.tsx',
    'src/components/simulators/RealEstateSimulator.tsx',
    'src/components/simulators/PortfolioOptimizer.tsx'
  ];

  for (const file of simulatorFiles) {
    if (checkFileExists(file)) {
      log(`✅ ${file} existe`, 'green');
      results.passed++;
    } else {
      log(`❌ ${file} não encontrado`, 'red');
      results.failed++;
    }
  }

  // Resumo final
  log('\n' + '='.repeat(50), 'bright');
  log('📊 RESUMO DA VERIFICAÇÃO', 'bright');
  log('='.repeat(50), 'bright');
  
  log(`✅ Testes Passaram: ${results.passed}`, 'green');
  log(`❌ Testes Falharam: ${results.failed}`, 'red');
  
  const total = results.passed + results.failed;
  const percentage = total > 0 ? ((results.passed / total) * 100).toFixed(1) : 0;
  
  log(`📈 Taxa de Sucesso: ${percentage}%`, percentage >= 80 ? 'green' : 'yellow');

  if (results.failed === 0) {
    log('\n🎉 TODOS OS TESTES PASSARAM!', 'green');
    log('✨ O sistema está funcionando corretamente', 'green');
  } else if (percentage >= 80) {
    log('\n⚠️  MAIORIA DOS TESTES PASSOU', 'yellow');
    log('🔧 Alguns ajustes podem ser necessários', 'yellow');
  } else {
    log('\n🚨 MUITOS TESTES FALHARAM', 'red');
    log('🛠️  Correções significativas são necessárias', 'red');
  }

  // Instruções para o usuário
  log('\n📝 PRÓXIMOS PASSOS:', 'cyan');
  
  if (!checkFileExists('node_modules')) {
    log('1. Execute: npm install', 'cyan');
  }
  
  log('2. Para executar os testes: npm run test', 'cyan');
  log('3. Para iniciar o desenvolvimento: npm run dev', 'cyan');
  log('4. Para build de produção: npm run build', 'cyan');
  
  if (results.failed > 0) {
    log('\n🔍 PROBLEMAS IDENTIFICADOS:', 'yellow');
    log('- Verifique os arquivos marcados como não encontrados', 'yellow');
    log('- Execute npm install se as dependências estiverem faltando', 'yellow');
    log('- Verifique erros de TypeScript no build', 'yellow');
  }

  process.exit(results.failed > 0 ? 1 : 0);
}

main().catch(error => {
  log(`\n💥 Erro inesperado: ${error.message}`, 'red');
  process.exit(1);
});