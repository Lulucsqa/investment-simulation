import { SimulationResult, FixedIncomeParameters, RealEstateParameters, MonthlyData } from "@/types/investment";

export const calculateFixedIncome = (params: FixedIncomeParameters): SimulationResult => {
  const {
    initialAmount,
    monthlyContribution,
    interestRate,
    years,
    inflationRate,
    type,
    taxRate
  } = params;

  const months = years * 12;
  const monthlyRate = interestRate / 100 / 12;
  const monthlyInflation = inflationRate / 100 / 12;
  const monthlyTaxRate = taxRate / 100;

  let currentValue = initialAmount;
  let totalInvested = initialAmount;
  let totalTaxes = 0;
  const monthlyData: MonthlyData[] = [];

  for (let month = 1; month <= months; month++) {
    // Add monthly contribution
    currentValue += monthlyContribution;
    totalInvested += monthlyContribution;

    // Calculate interest
    const interest = currentValue * monthlyRate;
    
    // Apply taxes
    let taxes = 0;
    if (type === 'CDI') {
      // CDI: tax applied monthly on interest
      taxes = interest * monthlyTaxRate;
    } else if (type === 'IPCA+' && month === months) {
      // IPCA+: tax applied only at maturity
      const totalGain = currentValue + interest - totalInvested;
      taxes = totalGain * monthlyTaxRate;
    }

    totalTaxes += taxes;
    const netInterest = interest - taxes;
    currentValue += netInterest;

    // Adjust for inflation (present value)
    const realValue = currentValue / Math.pow(1 + monthlyInflation, month);

    monthlyData.push({
      month,
      invested: totalInvested,
      grossValue: currentValue + taxes,
      netValue: realValue,
      taxes: totalTaxes
    });
  }

  const finalValue = monthlyData[monthlyData.length - 1].netValue;
  const totalReturn = finalValue - totalInvested;
  const returnPercentage = ((finalValue / totalInvested) ** (1 / years) - 1) * 100;

  return {
    id: `fixed-${Date.now()}`,
    name: `${type} ${interestRate.toFixed(1)}% - ${years} anos`,
    type: 'fixed-income',
    finalValue,
    totalInvested,
    totalReturn,
    returnPercentage,
    monthlyData,
    parameters: params,
    createdAt: new Date()
  };
};

export const calculateRealEstate = (params: RealEstateParameters): SimulationResult => {
  const {
    propertyValue,
    downPayment,
    financingRate,
    appreciationRate,
    monthlyRent,
    constructionYears = 0,
    years,
    inflationRate
  } = params;

  const months = years * 12;
  const constructionMonths = constructionYears * 12;
  const financedAmount = propertyValue - downPayment;
  const monthlyFinancingRate = financingRate / 100 / 12;
  const monthlyAppreciation = appreciationRate / 100;
  const monthlyInflation = inflationRate / 100 / 12;
  const rentTaxRate = 0.275; // 27.5% IR on rent

  // SAC calculation
  const principalPayment = financedAmount / months;
  let remainingDebt = financedAmount;
  
  let currentPropertyValue = propertyValue;
  let totalRentIncome = 0;
  let totalInvested = downPayment;
  const monthlyData: MonthlyData[] = [];

  for (let month = 1; month <= months; month++) {
    // Property appreciation
    currentPropertyValue *= (1 + monthlyAppreciation);

    // Financing payment (SAC)
    const interestPayment = remainingDebt * monthlyFinancingRate;
    const totalPayment = principalPayment + interestPayment;
    remainingDebt = Math.max(0, remainingDebt - principalPayment);

    // Rent income (only after construction period)
    let netRentIncome = 0;
    if (month > constructionMonths) {
      const grossRent = monthlyRent * Math.pow(1 + monthlyInflation, month);
      const rentTax = grossRent * rentTaxRate;
      netRentIncome = grossRent - rentTax;
      totalRentIncome += netRentIncome;
    }

    // Net equity calculation
    const equity = currentPropertyValue - remainingDebt + totalRentIncome;
    
    // Adjust for inflation (present value)
    const realValue = equity / Math.pow(1 + monthlyInflation, month);

    monthlyData.push({
      month,
      invested: totalInvested,
      grossValue: equity,
      netValue: realValue,
      taxes: 0, // Taxes already deducted from rent
      propertyValue: currentPropertyValue,
      debt: remainingDebt,
      rentIncome: totalRentIncome
    });
  }

  const finalValue = monthlyData[monthlyData.length - 1].netValue;
  const totalReturn = finalValue - totalInvested;
  const returnPercentage = ((finalValue / totalInvested) ** (1 / years) - 1) * 100;

  return {
    id: `realestate-${Date.now()}`,
    name: `Imobiliário ${constructionYears > 0 ? 'Planta' : 'Pronto'} - ${years} anos`,
    type: 'real-estate',
    finalValue,
    totalInvested,
    totalReturn,
    returnPercentage,
    monthlyData,
    parameters: params,
    createdAt: new Date()
  };
};

