# Задание 1. Анализ и планирование

### 1. Описание функциональности монолитного приложения

**Управление отоплением:**

- Пользователи могут включить или выключить отопление — контроллер предоставляет методы `/turn-on` и `/turn-off`
- Система поддерживает включение и выключение отопления на датчике — истема работает с сущностью `HeatingSystem`, которая хранит состояние
- Система поддерживает хранение информации о статусе отопления (включено/выключено) — поле `isOn` в `HeatingSystem` подтверждает это
- Система логирует все действия (включение/выключение отопления) — подтверждается наличием логирования через `logger.info`


**Мониторинг температуры:**

- Пользователи могут получить значение текущей температуры — метод `/current-temperature` в контроллере предоставляет эту возможность
- Пользователи могут установить новую температуру — метод `/set-temperature` позволяет это сделать
- Система поддерживает запрос и отправку данных о температуре через датчик — реализация полагается на currentTemperature в `HeatingSystem`
- Система поддерживает хранение информации о текущей температуре и о целевой температуре, которую задает пользователь, а также о дате ее изменения — поля `currentTemperature` и `targetTemperature` в `HeatingSystem` это подтверждают


### 2. Анализ архитектуры монолитного приложения

- Язык программирования: Java 17
- Фреймворк: Spring Boot
- База данных: Postgres 13 (используется JPA/Hibernate)
- Способ взаимодействия: JSON/HTTP (синхронный)
- Структура: Слоеная архитектура (контроллеры, сервисы, репозитории, сущности)
- Хранение данных: JPA-сущности, автоматическое обновление схемы базы данных
- Логирование: Используется SLF4J для логирования операций
- Документация API: Swagger
- Тестирование: Модульные тесты с использованием JUnit, Testcontainers
- Развертывание: Docker-контейнеры

### 3. Определение доменов и границы контекстов

Домены:
- Домен управления климатом - основной функционал системы (пользователь управляет отоплением и температурой)

Поддомен:
- Поддомен взаимодейсвтия с пользователем
- Поддомен управления датчиком

Контекст:
- Контекст управления отоплением (включение/выключение, поддержание статуса системы)
- Контекст управления температурой (измерение, установка, передача данных)

### **4. Проблемы монолитного решения**

1.	Масштабирование и отказоустойчивость:
    - Слабая масштабируемость из-за использования слоевой архитектуры
    - Синхронное взаимодействие и высокая связанность модулей: сбой в одном компоненте может привести к сбою всей системы
    - Отсутствие отказоустойчивости: нет механизмов обработки отказов или деградации
    - Сервер — узкое место: Центральный сервер обрабатывает все запросы, что может стать критической точкой
    - Узкое место в базе данных: одна база данных без шардирования или репликации становится критическим узлом при увеличении нагрузки
2.	Данные и функциональность:
    - Избыточность в модели данных: дублирование поля `currentTemperature` в `HeatingSystem` и `TemperatureSensor`
    - Отсутствие подтверждений выполнения команд
    - Отсутствие автоматического регулирования температуры
    - Отсутствие функциональности для хранения и анализа исторических данных
    - Отсутствие поддержки асинхронных событий: Датчики не могут самостоятельно отправлять данные о температуре в реальном времени
3.	Разработка и эксплуатация:
    - Длительные циклы разработки и развёртывания: команда разработки работает над одним большим приложением, что вызывает задержки
    - Сложность тестирования: изменения в одной части приложения требуют пересмотра тестов для всего монолита
    - Зависимость от текущей версии приложения: Каждое обновление или изменение версии требует адаптации всей системы
4.	Интеграция и взаимодействие с пользователями:
    - Ограниченная интеграция с внешними системами (умные устройства других производителей)
    - Ручная настройка системы: Пользователи не могут самостоятельно подключить устройства, что делает процесс дорогим и неудобным, то есть пользоватли полностью зависят от специалистов компании для настройки

### 5. Визуализация контекста системы — диаграмма С4

![Диаграмма контекста (AS IS)](docs/assets/c4_context.png)


# Задание 2. Проектирование микросервисной архитектуры

**Диаграмма контейнеров (Containers)**
![Диаграмма контейнеров](docs/assets/c4_containers.png)

**Диаграммы компонентов (Components)**
![Диаграмма компонентов для контейнера мониторинга и аналитики](docs/assets/c4_components_analytics.png)
![Диаграмма компонентов для контейнера управления устройствами](docs/assets/c4_components_management.png)
![Диаграмма компонентов для контейнера сбора телеметрии](docs/assets/c4_components_telemetry.png)

**Диаграмма кода (Code)**
Ниже описаны самые основные атрибуты и методы классов в разных компонентах для понимания общей картины объектов.
При этом я понимаю, что диаграмма кода строится на уровне одного конкретного компонента. Но на данный момент, не вижу смысла этого делать так как:
1. Уровень абстракции на уровне компонент не выявил сложных зависимостей, которые требуют высокий уровень детализации на уровне кода.
2. Нет достаточно информации, как именно команда будет вести разработку - какой паттерн будет использовать, какой опыт и так далее. В идеале, тут требуется взаимодействие с разработкой

![Диаграмма кода](docs/assets/c4_code.png)

# Задание 3. Разработка ER-диаграммы

![ER-диаграмма](docs/assets/er.png)

Описание ER диаграммы:
- User (Пользователь): Представляет пользователей системы; связан с домами, сценариями, отчетами и логами действий.
- Home (Дом): Привязан к пользователю; содержит устройства и сценарии.
- Device (Устройство): Включает конфигурацию, производителя и тип; связан с телеметрией, правилами и логами интеграции.
- Producer (Производитель): Представляет производителей устройств; отслеживает сертификацию и статус интеграции.
- Scenario (Сценарий): Управляет автоматизацией; связан с домами и устройствами.
- Rule (Правило): Определяет действия устройств в рамках сценариев.
- Stats (Статистика/Телеметрия): Хранит телеметрические данные; связана с устройствами, пользователями и отчетами.
- Report (Отчет): Генерируется на основе статистики; включает оповещения и временные метки.
- UserLog (Логи действий пользователя): Отслеживает действия пользователя; связаны с устройствами и описаниями действий через маппинг.
- IntegrationLog (Логи интеграции): Отслеживает историю интеграции устройств с производителями.
- ActionMapping (Описание действий): Содержит описания действий из логов пользователя.

Ключевые связи:
- User ↔ Home ↔ Device ↔ Stats ↔ Report
- User ↔ Scenario ↔ Rule ↔ Device
- Device ↔ Producer ↔ IntegrationLog
- UserLog ↔ ActionMapping