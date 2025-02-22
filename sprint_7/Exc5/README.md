# Управление трафиком внутри кластера Kubertnetes

- [Управление трафиком внутри кластера Kubertnetes](#управление-трафиком-внутри-кластера-kubertnetes)
  - [Инструкция по запуску:](#инструкция-по-запуску)

## Инструкция по запуску:
1. Запустить minikube с плагином: `minikube start --network-plugin=cni --cni=calico`
2. Создать namespace development: `kubectl create namespace development`
3. Развернуть 4 pod (Nginx), каждому дать свою метку (label): `sh create-services.sh`
4. Проверить, что все создалось: `kubectl get pods,svc -n development --show-labels`
5. Запретить весь входящий трафик: `kubectl apply -f default-deny.yaml`
6. Разрешить конкретный трафик: `kubectl apply -f non-admin-api-allow.yaml`
7. Проверить сетевые политики: `kubectl get networkpolicies -n development`
8. Проверить правильность настройки:
   1. Заходим в pod: `kubectl exec -it front-end-app -n development -- /bin/sh` 
      1. Проверяем доступ к `backend` (должно работать): `curl back-end-api-app:80`
      2. Проверяем доступ к `admin-backend` (не должно работать): `curl admin-back-end-api-app:80`
   2. Заходим в pod: `kubectl exec -it back-end-api-app -n development -- /bin/sh` 
      1. Проверяем доступ к `frontend` (должно работать): `curl front-end-app:80`
      2. Проверяем доступ к `admin-frontend` (не должно работать): `curl admin-front-end-app:80`
   3. Заходим в pod: `kubectl exec -it admin-front-end-app -n development -- /bin/sh`
      1. Проверяем доступ к `backend` (не должно работать): `curl back-end-api-app:80`
      2. Проверяем доступ к `admin-backend` (должно работать): `curl admin-back-end-api-app:80`
   4. Заходим в pod: `kubectl exec -it admin-back-end-api-app -n development -- /bin/sh`
      1. Проверяем доступ к `frontend` (не должно работать): `curl back-end-api-app:80`
      2. Проверяем доступ к `admin-frontend` (должно работать): `curl admin-front-end-app:80`