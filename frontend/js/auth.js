/**
 * CrediSphere AI - Interactive Auth Controller
 * Handles Login, Registration, Demo Autofill, Password Strength & Telemetry
 */

// Helper to fill demo credentials into login forms
function fillDemo(email, password) {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorDiv = document.getElementById('login-error');

    if (errorDiv) errorDiv.style.display = 'none';

    if (emailInput && passwordInput) {
        emailInput.value = email;
        passwordInput.value = password;

        // Visual flash effect to indicate fill
        [emailInput, passwordInput].forEach(input => {
            input.style.transition = 'background-color 0.3s ease, border-color 0.3s ease';
            input.style.backgroundColor = 'rgba(59, 130, 246, 0.25)';
            input.style.borderColor = '#3b82f6';
            setTimeout(() => {
                input.style.backgroundColor = '';
                input.style.borderColor = '';
            }, 600);
        });

        // Focus submit button
        const loginBtn = document.getElementById('login-btn');
        if (loginBtn) loginBtn.focus();
    }
}

// Helper to auto-fill sample applicant in sign-up form
function fillSampleSignup() {
    const randomSuffix = Math.floor(100 + Math.random() * 900);
    const sampleData = {
        name: 'Aarav Sharma',
        phone: '+91 98765 43210',
        email: `aarav.sharma${randomSuffix}@credisphere.ai`,
        pan: `ABCPS${randomSuffix}F`,
        password: 'Password@123',
        confirm_password: 'Password@123'
    };

    Object.keys(sampleData).forEach(fieldId => {
        const el = document.getElementById(fieldId);
        if (el) {
            el.value = sampleData[fieldId];
            el.style.transition = 'background-color 0.3s ease, border-color 0.3s ease';
            el.style.backgroundColor = 'rgba(59, 130, 246, 0.25)';
            el.style.borderColor = '#3b82f6';
            setTimeout(() => {
                el.style.backgroundColor = '';
                el.style.borderColor = '';
            }, 600);
        }
    });

    const termsBox = document.getElementById('terms');
    if (termsBox) termsBox.checked = true;

    // Trigger strength meter calculation
    const pwInput = document.getElementById('password');
    if (pwInput) {
        pwInput.dispatchEvent(new Event('input'));
    }

    const signupBtn = document.getElementById('signup-btn');
    if (signupBtn) signupBtn.focus();
}

