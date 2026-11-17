document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.style.display = 'none';

    const response = await fetchAPI('/login', 'POST', { email, senha });

    if (response.success) {
        localStorage.setItem('token', response.data.token);
        window.location.href = 'admin.html';
    } else {
        errorDiv.textContent = response.data.detail || "Erro ao fazer login.";
        errorDiv.style.display = 'block';
    }
});