// CrediSphere AI - Production Backend Configuration
const BACKEND_URL = (typeof window !== 'undefined' && window.BACKEND_API_URL)
    ? window.BACKEND_API_URL.replace(/\/+$/, '')
    : 'https://credisphere-ai.onrender.com'.replace(/\/+$/, '');

const API_BASE = `${BACKEND_URL}/api`;

/**
 * Safely resolves and normalizes API URLs, eliminating double slashes
 * and ensuring trailing/leading slashes resolve cleanly without duplicate /api prefixes.
 */
function resolveApiUrl(endpoint = '') {
    if (!endpoint) return API_BASE;
    if (endpoint.startsWith('http://') || endpoint.startsWith('https://')) {
        return endpoint;
    }
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    if (cleanEndpoint.startsWith('/api/')) {
        return `${BACKEND_URL}${cleanEndpoint}`.replace(/([^:]\/)\/+/g, '$1');
    }
    return `${API_BASE}${cleanEndpoint}`.replace(/([^:]\/)\/+/g, '$1');
}

if (typeof window !== 'undefined') {
    window.BACKEND_URL = BACKEND_URL;
    window.API_BASE = API_BASE;
    window.resolveApiUrl = resolveApiUrl;
}

async function apiCall(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
    const config = { method, headers };
    if (data) config.body = JSON.stringify(data);
    try {
        const targetUrl = resolveApiUrl(endpoint);
        const res = await fetch(targetUrl, config);
        const json = await res.json();
        if (!res.ok) throw new Error(json.error || 'API Error');
        return json;
    } catch (e) {
        console.error('API Call Failed:', e);
        throw e;
    }
}
