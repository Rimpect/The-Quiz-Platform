"""Лёгкая авто-миграция схемы.

create_all создаёт только отсутствующие таблицы, но не добавляет новые колонки
в уже существующие. Здесь при старте сравниваем колонки моделей с реальной БД и
ALTER-им недостающие — чтобы новые поля моделей (cover_url, rejection_reason и т.п.)
не требовали ручного ALTER TABLE.

Ограничения: выполняется только ДОБАВЛЕНИЕ колонок (как nullable). Изменение типа,
переименование и удаление колонок не делаются.
"""
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from ..utils.logger import logger
from .database import Base


def sync_missing_columns(engine: Engine) -> int:
    """Добавить недостающие колонки моделей в существующие таблицы. Возвращает
    количество добавленных колонок."""
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    added = 0

    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue  # новую таблицу создаст create_all

        existing_cols = {c["name"] for c in inspector.get_columns(table.name)}
        for col in table.columns:
            if col.name in existing_cols:
                continue
            try:
                col_type = col.type.compile(dialect=engine.dialect)
                ddl = f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {col_type}'
                with engine.begin() as conn:
                    conn.execute(text(ddl))
                added += 1
                logger.info(
                    f"Auto-migrate: added column {table.name}.{col.name} ({col_type})"
                )
            except Exception as e:
                logger.warning(
                    f"Auto-migrate: skip {table.name}.{col.name}: {e}"
                )

    return added
