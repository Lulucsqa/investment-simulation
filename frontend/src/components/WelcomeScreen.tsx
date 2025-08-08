import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  TrendingUp, 
  Building, 
  Target, 
  ArrowRight, 
  Calculator,
  PieChart,
  Zap,
  BookOpen,
  ChevronRight
} from "lucide-react";

interface Strategy {
  id: string;
  name: string;
  description: string;
  icon: any;
  difficulty: 'Iniciante' | 'Intermediário' | 'Avançado';
  timeToComplete: string;
  benefits: string[];
  color: string;
}

interface WelcomeScreenProps {
  onStrategySelect: (strategyId: string) => void;
  onSkip: () => void;
}

const strategies: Strategy[] = [
  {
    id: 'fixed-income',
    name: 'Renda Fixa',
    description: 'Simulações conservadoras com retornos previsíveis e baixo risco',
    icon: TrendingUp,
    difficulty: 'Iniciante',
    timeToComplete: '3-5 min',
    benefits: ['Baixo risco', 'Retorno previsível', 'Proteção contra inflação'],
    color: 'from-success to-success/80'
  },
  {
    id: 'real-estate',
    name: 'Investimento Imobiliário',
    description: 'Análise de fundos imobiliários e propriedades físicas',
    icon: Building,
    difficulty: 'Intermediário',
    timeToComplete: '5-8 min',
    benefits: ['Diversificação', 'Renda passiva', 'Proteção inflacionária'],
    color: 'from-warning to-warning/80'
  },
  {
    id: 'optimization',
    name: 'Otimização de Portfolio',
    description: 'Combine múltiplas estratégias para maximizar retornos',
    icon: Target,
    difficulty: 'Avançado',
    timeToComplete: '8-12 min',
    benefits: ['Máximo retorno', 'Risco controlado', 'Estratégia personalizada'],
    color: 'from-primary to-primary/80'
  }
];

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case 'Iniciante':
      return 'bg-success text-success-foreground';
    case 'Intermediário':
      return 'bg-warning text-warning-foreground';
    case 'Avançado':
      return 'bg-primary text-primary-foreground';
    default:
      return 'bg-muted text-muted-foreground';
  }
};

