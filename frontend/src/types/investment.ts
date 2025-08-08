export interface InvestmentParameters {
  initialAmount: number;
  monthlyContribution: number;
  interestRate: number;
  years: number;
  inflationRate: number;
}

export interface FixedIncomeParameters extends InvestmentParameters {
  type: 'CDI' | 'IPCA+';
  taxRate: number; // IR rate
}

export interface RealEstateParameters {
  propertyValue: number;
  downPayment: number;
  financingRate: number;
  appreciationRate: number;
  monthlyRent: number;
  constructionYears?: number; // For properties under construction
  years: number;
  inflationRate: number;
}

export interface SimulationResult {
  id: string;
  name: string;
  type: 'fixed-income' | 'real-estate' | 'mixed' | 'optimized';
  finalValue: number;
  totalInvested: number;
  totalReturn: number;
  returnPercentage: number;
  monthlyData: MonthlyData[];
  parameters: any;
  createdAt: Date;
}

export interface MonthlyData {
  month: number;
  invested: number;
  grossValue: number;
  netValue: number;
  taxes: number;
  propertyValue?: number;
  debt?: number;
  rentIncome?: number;
}

export interface OptimizationResult {
  weights: { [key: string]: number };
  optimalInitialAmount?: number;
  optimalMonthlyContribution?: number;
  expectedReturn: number;
  riskLevel: number;
}

export interface PortfolioAllocation {
  fixedIncome: number;
  realEstate: number;
  mixed?: number;
}