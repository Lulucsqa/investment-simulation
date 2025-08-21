-- Create logs table
CREATE TABLE IF NOT EXISTS logs (
    id BIGSERIAL PRIMARY KEY,
    level VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    data JSONB,
    user_id VARCHAR(255),
    component VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level);
CREATE INDEX IF NOT EXISTS idx_logs_user_id ON logs(user_id);

-- Create view for recent logs
CREATE OR REPLACE VIEW recent_logs AS
SELECT *
FROM logs
WHERE timestamp >= NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;

-- Create function to clean old logs
CREATE OR REPLACE FUNCTION cleanup_old_logs()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM logs
    WHERE timestamp < NOW() - INTERVAL '30 days';
END;
$$;

-- Create scheduled job to cleanup old logs
SELECT cron.schedule(
    'cleanup-old-logs',
    '0 0 * * *', -- Run daily at midnight
    'SELECT cleanup_old_logs()'
);
