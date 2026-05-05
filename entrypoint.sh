#!/bin/sh
set -e

# Crear la base de datos si no existe
python - <<'EOF'
import os, pymysql
conn = pymysql.connect(
    host=os.environ.get('DB_HOST', '192.168.100.50'),
    port=int(os.environ.get('DB_PORT', 3309)),
    user=os.environ.get('DB_USER', 'root'),
    password=os.environ.get('DB_PASSWORD', ''),
)
db_name = os.environ.get('DB_NAME', 'jossuni_db')
with conn.cursor() as cur:
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
conn.close()
print(f"Base de datos '{db_name}' lista.")
EOF

python manage.py migrate --noinput
python manage.py crear_grupos
exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 180 --graceful-timeout 30 herzendo.wsgi:application
