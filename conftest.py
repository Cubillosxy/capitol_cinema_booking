import os

import pytest

from bookings.tests.fixtures import *  # noqa
from cinemas.tests.fixtures import *  # noqa
from movies.tests.fixtures import *  # noqa
from screenings.tests.fixtures import *  # noqa
from users.tests.fixtures import *  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capitol_cinema.settings")


@pytest.fixture
def fixture_test():
    return 1
