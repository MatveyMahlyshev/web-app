from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

class Base(DeclarativeBase):
    __abstract__ = True # указание абстрактности

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) # поле id у каждой таблицы

    # имя таблицы от имени класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"