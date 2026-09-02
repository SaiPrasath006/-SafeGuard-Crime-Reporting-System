function updateAuthUI() {
    const navAuthLinks = document.getElementById('nav-auth-links');
    if (!navAuthLinks) return;

    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const role = localStorage.getItem('role');

    if (token) {
        let adminLink = role === 'admin' ? `<li><a href="admin.html">Dashboard</a></li>` : '';
        navAuthLinks.innerHTML = `
            <span style="margin-right: 1rem; color: var(--text-muted)">Welcome, <b>${username}</b></span>
            ${adminLink}
            <button onclick="logout()" class="btn btn-outline">Logout</button>
        `;
    }
}

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', updateAuthUI);
