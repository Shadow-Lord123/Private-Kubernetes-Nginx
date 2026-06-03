"""Cross-file consistency tests to verify selectors and labels match."""

import os
import yaml
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

YAML_FILES = [
    "nginx-deployment.yaml",
    "nginx-private-deployment.yaml",
    "nginx-nodeport-service.yaml",
    "nginx-private-service.yaml",
]


def _load(name):
    with open(os.path.join(REPO_ROOT, name)) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# YAML syntax validation
# ---------------------------------------------------------------------------

class TestYamlValidity:
    """Every YAML file in the repo root should parse without errors."""

    @pytest.mark.parametrize("filename", YAML_FILES)
    def test_yaml_parses(self, filename):
        doc = _load(filename)
        assert doc is not None
        assert isinstance(doc, dict)

    @pytest.mark.parametrize("filename", YAML_FILES)
    def test_has_api_version(self, filename):
        doc = _load(filename)
        assert "apiVersion" in doc

    @pytest.mark.parametrize("filename", YAML_FILES)
    def test_has_kind(self, filename):
        doc = _load(filename)
        assert "kind" in doc

    @pytest.mark.parametrize("filename", YAML_FILES)
    def test_has_metadata(self, filename):
        doc = _load(filename)
        assert "metadata" in doc
        assert "name" in doc["metadata"]

    @pytest.mark.parametrize("filename", YAML_FILES)
    def test_has_spec(self, filename):
        doc = _load(filename)
        assert "spec" in doc


# ---------------------------------------------------------------------------
# Cross-resource consistency
# ---------------------------------------------------------------------------

class TestServiceDeploymentConsistency:
    """Service selectors must match the Deployment pod template labels."""

    def test_public_service_selector_matches_deployment(self):
        deployment = _load("nginx-deployment.yaml")
        service = _load("nginx-nodeport-service.yaml")

        svc_selector = service["spec"]["selector"]
        pod_labels = deployment["spec"]["template"]["metadata"]["labels"]

        for key, value in svc_selector.items():
            assert pod_labels.get(key) == value, (
                f"Service selector {key}={value} not found in Deployment pod labels"
            )

    def test_private_service_selector_matches_deployment(self):
        deployment = _load("nginx-private-deployment.yaml")
        service = _load("nginx-private-service.yaml")

        svc_selector = service["spec"]["selector"]
        pod_labels = deployment["spec"]["template"]["metadata"]["labels"]

        for key, value in svc_selector.items():
            assert pod_labels.get(key) == value, (
                f"Service selector {key}={value} not found in Deployment pod labels"
            )

    def test_public_service_targetport_matches_container(self):
        deployment = _load("nginx-deployment.yaml")
        service = _load("nginx-nodeport-service.yaml")

        svc_target = service["spec"]["ports"][0]["targetPort"]
        container_port = deployment["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"]
        assert svc_target == container_port

    def test_private_service_targetport_matches_container(self):
        deployment = _load("nginx-private-deployment.yaml")
        service = _load("nginx-private-service.yaml")

        svc_target = service["spec"]["ports"][0]["targetPort"]
        container_port = deployment["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"]
        assert svc_target == container_port


# ---------------------------------------------------------------------------
# Namespace consistency
# ---------------------------------------------------------------------------

class TestNamespaceConsistency:
    """All resources should be in the same namespace."""

    def test_all_default_namespace(self):
        for filename in YAML_FILES:
            doc = _load(filename)
            assert doc["metadata"]["namespace"] == "default", (
                f"{filename} is not in the 'default' namespace"
            )
