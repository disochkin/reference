# universal_import.py
import csv
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from database import SessionLocal, Base, engine


def load_csv_to_db(file_path: str, model_class: Base, session: Session | None = None):
    """
    Универсальный загрузчик CSV в любую модель SQLAlchemy.

    :param file_path: путь к CSV файлу
    :param model_class: класс модели (например, Equipment)
    :param session: объект Session (если не передан — создаётся новый)
    """
    local_session = False
    if session is None:
        session = SessionLocal()
        local_session = True

    try:
        # получаем список допустимых полей модели
        mapper = inspect(model_class)
        model_columns = {c.key for c in mapper.columns}

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                # оставляем только известные модели поля
                filtered = {k: v for k, v in row.items() if k in model_columns}

                # приведение типов (float/int если нужно)
                for col in mapper.columns:
                    if col.name in filtered and filtered[col.name] != "":
                        try:
                            if isinstance(col.type.python_type, type):
                                filtered[col.name] = col.type.python_type(filtered[col.name])
                        except Exception:
                            pass  # если не удаётся преобразовать — оставляем строку

                obj = model_class(**filtered)
                session.merge(obj)
                count += 1

            session.commit()
            print(f"✅ Загружено {count} записей в {model_class.__tablename__}")
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка при загрузке {model_class.__tablename__}: {e}")
    finally:
        if local_session:
            session.close()
