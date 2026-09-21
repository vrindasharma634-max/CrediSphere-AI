
const API_BASE = 'http://localhost:5004/api';
async function apiCall(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
    const config = { method, headers };
    if (data) config.body = JSON.stringify(data);
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, config);
        const json = await res.json();
        if (!res.ok) throw new Error(json.error || 'API Error');
        return json;
    } catch (e) {
        console.error('API Call Failed:', e);
        throw e;
    }
}
