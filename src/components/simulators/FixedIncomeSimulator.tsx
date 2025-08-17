import React, { useState } from 'react';

function FixedIncomeSimulator() {
    const [selectedInvestment, setSelectedInvestment] = useState('');
    const investments = [
        { value: 'IPCA+', description: 'Investimento atrelado ao IPCA com juros adicionais.' },
        { value: 'Prefixado', description: 'Investimento com taxa fixa definida no início.' },
        { value: 'Poupança', description: 'Investimento tradicional com rendimento mensal.' }
    ];

    const handleSelectChange = (event) => {
        setSelectedInvestment(event.target.value);
    };

    const getSelectedDescription = () => {
        const investment = investments.find(inv => inv.value === selectedInvestment);
        return investment ? investment.description : '';
    };

    return (
        <div>
            <h2>Simulador de Renda Fixa</h2>
            <label htmlFor="investment-selector">Tipo de Investimento</label>
            <select
                id="investment-selector"
                value={selectedInvestment}
                onChange={handleSelectChange}
            >
                <option value="">Selecione um investimento</option>
                {investments.map(inv => (
                    <option key={inv.value} value={inv.value}>
                        {inv.value}
                    </option>
                ))}
            </select>
            {selectedInvestment && (
                <div>
                    <p><strong>Selecionado:</strong> {selectedInvestment}</p>
                    <p><strong>Descrição:</strong> {getSelectedDescription()}</p>
                </div>
            )}
        </div>
    );
}

export default FixedIncomeSimulator;