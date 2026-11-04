from datetime import datetime, timedelta, timezone
from src.security import can_cancel

def test_owner_within_24h():
    now = datetime.now(timezone.utc)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(timezone.utc)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(timezone.utc)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(timezone.utc)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)

def test_admin_cancel_new_stranger_order():
    now = datetime.now(timezone.utc)
    # Estado "NEW", propietario 1, usuario 2 (diferente), es administrador (True)
    assert can_cancel("NEW", 1, 2, True, now, now)

def test_owner_cancel_exactly_24h():
    now = datetime.now(timezone.utc)
    created_at = now - timedelta(hours=24)
    # Propietario intenta cancelar exactamente a las 24 horas de la creación
    assert not can_cancel("NEW", 1, 1, False, created_at, now)