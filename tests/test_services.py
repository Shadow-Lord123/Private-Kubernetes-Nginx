"""Unit tests for Kubernetes Service manifests."""

import pytest


# ---------------------------------------------------------------------------
# nginx-nodeport-service.yaml
# ---------------------------------------------------------------------------

class TestNginxNodePortService:
    """Tests for the public nginx NodePort Service."""

    def test_api_version(self, nginx_nodeport_service):
        assert nginx_nodeport_service["apiVersion"] == "v1"

    def test_kind(self, nginx_nodeport_service):
        assert nginx_nodeport_service["kind"] == "Service"

    def test_metadata_name(self, nginx_nodeport_service):
        assert nginx_nodeport_service["metadata"]["name"] == "nginx-service"

    def test_metadata_namespace(self, nginx_nodeport_service):
        assert nginx_nodeport_service["metadata"]["namespace"] == "default"

    def test_metadata_labels(self, nginx_nodeport_service):
        labels = nginx_nodeport_service["metadata"]["labels"]
        assert labels["app"] == "nginx"
        assert labels["tier"] == "web"

    def test_service_type(self, nginx_nodeport_service):
        assert nginx_nodeport_service["spec"]["type"] == "NodePort"

    def test_port_configuration(self, nginx_nodeport_service):
        ports = nginx_nodeport_service["spec"]["ports"]
        assert len(ports) == 1
        port = ports[0]
        assert port["port"] == 80
        assert port["targetPort"] == 80
        assert port["protocol"] == "TCP"
        assert port["name"] == "http"

    def test_nodeport_in_valid_range(self, nginx_nodeport_service):
        nodeport = nginx_nodeport_service["spec"]["ports"][0]["nodePort"]
        assert 30000 <= nodeport <= 32767

    def test_nodeport_value(self, nginx_nodeport_service):
        assert nginx_nodeport_service["spec"]["ports"][0]["nodePort"] == 30080

    def test_selector(self, nginx_nodeport_service):
        selector = nginx_nodeport_service["spec"]["selector"]
        assert selector["app"] == "nginx"


# ---------------------------------------------------------------------------
# nginx-private-service.yaml
# ---------------------------------------------------------------------------

class TestNginxPrivateService:
    """Tests for the private nginx NodePort Service."""

    def test_api_version(self, nginx_private_service):
        assert nginx_private_service["apiVersion"] == "v1"

    def test_kind(self, nginx_private_service):
        assert nginx_private_service["kind"] == "Service"

    def test_metadata_name(self, nginx_private_service):
        assert nginx_private_service["metadata"]["name"] == "nginx-private-service"

    def test_metadata_namespace(self, nginx_private_service):
        assert nginx_private_service["metadata"]["namespace"] == "default"

    def test_metadata_labels(self, nginx_private_service):
        labels = nginx_private_service["metadata"]["labels"]
        assert labels["app"] == "nginx-private"

    def test_service_type(self, nginx_private_service):
        assert nginx_private_service["spec"]["type"] == "NodePort"

    def test_port_configuration(self, nginx_private_service):
        ports = nginx_private_service["spec"]["ports"]
        assert len(ports) == 1
        port = ports[0]
        assert port["port"] == 80
        assert port["targetPort"] == 80
        assert port["protocol"] == "TCP"
        assert port["name"] == "http"

    def test_nodeport_in_valid_range(self, nginx_private_service):
        nodeport = nginx_private_service["spec"]["ports"][0]["nodePort"]
        assert 30000 <= nodeport <= 32767

    def test_nodeport_value(self, nginx_private_service):
        assert nginx_private_service["spec"]["ports"][0]["nodePort"] == 30080

    def test_selector(self, nginx_private_service):
        selector = nginx_private_service["spec"]["selector"]
        assert selector["app"] == "nginx-private"
