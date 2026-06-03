"""Unit tests for the GitHub Actions deploy workflow."""

import pytest


class TestDeployWorkflow:
    """Tests for .github/workflows/deploy-private-image.yaml."""

    def test_workflow_name(self, deploy_workflow):
        assert deploy_workflow["name"] == "Deploy"

    def test_trigger_on_push(self, deploy_workflow):
        # PyYAML parses the YAML key `on` as boolean True
        triggers = deploy_workflow[True]
        assert "push" in triggers

    def test_push_branches(self, deploy_workflow):
        branches = deploy_workflow[True]["push"]["branches"]
        assert "main" in branches
        assert "master" in branches

    def test_manual_trigger(self, deploy_workflow):
        assert "workflow_dispatch" in deploy_workflow[True]

    def test_deploy_job_exists(self, deploy_workflow):
        assert "deploy" in deploy_workflow["jobs"]

    def test_runs_on_ubuntu(self, deploy_workflow):
        assert deploy_workflow["jobs"]["deploy"]["runs-on"] == "ubuntu-latest"

    def test_checkout_step(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        checkout_steps = [s for s in steps if s.get("uses", "").startswith("actions/checkout")]
        assert len(checkout_steps) >= 1

    def test_ssh_deploy_step_exists(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        ssh_steps = [s for s in steps if "ssh-action" in s.get("uses", "")]
        assert len(ssh_steps) == 1

    def test_ssh_step_uses_secrets(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        ssh_step = next(s for s in steps if "ssh-action" in s.get("uses", ""))
        with_block = ssh_step["with"]
        assert "secrets.K3S_SERVER_IP" in str(with_block["host"])
        assert "secrets.K3S_SSH_PRIVATE_KEY" in str(with_block["key"])

    def test_deploy_script_creates_dockerhub_secret(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        ssh_step = next(s for s in steps if "ssh-action" in s.get("uses", ""))
        script = ssh_step["with"]["script"]
        assert "dockerhub-secret" in script
        assert "docker-registry" in script

    def test_deploy_script_applies_manifest(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        ssh_step = next(s for s in steps if "ssh-action" in s.get("uses", ""))
        script = ssh_step["with"]["script"]
        assert "kubectl apply" in script

    def test_deploy_script_checks_pods(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        ssh_step = next(s for s in steps if "ssh-action" in s.get("uses", ""))
        script = ssh_step["with"]["script"]
        assert "kubectl get pods" in script

    def test_deploy_script_checks_services(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        ssh_step = next(s for s in steps if "ssh-action" in s.get("uses", ""))
        script = ssh_step["with"]["script"]
        assert "kubectl get svc" in script

    def test_step_count(self, deploy_workflow):
        steps = deploy_workflow["jobs"]["deploy"]["steps"]
        assert len(steps) == 2
