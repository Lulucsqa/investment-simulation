import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { InfoCircledIcon } from "@radix-ui/react-icons";

export const FixedIncomeSimulator: React.FC = () => {
    const [selectedInvestment, setSelectedInvestment] = useState('');
    const investments = [
        { value: 'IPCA+', description: 'Investimento atrelado ao IPCA com juros adicionais.' },
        { value: 'Prefixado', description: 'Investimento com taxa fixa definida no início.' },
        { value: 'Poupança', description: 'Investimento tradicional com rendimento mensal.' }
    ];

    const handleSelectChange = (value: string) => {
        setSelectedInvestment(value);
    };

    const getSelectedDescription = () => {
        const investment = investments.find(inv => inv.value === selectedInvestment);
        return investment ? investment.description : '';
    };

    return (
        <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
                <CardTitle className="text-2xl font-bold text-center">
                    Simulador de Renda Fixa
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="space-y-2">
                    <Label htmlFor="investment-type">Tipo de Investimento</Label>
                    <Select onValueChange={handleSelectChange} value={selectedInvestment}>
                        <SelectTrigger>
                            <SelectValue placeholder="Selecione um investimento" />
                        </SelectTrigger>
                        <SelectContent>
                            {investments.map((inv) => (
                                <SelectItem key={inv.value} value={inv.value}>
                                    {inv.value}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>

                {selectedInvestment && (
                    <Card className="bg-muted">
                        <CardContent className="pt-6">
                            <div className="flex items-start space-x-2">
                                <InfoCircledIcon className="w-5 h-5 mt-0.5 text-muted-foreground" />
                                <div>
                                    <h4 className="font-medium">{selectedInvestment}</h4>
                                    <p className="text-sm text-muted-foreground">
                                        {getSelectedDescription()}
                                    </p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                )}
            </CardContent>
        </Card>
    );
};