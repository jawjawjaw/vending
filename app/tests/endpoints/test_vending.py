from unittest.mock import AsyncMock
import uuid
import pytest
from fastapi.testclient import TestClient
from app.api.auth import get_current_user
from app.api.endpoints.vending import router
from app.errors import (
    InvalidRoleError,
    NotEnoughChangeError,
    NotEnoughMoneyError,
    NotEnoughProductError,
    ProductNotFoundError,
    UserNotFoundError,
)

from app.users.models import UserReadFull
from app.vending.service import VendingService, get_vending_service


from fastapi.testclient import TestClient


from app.main import app


@pytest.fixture(scope="session")
def test_buyer_1():
    return UserReadFull(
        id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
        username="testbuyer",
        role="buyer",
        deposit=0,
    )


@pytest.fixture(scope="session")
def test_seller_1():
    return UserReadFull(
        id=uuid.UUID("11111111-0000-0000-0000-000000000000"),
        username="testseller",
        role="buyer",
        deposit=0,
    )


@pytest.fixture(scope="session")
def vending_service_mock():
    s = VendingService(
        user_repository=None,
        product_repository=None,
        vending_machine=None,
    )

    return s


@pytest.fixture(scope="session")
def api_client():
    yield TestClient(app)
    app.dependency_overrides = {}


@pytest.mark.parametrize("coin_value", [1, 2, 0, -5, 200])
def test_deposit_coins_returns_422_when_amount_is_invalid(
    api_client, test_buyer_1, coin_value
):
    app.dependency_overrides[get_current_user] = lambda: test_buyer_1
    response = api_client.post(
        "http://localhost/vending/deposit",
        json={
            "coin": coin_value,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "ctx": {"error": {}},
                "input": coin_value,
                "loc": ["body", "coin"],
                "msg": "Value error, Invalid coin amount",
                "type": "value_error",
                "url": "https://errors.pydantic.dev/2.4/v/value_error",
            }
        ]
    }
    assert response.status_code == 422


# add parametrized test for all coin values
@pytest.mark.parametrize("coin_value", [5, 10, 20, 50, 100])
def test_deposit_coins_returns_200_when_no_error_raised(
    api_client, test_buyer_1, vending_service_mock, coin_value
):
    vending_service_mock.deposit_coins = AsyncMock(
        return_value=UserReadFull(
            id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            username="testbuyer",
            role="buyer",
            deposit=coin_value,
        )
    )
    app.dependency_overrides[get_vending_service] = lambda: vending_service_mock
    # mock vending_service to return a user with role "buyer"

    app.dependency_overrides[get_current_user] = lambda: test_buyer_1
    response = api_client.post(
        "http://localhost/vending/deposit",
        json={
            "coin": coin_value,
        },
    )
    assert response.json() == {
        "deposit": coin_value,
        "id": "00000000-0000-0000-0000-000000000000",
        "role": "buyer",
        "username": "testbuyer",
    }
    assert response.status_code == 200


@pytest.mark.parametrize(
    "error",
    [
        {
            "err": InvalidRoleError,
            "code": 400,
            "msg": str(InvalidRoleError()),
        },
        {"err": ValueError, "code": 500, "msg": "Unexpected internal server error"},
        {"err": EOFError, "code": 500, "msg": "Unexpected internal server error"},
    ],
)
def test_deposit_coins_returns_400_when_error_raised(
    api_client, test_seller_1, vending_service_mock, error
):
    vending_service_mock.deposit_coins = AsyncMock(side_effect=error["err"]())
    app.dependency_overrides[get_vending_service] = lambda: vending_service_mock

    app.dependency_overrides[get_current_user] = lambda: test_seller_1
    response = api_client.post(
        "http://localhost/vending/deposit",
        json={
            "coin": 5,
        },
    )
    assert response.json() == {"detail": error["msg"]}

    assert response.status_code == error["code"]
