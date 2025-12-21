#!/bin/bash
# PostgreSQL 설정 확인 스크립트

echo "=== PostgreSQL 설정 확인 ==="

# pg_hba.conf 확인
echo "1. pg_hba.conf 설정 확인:"
echo "   다음 명령어로 확인하세요:"
echo "   sudo cat /etc/postgresql/*/main/pg_hba.conf | grep -E '^[^#]'"
echo ""

# postgresql.conf 확인
echo "2. postgresql.conf listen_addresses 확인:"
echo "   다음 명령어로 확인하세요:"
echo "   sudo grep '^listen_addresses' /etc/postgresql/*/main/postgresql.conf"
echo ""

# 현재 연결 테스트
echo "3. 현재 데이터베이스 연결 테스트:"
cd /srv/dbweb
source venv/bin/activate
python -c "
import os
from dotenv import load_dotenv
load_dotenv('/etc/dbweb/db.env')
import psycopg2
try:
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'dbweb'),
        user=os.getenv('DB_USER', 'django'),
        password=os.getenv('DB_PASSWORD', ''),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
    print('✓ 데이터베이스 연결 성공')
    conn.close()
except Exception as e:
    print(f'✗ 데이터베이스 연결 실패: {e}')
"

echo ""
echo "=== 확인 완료 ==="
echo ""
echo "만약 localhost만 허용되어 있다면, 다음을 확인하세요:"
echo "1. pg_hba.conf에서 'host' 설정이 '127.0.0.1/32' 또는 'localhost'로 되어 있는지"
echo "2. postgresql.conf에서 listen_addresses가 'localhost' 또는 '*'로 설정되어 있는지"
echo "3. Django는 localhost의 PostgreSQL에 연결하므로 문제없어야 합니다."

