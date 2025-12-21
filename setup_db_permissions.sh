#!/bin/bash
# PostgreSQL 데이터베이스 권한 설정 스크립트

echo "PostgreSQL 데이터베이스 권한을 설정합니다..."

sudo -u postgres psql << EOF
-- 데이터베이스 소유자 변경
ALTER DATABASE dbweb OWNER TO django;

-- dbweb 데이터베이스에 연결
\c dbweb

-- public 스키마 소유자 변경
ALTER SCHEMA public OWNER TO django;

-- 모든 권한 부여
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO django;

-- 기본 권한 설정 (향후 생성되는 객체에 대한 권한)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO django;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO django;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO django;
EOF

echo "권한 설정이 완료되었습니다!"

