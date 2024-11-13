class Api {
    constructor({ address }) {
	// стандартная реализация — объект options
        this._address = address;
    }
    
    login(username, password) {
        // В реальном приложении здесь будет обращение к API login service
        return 'fake-token';
    }

    getProfile() {
        // В реальном приложении здесь будет обращение к API login service
        return {
            userName: 'Студент',
        };
    }
}
 
const api = new Api({
    //address: 'http://localhost:3001',
    address: 'https://nomoreparties.co',
});
 
export default api;