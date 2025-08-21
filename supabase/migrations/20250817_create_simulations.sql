-- Create simulations table
CREATE TABLE IF NOT EXISTS simulations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL,
    type VARCHAR(50) NOT NULL,
    parameters JSONB NOT NULL,
    result JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_simulations_user_id ON simulations(user_id);
CREATE INDEX IF NOT EXISTS idx_simulations_type ON simulations(type);
CREATE INDEX IF NOT EXISTS idx_simulations_created_at ON simulations(created_at);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_simulations_updated_at
    BEFORE UPDATE ON simulations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add RLS policies
ALTER TABLE simulations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own simulations"
    ON simulations FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own simulations"
    ON simulations FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own simulations"
    ON simulations FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own simulations"
    ON simulations FOR DELETE
    USING (auth.uid() = user_id);
