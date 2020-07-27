import pytest


def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="device", help="None")

@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")