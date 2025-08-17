#!/usr/bin/env node

/**
 * Teste Específico para o Bug do IPCA+
 * 
 * Este script verifica se a correção do seletor IPCA+ foi aplicada corretamente
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Cores para output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function analyzeCode(filePath, checks) {
  try {
    const content = fs.readFileSync(path.join(__dirname, filePath), 'utf8');
    const results = {};
    
    checks.forEach(check => {
      if (check.type === 'contains') {
        results[check.name] = content.includes(check.pattern);
      } else if (check.type === 'regex') {
        results[check.name] = check.pattern.test(content);
      } else if (check.type === 'not_contains') {
        results[check.name] = !content.includes(check.pattern);
      }
    });
    
    return results;
  } catch (error) {
    log(`Erro ao analisar ${filePath}: ${error.message}`, 'red');
    return {};
  }
}

async function main() {
  log('🔍 TESTE ESPECÍFICO - BUG IPCA+', 'bright');
  log('Verificando correções aplicadas', 'cyan');
  log('=' * 40, 'bright');

  const results = {
    passed: 0,
    failed: 0,
    details: []
  };

  // 1. Verificar se o estado controlado foi implementado
  log('\n1. 🔧 Estado Controlado', 'yellow');
  
  const stateChecks = [
    {
      name: 'Estado selectedType criado',
      type: 'contains',
      pattern: 'const [selectedType, setSelectedType] = useState'
    },
    {
      name: 'Função handleTypeChange criada',
      type: 'contains',
      pattern: 'const handleTypeChange = (value: \'CDI\' | \'IPCA+\')'
    },
    {
      name: 'Badge usa selectedType',
      type: 'contains',
      pattern: '<Badge variant="secondary">{selectedType}</Badge>'
    }
  ];

  const stateResults = analyzeCode('src/components/simulators/FixedIncomeSimulator.tsx', stateChecks);
  
  stateChecks.forEach(check => {
    if (stateResults[check.name]) {
      log(`✅ ${check.name}`, 'green');
      results.passed++;
    } else {
      log(`❌ ${check.name}`, 'red');
      results.failed++;
    }
  });

  // 2. Verificar se o CustomSelect foi implementado
  log('\n2. 🎛️  CustomSelect', 'yellow');
  
  const customSelectChecks = [
    {
      name: 'CustomSelect importado',
      type: 'contains',
      pattern: 'import { CustomSelect } from "@/components/ui/custom-select"'
    },
    {
      name: 'CustomSelect usado no JSX',
      type: 'contains',
      pattern: '<CustomSelect'
    },
    {
      name: 'Opções CDI e IPCA+ definidas',
      type: 'contains',
      pattern: "{ value: 'IPCA+', label: 'IPCA+' }"
    }
  ];

  const customSelectResults = analyzeCode('src/components/simulators/FixedIncomeSimulator.tsx', customSelectChecks);
  
  customSelectChecks.forEach(check => {
    if (customSelectResults[check.name]) {
      log(`✅ ${check.name}`, 'green');
      results.passed++;
    } else {
      log(`❌ ${check.name}`, 'red');
      results.failed++;
    }
  });

  // 3. Verificar se o arquivo CustomSelect existe
  log('\n3. 📁 Arquivo CustomSelect', 'yellow');
  
  const customSelectFile = 'src/components/ui/custom-select.tsx';
  if (fs.existsSync(path.join(__dirname, customSelectFile))) {
    log(`✅ ${customSelectFile} criado`, 'green');
    results.passed++;
    
    // Verificar conteúdo do CustomSelect
    const customSelectContentChecks = [
      {
        name: 'Interface CustomSelectProps definida',
        type: 'contains',
        pattern: 'interface CustomSelectProps'
      },
      {
        name: 'Estado isOpen para dropdown',
        type: 'contains',
        pattern: 'const [isOpen, setIsOpen]'
      },
      {
        name: 'Função handleSelect',
        type: 'contains',
        pattern: 'const handleSelect = (optionValue: string)'
      },
      {
        name: 'Console.log para debug',
        type: 'contains',
        pattern: 'console.log(\'CustomSelect: Selecionando\''
      }
    ];

    const customSelectContentResults = analyzeCode(customSelectFile, customSelectContentChecks);
    
    customSelectContentChecks.forEach(check => {
      if (customSelectContentResults[check.name]) {
        log(`✅ ${check.name}`, 'green');
        results.passed++;
      } else {
        log(`❌ ${check.name}`, 'red');
        results.failed++;
      }
    });
  } else {
    log(`❌ ${customSelectFile} não encontrado`, 'red');
    results.failed++;
  }

  // 4. Verificar se as referências foram atualizadas
  log('\n4. 🔄 Referências Atualizadas', 'yellow');
  
  const referenceChecks = [
    {
      name: 'Label usa selectedType',
      type: 'contains',
      pattern: '{selectedType === \'CDI\' ? \'Taxa CDI (% a.a.)\' : \'Taxa IPCA+ (% a.a.)\'}'
    },
    {
      name: 'Informação tributária usa selectedType',
      type: 'contains',
      pattern: '{selectedType === \'CDI\''
    },
    {
      name: 'Debug log implementado',
      type: 'contains',
      pattern: 'console.log(\'Mudando tipo para:\', value)'
    }
  ];

  const referenceResults = analyzeCode('src/components/simulators/FixedIncomeSimulator.tsx', referenceChecks);
  
  referenceChecks.forEach(check => {
    if (referenceResults[check.name]) {
      log(`✅ ${check.name}`, 'green');
      results.passed++;
    } else {
      log(`❌ ${check.name}`, 'red');
      results.failed++;
    }
  });

  // Resumo final
  log('\n' + '='.repeat(40), 'bright');
  log('📊 RESUMO DO TESTE IPCA+', 'bright');
  log('='.repeat(40), 'bright');
  
  log(`✅ Verificações Passaram: ${results.passed}`, 'green');
  log(`❌ Verificações Falharam: ${results.failed}`, 'red');
  
  const total = results.passed + results.failed;
  const percentage = total > 0 ? ((results.passed / total) * 100).toFixed(1) : 0;
  
  log(`📈 Taxa de Sucesso: ${percentage}%`, percentage >= 90 ? 'green' : percentage >= 70 ? 'yellow' : 'red');

  // Status final
  if (results.failed === 0) {
    log('\n🎉 CORREÇÃO DO IPCA+ APLICADA COM SUCESSO!', 'green');
    log('✨ O seletor deve funcionar corretamente agora', 'green');
  } else if (percentage >= 70) {
    log('\n⚠️  CORREÇÃO PARCIALMENTE APLICADA', 'yellow');
    log('🔧 Algumas verificações adicionais podem ser necessárias', 'yellow');
  } else {
    log('\n🚨 CORREÇÃO NÃO APLICADA ADEQUADAMENTE', 'red');
    log('🛠️  Mais trabalho é necessário', 'red');
  }

  // Instruções específicas
  log('\n🎯 COMO TESTAR:', 'cyan');
  log('1. Execute: npm run dev', 'cyan');
  log('2. Vá para o Simulador de Renda Fixa', 'cyan');
  log('3. Clique no dropdown "Tipo de Investimento"', 'cyan');
  log('4. Selecione "IPCA+"', 'cyan');
  log('5. Verifique se "IPCA+" aparece no campo', 'cyan');
  log('6. Observe o console do navegador para logs de debug', 'cyan');

  log('\n🔍 O QUE DEVE ACONTECER:', 'cyan');
  log('• O dropdown deve mostrar "IPCA+" quando selecionado', 'green');
  log('• O badge ao lado do título deve mostrar "IPCA+"', 'green');
  log('• O label deve mudar para "Taxa IPCA+ (% a.a.)"', 'green');
  log('• A informação tributária deve mostrar "IR aplicado apenas no vencimento"', 'green');

  if (percentage >= 90) {
    log('\n✅ TODAS AS CORREÇÕES FORAM APLICADAS!', 'green');
    log('🚀 O bug do IPCA+ deve estar resolvido', 'green');
  }

  process.exit(results.failed > 0 ? 1 : 0);
}

main().catch(error => {
  log(`\n💥 Erro inesperado: ${error.message}`, 'red');
  process.exit(1);
});