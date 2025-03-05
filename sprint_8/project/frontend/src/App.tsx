import React from 'react';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import Keycloak, { KeycloakConfig } from 'keycloak-js';
import ReportPage from './components/ReportPage';

const keycloakConfig: KeycloakConfig = {
  url: process.env.REACT_APP_KEYCLOAK_URL,
  realm: process.env.REACT_APP_KEYCLOAK_REALM || "",
  clientId: process.env.REACT_APP_KEYCLOAK_CLIENT_ID || ""
};

const keycloak = new Keycloak(keycloakConfig);

// Передаем нужные опции в initOptions — именно здесь включается PKCE
const initOptions = {
  pkceMethod: 'S256',      // включаем PKCE c SHA256
  onLoad: 'check-sso'      // при загрузке проверяем наличие сессии
};

const App: React.FC = () => {
  return (
    <ReactKeycloakProvider
      authClient={keycloak}
      initOptions={initOptions} // здесь прокидываем initOptions
    >
      <div className="App">
        <ReportPage />
      </div>
    </ReactKeycloakProvider>
  );
};

export default App;