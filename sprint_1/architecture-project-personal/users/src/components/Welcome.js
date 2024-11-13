import { useEffect, useState } from 'react';
import api from '../utils/api';

export default function Welcome({ jwt }) {
    const [userName, setUserName] = useState('');

    useEffect(() => {
        if (jwt) {
            const profile = api.getProfile(jwt);
            setUserName(profile.userName);
        } else {
            setUserName('');
        }
    }, [jwt]);

    return (
        <h1>
            <div>Привет, {userName}!</div>
            <div>Добро пожаловать!</div>
        </h1>
    );
}
