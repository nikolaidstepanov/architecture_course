# Как работает PKCE (Proof Key for Code Exchange)

## Что такое PKCE и зачем он нужен?
PKCE (Proof Key for Code Exchange) — это **улучшенный вариант Authorization Code Grant**, который делает OAuth 2.0 **безопаснее** для мобильных приложений и одностраничных веб-приложений (SPA).

### В чём проблема обычного Authorization Code Grant?
- В классическом **Authorization Code Grant** клиент (например, Notion) получает `authorization_code` через браузер и затем **отправляет его на сервер авторизации для обмена на токен**.
- Чтобы доказать свою подлинность, клиент обычно использует `client_secret` в этом запросе.
- Но у мобильных приложений и SPA **нет безопасного способа хранить `client_secret`**, так как злоумышленник может его украсть из исходного кода.

### Как PKCE решает эту проблему?
- Вместо `client_secret` клиент использует **динамически сгенерированный код (`code_verifier` и `code_challenge`)**.
- Это защищает процесс от атак **перехвата кода (code interception attack)**.

---

## 🚀 Как работает PKCE (на примере Notion + Google)

### **1. Клиент (Notion) генерирует `code_verifier` и `code_challenge`**
Перед тем, как отправить пользователя на сервер авторизации, клиент создаёт два значения:
- **`code_verifier`** — случайная строка (минимум 43 символа, максимум 128).
- **`code_challenge`** — хеш (`SHA256`) от `code_verifier`.

Пример генерации:
```javascript
const generateCodeVerifier = () => {
  const array = new Uint8Array(32);
  window.crypto.getRandomValues(array);
  return btoa(String.fromCharCode(...array))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
};

const generateCodeChallenge = async (codeVerifier) => {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return btoa(String.fromCharCode(...new Uint8Array(digest)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
};

// Генерация значений
const codeVerifier = generateCodeVerifier();
const codeChallenge = await generateCodeChallenge(codeVerifier);
```
### 2. Notion отправляет пользователя на сервер авторизации (Google)

Браузер делает редирект, указывая:
- response_type=code
- client_id=notion
- redirect_uri=https://notion.so/callback
- code_challenge=<генерированный_хеш>
- code_challenge_method=S256

Пример запроса:
```http
https://accounts.google.com/o/oauth2/auth?
  response_type=code&
  client_id=notion&
  redirect_uri=https://notion.so/callback&
  code_challenge=Jz1lE6VvNBjY...&
  code_challenge_method=S256
```

### 3. Пользователь логинится в Google и даёт разрешение
- Google проверяет логин/пароль
- Показывает экран согласия: “Notion хочет доступ к Google Drive. Разрешить?”

### 4. Google редиректит пользователя обратно в Notion с authorization_code
- После успешной авторизации Google отправляет пользователя на:
```http
https://notion.so/callback?code=123abc
```

### 5. Notion делает серверный запрос в Google, чтобы обменять code на access_token
Теперь сервер Notion отправляет POST /token, но вместо client_secret использует code_verifier (тот самый случайный ключ, который он сгенерировал в начале)
```http
POST /token
Host: accounts.google.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=123abc&
client_id=notion&
redirect_uri=https://notion.so/callback&
code_verifier=Nn8L3p2kShB4...
```
- Google проверяет code_verifier: если он правильно раскодируется в code_challenge, значит, этот код не был подделан
- Если всё верно, Google отправляет access_token
  
### 6. Теперь Notion использует access_token, чтобы работать с API Google
```http
GET /drive/files
Host: googleapis.com
Authorization: Bearer eyJhbGciOi...
```

### Главное преимущество PKCE
- PKCE заменяет client_secret → теперь даже если кто-то перехватит authorization_code, он не сможет обменять его на токен, потому что не знает code_verifier
- Идеально подходит для мобильных и SPA-приложений, где нельзя безопасно хранить client_secret
- Используется вместе с Authorization Code Grant (это не отдельный механизм, а улучшение безопасности)

### Главное, что нужно запомнить
- PKCE — это защита Authorization Code Grant, заменяющая client_secret динамическим code_verifier
- Код сначала передаётся зашифрованным (code_challenge), а потом расшифровывается с code_verifier
- Даже если authorization_code утечёт, его нельзя будет обменять без code_verifier
- Сегодня PKCE рекомендуется для всех OAuth 2.0 клиентов, особенно для мобильных приложений и SPA