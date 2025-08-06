import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  TrendingUp, 
  Building, 
  Target, 
  BarChart3, 
  Settings,
  Users,
  Star,
  ArrowRight
} from "lucide-react";
import { WelcomeScreen } from "./WelcomeScreen";
import { OnboardingModal } from "./OnboardingModal";
import { HelpCenter } from "./HelpCenter";
import { SimulationWizard } from "./SimulationWizard";
import { ResultsComparison } from "./ResultsComparison";
import { SimulationResult } from "@/types/investment";

type ViewMode = 'welcome' | 'dashboard' | 'wizard';

const Dashboard = () => {
  const [results, setResults] = useState<SimulationResult[]>([]);
  const [viewMode, setViewMode] = useState<ViewMode>('welcome');
  const [selectedStrategy, setSelectedStrategy] = useState<string>('');
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [hasSeenWelcome, setHasSeenWelcome] = useState(false);

  useEffect(() => {
    // Check if user has seen welcome screen before
    const hasSeenWelcomeBefore = localStorage.getItem('hasSeenWelcome');
    if (hasSeenWelcomeBefore) {
      setHasSeenWelcome(true);
      setViewMode('dashboard');
    }
  }, []);

  const addResult = (result: SimulationResult) => {
    setResults(prev => [...prev, result]);
  };

  const clearResults = () => {
    setResults([]);
  };

  const handleStrategySelect = (strategyId: string) => {
    setSelectedStrategy(strategyId);
    setViewMode('wizard');
    
    // Mark welcome as seen
    if (!hasSeenWelcome) {
      localStorage.setItem('hasSeenWelcome', 'true');
      setHasSeenWelcome(true);
    }
  };

  const handleSkipWelcome = () => {
    localStorage.setItem('hasSeenWelcome', 'true');
    setHasSeenWelcome(true);
    setViewMode('dashboard');
  };

  const handleBackToDashboard = () => {
    setViewMode('dashboard');
    setSelectedStrategy('');
  };

  const handleQuickStart = (strategy: string) => {
    setSelectedStrategy(strategy);
    setViewMode('wizard');
  };

  const handleShowOnboarding = () => {
    setShowOnboarding(true);
  };

  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
  };

  // Show welcome screen for new users
  if (!hasSeenWelcome && viewMode === 'welcome') {
    return (
      <WelcomeScreen 
        onStrategySelect={handleStrategySelect}
        onSkip={handleSkipWelcome}
      />
    );
  }

  // Show simulation wizard
  if (viewMode === 'wizard' && selectedStrategy) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-muted/20 to-background p-6">
        <div className="max-w-7xl mx-auto">
          <SimulationWizard
            strategy={selectedStrategy}
            onResult={addResult}
            onBack={handleBackToDashboard}
            results={results}
          />
        </div>
      </div>
    );
  }

  // Main dashboard
  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-background via-muted/20 to-background">
        {/* Header */}
        <div className="border-b bg-card/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <h1 className="text-2xl font-bold text-gradient">
                  Sistema de Simulação de Investimentos
                </h1>
                <p className="text-muted-foreground">
                  Otimize suas estratégias de investimento com simulações inteligentes
                </p>
              </div>
              
              <div className="flex items-center gap-3">
                <Button variant="outline" size="sm" onClick={handleShowOnboarding}>
                  <Settings className="h-4 w-4 mr-2" />
                  Tour Guiado
                </Button>
                <HelpCenter />
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto p-6 space-y-8">
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card className="card-elevated">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Simulações</p>
                    <p className="text-2xl font-bold">{results.length}</p>
                  </div>
                  <BarChart3 className="h-8 w-8 text-primary" />
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-elevated">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Melhor Retorno</p>
                    <p className="text-2xl font-bold text-financial-gain">
                      {results.length > 0 
                        ? `${Math.max(...results.map(r => r.returnPercentage)).toFixed(1)}%`
                        : '0%'
                      }
                    </p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-financial-gain" />
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-elevated">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Estratégias</p>
                    <p className="text-2xl font-bold">3</p>
                  </div>
                  <Target className="h-8 w-8 text-warning" />
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-elevated">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Status</p>
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                      <span className="text-sm font-medium">Online</span>
                    </div>
                  </div>
                  <Users className="h-8 w-8 text-success" />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Start Cards */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Início Rápido</h2>
              <Badge variant="secondary" className="flex items-center gap-1">
                <Star className="h-3 w-3" />
                Recomendado
              </Badge>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="card-elevated group cursor-pointer hover:scale-105 transform transition-all duration-200"
                    onClick={() => handleQuickStart('fixed-income')}>
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="p-3 rounded-lg bg-gradient-to-br from-success to-success/80">
                      <TrendingUp className="h-6 w-6 text-white" />
                    </div>
                    <Badge className="bg-success text-success-foreground">
                      Iniciante
                    </Badge>
                  </div>
                  <CardTitle className="group-hover:text-primary transition-colors">
                    Renda Fixa
                  </CardTitle>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    Simulações conservadoras com CDB, Tesouro Direto e investimentos de baixo risco
                  </p>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Risco:</span>
                      <span className="text-success font-medium">Baixo</span>
                    </div>
                    <Button className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                      Começar Simulação
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-elevated group cursor-pointer hover:scale-105 transform transition-all duration-200"
                    onClick={() => handleQuickStart('real-estate')}>
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="p-3 rounded-lg bg-gradient-to-br from-warning to-warning/80">
                      <Building className="h-6 w-6 text-white" />
                    </div>
                    <Badge className="bg-warning text-warning-foreground">
                      Intermediário
                    </Badge>
                  </div>
                  <CardTitle className="group-hover:text-primary transition-colors">
                    Fundos Imobiliários
                  </CardTitle>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    Análise de FIIs com dividend yield e potencial de valorização
                  </p>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Risco:</span>
                      <span className="text-warning font-medium">Moderado</span>
                    </div>
                    <Button className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                      Começar Simulação
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-elevated group cursor-pointer hover:scale-105 transform transition-all duration-200"
                    onClick={() => handleQuickStart('optimization')}>
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="p-3 rounded-lg bg-gradient-to-br from-primary to-primary/80">
                      <Target className="h-6 w-6 text-white" />
                    </div>
                    <Badge className="bg-primary text-primary-foreground">
                      Avançado
                    </Badge>
                  </div>
                  <CardTitle className="group-hover:text-primary transition-colors">
                    Otimização
                  </CardTitle>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    Combine estratégias para maximizar retornos e controlar riscos
                  </p>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Complexidade:</span>
                      <span className="text-primary font-medium">Alta</span>
                    </div>
                    <Button 
                      className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
                      disabled={results.length === 0}
                    >
                      {results.length === 0 ? 'Precisa de Simulações' : 'Começar Otimização'}
                      {results.length > 0 && <ArrowRight className="ml-2 h-4 w-4" />}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Resultados e Comparações</h2>
            <ResultsComparison results={results} onClear={clearResults} />
          </div>
        </div>
      </div>

      {/* Onboarding Modal */}
      <OnboardingModal
        isOpen={showOnboarding}
        onClose={() => setShowOnboarding(false)}
        onComplete={handleOnboardingComplete}
      />
    </>
  );
};

export default Dashboard;