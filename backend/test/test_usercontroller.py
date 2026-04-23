import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController


@pytest.fixture
def mock_dao():
    return MagicMock()


@pytest.fixture
def user_controller(mock_dao):
    return UserController(dao=mock_dao)


def test_get_user_by_email_returns_user_when_exactly_one_user_found(user_controller, mock_dao):
    email = "alice@example.com"
    expected_user = {"email": email, "name": "Alice"}
    mock_dao.find.return_value = [expected_user]

    result = user_controller.get_user_by_email(email)

    assert result == expected_user
    mock_dao.find.assert_called_once_with({"email": email})


def test_get_user_by_email_returns_first_user_and_prints_warning_when_multiple_users_found(
    user_controller, mock_dao, capsys
):
    email = "bob@example.com"
    first_user = {"email": email, "name": "Bob1"}
    second_user = {"email": email, "name": "Bob2"}
    mock_dao.find.return_value = [first_user, second_user]

    result = user_controller.get_user_by_email(email)
    captured = capsys.readouterr()

    # Ensure first match is returned and warning is printed.
    assert result == first_user
    assert f"Error: more than one user found with mail {email}" in captured.out
    mock_dao.find.assert_called_once_with({"email": email})


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",
        "plainaddress",
        "missingatsign.com",
        "user@",
        None,
    ],
)
def test_get_user_by_email_raises_value_error_for_invalid_email(user_controller, mock_dao, invalid_email):
    with pytest.raises(ValueError, match="Error: invalid email address"):
        user_controller.get_user_by_email(invalid_email)

    mock_dao.find.assert_not_called()


def test_get_user_by_email_reraises_exception_when_dao_fails(user_controller, mock_dao):
    email = "charlie@example.com"
    mock_dao.find.side_effect = Exception("Database failure")

    with pytest.raises(Exception, match="Database failure"):
        user_controller.get_user_by_email(email)

    mock_dao.find.assert_called_once_with({"email": email})


def test_get_user_by_email_returns_none_when_no_user_found(user_controller, mock_dao):
    email = "nobody@example.com"
    mock_dao.find.return_value = []

    # Docstring contract: return None when no matching user exists.
    result = user_controller.get_user_by_email(email)

    assert result is None