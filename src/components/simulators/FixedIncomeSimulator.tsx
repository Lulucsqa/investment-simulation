import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { logger } from "@/lib/logger";
import { Input } from "@/components/ui/input";
import { Info } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export const FixedIncomeSimulator: React.FC = () => {
    const [selectedInvestment, setSelectedInvestment] = useState('');
    const [initialValue, setInitialValue] = useState('');
    const [monthlyContribution, setMonthlyContribution] = useState('');
    const [period, setPeriod] = useState('');
    const [interestRate, setInterestRate] = useState('');
    const [errors, setErrors] = useState<{
        initialValue?: string;
        monthlyContribution?: string;
        period?: string;
        interestRate?: string;
    }>({});
    const [chartData, setChartData] = useState<any[]>([]);
    const [result, setResult] = useState({
        totalValue: 0,
        totalInvested: 0,
        totalInterest: 0
    });

    const investments = [
        { value: 'IPCA+', description: 'Investimento atrelado ao IPCA com juros adicionais.' },
        { value: 'Prefixado', description: 'Investimento com taxa fixa definida no início.' },
        { value: 'Poupança', description: 'Investimento tradicional com rendimento mensal.' }
    ];

    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    };

    const formatNumberInput = (value: string) => {
        // Remove todos os caracteres não numéricos exceto ponto e vírgula
        const cleanValue = value.replace(/[^\d.,]/g, '');
        // Converte vírgula para ponto
        return cleanValue.replace(',', '.');
    };
    
    const handleNumberInput = (value: string, setter: (value: string) => void) => {
        const formattedValue = formatNumberInput(value);
        if (formattedValue === '' || (!isNaN(parseFloat(formattedValue)) && parseFloat(formattedValue) >= 0)) {
            setter(formattedValue);
        }
    };

    const validateFields = () => {
        const newErrors: any = {};
        logger.debug('Validando campos do simulador', {
            initialValue,
            monthlyContribution,
            period,
            interestRate
        });
        
        if (!initialValue || parseFloat(initialValue) <= 0) {
            newErrors.initialValue = 'Valor inicial deve ser maior que zero';
            logger.warn('Valor inicial inválido', { value: initialValue });
        }
        
        if (monthlyContribution && parseFloat(monthlyContribution) < 0) {
            newErrors.monthlyContribution = 'Aporte mensal não pode ser negativo';
        }
        
        if (!period || parseInt(period) < 1 || parseInt(period) > 600) {
            newErrors.period = 'Período deve estar entre 1 e 600 meses';
        }
        
        if (!interestRate || parseFloat(interestRate) <= 0 || parseFloat(interestRate) > 50) {
            newErrors.interestRate = 'Taxa deve estar entre 0% e 50% a.a.';
        }
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    // Efeito para persistir a seleção do investimento
    useEffect(() => {
        if (selectedInvestment) {
            const investment = investments.find(inv => inv.value === selectedInvestment);
            if (investment) {
                // Aqui podemos adicionar lógica específica para cada tipo de investimento
                switch (selectedInvestment) {
                    case 'IPCA+':
                        // Taxa IPCA + spread
                        setInterestRate('12');
                        break;
                    case 'Prefixado':
                        setInterestRate('10');
                        break;
                    case 'Poupança':
                        setInterestRate('6');
                        break;
                }
            }
        }
    }, [selectedInvestment]);

    useEffect(() => {
        if (initialValue && period && interestRate && validateFields()) {
            logger.info('Iniciando cálculo de simulação', {
                investment: selectedInvestment,
                initialValue,
                monthlyContribution,
                period,
                interestRate
            });

            try {
                const initial = parseFloat(initialValue);
                const monthly = parseFloat(monthlyContribution);
                const months = parseInt(period);
                const yearlyRate = parseFloat(interestRate) / 100;
            const monthlyRate = yearlyRate / 12;

            let data = [];
            let accumulated = initial;
            let invested = initial;

            for (let i = 0; i <= months; i++) {
                accumulated = i === 0 ? initial : 
                    accumulated * (1 + monthlyRate) + monthly;
                invested = i === 0 ? initial : invested + monthly;

                data.push({
                    month: i,
                    invested: invested,
                    accumulated: accumulated,
                });
            }

            setChartData(data);
                setResult({
                    totalValue: accumulated,
                    totalInvested: invested,
                    totalInterest: accumulated - invested
                });

                logger.info('Simulação calculada com sucesso', {
                    totalValue: accumulated,
                    totalInvested: invested,
                    totalInterest: accumulated - invested
                });
            } catch (error) {
                logger.error('Erro ao calcular simulação', error);
            }
        }
    }, [initialValue, monthlyContribution, period, interestRate, selectedInvestment]);

    return (
        <Card className="w-full p-6">
            <CardHeader>
                <CardTitle>Simulador de Renda Fixa</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-6">
                    <div className="space-y-2">
                        <Label>Tipo de Investimento</Label>
                        <Select 
                            value={selectedInvestment} 
                            onValueChange={(value) => {
                                logger.info('Tipo de investimento selecionado', { investment: value });
                                setSelectedInvestment(value);
                            }}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Selecione um investimento" />
                            </SelectTrigger>
                            <SelectContent>
                                {investments.map(inv => (
                                    <SelectItem key={inv.value} value={inv.value}>
                                        {inv.value}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <div className="flex items-center gap-2 mt-2 p-3 bg-secondary/20 rounded-md">
                            <Info className="h-4 w-4" />
                            <div className="flex flex-col">
                                <span className="font-medium">{selectedInvestment || 'Selecione um investimento'}</span>
                                <span className="text-sm text-muted-foreground">
                                    {selectedInvestment 
                                        ? investments.find(inv => inv.value === selectedInvestment)?.description
                                        : 'Escolha um tipo de investimento para ver mais informações'}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Valor Inicial (R$)</Label>
                            <div className="space-y-1">
                                <Input
                                    type="text"
                                    inputMode="decimal"
                                    value={initialValue}
                                    onChange={(e) => handleNumberInput(e.target.value, setInitialValue)}
                                    placeholder="0,00"
                                    className={`text-right ${errors.initialValue ? 'border-red-500' : ''}`}
                                />
                                {errors.initialValue && (
                                    <span className="text-sm text-red-500">{errors.initialValue}</span>
                                )}
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label>Aporte Mensal (R$)</Label>
                            <div className="space-y-1">
                                <Input
                                    type="text"
                                    inputMode="decimal"
                                    value={monthlyContribution}
                                    onChange={(e) => handleNumberInput(e.target.value, setMonthlyContribution)}
                                    placeholder="0,00"
                                    className={`text-right ${errors.monthlyContribution ? 'border-red-500' : ''}`}
                                />
                                {errors.monthlyContribution && (
                                    <span className="text-sm text-red-500">{errors.monthlyContribution}</span>
                                )}
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label>Período (meses)</Label>
                            <div className="space-y-1">
                                <Input
                                    type="number"
                                    value={period}
                                    onChange={(e) => setPeriod(e.target.value)}
                                    className={`text-right ${errors.period ? 'border-red-500' : ''}`}
                                />
                                {errors.period && (
                                    <span className="text-sm text-red-500">{errors.period}</span>
                                )}
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label>Taxa de Juros (% a.a.)</Label>
                            <div className="space-y-1">
                                <Input
                                    type="number"
                                    value={interestRate}
                                    onChange={(e) => setInterestRate(e.target.value)}
                                    className={`text-right ${errors.interestRate ? 'border-red-500' : ''}`}
                                />
                                {errors.interestRate && (
                                    <span className="text-sm text-red-500">{errors.interestRate}</span>
                                )}
                            </div>
                        </div>
                    </div>

                    {chartData.length > 0 && (
                        <div className="space-y-6 mt-6">
                            <Card className="p-4">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <div>
                                        <Label className="text-sm">Valor Total</Label>
                                        <p className="text-2xl font-bold">
                                            {formatCurrency(result.totalValue)}
                                        </p>
                                    </div>
                                    <div>
                                        <Label className="text-sm">Total Investido</Label>
                                        <p className="text-2xl font-bold">
                                            {formatCurrency(result.totalInvested)}
                                        </p>
                                    </div>
                                    <div>
                                        <Label className="text-sm">Juros Totais</Label>
                                        <p className="text-2xl font-bold text-green-500">
                                            {formatCurrency(result.totalInterest)}
                                        </p>
                                    </div>
                                </div>
                            </Card>

                            <div className="w-full overflow-x-auto">
                                <LineChart
                                    width={800}
                                    height={400}
                                    data={chartData}
                                    margin={{
                                        top: 5,
                                        right: 30,
                                        left: 20,
                                        bottom: 5,
                                    }}
                                >
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="month" />
                                    <YAxis />
                                    <Tooltip formatter={(value) => formatCurrency(Number(value))} />
                                    <Legend />
                                    <Line
                                        type="monotone"
                                        dataKey="invested"
                                        name="Total Investido"
                                        stroke="#8884d8"
                                    />
                                    <Line
                                        type="monotone"
                                        dataKey="accumulated"
                                        name="Valor Acumulado"
                                        stroke="#82ca9d"
                                    />
                                </LineChart>
                            </div>
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    );
};