export const WelcomeScreen = ({ onStrategySelect, onSkip }: WelcomeScreenProps) => {
  const [selectedStrategy, setSelectedStrategy] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState(0);

  const handleStrategySelect = (strategyId: string) => {
    setSelectedStrategy(strategyId);
    setCurrentStep(1);
  };

  const handleContinue = () => {
    if (selectedStrategy) {
      onStrategySelect(selectedStrategy);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted/30 to-background p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4 animate-slide-up">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full text-primary text-sm font-medium">
            <Zap className="h-4 w-4" />
            Sistema de Simulação Inteligente
          </div>
          
          <h1 className="text-5xl font-bold text-gradient leading-tight">
            Otimize seus Investimentos
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Descubra as melhores estratégias de investimento com simulações precisas 
            e análises detalhadas para maximizar seus retornos.
          </p>

          {/* Progress */}
          <div className="max-w-md mx-auto space-y-2">
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Selecione sua estratégia</span>
              <span>{currentStep + 1}/2</span>
            </div>
            <Progress value={(currentStep + 1) * 50} className="h-2" />
          </div>
        </div>

        {currentStep === 0 && (
          <div className="space-y-6 animate-fade-in">
            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
              <Card className="text-center p-4 border-0 bg-gradient-to-br from-primary/5 to-primary/10">
                <CardContent className="p-0">
                  <Calculator className="h-8 w-8 text-primary mx-auto mb-2" />
                  <div className="text-2xl font-bold text-primary">3+</div>
                  <div className="text-sm text-muted-foreground">Simuladores</div>
                </CardContent>
              </Card>
              
              <Card className="text-center p-4 border-0 bg-gradient-to-br from-success/5 to-success/10">
                <CardContent className="p-0">
                  <PieChart className="h-8 w-8 text-success mx-auto mb-2" />
                  <div className="text-2xl font-bold text-success">100%</div>
                  <div className="text-sm text-muted-foreground">Gratuito</div>
                </CardContent>
              </Card>
              
              <Card className="text-center p-4 border-0 bg-gradient-to-br from-warning/5 to-warning/10">
                <CardContent className="p-0">
                  <BookOpen className="h-8 w-8 text-warning mx-auto mb-2" />
                  <div className="text-2xl font-bold text-warning">5min</div>
                  <div className="text-sm text-muted-foreground">Setup rápido</div>
                </CardContent>
              </Card>
            </div>

            {/* Strategy Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
              {strategies.map((strategy, index) => {
                const Icon = strategy.icon;
                const isSelected = selectedStrategy === strategy.id;
                
                return (
                  <Card 
                    key={strategy.id}
                    className={`
                      cursor-pointer transition-all duration-300 group hover:shadow-elevated
                      ${isSelected ? 'ring-2 ring-primary shadow-glow scale-105' : 'hover:scale-102'}
                    `}
                    style={{ animationDelay: `${index * 100}ms` }}
                    onClick={() => handleStrategySelect(strategy.id)}
                  >
                    <CardHeader className="pb-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className={`p-3 rounded-lg bg-gradient-to-br ${strategy.color}`}>
                          <Icon className="h-6 w-6 text-white" />
                        </div>
                        <Badge className={getDifficultyColor(strategy.difficulty)}>
                          {strategy.difficulty}
                        </Badge>
                      </div>
                      
                      <CardTitle className="text-xl group-hover:text-primary transition-colors">
                        {strategy.name}
                      </CardTitle>
                      
                      <p className="text-muted-foreground leading-relaxed">
                        {strategy.description}
                      </p>
                    </CardHeader>
                    
                    <CardContent className="pt-0">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-muted-foreground">Tempo estimado:</span>
                          <span className="font-medium">{strategy.timeToComplete}</span>
                        </div>
                        
                        <div className="space-y-2">
                          <span className="text-sm font-medium text-muted-foreground">Benefícios:</span>
                          <ul className="space-y-1">
                            {strategy.benefits.map((benefit, idx) => (
                              <li key={idx} className="flex items-center gap-2 text-sm">
                                <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                                {benefit}
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <Button 
                          variant={isSelected ? "default" : "outline"}
                          className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
                        >
                          {isSelected ? 'Selecionado' : 'Selecionar'}
                          <ArrowRight className="ml-2 h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        )}

        {currentStep === 1 && selectedStrategy && (
          <div className="max-w-2xl mx-auto text-center space-y-6 animate-slide-up">
            <div className="space-y-4">
              <div className="w-16 h-16 bg-gradient-to-br from-primary to-primary/80 rounded-full flex items-center justify-center mx-auto">
                <ArrowRight className="h-8 w-8 text-white" />
              </div>
              
              <h2 className="text-3xl font-bold">Pronto para começar!</h2>
              
              <p className="text-muted-foreground text-lg">
                Você selecionou: <strong>{strategies.find(s => s.id === selectedStrategy)?.name}</strong>
              </p>
              
              <div className="bg-muted/50 rounded-lg p-6 space-y-3">
                <h3 className="font-semibold">O que acontece a seguir:</h3>
                <ul className="space-y-2 text-left">
                  <li className="flex items-center gap-3">
                    <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">1</div>
                    <span>Preencha os parâmetros de investimento</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">2</div>
                    <span>Execute a simulação personalizada</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">3</div>
                    <span>Analise os resultados e compare estratégias</span>
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="flex gap-4 justify-center">
              <Button 
                variant="outline" 
                onClick={() => setCurrentStep(0)}
                className="px-8"
              >
                Voltar
              </Button>
              <Button 
                onClick={handleContinue}
                className="btn-gradient px-8"
              >
                Continuar
                <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        )}

        {/* Skip Option */}
        <div className="text-center">
          <Button 
            variant="ghost" 
            onClick={onSkip}
            className="text-muted-foreground hover:text-foreground"
          >
            Pular introdução e ir direto para o dashboard
          </Button>
        </div>
      </div>
    </div>
  );
};