import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { MobileFriendlyInput } from "@/components/ui/mobile-friendly-input";
import { Badge } from "@/components/ui/badge";
import { Home, Building, Calculator } from "lucide-react";
import { SimulationResult, RealEstateParameters } from "@/types/investment";
import { calculateRealEstate } from "@/lib/calculations";
import { toast } from "sonner";

interface RealEstateSimulatorProps {
  onResult: (result: SimulationResult) => void;
}

export const RealEstateSimulator = ({ onResult }: RealEstateSimulatorProps) => {
  const [parameters, setParameters] = useState<RealEstateParameters>({
    propertyValue: 500000,
    downPayment: 150000,
    financingRate: 10.5,
    appreciationRate: 0.5, // Monthly appreciation
    monthlyRent: 2500,
    years: 20,
    inflationRate: 4.5,
    constructionYears: 0
  });

  const [isUnderConstruction, setIsUnderConstruction] = useState(false);
  const [isCalculating, setIsCalculating] = useState(false);

  const handleInputChange = (field: keyof RealEstateParameters, value: string | number) => {
    setParameters(prev => ({
      ...prev,
      [field]: typeof value === 'string' ? (value === '' ? 0 : parseFloat(value) || 0) : value
    }));
  };

  const handleConstructionToggle = (checked: boolean) => {
    setIsUnderConstruction(checked);
    setParameters(prev => ({
      ...prev,
      constructionYears: checked ? 3 : 0
    }));
  };

  const handleSimulate = async () => {
    setIsCalculating(true);
    
    try {
      const result = calculateRealEstate(parameters);
      onResult(result);
      
      toast.success("Simulação imobiliária concluída!", {
        description: `Patrimônio final: R$ ${result.finalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
      });
    } catch (error) {
      toast.error("Erro na simulação", {
        description: "Verifique os parâmetros inseridos."
      });
    } finally {
      setIsCalculating(false);
    }
  };

  const financedAmount = parameters.propertyValue - parameters.downPayment;
  const loanToValue = (financedAmount / parameters.propertyValue) * 100;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          {isUnderConstruction ? (
            <Building className="h-5 w-5 text-warning" />
          ) : (
            <Home className="h-5 w-5 text-success" />
          )}
          <h3 className="text-lg font-semibold">Simulador Imobiliário</h3>
          <Badge variant={isUnderConstruction ? "secondary" : "default"}>
            {isUnderConstruction ? "Na Planta" : "Pronto"}
          </Badge>
        </div>

        <div className="flex items-center space-x-2">
          <Label htmlFor="construction-toggle" className="text-sm">
            Na planta
          </Label>
          <Switch
            id="construction-toggle"
            checked={isUnderConstruction}
            onCheckedChange={handleConstructionToggle}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <MobileFriendlyInput
          id="property-value"
          label="Valor do Imóvel (R$)"
          type="number"
          value={parameters.propertyValue}
          onChange={(e) => handleInputChange('propertyValue', e.target.value)}
          placeholder="500.000"
          onClear={() => handleInputChange('propertyValue', 0)}
        />

        <MobileFriendlyInput
          id="down-payment"
          label="Entrada (R$)"
          type="number"
          value={parameters.downPayment}
          onChange={(e) => handleInputChange('downPayment', e.target.value)}
          placeholder="150.000"
          onClear={() => handleInputChange('downPayment', 0)}
        />

        <MobileFriendlyInput
          id="financing-rate"
          label="Taxa de Financiamento (% a.a.)"
          type="number"
          step="0.1"
          value={parameters.financingRate}
          onChange={(e) => handleInputChange('financingRate', e.target.value)}
          placeholder="10.5"
          onClear={() => handleInputChange('financingRate', 0)}
        />

        <MobileFriendlyInput
          id="appreciation-rate"
          label="Valorização Mensal (%)"
          type="number"
          step="0.1"
          value={parameters.appreciationRate}
          onChange={(e) => handleInputChange('appreciationRate', e.target.value)}
          placeholder="0.5"
          onClear={() => handleInputChange('appreciationRate', 0)}
        />

        <MobileFriendlyInput
          id="monthly-rent"
          label="Aluguel Mensal (R$)"
          type="number"
          value={parameters.monthlyRent}
          onChange={(e) => handleInputChange('monthlyRent', e.target.value)}
          placeholder="2.500"
          onClear={() => handleInputChange('monthlyRent', 0)}
        />

        <MobileFriendlyInput
          id="years"
          label="Prazo (anos)"
          type="number"
          value={parameters.years}
          onChange={(e) => handleInputChange('years', e.target.value)}
          placeholder="20"
          onClear={() => handleInputChange('years', 0)}
        />

        {isUnderConstruction && (
          <MobileFriendlyInput
            id="construction-years"
            label="Tempo de Construção (anos)"
            type="number"
            value={parameters.constructionYears}
            onChange={(e) => handleInputChange('constructionYears', e.target.value)}
            placeholder="3"
            onClear={() => handleInputChange('constructionYears', 0)}
          />
        )}

        <MobileFriendlyInput
          id="inflation"
          label="Inflação (% a.a.)"
          type="number"
          step="0.1"
          value={parameters.inflationRate}
          onChange={(e) => handleInputChange('inflationRate', e.target.value)}
          placeholder="4.5"
          onClear={() => handleInputChange('inflationRate', 0)}
        />
      </div>

      <Card className="bg-muted/50">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Resumo do Financiamento
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Valor Financiado:</span>
            <span className="font-medium">
              R$ {financedAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span>LTV (Loan to Value):</span>
            <span className="font-medium">{loanToValue.toFixed(1)}%</span>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            Sistema SAC (Amortização Constante) • IR de 27,5% sobre aluguel
          </p>
        </CardContent>
      </Card>

      <Button 
        onClick={handleSimulate} 
        disabled={isCalculating}
        className="w-full"
        size="lg"
      >
        <Calculator className="mr-2 h-4 w-4" />
        {isCalculating ? 'Calculando...' : 'Simular Investimento'}
      </Button>
    </div>
  );
};