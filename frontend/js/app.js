document.addEventListener('DOMContentLoaded', () => {
    const navLinksContainer = document.getElementById('nav-links');
    
    if (navLinksContainer) {
        const currentPage = window.location.pathname.split('/').pop();
        
        let navItems = [];
        
        // Admin Pages
        const adminPages = ['admin-dashboard.html', 'admin-loans.html', 'credit-intelligence.html', 'risk-policy.html', 'collections-ai.html', 'legal-repossession.html', 'reports.html', 'screen-configuration.html'];
        // Customer Pages
        const customerPages = ['customer-dashboard.html', 'loan-application.html', 'loan-offers.html', 'loan-tracking.html', 'kyc-upload.html'];
        // Public Pages
        const publicPages = ['login.html', 'signup.html', 'admin-login.html', 'index.html', ''];

        if (adminPages.includes(currentPage)) {
            navItems = [
                { name: 'Dashboard', url: 'admin-dashboard.html' },
                { name: 'Loan Applications', url: 'admin-loans.html' },
                { name: 'Risk Policies', url: 'risk-policy.html' },
                { name: 'Logout', url: 'login.html' }
            ];
            // Update the brand title to include ADMIN tag if not already there
            const brandH1 = document.querySelector('nav h1');
            if (brandH1 && !brandH1.innerHTML.includes('ADMIN')) {
                brandH1.innerHTML = 'CrediSphere AI <span style="font-size:12px; background:var(--teal); padding:2px 8px; border-radius:10px; margin-left:10px; vertical-align:middle;">ADMIN</span>';
            }
        } 
        else if (customerPages.includes(currentPage)) {
            navItems = [
                { name: 'Dashboard', url: 'customer-dashboard.html' },
                { name: 'Apply', url: 'loan-application.html' },
                { name: 'My Loans', url: 'loan-tracking.html' },
                { name: 'Logout', url: 'login.html' }
            ];
        } 
        else if (currentPage === 'admin-login.html') {
            navItems = [
                { name: 'Home', url: '../index.html' },
                { name: 'Customer Login', url: 'login.html' },
                { name: 'Admin Portal', url: 'admin-login.html' }
            ];
        }
        else {
            // Public Navigation
            navItems = [
                { name: 'Home', url: '../index.html' },
                { name: 'Sign Up', url: 'signup.html' },
                { name: 'Login', url: 'login.html' }
            ];
        }

        let navHTML = '';
        navItems.forEach(item => {
            const isActive = currentPage === item.url || (currentPage === '' && item.url === '../index.html');
            const activeClass = isActive ? 'active-link' : '';
            navHTML += `<a href="${item.url}" class="nav-item ${activeClass}">${item.name}</a>`;
        });

        navLinksContainer.innerHTML = navHTML;
    }
});
