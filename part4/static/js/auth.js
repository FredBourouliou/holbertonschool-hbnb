// Fonctions utilitaires pour l'authentification
const auth = {
    // Récupérer le token JWT depuis les cookies
    getToken() {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; token=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    },

    // Vérifier si l'utilisateur est connecté
    isLoggedIn() {
        return !!this.getToken();
    },

    // Mettre à jour l'interface utilisateur en fonction de l'état de connexion
    updateUI() {
        const loginLink = document.getElementById('login-link');
        if (loginLink) {
            if (this.isLoggedIn()) {
                loginLink.textContent = 'Logout';
                loginLink.href = '#';
                loginLink.onclick = (e) => {
                    e.preventDefault();
                    this.logout();
                };
            } else {
                loginLink.textContent = 'Login';
                loginLink.href = '/templates/login.html';
                loginLink.onclick = null;
            }
        }
    },

    // Déconnexion de l'utilisateur
    logout() {
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/templates/login.html';
    }
};

// Mettre à jour l'interface utilisateur au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    auth.updateUI();
}); 