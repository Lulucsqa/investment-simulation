import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { MobileFriendlyInput } from "@/components/ui/mobile-friendly-input";
import { Target, Zap, TrendingUp } from "lucide-react";
import { SimulationResult } from "@/types/investment";
import { optimizePortfolio } from "@/lib/calculations";
import { toast } from "sonner";

interface PortfolioOptimizerProps {
  results: SimulationResult[];
  onResult: (result: SimulationResult) => void;
}

export const PortfolioOptimizer = ({ results, onResult }: PortfolioOptimizerProps) => {
  const [targetReturn, setTargetReturn] = useState(15);
  const [riskTolerance, setRiskTolerance] = useState(50);
  const [maxAllocation, setMaxAllocation] = useState(80);
  const [isOptimizing, setIsOptimizing] = useState(false);

  const handleOptimize = async () => {
    if (results.length < 2) {
      toast.error("Erro na otimização", {
        description: "É necessário ter pelo menos 2 simulações para otimizar."
      });
      return;
    }

    setIsOptimizing(true);
    
    try {
      const optimizedResult = optimizePortfolio(results, {
        targetReturn,
        riskTolerance,
        maxAllocation
      });
      
      onResult(optimizedResult);
      
      toast.success("Otimização concluída!", {
        description: `Portfólio otimizado com retorno esperado de ${optimizedResult.returnPercentage.toFixed(2)}%`
      });
    } catch (error) {
      toast.error("Erro na otimização", {
        description: "Não foi possível encontrar uma alocação ótima com os parâmetros fornecidos."
      });
    } finally {
      setIsOptimizing(false);
    }
  };

  const availableStrategies = results.filter(r => r.type !== 'optimized');

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <Target className="h-5 w-5 text-warning" />
        <h3 className="text-lg font-semibold">Otimização de Portfólio</h3>
        <Badge variant="secondary">
          {availableStrategies.length} estratégias
        </Badge>
      </div>

      {availableStrategies.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-8 text-center">
            <TrendingUp className="h-12 w-12 text-muted-foreground mb-4" />
            <h4 className="text-lg font-medium text-muted-foreground mb-2">
              Nenhuma simulação disponível
            </h4>
            <p className="text-sm text-muted-foreground">
              Execute simulações de renda fixa e imobiliário para otimizar seu portfólio.
            </p>
          </CardContent>
        </Card>
      ) : (
        <>
          <Card className="bg-muted/50">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Estratégias Disponíveis
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {availableStrategies.map((result) => (
                <div key={result.id} className="flex items-center justify-between py-2">
                  <div className="flex items-center gap-2">
                    <div className={`w-3 h-3 rounded-full ${
                      result.type === 'fixed-income' ? 'bg-info' : 'bg-success'
                    }`} />
                    <span className="text-sm font-medium">{result.name}</span>
                  </div>
                  <Badge variant="outline">
                    {result.returnPercentage.toFixed(1)}% a.a.
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>

          <div className="space-y-4">
            <MobileFriendlyInput
              id="target-return"
              label="Retorno Alvo (% a.a.)"
              type="number"
              step="0.1"
              value={targetReturn}
              onChange={(e) => setTargetReturn(e.target.value === '' ? 0 : parseFloat(e.target.value) || 0)}
              placeholder="15"
              onClear={() => setTargetReturn(0)}
            />

            <div className="space-y-3">
              <Label htmlFor="risk-tolerance">
                Tolerância ao Risco: {riskTolerance}%
              </Label>
              <Progress value={riskTolerance} className="w-full" />
              <Input
                id="risk-tolerance"
                type="range"
                min="0"
                max="100"
                value={riskTolerance}
                onChange={(e) => setRiskTolerance(parseInt(e.target.value))}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Conservador</span>
                <span>Moderado</span>
                <span>Agressivo</span>
              </div>
            </div>

            <MobileFriendlyInput
              id="max-allocation"
              label="Alocação Máxima por Ativo (%)"
              type="number"
              min="1"
              max="100"
              value={maxAllocation}
              onChange={(e) => setMaxAllocation(e.target.value === '' ? 50 : parseInt(e.target.value) || 50)}
              placeholder="80"
              onClear={() => setMaxAllocation(50)}
            />
            <p className="text-xs text-muted-foreground">
              Limite máximo de concentração em um único ativo
            </p>
          </div>

          <Button 
            onClick={handleOptimize} 
            disabled={isOptimizing || availableStrategies.length < 2}
            className="w-full"
            size="lg"
          >
            <Zap className="mr-2 h-4 w-4" />
            {isOptimizing ? 'Otimizando...' : 'Otimizar Portfólio'}
          </Button>
        </>
      )}
    </div>
  );
};