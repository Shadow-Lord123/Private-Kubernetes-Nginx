"""Unit tests for Kubernetes Deployment manifests."""

import pytest


# ---------------------------------------------------------------------------
# nginx-deployment.yaml
# ---------------------------------------------------------------------------

class TestNginxDeployment:
    """Tests for the public nginx Deployment manifest."""

    def test_api_version(self, nginx_deployment):
        assert nginx_deployment["apiVersion"] == "apps/v1"

    def test_kind(self, nginx_deployment):
        assert nginx_deployment["kind"] == "Deployment"

    def test_metadata_name(self, nginx_deployment):
        assert nginx_deployment["metadata"]["name"] == "nginx-deployment"

    def test_metadata_namespace(self, nginx_deployment):
        assert nginx_deployment["metadata"]["namespace"] == "default"

    def test_metadata_labels(self, nginx_deployment):
        labels = nginx_deployment["metadata"]["labels"]
        assert labels["app"] == "nginx"
        assert labels["tier"] == "web"

    def test_replicas(self, nginx_deployment):
        assert nginx_deployment["spec"]["replicas"] == 2

    def test_selector_matches_template_labels(self, nginx_deployment):
        selector = nginx_deployment["spec"]["selector"]["matchLabels"]
        template_labels = nginx_deployment["spec"]["template"]["metadata"]["labels"]
        for key, value in selector.items():
            assert template_labels.get(key) == value

    def test_container_name(self, nginx_deployment):
        container = nginx_deployment["spec"]["template"]["spec"]["containers"][0]
        assert container["name"] == "nginx"

    def test_container_image(self, nginx_deployment):
        container = nginx_deployment["spec"]["template"]["spec"]["containers"][0]
        assert container["image"] == "nginx:latest"

    def test_container_port(self, nginx_deployment):
        container = nginx_deployment["spec"]["template"]["spec"]["containers"][0]
        ports = container["ports"]
        assert len(ports) == 1
        assert ports[0]["containerPort"] == 80
        assert ports[0]["name"] == "http"

    def test_resource_requests(self, nginx_deployment):
        resources = nginx_deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
        assert "requests" in resources
        assert resources["requests"]["memory"] == "64Mi"
        assert resources["requests"]["cpu"] == "50m"

    def test_resource_limits(self, nginx_deployment):
        resources = nginx_deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
        assert "limits" in resources
        assert resources["limits"]["memory"] == "128Mi"
        assert resources["limits"]["cpu"] == "100m"

    def test_liveness_probe(self, nginx_deployment):
        container = nginx_deployment["spec"]["template"]["spec"]["containers"][0]
        probe = container["livenessProbe"]
        assert probe["httpGet"]["path"] == "/"
        assert probe["httpGet"]["port"] == 80
        assert probe["initialDelaySeconds"] == 15
        assert probe["periodSeconds"] == 10

    def test_readiness_probe(self, nginx_deployment):
        container = nginx_deployment["spec"]["template"]["spec"]["containers"][0]
        probe = container["readinessProbe"]
        assert probe["httpGet"]["path"] == "/"
        assert probe["httpGet"]["port"] == 80
        assert probe["initialDelaySeconds"] == 5
        assert probe["periodSeconds"] == 5

    def test_single_container(self, nginx_deployment):
        containers = nginx_deployment["spec"]["template"]["spec"]["containers"]
        assert len(containers) == 1

    def test_resource_limits_gte_requests(self, nginx_deployment):
        resources = nginx_deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
        req_mem = int(resources["requests"]["memory"].replace("Mi", ""))
        lim_mem = int(resources["limits"]["memory"].replace("Mi", ""))
        assert lim_mem >= req_mem

        req_cpu = int(resources["requests"]["cpu"].replace("m", ""))
        lim_cpu = int(resources["limits"]["cpu"].replace("m", ""))
        assert lim_cpu >= req_cpu


# ---------------------------------------------------------------------------
# nginx-private-deployment.yaml
# ---------------------------------------------------------------------------

class TestNginxPrivateDeployment:
    """Tests for the private nginx Deployment manifest."""

    def test_api_version(self, nginx_private_deployment):
        assert nginx_private_deployment["apiVersion"] == "apps/v1"

    def test_kind(self, nginx_private_deployment):
        assert nginx_private_deployment["kind"] == "Deployment"

    def test_metadata_name(self, nginx_private_deployment):
        assert nginx_private_deployment["metadata"]["name"] == "nginx-private-deployment"

    def test_metadata_namespace(self, nginx_private_deployment):
        assert nginx_private_deployment["metadata"]["namespace"] == "default"

    def test_metadata_labels(self, nginx_private_deployment):
        labels = nginx_private_deployment["metadata"]["labels"]
        assert labels["app"] == "nginx-private"
        assert labels["environment"] == "production"

    def test_replicas(self, nginx_private_deployment):
        assert nginx_private_deployment["spec"]["replicas"] == 2

    def test_selector_matches_template_labels(self, nginx_private_deployment):
        selector = nginx_private_deployment["spec"]["selector"]["matchLabels"]
        template_labels = nginx_private_deployment["spec"]["template"]["metadata"]["labels"]
        for key, value in selector.items():
            assert template_labels.get(key) == value

    def test_container_image_uses_private_registry(self, nginx_private_deployment):
        container = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]
        assert "kritagyadockeruser/nginx-private" in container["image"]

    def test_image_pull_policy(self, nginx_private_deployment):
        container = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]
        assert container["imagePullPolicy"] == "Always"

    def test_image_pull_secrets(self, nginx_private_deployment):
        secrets = nginx_private_deployment["spec"]["template"]["spec"]["imagePullSecrets"]
        assert len(secrets) == 1
        assert secrets[0]["name"] == "dockerhub-secret"

    def test_container_port(self, nginx_private_deployment):
        container = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]
        ports = container["ports"]
        assert len(ports) == 1
        assert ports[0]["containerPort"] == 80
        assert ports[0]["name"] == "http"

    def test_resource_requests(self, nginx_private_deployment):
        resources = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
        assert resources["requests"]["memory"] == "64Mi"
        assert resources["requests"]["cpu"] == "50m"

    def test_resource_limits(self, nginx_private_deployment):
        resources = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
        assert resources["limits"]["memory"] == "128Mi"
        assert resources["limits"]["cpu"] == "100m"

    def test_liveness_probe(self, nginx_private_deployment):
        container = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]
        probe = container["livenessProbe"]
        assert probe["httpGet"]["path"] == "/"
        assert probe["httpGet"]["port"] == 80
        assert probe["initialDelaySeconds"] == 15
        assert probe["periodSeconds"] == 10

    def test_readiness_probe(self, nginx_private_deployment):
        container = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]
        probe = container["readinessProbe"]
        assert probe["httpGet"]["path"] == "/"
        assert probe["httpGet"]["port"] == 80
        assert probe["initialDelaySeconds"] == 5
        assert probe["periodSeconds"] == 5

    def test_resource_limits_gte_requests(self, nginx_private_deployment):
        resources = nginx_private_deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
        req_mem = int(resources["requests"]["memory"].replace("Mi", ""))
        lim_mem = int(resources["limits"]["memory"].replace("Mi", ""))
        assert lim_mem >= req_mem

        req_cpu = int(resources["requests"]["cpu"].replace("m", ""))
        lim_cpu = int(resources["limits"]["cpu"].replace("m", ""))
        assert lim_cpu >= req_cpu
