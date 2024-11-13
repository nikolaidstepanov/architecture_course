// import React from "react";
// import React, { lazy }  from "react";
import React, { lazy, Suspense, useState, useEffect }  from "react";
import ReactDOM from "react-dom/client";

import "./index.css";

const UserLogin = lazy(() => import('users/UserLogin').catch(() => {
  return { default: () => <div className='error'>Component is not available!</div> };
 })
);

const Welcome = lazy(() => import('users/Welcome').catch(() => {
  return { default: () => <div className='error'>Component is not available!</div> };
 })
);

// const UsersTestControl = lazy(() => import('users/UsersTestControl').catch(() => {
//   return { default: () => <div className='error'>Component is not available!</div> };
//  })
// );

const TaskList = lazy(() => import('tasks/TaskList').catch(() => {
  return { default: () => <div className='error'>Component is not available!</div> };
 })
);

// const TasksTestControl = lazy(() => import('tasks/TasksTestControl').catch(() => {
//   return { default: () => <div className='error'>Component is not available!</div> };
//  })
// );

const App = () => {
  const [jwt, setJwt] = useState('');

  const handleJwtChange = event => { // Эта функция получает нотификации о событиях изменения jwt
    setJwt(event.detail)
  }

  useEffect(() => {
    addEventListener("jwt-change", handleJwtChange); // Этот код добавляет подписку на нотификации о событиях изменения localStorage
    return () => removeEventListener("jwt-change", handleJwtChange) // Этот код удаляет подписку на нотификации о событиях изменения localStorage, когда в ней пропадает необходимость
  }, []);

  return <div className="container">
    <header className='App-header'>
        Лабораторная работа по микрофронтендам
    </header>
    <section className='App-content'>
        {jwt ? (
            <>
                <Suspense>
                  <Welcome jwt={jwt} />
                </Suspense>
                <Suspense>
                  <TaskList jwt={jwt} />
                </Suspense>
            </>
        ) : (
            <Suspense>
              <UserLogin />
            </Suspense>
        )}
    </section>
  </div>
};

const rootElement = document.getElementById("app")
if (!rootElement) throw new Error("Failed to find the root element")

const root = ReactDOM.createRoot(rootElement)

root.render(<App />)