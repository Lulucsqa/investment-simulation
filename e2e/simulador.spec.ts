import { test, expect } from '@playwright/test';

test('fluxo básico do simulador de investimentos', async ({ page }) => {
  // Navega para a página inicial
  await page.goto('/');

  // Verifica se o título está presente
  await expect(page).toHaveTitle(/Simulador/);

  // Preenche os campos do formulário
  await page.getByLabel('Valor Inicial').fill('1000');
  await page.getByLabel('Aporte Mensal').fill('100');
  await page.getByLabel('Taxa de Juros (%)').fill('0.5');
  await page.getByLabel('Período (meses)').fill('12');

  // Clica no botão de simular
  await page.getByRole('button', { name: 'Simular' }).click();

  // Verifica se o gráfico é renderizado
  await expect(page.getByTestId('investment-chart')).toBeVisible();

  // Verifica se a tabela de resultados é exibida
  await expect(page.getByTestId('results-table')).toBeVisible();

  // Verifica alguns valores específicos nos resultados
  const resultadoFinal = await page.getByTestId('valor-final').textContent();
  expect(Number(resultadoFinal?.replace('R$ ', '').replace('.', '').replace(',', '.'))).toBeGreaterThan(1000);
});
