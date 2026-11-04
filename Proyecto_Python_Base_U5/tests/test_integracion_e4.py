"""E4: pruebas de integración SQLite aisladas por prueba."""
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.domain import Order
from src.repository import OrderRow, SqlOrderRepository, make_engine


@pytest.fixture
def engine_sqlite():
    engine = make_engine()
    yield engine
    engine.dispose()


def test_e4_commit_pedido_250_id_2(engine_sqlite):
    """Tras commit, id, total y estado persisten en otra sesión."""
    with Session(engine_sqlite) as session:
        SqlOrderRepository(session).save(2, Order(total=250, status="NEW"))
        session.commit()

    with Session(engine_sqlite) as new_session:
        saved = new_session.get(OrderRow, 2)
        assert saved is not None
        assert saved.id == 2
        assert saved.total == 250
        assert saved.status == "NEW"


def test_e4_rollback_descarta_pedido(engine_sqlite):
    with Session(engine_sqlite) as session:
        SqlOrderRepository(session).save(3, Order(total=90))
        session.flush()  # fuerza el INSERT antes de revertir
        assert session.get(OrderRow, 3) is not None
        session.rollback()

    with Session(engine_sqlite) as new_session:
        assert new_session.get(OrderRow, 3) is None


def test_e4_rechaza_id_duplicado_sin_perder_original(engine_sqlite):
    with Session(engine_sqlite) as session:
        repo = SqlOrderRepository(session)
        repo.save(4, Order(total=120))
        session.commit()
        repo.save(4, Order(total=999))
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    with Session(engine_sqlite) as new_session:
        rows = new_session.scalars(select(OrderRow).where(OrderRow.id == 4)).all()
        assert len(rows) == 1
        assert rows[0].total == 120
