# Защита доступа к кластеру Kubernetes

- [Защита доступа к кластеру Kubernetes](#защита-доступа-к-кластеру-kubernetes)
  - [RBAC](#rbac)
  - [Как настраивать](#как-настраивать)

## RBAC

| Роль                          | Права роли (resources + verbs)                                                                                                                                                | Группы пользователей                                         |
|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| **security-admin** (Role)     | - `secrets` (namespace=development): get, list, watch <br/> - `configmaps` (namespace=development): get, list, watch                                                             | Специалист по ИБ (security-team)                             |
| **devops-ops-engineer** (Role) | - `pods`: create, delete, update, list, get, watch<br/> - `deployments` (apps): create, delete, update, list, get, watch<br/> - `services`: create, delete, update, list, get, watch<br/> - `configmaps`: get, list, watch | DevOps-инженеры и инженеры по эксплуатации (ops)            |
| **developer** (Role)         | - `pods`: get, list, watch<br/> - `services`: get, list, watch<br/> - `configmaps`: get, list, watch<br/> - `deployments` (apps): get, list, watch                                 | Разработчики (developers)                                    |
| **cluster-readonly** (ClusterRole) | - (кластерные ресурсы) `pods`, `nodes`, `namespaces`, `persistentvolumes`, `storageclasses`: get, list, watch                                                                | Любая ограниченная группа, нуждающаяся в чтении всей конфигурации кластера |

## Как настраивать
1. Создать namespace `development`: `kubectl create namespace development`
2. Создать роли: `kubectl apply -f role-creating.yaml`
3. Привязать пользователей (или группы) к ролям: `kubectl apply -f role-binding.yaml`
