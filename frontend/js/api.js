const BASE_URL = 'http://localhost:8000';

async function fetchAPI(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const config = { method, headers };
    if (body) config.body = JSON.stringify(body);

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);
        if (response.status === 401) {
            localStorage.removeItem('token');
            if (!window.location.pathname.endsWith('login.html')) window.location.href = 'login.html';
        }
        if (response.status === 204) return { success: true };
        const data = await response.json();
        return { success: response.ok, status: response.status, data };
    } catch (error) {
        console.error("Erro:", error);
        return { success: false, data: { detail: "Erro de conexão com o servidor." } };
    }
}