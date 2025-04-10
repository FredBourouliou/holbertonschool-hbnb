document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const API_URL = 'http://localhost:5001/api/v1'; // URL de l'API backend de la part3 (port 5001 pour Mac)

    // Si l'utilisateur est déjà connecté, rediriger vers la page d'accueil
    if (auth.isLoggedIn()) {
        window.location.href = '/templates/index.html';
        return;
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Stockage du JWT token dans un cookie sécurisé
                    document.cookie = `token=${data.access_token}; path=/; Secure; SameSite=Strict`;
                    // Mettre à jour l'interface utilisateur
                    auth.updateUI();
                    // Redirection vers la page d'accueil
                    window.location.href = '/templates/index.html';
                } else {
                    const errorData = await response.json();
                    alert(errorData.message || 'Login failed. Please check your credentials.');
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred during login. Please try again.');
            }
        });
    }

    // Fonction utilitaire pour récupérer un cookie par son nom
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Vérifier si l'utilisateur est déjà connecté
    const token = getCookie('token');
    if (token) {
        // Si l'utilisateur est déjà connecté, rediriger vers la page d'accueil
        window.location.href = 'index.html';
    }
}); 