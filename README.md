# Private Kubernetes Nginx

Kubernetes manifests for deploying public and private Nginx instances, structured with [Kustomize](https://kustomize.io/) to eliminate configuration duplication.

## Project Structure

```
base/                          # Shared deployment and service templates
  deployment.yaml              # Base Deployment (replicas, resources, probes)
  service.yaml                 # Base Service (NodePort, port config)
  kustomization.yaml
overlays/
  public/                      # Public nginx (nginx:latest)
    kustomization.yaml
  private/                     # Private nginx (kritagyadockeruser/nginx-private)
    kustomization.yaml
```

## Usage

### Deploy public Nginx

```bash
kubectl apply -k overlays/public
```

### Deploy private Nginx

Requires a `dockerhub-secret` image pull secret in the `default` namespace:

```bash
kubectl create secret docker-registry dockerhub-secret \
  --docker-username=<username> \
  --docker-password=<password>

kubectl apply -k overlays/private
```

### Preview generated manifests

```bash
# Public variant
kubectl kustomize overlays/public

# Private variant
kubectl kustomize overlays/private
```

## Overlay Differences

| Property | Public | Private |
|---|---|---|
| Image | `nginx:latest` | `kritagyadockeruser/nginx-private:latest` |
| App label | `nginx` | `nginx-private` |
| Extra labels | `tier: web` | `environment: production` |
| Image pull secrets | None | `dockerhub-secret` |
| Image pull policy | Default | `Always` |
