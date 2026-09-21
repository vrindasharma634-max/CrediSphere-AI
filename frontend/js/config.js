/**
 * CrediSphere AI - Global Runtime Configuration
 * Production Backend API: https://credisphere-ai.onrender.com
 */
(function() {
    const DEFAULT_BACKEND_URL = 'https://credisphere-ai.onrender.com';

    window.BACKEND_API_URL = window.BACKEND_API_URL || DEFAULT_BACKEND_URL;
    window.APP_CONFIG = {
        BACKEND_URL: window.BACKEND_API_URL.replace(/\/+$/, ''),
        API_BASE: `${window.BACKEND_API_URL.replace(/\/+$/, '')}/api`,
        VERSION: '2.0.0-production'
    };
})();
