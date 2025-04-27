# Изменения
- [Изменения](#изменения)
  - [Технический радар](#технический-радар)
  - [Дорожная карта трансформации с обоснованием этапов (Q2-2025 → Q2-2026)](#дорожная-карта-трансформации-с-обоснованием-этапов-q2-2025--q2-2026)


## Технический радар

| Категория | Технология / Подход | Статус<sup>1</sup> | Комментарий |
|-----------|---------------------|--------------------|-------------|
| **Хранилища и обработка** | MS SQL Server 2008 (монолитный DWH) | Hold | Работаем только как источник, нагрузку выводим постепенно |
| | ClickHouse (Analytics DB) | Adopt | Быстрые агрегации для витрин; подключается к Tableau |
| | Object Storage (S3/Azure Blob) | Adopt | Бронзовая зона Lakehouse |
| | Apache Iceberg | Trial | Табличный слой ACID, schema-evolution |
| | Apache Spark (ETL/ELT) | Adopt | Основной движок трансформаций |
| | Apache Flink / Spark Structured Streaming | Assess | Для CDC и near-real-time потоков |
| | Trino (PrestoSQL) | Trial | Federated-query поверх Lakehouse |
| **Оркестрация и Governance** | Apache Airflow | Adopt | Планировщик пайплайнов Spark / DQ / публикации |
| | Data Hub (Metadata & Lineage) | Trial | Единый каталог, lineage, data-product registry |
| | Great Expectations | Trial | Проверки качества в пайплайнах |
| | IAM (RBAC / OAuth 2.0) | Adopt | Централизованный контроль доступа |
| **Интеграция** | Apache Camel | Assess | Сохраняем на 1-й фазе, переводим потоки в Kafka позже |
| | Apache Kafka / Pulsar | Assess | Кандидат на замену Camel для событийной шины |
| **BI и аналитика** | Power BI | Adopt | Сохраняем для офисных команд |
| | Tableau | Trial | Главный инструмент дэшбордов на витринах ClickHouse |
| **Языки и инструменты** | Java | Adopt | Spark-ETL, финтех-микросервисы |
| | Python | Adopt | ML-модели, аналитические ноутбуки |
| | Terraform / CDK | Trial | IaC для новой платформы |
| **Методологии** | Data Lakehouse | Adopt | Целевая модель хранения |
| | Data Mesh | Trial | Доменная ответственность за данные |
| | DevSecOps | Adopt | Бесшовный CI/CD с безопасностью by design |

<sup>1</sup> **Adopt** – активно используем; **Trial** – пилотируем; **Assess** – анализируем; **Hold** – постепенно выводим

---

## Дорожная карта трансформации с обоснованием этапов (Q2-2025 → Q2-2026)

| Этап | Период | Основные результаты | Ответственные | Ресурсы | Обоснование |
|------|--------|--------------------|---------------|---------|-------------|
| **0. Discovery & Domain Design** | Q2 2025 | • Подтверждены границы доменов (Data Mesh)<br>• Инвентаризация источников | CDO-офис, EA-команда | 2 архитектора, 1 BA | Без чёткого доменного рисунка невозможен план миграции и SLA |
| **1. Platform Foundation** | Q3 2025 | • Развёрнут Object Storage + Iceberg<br>• Spark-кластер + Airflow<br>• Tableau Server подключён к ClickHouse (POC) | Platform Eng | DevOps 2 FTE, облако $50k | Создаём минимально жизнеспособную Lakehouse-платформу, чтобы команды сразу начинали пилоты |
| **2. Governance & Quality** | Q3-Q4 2025 | • Data Hub в проде (каталог, lineage)<br>• Great Expectations в Spark-пайпах<br>• RBAC/OAuth интегрирован с HR-LDAP | Data Gov Team | Data Steward 2 FTE, Security 1 FTE | Если не ввести каталог и DQ до масштабирования, появятся теневые датасеты и утратится доверие |
| **3. Domain On-Boarding — Wave 1** | Q4 2025 | • Клиники и ИИ-сервисы публикуют Bronze→Silver Iceberg-таблицы<br>• Gold-март Patient в ClickHouse | Clinics Data, AI Team | Data Eng 4 FTE | Быстрый бизнес-выигрыш: сквозной взгляд на пациента, демонстрация ценности Lakehouse |
| **4. Self-Service BI Rollout** | Q1 2026 | • Tableau-дашборды поверх ClickHouse<br>• Шаблон для ad-hoc отчётов | Analytics COE | BI Dev 2 FTE, Tableau lics | Самообслуживание снижает очередь в IT, повышает удовлетворённость бизнеса |
| **5. Domain On-Boarding — Wave 2** | Q1-Q2 2026 | • Финтех, Фарма, Электроника подключены<br>• Топ-80 % отчётов работают через Tableau/ClickHouse | Domain Teams | Data Eng 6 FTE, облако $30k | Достигаем критической массы данных для сквозной аналитики и ML |
| **6. Legacy Drain & Cost Optimisation** | Q2 2026 | • Массовые отчёты сняты с SQL Server<br>• Camel-потоки переведены на Kafka (MVP)<br>• TCO снижен на 30 % | Platform Ops | DBA 1 FTE, FinOps | Высвобождаем бюджеты и уменьшаем операционную сложность, подготавливаясь к дальнейшей эволюции |