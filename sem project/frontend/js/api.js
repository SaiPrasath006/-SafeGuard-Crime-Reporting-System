const API_URL = `${window.location.protocol}//${window.location.hostname}:5000/api`;

const api = {
    async post(endpoint, data, isFormData = false) {
        const headers = {};
        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }

        const token = localStorage.getItem('token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const options = {
            method: 'POST',
            headers: headers,
            body: isFormData ? data : JSON.stringify(data)
        };

        const response = await fetch(`${API_URL}${endpoint}`, options);
        return await response.json();
    },

    async get(endpoint) {
        const headers = {};
        const token = localStorage.getItem('token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            headers: headers
        });
        return await response.json();
    },

    async put(endpoint, data) {
        const headers = {
            'Content-Type': 'application/json'
        };
        const token = localStorage.getItem('token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify(data)
        });
        return await response.json();
    }
};

function showNotification(message, type = 'success') {
    const bar = document.getElementById('notification-bar');
    if (!bar) return;

    bar.innerText = message;
    bar.style.display = 'block';
    bar.style.borderColor = type === 'success' ? 'var(--accent-green)' : 'var(--accent-red)';

    setTimeout(() => {
        bar.style.display = 'none';
    }, 4000);
}
