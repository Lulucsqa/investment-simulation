import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Trash2, TrendingUp, DollarSign, Percent, Calendar } from "lucide-react";
import { SimulationResult } from "@/types/investment";

interface ResultsComparisonProps {
  results: SimulationResult[];
  onClear: () => void;
}

export const ResultsComparison = ({ results, onClear }: ResultsComparisonProps) => {
  if (results.length === 0) {
    return (
      <Card className="border-dashed">
        <CardContent className="flex flex-col items-center justify-center py-8 text-center">
          <TrendingUp className="h-12 w-12 text-muted-foreground mb-4" />
          <h4 className="text-lg font-medium text-muted-foreground mb-2">
            Nenhuma simulação realizada
          </h4>
          <p className="text-sm text-muted-foreground">
            Execute simulações para ver os resultados e comparações aqui.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Prepare chart data
  const maxLength = Math.max(...results.map(r => r.monthlyData.length));
  const chartData = Array.from({ length: maxLength }, (_, index) => {
    const dataPoint: any = { month: index + 1 };
    
    results.forEach((result, resultIndex) => {
      const monthData = result.monthlyData[index];
      if (monthData) {
        dataPoint[`strategy_${resultIndex}`] = monthData.netValue;
      }
    });
    
    return dataPoint;
  });

  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${value.toFixed(2)}%`;
  };

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-base font-medium">Resultados</CardTitle>
          <Button
            variant="outline"
            size="sm"
            onClick={onClear}
            className="h-8 w-8 p-0"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </CardHeader>
        <CardContent className="space-y-4">
          {results.map((result, index) => (
            <div key={result.id} className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: colors[index % colors.length] }}
                  />
                  <span className="font-medium text-sm">{result.name}</span>
                  <Badge 
                    variant={result.type === 'optimized' ? 'default' : 'secondary'}
                    className="text-xs"
                  >
                    {result.type === 'fixed-income' ? 'Renda Fixa' : 
                     result.type === 'real-estate' ? 'Imobiliário' : 
                     result.type === 'optimized' ? 'Otimizado' : 'Misto'}
                  </Badge>
                </div>
                <span className="text-xs text-muted-foreground">
                  {new Date(result.createdAt).toLocaleDateString('pt-BR')}
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="flex items-center gap-1">
                  <DollarSign className="h-3 w-3 text-muted-foreground" />
                  <span className="text-muted-foreground">Final:</span>
                  <span className="font-medium">{formatCurrency(result.finalValue)}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Percent className="h-3 w-3 text-muted-foreground" />
                  <span className="text-muted-foreground">Retorno:</span>
                  <span className={`font-medium ${result.returnPercentage > 0 ? 'text-financial-gain' : 'text-financial-loss'}`}>
                    {formatPercent(result.returnPercentage)}
                  </span>
                </div>
              </div>
              
              {index < results.length - 1 && <Separator />}
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Evolução do Patrimônio
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis 
                  dataKey="month" 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `${value}m`}
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `R$ ${(value / 1000).toFixed(0)}k`}
                />
                <Tooltip 
                  formatter={(value: number, name: string) => [
                    formatCurrency(value),
                    results[parseInt(name.split('_')[1])]?.name || 'Estratégia'
                  ]}
                  labelFormatter={(label) => `Mês ${label}`}
                />
                <Legend 
                  formatter={(value) => {
                    const index = parseInt(value.split('_')[1]);
                    return results[index]?.name || 'Estratégia';
                  }}
                />
                {results.map((_, index) => (
                  <Line
                    key={index}
                    type="monotone"
                    dataKey={`strategy_${index}`}
                    stroke={colors[index % colors.length]}
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 4 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};