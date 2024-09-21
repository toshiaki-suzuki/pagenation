-- テーブルの作成
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- サンプルデータの挿入
INSERT INTO users (name)
SELECT 'User ' || generate_series
FROM generate_series(1, 100);
