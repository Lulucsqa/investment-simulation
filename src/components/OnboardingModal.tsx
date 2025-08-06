import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { 
  ChevronRight, 
  ChevronLeft, 
  Play, 
  Target, 
  TrendingUp, 
  PieChart,
  X,
  CheckCircle
} from "lucide-react";

interface OnboardingStep {
  title: string;
  description: string;
  content: React.ReactNode;
  action?: string;
}

interface OnboardingModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: () => void;
}

export const OnboardingModal = ({ isOpen, onClose, onComplete }: OnboardingModalProps) => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps: OnboardingStep[] = [
    {
      title: "Bem-vindo ao Sistema de Simulação",
      description: "Descubra como otimizar seus investimentos em apenas alguns minutos",
      content: (
        <div className="space-y-6 text-center">
          <div className="w-20 h-20 bg-gradient-to-br from-primary to-primary/80 rounded-full flex items-center justify-center mx-auto">
            <Target className="h-10 w-10 text-white" />
          </div>
          
          <div className="space-y-3">
            <p className="text-muted-foreground leading-relaxed">
              Este sistema foi desenvolvido para ajudar você a tomar decisões 
              inteligentes sobre seus investimentos através de simulações precisas.
            </p>
            
            <div className="grid grid-cols-3 gap-4 mt-6">
              <div className="space-y-2">
                <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center mx-auto">
                  <TrendingUp className="h-6 w-6 text-success" />
                </div>
                <p className="text-sm font-medium">Renda Fixa</p>
              </div>
              
              <div className="space-y-2">
                <div className="w-12 h-12 bg-warning/10 rounded-lg flex items-center justify-center mx-auto">
                  <PieChart className="h-6 w-6 text-warning" />
                </div>
                <p className="text-sm font-medium">Imobiliário</p>
              </div>
              
              <div className="space-y-2">
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto">
                  <Target className="h-6 w-6 text-primary" />
                </div>
                <p className="text-sm font-medium">Otimização</p>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      title: "Simuladores Disponíveis",
      description: "Explore diferentes estratégias de investimento",
      content: (
        <div className="space-y-4">
          <div className="grid gap-4">
            <div className="flex items-start gap-4 p-4 bg-muted/50 rounded-lg">
              <div className="w-10 h-10 bg-success rounded-lg flex items-center justify-center flex-shrink-0">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
              <div>
                <h4 className="font-semibold">Renda Fixa</h4>
                <p className="text-sm text-muted-foreground">
                  Simule CDBs, Tesouro Direto e outros investimentos de baixo risco
                </p>
                <Badge variant="secondary" className="mt-2">Iniciante</Badge>
              </div>
            </div>
            
            <div className="flex items-start gap-4 p-4 bg-muted/50 rounded-lg">
              <div className="w-10 h-10 bg-warning rounded-lg flex items-center justify-center flex-shrink-0">
                <PieChart className="h-5 w-5 text-white" />
              </div>
              <div>
                <h4 className="font-semibold">Fundos Imobiliários</h4>
                <p className="text-sm text-muted-foreground">
                  Analise FIIs e investimentos imobiliários com dividend yield
                </p>
                <Badge variant="secondary" className="mt-2">Intermediário</Badge>
              </div>
            </div>
            
            <div className="flex items-start gap-4 p-4 bg-muted/50 rounded-lg">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
                <Target className="h-5 w-5 text-white" />
              </div>
              <div>
                <h4 className="font-semibold">Otimização de Portfolio</h4>
                <p className="text-sm text-muted-foreground">
                  Combine estratégias para maximizar retornos e minimizar riscos
                </p>
                <Badge variant="secondary" className="mt-2">Avançado</Badge>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      title: "Como Funciona",
      description: "Processo simples em 3 passos",
      content: (
        <div className="space-y-6">
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h4 className="font-semibold">Configure os Parâmetros</h4>
                <p className="text-sm text-muted-foreground">
                  Defina valores, prazos e preferências de risco
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h4 className="font-semibold">Execute a Simulação</h4>
                <p className="text-sm text-muted-foreground">
                  Nosso algoritmo calcula projeções baseadas em dados reais
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h4 className="font-semibold">Analise os Resultados</h4>
                <p className="text-sm text-muted-foreground">
                  Compare estratégias com gráficos e relatórios detalhados
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="h-5 w-5 text-primary" />
              <span className="font-semibold text-primary">Dica Pro</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Execute múltiplas simulações e compare os resultados para 
              encontrar a estratégia ideal para seu perfil.
            </p>
          </div>
        </div>
      )
    },
    {
      title: "Pronto para Começar!",
      description: "Tudo configurado para suas primeiras simulações",
      content: (
        <div className="space-y-6 text-center">
          <div className="w-20 h-20 bg-gradient-to-br from-success to-success/80 rounded-full flex items-center justify-center mx-auto">
            <CheckCircle className="h-10 w-10 text-white" />
          </div>
          
          <div className="space-y-3">
            <p className="text-muted-foreground leading-relaxed">
              Agora você tem todas as informações necessárias para começar a 
              simular e otimizar seus investimentos.
            </p>
            
            <div className="bg-gradient-to-r from-primary/5 to-success/5 rounded-lg p-6 space-y-3">
              <h4 className="font-semibold">Recursos que você pode usar:</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-success" />
                  Simulações ilimitadas e gratuitas
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-success" />
                  Comparação entre estratégias
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-success" />
                  Gráficos interativos e relatórios
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-success" />
                  Suporte e tutoriais integrados
                </li>
              </ul>
            </div>
          </div>
        </div>
      ),
      action: "Começar a Simular"
    }
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSkip = () => {
    onComplete();
  };

  const currentStepData = steps[currentStep];
  const isLastStep = currentStep === steps.length - 1;
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-hidden">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle className="text-xl font-bold">
              {currentStepData.title}
            </DialogTitle>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="h-8 w-8 p-0"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          
          <p className="text-muted-foreground">
            {currentStepData.description}
          </p>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Progresso</span>
              <span>{currentStep + 1} de {steps.length}</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
        </DialogHeader>

        <div className="py-6 overflow-y-auto max-h-96">
          {currentStepData.content}
        </div>

        <div className="flex items-center justify-between pt-4 border-t">
          <div className="flex items-center gap-2">
            {currentStep > 0 && (
              <Button variant="outline" onClick={handlePrevious}>
                <ChevronLeft className="h-4 w-4 mr-2" />
                Anterior
              </Button>
            )}
            
            <Button variant="ghost" onClick={handleSkip} className="text-muted-foreground">
              Pular tour
            </Button>
          </div>

          <Button onClick={handleNext} className="btn-gradient">
            {isLastStep ? (
              <>
                <Play className="h-4 w-4 mr-2" />
                {currentStepData.action || 'Finalizar'}
              </>
            ) : (
              <>
                Próximo
                <ChevronRight className="h-4 w-4 ml-2" />
              </>
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};