import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { CustomSelect } from "@/components/ui/custom-select";
import { MobileFriendlyInput } from "@/components/ui/mobile-friendly-input";
import { Badge } from "@/components/ui/badge";
import { Calculator, TrendingUp } from "lucide-react";
import { SimulationResult, FixedIncomeParameters } from "@/types/investment";
import { calculateFixedIncome } from "@/lib/calculations";
import { toast } from "sonner";

interface FixedIncomeSimulatorProps {
  onResult: (result: SimulationResult) => void;
}

export const FixedIncomeSimulator = ({ onResult }: FixedIncomeSimulatorProps) => {
  const [parameters, setParameters] = useState<FixedIncomeParameters>({
    initialAmount: 50000,
    monthlyContribution: 2000,
    interestRate: 12.5, // CDI percentage
    years: 10,
    inflationRate: 4.5,
    type: 'CDI',
    taxRate: 15
  });

  const [isCalculating, setIsCalculating] = useState(false);
  const [selectedType, setSelectedType] = useState<'CDI' | 'IPCA+'>('CDI');

  const handleInputChange = (field: keyof FixedIncomeParameters, value: string | number) => {
    setParameters(prev => ({
      ...prev,
      [field]: typeof value === 'string' ? (value === '' ? 0 : parseFloat(value) || 0) : value
    }));
  };

  const handleTypeChange = (value: 'CDI' | 'IPCA+') => {
    console.log('Mudando tipo para:', value);
    setSelectedType(value);
    setParameters(prev => ({
      ...prev,
      type: value
    }));
  };

  const handleSimulate = async () => {
    setIsCalculating(true);
    
    try {
      const result = calculateFixedIncome(parameters);
      onResult(result);
      
      toast.success("Simulação de renda fixa concluída!", {
        description: `Valor final: R$ ${result.finalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
      });
    } catch (error) {
      toast.error("Erro na simulação", {
        description: "Verifique os parâmetros inseridos."
      });
    } finally {
      setIsCalculating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp className="h-5 w-5 text-info" />
        <h3 className="text-lg font-semibold">Simulador de Renda Fixa</h3>
        <Badge variant="secondary">{selectedType}</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="investment-type">Tipo de Investimento</Label>
          <CustomSelect
            id="investment-type"
            value={selectedType}
            onValueChange={handleTypeChange}
            options={[
              { value: 'CDI', label: 'CDI' },
              { value: 'IPCA+', label: 'IPCA+' }
            ]}
            placeholder="Selecione o tipo de investimento"
            className="w-full"
          />
        </div>

        <MobileFriendlyInput
          id="initial-amount"
          label="Aporte Inicial (R$)"
          type="number"
          value={parameters.initialAmount}
          onChange={(e) => handleInputChange('initialAmount', e.target.value)}
          placeholder="50.000"
          onClear={() => handleInputChange('initialAmount', 0)}
        />

        <MobileFriendlyInput
          id="monthly-contribution"
          label="Aporte Mensal (R$)"
          type="number"
          value={parameters.monthlyContribution}
          onChange={(e) => handleInputChange('monthlyContribution', e.target.value)}
          placeholder="2.000"
          onClear={() => handleInputChange('monthlyContribution', 0)}
        />

        <MobileFriendlyInput
          id="interest-rate"
          label={selectedType === 'CDI' ? 'Taxa CDI (% a.a.)' : 'Taxa IPCA+ (% a.a.)'}
          type="number"
          step="0.1"
          value={parameters.interestRate}
          onChange={(e) => handleInputChange('interestRate', e.target.value)}
          placeholder="12.5"
          onClear={() => handleInputChange('interestRate', 0)}
        />

        <MobileFriendlyInput
          id="years"
          label="Prazo (anos)"
          type="number"
          value={parameters.years}
          onChange={(e) => handleInputChange('years', e.target.value)}
          placeholder="10"
          onClear={() => handleInputChange('years', 0)}
        />

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
            Informações Tributárias
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <MobileFriendlyInput
              id="tax-rate"
              label="Imposto de Renda (%)"
              type="number"
              step="0.1"
              value={parameters.taxRate}
              onChange={(e) => handleInputChange('taxRate', e.target.value)}
              placeholder="15"
              onClear={() => handleInputChange('taxRate', 0)}
            />
            <p className="text-xs text-muted-foreground">
              {selectedType === 'CDI' 
                ? 'IR aplicado mensalmente sobre rendimentos' 
                : 'IR aplicado apenas no vencimento'
              }
            </p>
          </div>
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