document.addEventListener('DOMContentLoaded', () => {
    // Check URL parameters for auto-fill request (e.g. ?fill=admin)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('fill') === 'admin') {
        fillDemo('admin@admin.in', 'admin123');
    }

    // Setup Password Show / Hide Toggles
    const setupPasswordToggle = (toggleBtnId, inputId) => {
        const toggleBtn = document.getElementById(toggleBtnId);
        const input = document.getElementById(inputId);
        if (toggleBtn && input) {
            toggleBtn.addEventListener('click', () => {
                const isPassword = input.type === 'password';
                input.type = isPassword ? 'text' : 'password';
                toggleBtn.textContent = isPassword ? '🔒' : '👁️';
            });
        }
    };

    setupPasswordToggle('toggle-pw-btn', 'password');
    setupPasswordToggle('toggle-pw-btn-1', 'password');
    setupPasswordToggle('toggle-pw-btn-2', 'confirm_password');

    // Live Password Strength Indicator (Sign-Up Page)
    const pwInput = document.getElementById('password');
    const strengthBox = document.getElementById('pw-strength-box');
    const bar1 = document.getElementById('str-bar-1');
    const bar2 = document.getElementById('str-bar-2');
    const bar3 = document.getElementById('str-bar-3');
    const bar4 = document.getElementById('str-bar-4');
    const strLabel = document.getElementById('str-label');

    if (pwInput && strengthBox && bar1 && bar2 && bar3 && bar4 && strLabel) {
        pwInput.addEventListener('input', () => {
            const val = pwInput.value;
            if (!val) {
                strengthBox.style.display = 'none';
                return;
            }
            strengthBox.style.display = 'block';

            let score = 0;
            if (val.length >= 6) score++;
            if (val.length >= 8 && /[A-Z]/.test(val) && /[a-z]/.test(val)) score++;
            if (/\d/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;

            // Reset classes
            [bar1, bar2, bar3, bar4].forEach(b => {
                b.className = 'strength-segment';
            });

            if (score <= 1) {
                bar1.classList.add('strength-weak');
                strLabel.textContent = 'Weak';
                strLabel.style.color = '#ef4444';
            } else if (score === 2) {
                bar1.classList.add('strength-fair');
                bar2.classList.add('strength-fair');
                strLabel.textContent = 'Moderate';
                strLabel.style.color = '#f59e0b';
            } else if (score === 3) {
                bar1.classList.add('strength-good');
                bar2.classList.add('strength-good');
                bar3.classList.add('strength-good');
                strLabel.textContent = 'Strong';
                strLabel.style.color = '#3b82f6';
            } else {
                bar1.classList.add('strength-strong');
                bar2.classList.add('strength-strong');
                bar3.classList.add('strength-strong');
                bar4.classList.add('strength-strong');
                strLabel.textContent = 'Military-Grade';
                strLabel.style.color = '#10b981';
            }
        });
    }

    // PAN Uppercase Auto-Format
    const panInput = document.getElementById('pan');
    if (panInput) {
        panInput.addEventListener('input', () => {
            panInput.value = panInput.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    }

    // LOGIN FORM SUBMISSION
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('login-error');
            const loginBtn = document.getElementById('login-btn');
            const originalBtnHTML = loginBtn ? loginBtn.innerHTML : 'Sign in securely';
            
            // UI Loading state
            if (errorDiv) errorDiv.style.display = 'none';
            if (loginBtn) {
                loginBtn.innerHTML = '<span>Authenticating with AI...</span> <span style="display:inline-block; animation:spin 1s infinite linear;">↻</span>';
                loginBtn.disabled = true;
            }
            
            try {
                // apiCall is globally available from api.js
                const response = await apiCall('/auth/login', 'POST', { email, password });
                
                // Save token and user info
                localStorage.setItem('token', response.token);
                localStorage.setItem('user', JSON.stringify(response.user));
                
                // Redirect based on role
                if (response.user.role === 'ADMIN') {
                    window.location.href = 'admin-dashboard.html';
                } else {
                    window.location.href = 'customer-dashboard.html';
                }
            } catch (err) {
                // Show error message
                if (errorDiv) {
                    errorDiv.textContent = err.message || 'Authentication failed. Please verify your email and password.';
                    errorDiv.style.display = 'block';
                }
            } finally {
                // Reset UI
                if (loginBtn) {
                    loginBtn.innerHTML = originalBtnHTML;
                    loginBtn.disabled = false;
                }
            }
        });
    }

    // SIGNUP FORM SUBMISSION
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            const errorDiv = document.getElementById('signup-error');
            const signupBtn = document.getElementById('signup-btn');
            const originalBtnHTML = signupBtn ? signupBtn.innerHTML : 'Create account & verify KYC';
            
            if (password !== confirmPassword) {
                if (errorDiv) {
                    errorDiv.textContent = 'Passwords do not match. Please re-enter your password.';
                    errorDiv.style.display = 'block';
                }
                return;
            }

            if (password.length < 6) {
                if (errorDiv) {
                    errorDiv.textContent = 'Password must be at least 6 characters long.';
                    errorDiv.style.display = 'block';
                }
                return;
            }
            
            // UI Loading state
            if (errorDiv) errorDiv.style.display = 'none';
            if (signupBtn) {
                signupBtn.innerHTML = '<span>Creating AI KYC Profile...</span> <span style="display:inline-block; animation:spin 1s infinite linear;">↻</span>';
                signupBtn.disabled = true;
            }
            const pan = document.getElementById('pan') ? document.getElementById('pan').value.trim().toUpperCase() : '';
            
            try {
                const response = await apiCall('/auth/signup', 'POST', { name, email, password, phone, pan });
                
                // On success, save token and user info immediately
                if (response.token) {
                    localStorage.setItem('token', response.token);
                }
                if (response.user) {
                    localStorage.setItem('user', JSON.stringify(response.user));
                }
                
                // Redirect immediately to Customer Portal
                window.location.href = 'customer-dashboard.html';
                
            } catch (err) {
                // Show error message
                if (errorDiv) {
                    errorDiv.textContent = err.message || 'Signup failed. Email may already be registered.';
                    errorDiv.style.display = 'block';
                }
            } finally {
                // Reset UI
                if (signupBtn) {
                    signupBtn.innerHTML = originalBtnHTML;
                    signupBtn.disabled = false;
                }
            }
        });
    }
});
