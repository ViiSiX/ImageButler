import pytest
from imagebutler import utils


def test_validate_email():
    """Test validate_email function."""

    valid_emails = [
        'test@test.test',
        'so.long.i.dont.care.test@te.te.te',
        'iAmS0lesS_wAnNa@B3aUt1.Fu1.lol'
    ]
    invalid_emails = [
        'invalid email bleh bleh',
        'user@mail',
        'usermail@',
        '@usermail',
        'user@mail.',
        'user@.mail',
        'user.mail@domain',
        'user.@mail',
        '.user@mail'
    ]
    for email in valid_emails:
        assert utils.validate_email(email)
    for email in invalid_emails:
        assert not utils.validate_email(email)
    with pytest.raises(TypeError):
        utils.validate_email(list)
