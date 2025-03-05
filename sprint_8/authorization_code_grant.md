# Как работает Authorization Code Grant (простыми словами)

## 1. Клиент (например, Notion) отправляет пользователя на сервер авторизации (Google)
- В URL передаётся `client_id=notion` и `redirect_uri=https://notion.so/callback`
- Это значит: "Google, проверь, кто этот пользователь, и если он согласен, верни его с кодом авторизации."

## 2. Пользователь логинится в Google и даёт разрешение
- Google проверяет логин/пароль
- Показывает экран согласия: "Notion хочет доступ к Google Drive. Разрешить?"

## 3. Google редиректит пользователя обратно в Notion, добавляя `authorization_code`
- Браузер переходит по `https://notion.so/callback?code=123abc`
- Код `123abc` виден в адресной строке

## 4. Клиент (Notion) делает скрытый серверный запрос в Google, чтобы обменять код на токен
- Сервер Notion (НЕ браузер) отправляет `POST /token` запрос в Google:
  ```http
  POST /token
  Host: accounts.google.com
  Content-Type: application/x-www-form-urlencoded

  grant_type=authorization_code
  code=123abc
  client_id=notion
  client_secret=super-secret
  redirect_uri=https://notion.so/callback
  ```
- Этот запрос браузер НЕ видит, потому что он идёт напрямую с сервера Notion на сервер Google
- Google проверяет code, убеждается, что всё ок, и отправляет access_token

## 5. Теперь Notion использует access_token, чтобы работать с API Google

- Например, запрашивает файлы Google Drive:
```http
GET /drive/files
Host: googleapis.com
Authorization: Bearer eyJhbGciOi...
```

- Google проверяет токен и отдаёт данные

## Почему нельзя сразу получить токен?
- Если бы access_token передавался сразу через браузер, его могли бы украсть
- Вместо этого выдаётся временный authorization_code, который можно использовать только один раз
- Этот код меняется на токен на сервере, а не в браузере, что делает процесс безопасным

## Главное, что нужно запомнить
- Код (authorization_code) виден в URL → Но бесполезен без обмена
- Токен (access_token) браузер НЕ получает напрямую → Его получает сервер
- Браузер НЕ делает POST /token, это делает только сервер клиента
- Безопасность достигается разделением этих двух шагов