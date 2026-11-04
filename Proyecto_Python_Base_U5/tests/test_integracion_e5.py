"""E5: mocks sin pagos ni llamadas a proveedores reales."""
from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_e5_pago_aprobado_regular():
    gateway = Mock()
    gateway.charge.return_value = True
    order = Order(100)
    assert OrderService(gateway).checkout(order) == 100
    gateway.charge.assert_called_once_with(100)
    assert order.status == "CONFIRMED"


def test_e5_pago_aprobado_vip_aplica_descuento():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(200, vip=True)) == 170
    gateway.charge.assert_called_once_with(170)


def test_e5_pago_rechazado_vip_200():
    gateway = Mock()
    gateway.charge.return_value = False
    order = Order(200, vip=True)
    with pytest.raises(RuntimeError, match="payment rejected"):
        OrderService(gateway).checkout(order)
    gateway.charge.assert_called_once_with(170)
    # Observación del defecto actual, no una aprobación de este comportamiento.
    assert order.status == "CONFIRMED"


def test_e5_error_comunicacion_timeout():
    gateway = Mock()
    gateway.charge.side_effect = TimeoutError("gateway timeout")
    order = Order(100)
    with pytest.raises(TimeoutError, match="gateway timeout"):
        OrderService(gateway).checkout(order)
    gateway.charge.assert_called_once_with(100)
    # Evidencia del riesgo de consistencia de la versión base.
    assert order.status == "CONFIRMED"


def test_e5_fondos_insuficientes_simulado_como_rechazo():
    # El contrato del gateway base solo devuelve booleano: False representa rechazo,
    # pero no permite distinguir formalmente la causa (fondos insuficientes, etc.).
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError, match="payment rejected"):
        OrderService(gateway).checkout(Order(75))
    gateway.charge.assert_called_once_with(75)
