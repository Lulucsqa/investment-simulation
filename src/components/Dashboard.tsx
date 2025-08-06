import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FixedIncomeSimulator } from "./simulators/FixedIncomeSimulator";
import { RealEstateSimulator } from "./simulators/RealEstateSimulator";
import { PortfolioOptimizer } from "./simulators/PortfolioOptimizer";
import { ResultsComparison } from "./ResultsComparison";
import { SimulationResult } from "@/types/investment";

const Dashboard = () => {
  const [results, setResults] = useState<SimulationResult[]>([]);

  const addResult = (result: SimulationResult) => {
    setResults(prev => [...prev, result]);
  };

  const clearResults = () => {
    setResults([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/30 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-info bg-clip-text text-transparent">
            Sistema de Simulação de Investimentos
          </h1>
          <p className="text-muted-foreground text-lg">
            Otimize suas estratégias de investimento em renda fixa e imobiliário
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Simulators Panel */}
          <div className="lg:col-span-2">
            <Card className="shadow-financial">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-gradient-to-r from-primary to-info"></span>
                  Simuladores de Investimento
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="fixed-income" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="fixed-income">Renda Fixa</TabsTrigger>
                    <TabsTrigger value="real-estate">Imobiliário</TabsTrigger>
                    <TabsTrigger value="optimization">Otimização</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="fixed-income" className="mt-6">
                    <FixedIncomeSimulator onResult={addResult} />
                  </TabsContent>
                  
                  <TabsContent value="real-estate" className="mt-6">
                    <RealEstateSimulator onResult={addResult} />
                  </TabsContent>
                  
                  <TabsContent value="optimization" className="mt-6">
                    <PortfolioOptimizer results={results} onResult={addResult} />
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            <ResultsComparison results={results} onClear={clearResults} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;