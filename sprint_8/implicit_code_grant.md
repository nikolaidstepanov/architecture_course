# Как работает Implicit Grant (простыми словами)

## 1. Клиент (например, Notion) отправляет пользователя на сервер авторизации (Google)
- В URL передаётся `client_id=notion`, `redirect_uri=https://notion.so/callback`, `response_type=token`.
- Это значит: "Google, проверь, кто этот пользователь, и если он согласен, сразу верни `access_token` в URL."

## 2. Пользователь логинится в Google и даёт разрешение
- Google проверяет логин/пароль
- Показывает экран согласия: "Notion хочет доступ к Google Drive. Разрешить?"

## 3. Google сразу возвращает `access_token` в URL редиректа
- После подтверждения Google **сразу** редиректит пользователя: ```https://notion.so/callback#access_token=eyJhbGciOiJ…```
- Внимание: **токен передаётся в URL после `#` (hash fragment), а не в query-параметре `?`**

## 4. Фронтенд Notion извлекает `access_token` из URL
- Браузерный JS-код делает:
```javascript
const token = window.location.hash.split('=')[1];
```
- Токен сохраняется в localStorage или sessionStorage

## 5. Теперь Notion использует access_token, чтобы работать с API Google

Например, запрашивает файлы Google Drive:
```http
GET /drive/files
Host: googleapis.com
Authorization: Bearer eyJhbGciOi...
```
- Google проверяет токен и отдаёт данные

## Почему этот вариант небезопасный?
- Токен виден в URL → его могут украсть злоумышленники
- Браузер хранит токен в JS (localStorage, sessionStorage) → возможны XSS-атаки
- Нет refresh_token → когда access_token истечёт, нужно заново проходить авторизацию

## Главное, что нужно запомнить
- access_token передаётся сразу, без кода (authorization_code)
- Браузер получает токен напрямую в URL
- Токен хранится в браузере и используется для API-запросов
- Не рекомендуется использовать, так как уязвим для атак