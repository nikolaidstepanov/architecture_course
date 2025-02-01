## HPA with default metrics

1. Start Minikube and enable metrics-server:
 - `minikube start --addons=metrics-server`
2. Check metrics-server status:
 - `kubectl get deployment metrics-server -n kube-system`
3. Create an HPA manifest
4. Apply the HPA manifest and verify:
 - `kubectl apply -f hpa.yml`
 - `kubectl get hpa`