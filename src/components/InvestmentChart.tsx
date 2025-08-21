import React, { useMemo, useCallback } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Card } from '@/components/ui/card';

interface InvestmentChartProps {
  data: Array<{
    month: number;
    invested: number;
    accumulated: number;
  }>;
  width?: number;
  height?: number;
}

export const InvestmentChart: React.FC<InvestmentChartProps> = ({
  data,
  width = 800,
  height = 400
}) => {
  // Memo para formatar valores em reais
  const formatCurrency = useCallback((value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  }, []);

  // Memo para calcular domínio do eixo Y
  const yDomain = useMemo(() => {
    if (!data.length) return [0, 100];
    const values = data.flatMap(d => [d.invested, d.accumulated]);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const padding = (max - min) * 0.1;
    return [min - padding, max + padding];
  }, [data]);

  // Memo para calcular ticks do eixo X
  const xTicks = useMemo(() => {
    if (!data.length) return [];
    const totalMonths = data[data.length - 1].month;
    const interval = Math.ceil(totalMonths / 12);
    return Array.from({ length: Math.ceil(totalMonths / interval) + 1 }, (_, i) => i * interval);
  }, [data]);

  // Tooltip personalizado com memo
  const CustomTooltip = useCallback(({ active, payload, label }: any) => {
    if (!active || !payload) return null;

    return (
      <Card className="p-3 bg-background/95 backdrop-blur-sm shadow-lg">
        <p className="font-medium">Mês {label}</p>
        <div className="space-y-1 mt-2">
          <p className="text-sm text-muted-foreground">
            <span className="inline-block w-4 h-2 bg-[#8884d8] mr-2" />
            Investido: {formatCurrency(payload[0].value)}
          </p>
          <p className="text-sm text-muted-foreground">
            <span className="inline-block w-4 h-2 bg-[#82ca9d] mr-2" />
            Acumulado: {formatCurrency(payload[1].value)}
          </p>
        </div>
      </Card>
    );
  }, [formatCurrency]);

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
        <XAxis
          dataKey="month"
          ticks={xTicks}
          label={{ value: 'Meses', position: 'bottom' }}
        />
        <YAxis
          domain={yDomain}
          tickFormatter={formatCurrency}
          width={100}
        />
        <Tooltip content={CustomTooltip} />
        <Legend />
        <Line
          type="monotone"
          dataKey="invested"
          name="Total Investido"
          stroke="#8884d8"
          dot={false}
          strokeWidth={2}
        />
        <Line
          type="monotone"
          dataKey="accumulated"
          name="Valor Acumulado"
          stroke="#82ca9d"
          dot={false}
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
