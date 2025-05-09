# **Глобальная картина IAM, OAuth 2.0, Keycloak, LDAP и аутентификационных механизмов**

## **1. IAM (Identity and Access Management) — управление идентификацией и доступом**
**IAM** — это общий термин для систем, которые управляют **пользователями, их учетными записями, правами доступа и аутентификацией** в IT-инфраструктуре.

### **Основные функции IAM**
- Управление **учетными записями пользователей**.
- Контроль **аутентификации (входа в систему)**.
- Контроль **авторизации (кто и к чему имеет доступ)**.
- Поддержка **SSO (единого входа)** и управления сессиями.

### **Связь с другими технологиями**
- IAM **реализуется через инструменты**, такие как **Keycloak, Active Directory, LDAP**.
- Использует **протоколы аутентификации**, такие как **OAuth 2.0, OpenID Connect, SAML**.

---

## **2. Keycloak — система IAM и управления аутентификацией**
**Keycloak** — это **open-source сервер IAM**, который управляет аутентификацией и авторизацией пользователей в приложениях.

### **Что делает Keycloak?**
- Позволяет **аутентифицировать пользователей** (через логин/пароль, Google, GitHub и др.).
- Генерирует **токены доступа (JWT) для API**.
- Поддерживает **SSO (Single Sign-On)**.
- Интегрируется с **LDAP** и **Active Directory**.
- Работает по **OAuth 2.0, OpenID Connect, SAML**.

### **Связь с другими технологиями**
- Keycloak может **заменять или работать вместе с LDAP/Active Directory**.
- Использует **OAuth 2.0 и OpenID Connect** для аутентификации.
- Может выступать в роли **авторизационного сервера** для приложений.

---

## **3. LDAP — протокол хранения и управления учетными записями**
**LDAP (Lightweight Directory Access Protocol)** — это **база данных пользователей** в компании.

### **Что делает LDAP?**
- Хранит **информацию о пользователях и их ролях**.
- Позволяет централизованно управлять **аутентификацией и доступами**.
- Используется в **Active Directory (Microsoft)** и других корпоративных системах.

### **Связь с другими технологиями**
- Keycloak может использовать **LDAP как базу пользователей**.
- В IAM-системах (например, Keycloak) LDAP используется для **аутентификации и авторизации**.
- **OAuth 2.0 не хранит пользователей**, но может использовать LDAP для проверки данных.

---

## **4. OAuth 2.0 — протокол аутентификации и авторизации**
**OAuth 2.0** — это **протокол, который позволяет приложениям получать доступ к ресурсам пользователей без передачи пароля**.

### **Как работает OAuth 2.0?**
1. Пользователь входит в систему через **Authorization Server** (например, Keycloak, Google, Facebook).
2. Сервер авторизации выдаёт **токен (access token)**.
3. Клиент (например, веб-приложение) использует этот токен для доступа к API.

### **Связь с другими технологиями**
- Keycloak является **авторизационным сервером**, работающим по OAuth 2.0.
- LDAP может использоваться как источник данных для OAuth 2.0.

---

## **5. Основные типы OAuth 2.0 аутентификации**
OAuth 2.0 поддерживает несколько способов (грантов) получения токена.

### **5.1 Authorization Code Grant (Код авторизации)**
- **Рекомендуемый метод** для веб-приложений и мобильных приложений.
- **Процесс**:
  1. Клиент получает `authorization_code` через редирект.
  2. Клиент обменивает `authorization_code` на `access_token` через защищённый серверный запрос.
- **Безопасность**: токен не передаётся через браузер.

### **5.2 Implicit Grant (Устаревший метод)**
- **Ранее использовался в SPA (одностраничных приложениях)**.
- **Процесс**:
  1. Клиент сразу получает `access_token` в URL после редиректа.
- **Недостатки**: токен легко украсть, **не рекомендуется**.

### **5.3 PKCE (Proof Key for Code Exchange)**
- **Дополнение к Authorization Code Grant**, используется в мобильных и веб-приложениях.
- **Процесс**:
  1. Клиент передаёт `code_challenge` вместо `client_secret` при запросе кода.
  2. Затем доказывает свою подлинность с помощью `code_verifier`.
- **Преимущество**: защита от атак перехвата кода (`code interception`).

---

## **6. OpenID Connect (OIDC) — расширение OAuth 2.0**
**OpenID Connect (OIDC)** — это **надстройка над OAuth 2.0**, которая добавляет возможность **аутентификации пользователей**.

### **Чем отличается от OAuth 2.0?**
| Протокол        | Основная цель                  | Что выдаёт?     |
|----------------|--------------------------------|----------------|
| **OAuth 2.0**  | Авторизация (доступ к ресурсам) | `access_token` |
| **OIDC**       | Аутентификация (кто ты?)       | `id_token`     |

### **Связь с другими технологиями**
- Keycloak поддерживает **OIDC**, позволяя входить в системы через Google, GitHub и другие провайдеры.
- **OIDC + JWT** позволяет безопасно передавать данные о пользователе в API.

---

## **7. Как всё это связано в единую систему?**
1. **LDAP/Active Directory** хранят пользователей и управляют их учетными записями.
2. **Keycloak** подключается к LDAP/AD и становится сервером авторизации.
3. **OAuth 2.0 + OpenID Connect** позволяют приложениям входить через Keycloak.
4. **Authorization Code Grant + PKCE** обеспечивают безопасную аутентификацию.
5. **Клиенты (веб, мобильные, API)** получают токены и используют их для работы с ресурсами.

---

## **📌 Главное, что нужно запомнить**
- **IAM** управляет пользователями и их доступами.
- **Keycloak** — сервер IAM, который реализует аутентификацию и авторизацию.
- **LDAP** хранит пользователей, а Keycloak может его использовать.
- **OAuth 2.0** управляет доступом, **OIDC** — идентификацией.
- **PKCE + Authorization Code** — лучший метод аутентификации в современных приложениях.