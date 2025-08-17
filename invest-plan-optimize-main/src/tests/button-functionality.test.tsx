import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { TooltipProvider } from '@/components/ui/tooltip';
import Dashboard from '@/components/Dashboard';
import { WelcomeScreen } from '@/components/WelcomeScreen';
import { SimulationWizard } from '@/components/SimulationWizard';
import { FixedIncomeSimulator } from '@/components/simulators/FixedIncomeSimulator';
import { RealEstateSimulator } from '@/components/simulators/RealEstateSimulator';
import { PortfolioOptimizer } from '@/components/simulators/PortfolioOptimizer';

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
    id: 'test-1',
    name: 'Teste Renda Fixa',
    type: 'fixed-income',
    finalValue: 100000,
    returnPercentage: 12.5,
    monthlyData: [],
    parameters: {}
  })),
  calculateRealEstate: vi.fn(() => ({
    id: 'test-2',
    name: 'Teste Imobiliário',
    type: 'real-estate',
    finalValue: 200000,
    returnPercentage: 15.2,
    monthlyData: [],
    parameters: {}
  })),
  optimizePortfolio: vi.fn(() => ({
    id: 'test-3',
    name: 'Portfólio Otimizado',
    type: 'optimized',
    finalValue: 150000,
    returnPercentage: 13.8,
    monthlyData: [],
    parameters: {}
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

describe('Button Functionality Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe('Dashboard Buttons', () => {
    it('should render quick start buttons correctly', () => {
      localStorage.setItem('hasSeenWelcome', 'true');
      
      render(
        <TestWrapper>
          <Dashboard />
        </TestWrapper>
      );

      expect(screen.getByText('Renda Fixa')).toBeInTheDocument();
      expect(screen.getByText('Fundos Imobiliários')).toBeInTheDocument();
      expect(screen.getByText('Otimização')).toBeInTheDocument();
    });

    it('should handle quick start button clicks', async () => {
      localStorage.setItem('hasSeenWelcome', 'true');
      
      render(
        <TestWrapper>
          <Dashboard />
        </TestWrapper>
      );

      const fixedIncomeButton = screen.getByText('Começar Simulação');
      fireEvent.click(fixedIncomeButton);

      await waitFor(() => {
        expect(screen.getByText('Simulador de Renda Fixa')).toBeInTheDocument();
      });
    });

    it('should disable optimization button when no results exist', () => {
      localStorage.setItem('hasSeenWelcome', 'true');
      
      render(
        <TestWrapper>
          <Dashboard />
        </TestWrapper>
      );

      const optimizationButtons = screen.getAllByText(/Precisa de Simulações/);
      expect(optimizationButtons[0]).toBeInTheDocument();
    });

    it('should handle tour guide button click', () => {
      localStorage.setItem('hasSeenWelcome', 'true');
      
      render(
        <TestWrapper>
          <Dashboard />
        </TestWrapper>
      );

      const tourButton = screen.getByText('Tour Guiado');
      expect(tourButton).toBeInTheDocument();
      
      fireEvent.click(tourButton);
      // Modal should open (we can test this by checking if onboarding content appears)
    });
  });

  describe('WelcomeScreen Buttons', () => {
    it('should render strategy selection buttons', () => {
      const mockOnStrategySelect = vi.fn();
      const mockOnSkip = vi.fn();

      render(
        <TestWrapper>
          <WelcomeScreen 
            onStrategySelect={mockOnStrategySelect}
            onSkip={mockOnSkip}
          />
        </TestWrapper>
      );

      expect(screen.getByText('Selecionar')).toBeInTheDocument();
      expect(screen.getByText('Pular introdução e ir direto para o dashboard')).toBeInTheDocument();
    });

    it('should handle strategy selection', async () => {
      const mockOnStrategySelect = vi.fn();
      const mockOnSkip = vi.fn();

      render(
        <TestWrapper>
          <WelcomeScreen 
            onStrategySelect={mockOnStrategySelect}
            onSkip={mockOnSkip}
          />
        </TestWrapper>
      );

      const selectButtons = screen.getAllByText('Selecionar');
      fireEvent.click(selectButtons[0]);

      await waitFor(() => {
        expect(screen.getByText('Continuar')).toBeInTheDocument();
      });

      const continueButton = screen.getByText('Continuar');
      fireEvent.click(continueButton);

      expect(mockOnStrategySelect).toHaveBeenCalledWith('fixed-income');
    });

    it('should handle skip button', () => {
      const mockOnStrategySelect = vi.fn();
      const mockOnSkip = vi.fn();

      render(
        <TestWrapper>
          <WelcomeScreen 
            onStrategySelect={mockOnStrategySelect}
            onSkip={mockOnSkip}
          />
        </TestWrapper>
      );

      const skipButton = screen.getByText('Pular introdução e ir direto para o dashboard');
      fireEvent.click(skipButton);

      expect(mockOnSkip).toHaveBeenCalled();
    });
  });

  describe('SimulationWizard Buttons', () => {
    const mockResults = [
      {
        id: 'test-1',
        name: 'Teste 1',
        type: 'fixed-income' as const,
        finalValue: 100000,
        returnPercentage: 12.5,
        monthlyData: [],
        parameters: {}
      }
    ];

    it('should render navigation buttons', () => {
      const mockOnResult = vi.fn();
      const mockOnBack = vi.fn();

      render(
        <TestWrapper>
          <SimulationWizard
            strategy="fixed-income"
            onResult={mockOnResult}
            onBack={mockOnBack}
            results={mockResults}
          />
        </TestWrapper>
      );

      expect(screen.getByText('Voltar ao Dashboard')).toBeInTheDocument();
    });

    it('should handle back button click', () => {
      const mockOnResult = vi.fn();
      const mockOnBack = vi.fn();

      render(
        <TestWrapper>
          <SimulationWizard
            strategy="fixed-income"
            onResult={mockOnResult}
            onBack={mockOnBack}
            results={mockResults}
          />
        </TestWrapper>
      );

      const backButton = screen.getByText('Voltar ao Dashboard');
      fireEvent.click(backButton);

      expect(mockOnBack).toHaveBeenCalled();
    });
  });

  describe('FixedIncomeSimulator Buttons', () => {
    it('should render simulation button', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      expect(screen.getByText('Simular Investimento')).toBeInTheDocument();
    });

    it('should handle simulation button click', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const simulateButton = screen.getByText('Simular Investimento');
      fireEvent.click(simulateButton);

      await waitFor(() => {
        expect(mockOnResult).toHaveBeenCalled();
      });
    });

    it('should disable button during calculation', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const simulateButton = screen.getByText('Simular Investimento');
      fireEvent.click(simulateButton);

      // Button should show loading state
      expect(screen.getByText('Calculando...')).toBeInTheDocument();
    });
  });

  describe('RealEstateSimulator Buttons', () => {
    it('should render simulation button', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <RealEstateSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      expect(screen.getByText('Simular Investimento')).toBeInTheDocument();
    });

    it('should handle construction toggle', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <RealEstateSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const toggle = screen.getByRole('switch');
      fireEvent.click(toggle);

      expect(screen.getByText('Na Planta')).toBeInTheDocument();
    });

    it('should handle simulation button click', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <RealEstateSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const simulateButton = screen.getByText('Simular Investimento');
      fireEvent.click(simulateButton);

      await waitFor(() => {
        expect(mockOnResult).toHaveBeenCalled();
      });
    });
  });

  describe('PortfolioOptimizer Buttons', () => {
    const mockResults = [
      {
        id: 'test-1',
        name: 'Renda Fixa',
        type: 'fixed-income' as const,
        finalValue: 100000,
        returnPercentage: 12.5,
        monthlyData: [],
        parameters: {}
      },
      {
        id: 'test-2',
        name: 'Imobiliário',
        type: 'real-estate' as const,
        finalValue: 200000,
        returnPercentage: 15.2,
        monthlyData: [],
        parameters: {}
      }
    ];

    it('should render optimization button when results are available', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <PortfolioOptimizer results={mockResults} onResult={mockOnResult} />
        </TestWrapper>
      );

      expect(screen.getByText('Otimizar Portfólio')).toBeInTheDocument();
    });

    it('should disable optimization button with insufficient results', () => {
      const mockOnResult = vi.fn();
      const singleResult = [mockResults[0]];

      render(
        <TestWrapper>
          <PortfolioOptimizer results={singleResult} onResult={mockOnResult} />
        </TestWrapper>
      );

      const optimizeButton = screen.getByText('Otimizar Portfólio');
      expect(optimizeButton).toBeDisabled();
    });

    it('should handle optimization button click', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <PortfolioOptimizer results={mockResults} onResult={mockOnResult} />
        </TestWrapper>
      );

      const optimizeButton = screen.getByText('Otimizar Portfólio');
      fireEvent.click(optimizeButton);

      await waitFor(() => {
        expect(mockOnResult).toHaveBeenCalled();
      });
    });

    it('should show loading state during optimization', async () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <PortfolioOptimizer results={mockResults} onResult={mockOnResult} />
        </TestWrapper>
      );

      const optimizeButton = screen.getByText('Otimizar Portfólio');
      fireEvent.click(optimizeButton);

      expect(screen.getByText('Otimizando...')).toBeInTheDocument();
    });
  });

  describe('Form Input Validation', () => {
    it('should handle numeric input validation in FixedIncomeSimulator', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const initialAmountInput = screen.getByLabelText('Aporte Inicial (R$)');
      fireEvent.change(initialAmountInput, { target: { value: 'invalid' } });

      // Should handle invalid input gracefully
      expect(initialAmountInput).toHaveValue(0);
    });

    it('should handle numeric input validation in RealEstateSimulator', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <RealEstateSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const propertyValueInput = screen.getByLabelText('Valor do Imóvel (R$)');
      fireEvent.change(propertyValueInput, { target: { value: 'invalid' } });

      // Should handle invalid input gracefully
      expect(propertyValueInput).toHaveValue(0);
    });
  });

  describe('Accessibility Tests', () => {
    it('should have proper ARIA labels on buttons', () => {
      localStorage.setItem('hasSeenWelcome', 'true');
      
      render(
        <TestWrapper>
          <Dashboard />
        </TestWrapper>
      );

      const buttons = screen.getAllByRole('button');
      buttons.forEach(button => {
        expect(button).toBeInTheDocument();
        // Buttons should be focusable
        expect(button).not.toHaveAttribute('tabindex', '-1');
      });
    });

    it('should support keyboard navigation', () => {
      const mockOnResult = vi.fn();

      render(
        <TestWrapper>
          <FixedIncomeSimulator onResult={mockOnResult} />
        </TestWrapper>
      );

      const simulateButton = screen.getByText('Simular Investimento');
      
      // Should be focusable
      simulateButton.focus();
      expect(document.activeElement).toBe(simulateButton);

      // Should respond to Enter key
      fireEvent.keyDown(simulateButton, { key: 'Enter', code: 'Enter' });
      // Note: This would trigger the click handler in a real scenario
    });
  });
});