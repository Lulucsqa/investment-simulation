-- Investment Simulation System - Supabase Database Setup
-- Execute este script no SQL Editor do Supabase

-- 1. Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Criar tabela de simulações
CREATE TABLE IF NOT EXISTS simulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    strategy VARCHAR NOT NULL CHECK (strategy IN ('CDI', 'IPCA', 'REAL_ESTATE_CONSTRUCTION', 'REAL_ESTATE_READY', 'MIXED_STRATEGY')),
    parameters JSONB NOT NULL,
    result JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Criar tabela de portfólios otimizados
CREATE TABLE IF NOT EXISTS portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR NOT NULL,
    strategies JSONB NOT NULL,
    optimal_weights JSONB NOT NULL,
    final_return DECIMAL(15,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_simulations_user_id ON simulations(user_id);
CREATE INDEX IF NOT EXISTS idx_simulations_strategy ON simulations(strategy);
CREATE INDEX IF NOT EXISTS idx_simulations_created_at ON simulations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 5. Criar função para estatísticas de estratégias
CREATE OR REPLACE FUNCTION get_strategy_stats()
RETURNS TABLE(strategy VARCHAR, count BIGINT, avg_return DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.strategy,
        COUNT(*) as count,
        AVG((s.result->>'patrimonio_final')::DECIMAL) as avg_return
    FROM simulations s
    GROUP BY s.strategy
    ORDER BY count DESC;
END;
$$ LANGUAGE plpgsql;

-- 6. Criar função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 7. Criar triggers para updated_at
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolios_updated_at 
    BEFORE UPDATE ON portfolios 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 8. Configurar Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE simulations ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolios ENABLE ROW LEVEL SECURITY;

-- 9. Políticas de segurança para usuários
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- 10. Políticas de segurança para simulações
CREATE POLICY "Users can view own simulations" ON simulations
    FOR SELECT USING (
        user_id IN (
            SELECT id FROM users WHERE auth.uid()::text = id::text
        )
    );

CREATE POLICY "Users can insert own simulations" ON simulations
    FOR INSERT WITH CHECK (
        user_id IN (
            SELECT id FROM users WHERE auth.uid()::text = id::text
        )
    );

CREATE POLICY "Users can delete own simulations" ON simulations
    FOR DELETE USING (
        user_id IN (
            SELECT id FROM users WHERE auth.uid()::text = id::text
        )
    );

-- 11. Políticas de segurança para portfólios
CREATE POLICY "Users can view own portfolios" ON portfolios
    FOR SELECT USING (
        user_id IN (
            SELECT id FROM users WHERE auth.uid()::text = id::text
        )
    );

CREATE POLICY "Users can insert own portfolios" ON portfolios
    FOR INSERT WITH CHECK (
        user_id IN (
            SELECT id FROM users WHERE auth.uid()::text = id::text
        )
    );

CREATE POLICY "Users can update own portfolios" ON portfolios
    FOR UPDATE USING (
        user_id IN (
            SELECT id FROM users WHERE auth.uid()::text = id::text
        )
    );

CREATE POLICY "Users can delete own portfolios" ON portfolios
    FOR DELETE USING (
        user_id IN (
            SELECT id FROM users WHERE auth.uid()::text = id::text
        )
    );

-- 12. Política para acesso público de leitura (opcional - para estatísticas)
CREATE POLICY "Public read access for stats" ON simulations
    FOR SELECT USING (true);

-- 13. Inserir dados de exemplo (opcional)
INSERT INTO users (email, name) VALUES 
    ('demo@investsim.com', 'Usuário Demo'),
    ('test@investsim.com', 'Usuário Teste')
ON CONFLICT (email) DO NOTHING;

-- 14. Criar view para estatísticas públicas
CREATE OR REPLACE VIEW public_stats AS
SELECT 
    COUNT(*) as total_simulations,
    COUNT(DISTINCT user_id) as total_users,
    strategy,
    COUNT(*) as strategy_count,
    AVG((result->>'patrimonio_final')::DECIMAL) as avg_final_value,
    AVG((result->>'rentabilidade_total')::DECIMAL) as avg_total_return
FROM simulations
GROUP BY strategy;

-- 15. Comentários nas tabelas
COMMENT ON TABLE users IS 'Usuários do sistema de simulação de investimentos';
COMMENT ON TABLE simulations IS 'Simulações de investimento realizadas pelos usuários';
COMMENT ON TABLE portfolios IS 'Portfólios otimizados criados pelos usuários';

COMMENT ON COLUMN simulations.strategy IS 'Tipo de estratégia: CDI, IPCA, REAL_ESTATE_CONSTRUCTION, REAL_ESTATE_READY, MIXED_STRATEGY';
COMMENT ON COLUMN simulations.parameters IS 'Parâmetros de entrada da simulação em formato JSON';
COMMENT ON COLUMN simulations.result IS 'Resultado da simulação em formato JSON';

-- 16. Função para limpar dados antigos (opcional)
CREATE OR REPLACE FUNCTION cleanup_old_simulations(days_old INTEGER DEFAULT 365)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM simulations 
    WHERE created_at < NOW() - INTERVAL '1 day' * days_old;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Mensagem de sucesso
DO $$
BEGIN
    RAISE NOTICE 'Investment Simulation System database setup completed successfully!';
    RAISE NOTICE 'Tables created: users, simulations, portfolios';
    RAISE NOTICE 'Indexes, functions, and RLS policies configured';
    RAISE NOTICE 'Ready to use with the FastAPI backend';
END $$;