export const optimizePortfolio = (
  results: SimulationResult[],
  constraints: {
    targetReturn: number;
    riskTolerance: number;
    maxAllocation: number;
  }
): SimulationResult => {
  const { targetReturn, riskTolerance, maxAllocation } = constraints;
  
  // Simple optimization: weight based on return and risk tolerance
  const returns = results.map(r => r.returnPercentage);
  const maxReturn = Math.max(...returns);
  const minReturn = Math.min(...returns);
  
  // Calculate weights based on normalized returns and risk tolerance
  const weights = results.map(result => {
    const normalizedReturn = (result.returnPercentage - minReturn) / (maxReturn - minReturn);
    const riskAdjustedWeight = normalizedReturn * (riskTolerance / 100);
    return Math.min(riskAdjustedWeight, maxAllocation / 100);
  });

  // Normalize weights to sum to 1
  const totalWeight = weights.reduce((sum, w) => sum + w, 0);
  const normalizedWeights = weights.map(w => w / totalWeight);

  // Calculate portfolio metrics
  const portfolioReturn = results.reduce((sum, result, index) => 
    sum + result.returnPercentage * normalizedWeights[index], 0
  );

  const portfolioFinalValue = results.reduce((sum, result, index) => 
    sum + result.finalValue * normalizedWeights[index], 0
  );

  const portfolioInvested = results.reduce((sum, result, index) => 
    sum + result.totalInvested * normalizedWeights[index], 0
  );

  // Create combined monthly data
  const maxMonths = Math.max(...results.map(r => r.monthlyData.length));
  const monthlyData: MonthlyData[] = [];

  for (let month = 1; month <= maxMonths; month++) {
    let totalValue = 0;
    let totalInvested = 0;
    let totalTaxes = 0;

    results.forEach((result, index) => {
      const monthData = result.monthlyData[month - 1];
      if (monthData) {
        totalValue += monthData.netValue * normalizedWeights[index];
        totalInvested += monthData.invested * normalizedWeights[index];
        totalTaxes += (monthData.taxes || 0) * normalizedWeights[index];
      }
    });

    monthlyData.push({
      month,
      invested: totalInvested,
      grossValue: totalValue,
      netValue: totalValue,
      taxes: totalTaxes
    });
  }

  // Create weight description for name
  const weightDescriptions = results.map((result, index) => 
    `${result.name.split(' - ')[0]}: ${(normalizedWeights[index] * 100).toFixed(1)}%`
  ).join(', ');

  return {
    id: `optimized-${Date.now()}`,
    name: `Portfólio Otimizado (${weightDescriptions})`,
    type: 'optimized',
    finalValue: portfolioFinalValue,
    totalInvested: portfolioInvested,
    totalReturn: portfolioFinalValue - portfolioInvested,
    returnPercentage: portfolioReturn,
    monthlyData,
    parameters: { weights: normalizedWeights, targetReturn, riskTolerance },
    createdAt: new Date()
  };
};