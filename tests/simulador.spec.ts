import { test, expect } from '@playwright/test';

test.describe('Simulador de Investimentos', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('deve permitir simular investimento em renda fixa', async ({ page }) => {
    // Seleciona tipo de investimento
    await page.selectOption('select[name="investment-type"]', 'IPCA+');
    
    // Preenche os valores
    await page.fill('input[name="initial-value"]', '1000');
    await page.fill('input[name="monthly-contribution"]', '100');
    await page.fill('input[name="period"]', '12');
    await page.fill('input[name="interest-rate"]', '12');

    // Verifica se o gráfico é atualizado
    await expect(page.locator('.recharts-surface')).toBeVisible();
    
    // Verifica se os resultados são exibidos
    await expect(page.locator('text=Valor Total')).toBeVisible();
    await expect(page.locator('text=Total Investido')).toBeVisible();
    await expect(page.locator('text=Juros Totais')).toBeVisible();
  });

  test('deve validar campos obrigatórios', async ({ page }) => {
    // Tenta simular sem preencher os campos
    await page.click('button:has-text("Simular")');
    
    // Verifica mensagens de erro
    await expect(page.locator('text=Valor inicial deve ser maior que zero')).toBeVisible();
    await expect(page.locator('text=Período deve estar entre 1 e 600 meses')).toBeVisible();
    await expect(page.locator('text=Taxa deve estar entre 0% e 50% a.a.')).toBeVisible();
  });

  test('deve calcular corretamente os valores', async ({ page }) => {
    // Preenche valores conhecidos
    await page.selectOption('select[name="investment-type"]', 'Prefixado');
    await page.fill('input[name="initial-value"]', '1000');
    await page.fill('input[name="monthly-contribution"]', '100');
    await page.fill('input[name="period"]', '12');
    await page.fill('input[name="interest-rate"]', '10');

    // Valores esperados (calculados previamente)
    const expectedTotal = 'R$ 2.321,47'; // Valor aproximado
    const expectedInvested = 'R$ 2.200,00';
    
    // Verifica os resultados
    await expect(page.locator('text=' + expectedTotal)).toBeVisible();
    await expect(page.locator('text=' + expectedInvested)).toBeVisible();
  });

  test('deve persistir simulação no Supabase', async ({ page }) => {
    // Faz login (assumindo que existe uma função de helper)
    await loginUser(page);
    
    // Realiza simulação
    await page.selectOption('select[name="investment-type"]', 'IPCA+');
    await page.fill('input[name="initial-value"]', '1000');
    await page.fill('input[name="monthly-contribution"]', '100');
    await page.fill('input[name="period"]', '12');
    await page.fill('input[name="interest-rate"]', '12');
    
    // Salva simulação
    await page.click('button:has-text("Salvar Simulação")');
    
    // Verifica se aparece na lista de simulações
    await page.click('text=Minhas Simulações');
    await expect(page.locator('text=IPCA+ 12% - 1 ano')).toBeVisible();
  });
});

// Helpers
async function loginUser(page) {
  // Implementar lógica de login
  await page.goto('/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button:has-text("Entrar")');
  await expect(page.locator('text=Dashboard')).toBeVisible();
}
