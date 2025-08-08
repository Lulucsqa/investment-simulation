import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { 
  ChevronLeft, 
  ChevronRight, 
  CheckCircle, 
  AlertCircle,
  Info,
  Target,
  Calculator,
  BarChart3
} from "lucide-react";
import { FixedIncomeSimulator } from "./simulators/FixedIncomeSimulator";
import { RealEstateSimulator } from "./simulators/RealEstateSimulator";
import { PortfolioOptimizer } from "./simulators/PortfolioOptimizer";
import { SimulationResult } from "@/types/investment";
import { Breadcrumbs } from "./Breadcrumbs";

interface Step {
  id: string;
  title: string;
  description: string;
  icon: any;
  isCompleted?: boolean;
  isOptional?: boolean;
}

interface SimulationWizardProps {
  strategy: string;
  onResult: (result: SimulationResult) => void;
  onBack: () => void;
  results: SimulationResult[];
}

export const SimulationWizard = ({ strategy, onResult, onBack, results }: SimulationWizardProps) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);

  const getStepsForStrategy = (strategy: string): Step[] => {
    const baseSteps = [
      {
        id: 'configure',
        title: 'Configurar Parâmetros',
        description: 'Configure os valores e condições do investimento',
        icon: Target,
        isCompleted: false
      },
      {
        id: 'simulate',
        title: 'Executar Simulação',
        description: 'Execute os cálculos com base nos parâmetros definidos',
        icon: Calculator,
        isCompleted: false
      },
      {
        id: 'analyze',
        title: 'Analisar Resultados',
        description: 'Visualize e compare os resultados obtidos',
        icon: BarChart3,
        isCompleted: false
      }
    ];

    if (strategy === 'optimization') {
      return [
        {
          id: 'review',
          title: 'Revisar Simulações',
          description: 'Analise as simulações anteriores disponíveis',
          icon: BarChart3,
          isCompleted: false,
          isOptional: results.length === 0
        },
        ...baseSteps
      ];
    }

    return baseSteps;
  };

  const steps = getStepsForStrategy(strategy);
  const currentStepData = steps[currentStep];
  const progress = ((currentStep + 1) / steps.length) * 100;

  const markStepCompleted = (stepId: string) => {
    if (!completedSteps.includes(stepId)) {
      setCompletedSteps([...completedSteps, stepId]);
    }
  };

  const handleNext = () => {
    markStepCompleted(currentStepData.id);
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSimulationResult = (result: SimulationResult) => {
    onResult(result);
    markStepCompleted('simulate');
    handleNext();
  };

  const getStrategyName = (strategy: string) => {
    switch (strategy) {
      case 'fixed-income':
        return 'Renda Fixa';
      case 'real-estate':
        return 'Investimento Imobiliário';
      case 'optimization':
        return 'Otimização de Portfolio';
      default:
        return 'Simulação';
    }
  };

  const getBreadcrumbItems = () => {
    const items = [
      { label: 'Simulações', href: '/' },
      { label: getStrategyName(strategy) }
    ];

    if (currentStepData) {
      items.push({ label: currentStepData.title });
    }

    return items;
  };

  const renderStepContent = () => {
    const stepId = currentStepData.id;

    if (stepId === 'review' && strategy === 'optimization') {
      return (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Simulações Anteriores
            </CardTitle>
          </CardHeader>
          <CardContent>
            {results.length === 0 ? (
              <div className="text-center py-8 space-y-4">
                <AlertCircle className="h-12 w-12 text-warning mx-auto" />
                <div>
                  <h4 className="font-semibold text-warning mb-2">
                    Nenhuma simulação encontrada
                  </h4>
                  <p className="text-muted-foreground">
                    Execute algumas simulações primeiro para poder otimizar seu portfolio.
                    Você pode pular esta etapa e voltar depois.
                  </p>
                </div>
                <Button variant="outline" onClick={onBack}>
                  Voltar ao Dashboard
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <p className="text-muted-foreground">
                  Encontramos {results.length} simulação(ões) anteriores que serão usadas para otimização:
                </p>
                
                <div className="space-y-2">
                  {results.map((result, index) => (
                    <div key={result.id} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <CheckCircle className="h-4 w-4 text-success" />
                        <div>
                          <span className="font-medium">{result.name}</span>
                          <Badge variant="secondary" className="ml-2 text-xs">
                            {result.type === 'fixed-income' ? 'Renda Fixa' : 'Imobiliário'}
                          </Badge>
                        </div>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        R$ {result.finalValue.toLocaleString('pt-BR')}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      );
    }

    if (stepId === 'configure' || stepId === 'simulate') {
      return (
        <div className="space-y-6">
          {strategy === 'fixed-income' && (
            <FixedIncomeSimulator onResult={handleSimulationResult} />
          )}
          {strategy === 'real-estate' && (
            <RealEstateSimulator onResult={handleSimulationResult} />
          )}
          {strategy === 'optimization' && (
            <PortfolioOptimizer results={results} onResult={handleSimulationResult} />
          )}
        </div>
      );
    }

    if (stepId === 'analyze') {
      return (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-success" />
              Simulação Concluída!
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-gradient-to-br from-success to-success/80 rounded-full flex items-center justify-center mx-auto">
                <CheckCircle className="h-8 w-8 text-white" />
              </div>
              
              <div>
                <h3 className="text-xl font-semibold mb-2">
                  Simulação executada com sucesso!
                </h3>
                <p className="text-muted-foreground">
                  Os resultados foram adicionados ao painel de comparação. 
                  Você pode visualizar gráficos detalhados e comparar com outras estratégias.
                </p>
              </div>
            </div>

            <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <Info className="h-5 w-5 text-primary" />
                <span className="font-semibold text-primary">Próximos Passos</span>
              </div>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• Execute outras simulações para comparar estratégias</li>
                <li>• Use o otimizador para combinar múltiplas estratégias</li>
                <li>• Analise os gráficos de evolução do patrimônio</li>
                <li>• Ajuste parâmetros para diferentes cenários</li>
              </ul>
            </div>

            <div className="flex gap-4 justify-center">
              <Button variant="outline" onClick={onBack}>
                Voltar ao Dashboard
              </Button>
              <Button onClick={() => { setCurrentStep(0); setCompletedSteps([]); window.scrollTo({ top: 0, behavior: "smooth" }); }} className="btn-gradient">
                Nova Simulação
              </Button>
            </div>
          </CardContent>
        </Card>
      );
    }

    return null;
  };

  return (
    <div className="space-y-6">
      {/* Breadcrumbs */}
      <Breadcrumbs items={getBreadcrumbItems()} />

      {/* Progress Header */}
      <Card className="bg-gradient-to-r from-primary/5 to-accent/5">
        <CardHeader>
          <div className="flex items-center justify-between mb-4">
            <div>
              <CardTitle className="text-xl">
                {getStrategyName(strategy)}
              </CardTitle>
              <p className="text-muted-foreground">
                {currentStepData.description}
              </p>
            </div>
            
            <Badge variant="secondary" className="text-sm">
              Passo {currentStep + 1} de {steps.length}
            </Badge>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Progresso da Simulação</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
        </CardHeader>
      </Card>

      {/* Steps Navigation */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => {
              const Icon = step.icon;
              const isCompleted = completedSteps.includes(step.id);
              const isCurrent = index === currentStep;
              const isPast = index < currentStep;
              
              return (
                <div key={step.id} className="flex items-center">
                  <div className={`
                    flex items-center gap-3 p-3 rounded-lg transition-all
                    ${isCurrent ? 'bg-primary/10 text-primary' : ''}
                    ${isCompleted ? 'bg-success/10 text-success' : ''}
                    ${!isCurrent && !isCompleted && !isPast ? 'text-muted-foreground' : ''}
                  `}>
                    <div className={`
                      w-8 h-8 rounded-full flex items-center justify-center
                      ${isCurrent ? 'bg-primary text-primary-foreground' : ''}
                      ${isCompleted ? 'bg-success text-success-foreground' : ''}
                      ${!isCurrent && !isCompleted && !isPast ? 'bg-muted text-muted-foreground' : ''}
                    `}>
                      {isCompleted ? (
                        <CheckCircle className="h-5 w-5" />
                      ) : (
                        <Icon className="h-5 w-5" />
                      )}
                    </div>
                    
                    <div className="hidden md:block">
                      <div className="font-medium text-sm">{step.title}</div>
                      {step.isOptional && (
                        <Badge variant="outline" className="text-xs mt-1">
                          Opcional
                        </Badge>
                      )}
                    </div>
                  </div>
                  
                  {index < steps.length - 1 && (
                    <Separator orientation="horizontal" className="w-8 mx-2" />
                  )}
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Step Content */}
      <div className="animate-slide-up">
        {renderStepContent()}
      </div>

      {/* Navigation */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex gap-2">
              {currentStep > 0 && (
                <Button variant="outline" onClick={handlePrevious}>
                  <ChevronLeft className="h-4 w-4 mr-2" />
                  Anterior
                </Button>
              )}
              
              <Button variant="outline" onClick={onBack}>
                Voltar ao Dashboard
              </Button>
            </div>

            <div className="flex gap-2">
              {currentStepData.isOptional && (
                <Button variant="ghost" onClick={handleNext}>
                  Pular
                </Button>
              )}
              
              {currentStep < steps.length - 1 && 
               currentStepData.id !== 'configure' && 
               currentStepData.id !== 'simulate' && (
                <Button onClick={handleNext}>
                  Próximo
                  <ChevronRight className="h-4 w-4 ml-2" />
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};