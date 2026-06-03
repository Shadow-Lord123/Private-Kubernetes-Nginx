import os
import yaml
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_yaml(filename):
    path = os.path.join(REPO_ROOT, filename)
    with open(path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def nginx_deployment():
    return _load_yaml("nginx-deployment.yaml")


@pytest.fixture
def nginx_private_deployment():
    return _load_yaml("nginx-private-deployment.yaml")


@pytest.fixture
def nginx_nodeport_service():
    return _load_yaml("nginx-nodeport-service.yaml")


@pytest.fixture
def nginx_private_service():
    return _load_yaml("nginx-private-service.yaml")


@pytest.fixture
def deploy_workflow():
    return _load_yaml(".github/workflows/deploy-private-image.yaml")
