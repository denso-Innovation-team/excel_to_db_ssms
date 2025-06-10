# fix_settings.py
content = """from typing import Optional

class Settings:
    DB_HOST=aws-0-ap-southeast-1.pooler.supabase.com
    DB_PORT=6543
    DB_NAME=postgres
    DB_USER=postgres.ydmmxivfmfgbbphmitgy
    DB_PASSWORD=jsCvOpw2RbFdpf5L
    DB_TYPE=postgresql
    BATCH_SIZE=2000
    MAX_WORKERS=6
    CHUNK_SIZE=10000
    LOG_LEVEL=INFO
    LOG_FILE=logs/excel_to_db.log

settings = Settings()"""

with open("src/config/settings.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed settings.py")
