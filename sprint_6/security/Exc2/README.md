# Динамическое масштабирование контейнеров в K8S
- [Динамическое масштабирование контейнеров в K8S](#динамическое-масштабирование-контейнеров-в-k8s)
  - [Скрины](#скрины)
  - [Инструкция для проверки и повторения пайплайна на Minikube](#инструкция-для-проверки-и-повторения-пайплайна-на-minikube)
  
## Скрины
Картинки сервисов и логов хранятся в директории `assets`

## Инструкция для проверки и повторения пайплайна на Minikube
1. Запустить Minikube с поддержкой метрик: `minikube start --driver=docker --cpus=4 --memory=8192 --addons=metrics-server`
2. Убедиться, что metrics-server работает:
   1. Проверить развертывание: `kubectl get deployment metrics-server -n kube-system`
   2. Убедиться, что метрики собираются: `kubectl top nodes` и `kubectl top pods`
3. Применить манифест Deployment для тестового приложения
   1. Развернуть приложение: `kubectl apply -f scale-test-deployment.yaml`
   2. Убедиться, что поды работают: `kubectl get deployments` и `kubectl get pods`
4. Создать сервис (Service) для приложения
   1. Применить манифест: `kubectl apply -f scale-test-service.yaml`
5. Настроить доступ к сервису
   1. Использовать команду для получения URL сервиса: `minikube service scale-test-svc --url`
   2. Если нужно использовать локальный доступ, настроить `port-forward`: `kubectl port-forward svc/scale-test-svc 8080:8080`
6. Применить манифест HPA
   1. Настроить Horizontal Pod Autoscaler: `kubectl apply -f scale-test-hpa.yaml`
   2. Проверить состояние HPA: `kubectl get hpa`
7. Запустить нагрузочное тестирование Locust
   1. Убедиться, что Locust установлен: `pip install locust`
   2. Запустить Locust: `locust -f locustfile.py --host <URL вашего сервиса>`
8. Наблюдать за масштабированием подов
   1. Проверить состояние HPA в реальном времени: `kubectl get hpa --watch`
   2. Следить за количеством подов: `kubectl get pods --watch`
9. Проверить масштабирование через Dashboard**
   1.  Открыть Minikube Dashboard: `minikube dashboard`
   2.  Наблюдать за масштабированием через интерфейс Dashboard
10. Оставноить и почстить minikube:
    1.  Оставновить minikube: `minikube stop`
    2.  Удалить minikube кластер с очисткой данных: `minikube delete --all`