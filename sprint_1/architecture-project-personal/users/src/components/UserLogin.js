import { useState } from 'react';
import './UserLogin.css';
import api from '../utils/api'

export default function UserLogin() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    function onLogin(name, password) {
        dispatchEvent(new CustomEvent("jwt-change", {
            detail: api.login(name, password)
        }) );
    }
    
    return (
        <div className='login-box'>
            <div className='caption'>Имя пользователя</div>
            <div className='control'>
                <input name='userName' onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div className='caption'>Пароль</div>
            <div className='control'>
                <input name='password' type='password' onChange={(e) => setPassword(e.target.value)} required />
            </div>
            <div className='actions'>
                <button onClick={() => onLogin(email, password)}>Войти</button>
            </div>
        </div>
    );
}
