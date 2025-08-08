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
      <div className="min-h-screen relative overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-background via-primary/5 to-accent/10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-float"></div>
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-accent/20 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-success/10 rounded-full blur-2xl animate-bounce-gentle"></div>
        </div>

        {/* Header */}
        <div className="relative z-10 border-b bg-card/50 backdrop-blur-xl">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div className="space-y-2 animate-slide-up">
                <h1 className="text-4xl font-bold text-rainbow animate-rainbow-flow">
                  Sistema de Simulação de Investimentos
                </h1>
                <p className="text-lg text-muted-foreground">
                  🚀 Otimize suas estratégias com IA e simulações inteligentes
                </p>
              </div>
              
              <div className="flex items-center gap-4 animate-slide-in-right">
                <Button 
                  variant="outline" 
                  size="lg" 
                  onClick={handleShowOnboarding}
                  className="btn-neon hover:shadow-neon"
                >
                  <Settings className="h-5 w-5 mr-2 animate-rotate-slow" />
                  <span>Tour Guiado</span>
                </Button>
                <div className="glow-on-hover">
                  <HelpCenter />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto p-6 space-y-10">
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 animate-fade-in">
            <Card className="card-floating group cursor-pointer">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Simulações</p>
                    <p className="text-3xl font-bold text-glow">{results.length}</p>
                  </div>
                  <div className="p-4 rounded-2xl bg-gradient-to-br from-primary to-accent group-hover:animate-bounce-gentle">
                    <BarChart3 className="h-8 w-8 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-floating group cursor-pointer">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Melhor Retorno</p>
                    <p className="text-3xl font-bold text-financial-gain">
                      {results.length > 0 
                        ? `${Math.max(...results.map(r => r.returnPercentage)).toFixed(1)}%`
                        : '0%'
                      }
                    </p>
                  </div>
                  <div className="p-4 rounded-2xl bg-gradient-to-br from-success to-green-400 group-hover:animate-pulse-glow">
                    <TrendingUp className="h-8 w-8 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-floating group cursor-pointer">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Estratégias</p>
                    <p className="text-3xl font-bold">3</p>
                  </div>
                  <div className="p-4 rounded-2xl bg-gradient-to-br from-warning to-orange-400 group-hover:animate-float">
                    <Target className="h-8 w-8 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="card-floating group cursor-pointer">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Status</p>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-success animate-pulse"></div>
                      <span className="text-lg font-medium">Online</span>
                    </div>
                  </div>
                  <div className="p-4 rounded-2xl bg-gradient-to-br from-success to-emerald-400 group-hover:animate-bounce-gentle">
                    <Users className="h-8 w-8 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Start Cards */}
          <div className="space-y-6 animate-slide-up">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold text-gradient">Início Rápido</h2>
              <Badge variant="secondary" className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary/20 to-accent/20 border-primary/30">
                <Star className="h-4 w-4 animate-pulse" />
                Recomendado
              </Badge>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card className="card-holographic group cursor-pointer relative overflow-hidden"
                    onClick={() => handleQuickStart('fixed-income')}>
                <div className="absolute inset-0 bg-gradient-to-br from-success/20 to-emerald-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <CardHeader className="pb-6 relative z-10">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-success to-emerald-600 shadow-glow group-hover:animate-bounce-gentle">
                      <TrendingUp className="h-8 w-8 text-white" />
                    </div>
                    <Badge className="bg-success/20 text-success border-success/30 px-3 py-1">
                      Iniciante
                    </Badge>
                  </div>
                  <CardTitle className="text-2xl group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-success group-hover:to-emerald-600 group-hover:bg-clip-text transition-all duration-300">
                    Renda Fixa
                  </CardTitle>
                  <p className="text-muted-foreground leading-relaxed">
                    💰 Simulações conservadoras com CDB, Tesouro Direto e investimentos de baixo risco
                  </p>
                </CardHeader>
                <CardContent className="pt-0 relative z-10">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Risco:</span>
                      <span className="text-success font-semibold">Baixo 📈</span>
                    </div>
                    <Button className="w-full btn-gradient group-hover:shadow-neon">
                      Começar Simulação
                      <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-holographic group cursor-pointer relative overflow-hidden"
                    onClick={() => handleQuickStart('real-estate')}>
                <div className="absolute inset-0 bg-gradient-to-br from-warning/20 to-orange-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <CardHeader className="pb-6 relative z-10">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-warning to-orange-600 shadow-glow group-hover:animate-float">
                      <Building className="h-8 w-8 text-white" />
                    </div>
                    <Badge className="bg-warning/20 text-warning border-warning/30 px-3 py-1">
                      Intermediário
                    </Badge>
                  </div>
                  <CardTitle className="text-2xl group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-warning group-hover:to-orange-600 group-hover:bg-clip-text transition-all duration-300">
                    Fundos Imobiliários
                  </CardTitle>
                  <p className="text-muted-foreground leading-relaxed">
                    🏢 Análise de FIIs com dividend yield e potencial de valorização
                  </p>
                </CardHeader>
                <CardContent className="pt-0 relative z-10">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Risco:</span>
                      <span className="text-warning font-semibold">Moderado ⚖️</span>
                    </div>
                    <Button className="w-full btn-gradient group-hover:shadow-neon">
                      Começar Simulação
                      <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-holographic group cursor-pointer relative overflow-hidden"
                    onClick={() => handleQuickStart('optimization')}>
                <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-purple-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <CardHeader className="pb-6 relative z-10">
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-primary to-purple-600 shadow-glow group-hover:animate-pulse-glow">
                      <Target className="h-8 w-8 text-white" />
                    </div>
                    <Badge className="bg-primary/20 text-primary border-primary/30 px-3 py-1">
                      Avançado
                    </Badge>
                  </div>
                  <CardTitle className="text-2xl group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-primary group-hover:to-purple-600 group-hover:bg-clip-text transition-all duration-300">
                    Otimização
                  </CardTitle>
                  <p className="text-muted-foreground leading-relaxed">
                    🎯 Combine estratégias para maximizar retornos e controlar riscos
                  </p>
                </CardHeader>
                <CardContent className="pt-0 relative z-10">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Complexidade:</span>
                      <span className="text-primary font-semibold">Alta 🚀</span>
                    </div>
                    <Button 
                      className={`w-full transition-all duration-300 ${
                        results.length === 0 
                          ? 'opacity-50 cursor-not-allowed' 
                          : 'btn-gradient hover:shadow-neon'
                      }`}
                      disabled={results.length === 0}
                    >
                      {results.length === 0 ? '⏳ Precisa de Simulações' : '🚀 Começar Otimização'}
                      {results.length > 0 && <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6 animate-fade-in">
            <h2 className="text-3xl font-bold text-gradient">Resultados e Comparações</h2>
            <div className="card-floating">
              <ResultsComparison results={results} onClear={clearResults} />
            </div>
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