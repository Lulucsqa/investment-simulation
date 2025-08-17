import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { TooltipProvider } from '@/components/ui/tooltip';
import { ResultsComparison } from '@/components/ResultsComparison';
import { FixedIncomeSimulator } from '@/components/simulators/FixedIncomeSimulator';
import { SimulationResult } from '@/types/investment';

// Mock toast notifications
vi.mock('sonner', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

// Mock calculations
vi.mock('@/lib/calculations', () => ({
  calculateFixedIncome: vi.fn(() => ({
    id: 'test-fixed-income',
    name: 'CDI 12.5% - 10 anos',
    type: 'fixed-income',
    finalValue: 150000,
    totalInvested: 100000,
    totalReturn: 50000,
    returnPercentage: 12.5,
    monthlyData: Array.from({ length: 120 }, (_, i) => ({
      month: i + 1,
      invested: 100000 + (i * 1000),
      grossValue: 100000 + (i * 1200),
      netValue: 100000 + (i * 1100),
      taxes: i * 100
    })),
    parameters: {},
    createdAt: new Date()
  })),
}));

const TestWrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <BrowserRouter>
          {children}
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

describe('Bug Fixes Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Gráfico de Evolução do Patrimônio', () => {
    const mockResults: SimulationResult[] = [
      {
        id: 'result-1',
        name: 'CDI 12.5% - 10 anos',
        type: 'fixed-income',
        finalValue: 150000,
        totalInvested: 100000,
        totalReturn: 50000,
        returnPercentage: 12.5,
        monthlyData: Array.from({ length: 12 }, (_, i) => ({
          month: i + 1,
          invested: 10000 + (i * 1000),
          grossValue: 10000 + (i * 1200),
          netValue: 10000 + (i * 1100),
          taxes: i * 100
        })),
        parameters: {},
        createdAt: new Date()
      },
      {
        id: 'result-2',
        name: 'Imobiliário Pronto - 20 anos',
        type: 'real-estate',
        finalValue: 200000,
        totalInvested: 120000,
        totalReturn: 80000,
        returnPercentage: 15.2,
        monthlyData: Array.from({ length: 12 }, (_, i) => ({
          month: i + 1,
          invested: 12000 + (i * 1000),
          grossValue: 12000 + (i * 1500),
          netValue: 12000 + (i * 1400),
          taxes: i * 50
        })),
        parameters: {},
        createdAt: new Date()
      }
    ];

    it('should render chart without overlapping data', () => {
      const mockOnClear = vi.fn();

      render(
        <TestWrapper>
          <ResultsComparison results={mockResults} onClear={mockOnClear} />
        </TestWrapper>
      );

      // Verificar se o título do gráfico está presente
      expect(screen.getByText('Evolução do Patrimônio')).toBeInTheDocument();

      // Verificar se os resultados estão sendo exibidos
      expect(screen.getByText('CDI 12.5% - 10 anos')).toBeInTheDocument();
      expect(screen.getByText('Imobiliário Pronto - 20 anos')).toBeInTheDocument();
    });

    it('should handle empty or invalid data gracefully', () => {
      const resultsWithInvalidData: SimulationResult[] = [
        {
          id: 'result-invalid',
          name: 'Teste com dados inválidos',
          type: 'fixed-income',
          finalValue: 0,
          totalInvested: 0,
          totalReturn: 0,
          returnPercentage: 0,
          monthlyData: [
            {
              month: 1,
              invested: 1000,
              grossValue: NaN, // Valor inválido
              netValue: 1100,
              taxes: 0
            },
            {
              month: 2,
              invested: 2000,
              grossValue: 2200,
              netValue: undefined as any, // Valor inválido
              taxes: 0
            }
          ],
          parameters: {},
          createdAt: new Date()
        }
      ];

      const mockOnClear = vi.fn();

      render(
        <TestWrapper>
          <ResultsComparison results={resultsWithInvalidData} onClear={mockOnClear} />
        </TestWrapper>
      );

      // O componente deve renderizar sem erros mesmo com dados inválidos
      expect(screen.getByText('Evolução do Patrimônio')).toBeInTheDocument();
    });

    it('should format currency values correctly in chart', () => {
      const mockOnClear = vi.fn();

      render(
        <TestWrapper>
          <ResultsComparison results={mockResults} onClear={mockOnClear} />
        </TestWrapper>
      );

      // Verificar se os valores estão formatados corretamente
      expect(screen.getByText(/R\$ 150\.000/)).toBeInTheDocument();
      expect(screen.getByText(/R\$ 200\.000/)).toBeInTheDocument();
    });

    it('should clear results when clear button is clicked', () => {
      const mockOnClear = vi.fn();

      render(
        <TestWrapper>
          <ResultsComparison results={mockResults} onClear={mockOnClear} />
        </TestWrapper>
      );

      const clearButton = screen.getByRole('button');
      fireEvent.click(clearButton);

      expect(mockOnClear).toHaveBeenCalledTimes(1);
    });
  });

  describe('Seletor IPCA+ Bug Fix', () => {
    it('should maintain IPCA+ selection when selected', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      // Encontrar o seletor de tipo de investimento
      const selectTrigger = screen.getByRole('combobox');
      expect(selectTrigger).toBeInTheDocument();

      // Clicar no seletor para abrir as opções
      fireEvent.click(selectTrigger);

      // Aguardar as opções aparecerem
      await waitFor(() => {
        expect(screen.getByText('IPCA+')).toBeInTheDocument();
      });

      // Selecionar IPCA+
      const ipcaOption = screen.getByText('IPCA+');
      fireEvent.click(ipcaOption);

      // Verificar se IPCA+ permanece selecionado
      await waitFor(() => {
        // O valor deve estar visível no trigger
        expect(selectTrigger).toHaveTextContent('IPCA+');
      });
    });

    it('should show correct label for IPCA+ interest rate', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      // Selecionar IPCA+
      const selectTrigger = screen.getByRole('combobox');
      fireEvent.click(selectTrigger);

      await waitFor(() => {
        expect(screen.getByText('IPCA+')).toBeInTheDocument();
      });

      const ipcaOption = screen.getByText('IPCA+');
      fireEvent.click(ipcaOption);

      // Verificar se o label da taxa mudou
      await waitFor(() => {
        expect(screen.getByText('Taxa IPCA+ (% a.a.)')).toBeInTheDocument();
      });
    });

    it('should show correct tax information for IPCA+', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      // Selecionar IPCA+
      const selectTrigger = screen.getByRole('combobox');
      fireEvent.click(selectTrigger);

      await waitFor(() => {
        expect(screen.getByText('IPCA+')).toBeInTheDocument();
      });

      const ipcaOption = screen.getByText('IPCA+');
      fireEvent.click(ipcaOption);

      // Verificar se a informação tributária está correta
      await waitFor(() => {
        expect(screen.getByText('IR aplicado apenas no vencimento')).toBeInTheDocument();
      });
    });

    it('should switch between CDI and IPCA+ correctly', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const selectTrigger = screen.getByRole('combobox');

      // Inicialmente deve estar CDI
      expect(selectTrigger).toHaveTextContent('CDI');

      // Mudar para IPCA+
      fireEvent.click(selectTrigger);
      await waitFor(() => {
        expect(screen.getByText('IPCA+')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByText('IPCA+'));
      await waitFor(() => {
        expect(selectTrigger).toHaveTextContent('IPCA+');
      });

      // Voltar para CDI
      fireEvent.click(selectTrigger);
      await waitFor(() => {
        expect(screen.getByText('CDI')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByText('CDI'));
      await waitFor(() => {
        expect(selectTrigger).toHaveTextContent('CDI');
      });
    });
  });

  describe('Data Validation and Error Handling', () => {
    it('should handle simulation with IPCA+ parameters', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      // Selecionar IPCA+
      const selectTrigger = screen.getByRole('combobox');
      fireEvent.click(selectTrigger);

      await waitFor(() => {
        expect(screen.getByText('IPCA+')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByText('IPCA+'));

      // Preencher alguns campos
      const initialAmountInput = screen.getByLabelText('Aporte Inicial (R$)');
      fireEvent.change(initialAmountInput, { target: { value: '10000' } });

      // Executar simulação
      const simulateButton = screen.getByText('Simular Investimento');
      fireEvent.click(simulateButton);

      await waitFor(() => {
        expect(mockOnResult).toHaveBeenCalled();
      });
    });

    it('should validate numeric inputs correctly', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      // Testar input inválido
      const initialAmountInput = screen.getByLabelText('Aporte Inicial (R$)');
      fireEvent.change(initialAmountInput, { target: { value: 'invalid' } });

      // O valor deve ser 0 ou o valor anterior
      expect(initialAmountInput).toHaveValue(0);
    });
  });

  describe('Chart Responsiveness', () => {
    it('should render chart with proper responsive container', () => {
      const mockOnClear = vi.fn();

      render(
        <TestWrapper>
          <ResultsComparison results={mockResults} onClear={mockOnClear} />
        </TestWrapper>
      );

      // Verificar se o container responsivo está presente
      const chartContainer = screen.getByText('Evolução do Patrimônio').closest('.h-80');
      expect(chartContainer).toBeInTheDocument();
      expect(chartContainer).toHaveClass('w-full');
    });
  });
});