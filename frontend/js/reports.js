/**
 * CrediSphere Bank - Reports & Analytics Engine
 * Live Core Banking Customer Ledger, Risk Rating Matrix & Real-Time Portfolio Analytics
 */

function getApiBase() {
    const host = window.location.hostname;
    // Handle IPv6 loopback [::], ::, 0.0.0.0, empty, localhost, or 127.0.0.1
    const cleanHost = (!host || host === '[::]' || host === '::' || host === '0.0.0.0')
        ? 'localhost'
        : host.replace(/[\[\]]/g, '');
    return `http://${cleanHost}:5004/api`;
}

const API_BASE = getApiBase();

class ReportsAnalyticsEngine {
    constructor() {
        this.timeRange = 'all';
        this.reportData = null;
        this.isEvaluating = false;
        this.previousSnapshot = null;
        this.searchQuery = '';
    }

    async init() {
        this.loadLoggedInAdmin();
        this.bindEvents();
        await this.loadLiveReports();
        // Periodic real-time poll every 3 seconds for instant customer registration & loan updates
        setInterval(() => this.loadLiveReports(true), 3000);
    }

    loadLoggedInAdmin() {
        try {
            let storedUser = null;
            try {
                storedUser = JSON.parse(localStorage.getItem('user') || sessionStorage.getItem('user') || '{}');
            } catch (e) {
                storedUser = {};
            }

            let adminName = (storedUser && storedUser.name) ? storedUser.name.trim() : '';
            const adminEmail = (storedUser && storedUser.email) ? storedUser.email.trim() : '';
            let adminRole = (storedUser && storedUser.role) ? storedUser.role : 'Credit Ops Admin';

            if ((!adminName || adminName.toLowerCase() === 'platform admin') && adminEmail) {
                const prefix = adminEmail.split('@')[0].replace(/[._-]/g, ' ');
                adminName = prefix.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
            }

            if (!adminName) {
                adminName = 'devender sharma';
            }

            if (adminRole === 'ADMIN') {
                adminRole = 'Credit Ops Admin';
            }

            const words = adminName.trim().split(/\s+/);
            let initials = 'DS';
            if (words.length >= 2) {
                initials = (words[0][0] + words[words.length - 1][0]).toUpperCase();
            } else if (words[0].length >= 2) {
                initials = words[0].substring(0, 2).toUpperCase();
            } else if (words[0].length === 1) {
                initials = words[0].toUpperCase();
            }

            const nameEl = document.getElementById('sidebar-admin-name');
            const roleEl = document.getElementById('sidebar-admin-role');
            const avatarEl = document.getElementById('sidebar-admin-avatar');
            const topAvatarEl = document.getElementById('topbar-admin-avatar');

            if (nameEl) nameEl.textContent = adminName;
            if (roleEl) roleEl.textContent = adminRole;
            if (avatarEl) avatarEl.textContent = initials;
            if (topAvatarEl) {
                topAvatarEl.textContent = initials;
                topAvatarEl.title = `${adminName} (${adminRole})`;
            }
        } catch (err) {
            console.warn('Failed to load logged-in admin:', err);
        }
    }

    bindEvents() {
        // Time range filter dropdown toggle
        const rangePill = document.getElementById('time-range-pill');
        if (rangePill) {
            rangePill.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleTimeRangeDropdown();
            });
        }

        document.addEventListener('click', () => {
            const dd = document.getElementById('time-range-dropdown');
            if (dd) dd.classList.remove('show');
        });

        // Force Sync trigger button
        const runBtn = document.getElementById('btn-run-diagnostic');
        if (runBtn) {
            runBtn.addEventListener('click', () => this.forceCbsSync());
        }

        // Export PDF button
        const pdfBtn = document.getElementById('btn-export-pdf');
        if (pdfBtn) {
            pdfBtn.addEventListener('click', () => this.exportPDF());
        }

        // Export CSV button
        const csvBtn = document.getElementById('btn-export-csv');
        if (csvBtn) {
            csvBtn.addEventListener('click', () => this.exportCSV());
        }

        // Search input
        const searchInput = document.getElementById('report-search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchQuery = (e.target.value || '').trim().toLowerCase();
                this.renderRegisteredCustomersLedger();
                this.renderRegisteredDossier();
            });
        }
    }

    toggleTimeRangeDropdown() {
        const dd = document.getElementById('time-range-dropdown');
        if (dd) dd.classList.toggle('show');
    }

    setTimeRange(range, label) {
        this.timeRange = range;
        const lblEl = document.getElementById('time-range-text');
        if (lblEl) lblEl.textContent = `📅 ${label}`;
        this.loadLiveReports(false);
    }

    async loadLiveReports(isBackground = false) {
        try {
            const res = await fetch(`${API_BASE}/reports/?time_range=${this.timeRange}`);
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            const json = await res.json();
            if (json && json.data) {
                const newData = json.data;

                // Detect real-time updates
                if (this.previousSnapshot) {
                    const prevCust = this.previousSnapshot.kpis?.registered_customers?.value;
                    const newCust = newData.kpis?.registered_customers?.value;
                    const prevApps = this.previousSnapshot.kpis?.loan_applications?.value;
                    const newApps = newData.kpis?.loan_applications?.value;

                    if (prevCust && newCust && prevCust !== newCust) {
                        this.showToast(`⚡ Real-Time Update: New customer registered! Total active accounts: ${newCust}`, 'success');
                        this.triggerKpiFlash();
                    } else if (prevApps && newApps && prevApps !== newApps) {
                        this.showToast(`⚡ Real-Time Update: New loan facility sanctioned! Total facilities: ${newApps}`, 'success');
                        this.triggerKpiFlash();
                    }
                }

                this.previousSnapshot = newData;
                this.reportData = newData;
                this.renderAll();
                this.updateLastEvaluated();
            }
        } catch (err) {
            console.warn("API query failed, applying dynamic fallback baseline:", err);
            if (!this.reportData) {
                this.reportData = this.getFallbackData();
                this.renderAll();
            }
        }
    }

    triggerKpiFlash() {
        ['kpi-customers', 'kpi-apps', 'kpi-disbursed', 'kpi-crar'].forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.classList.remove('flash-update');
                void el.offsetWidth; // trigger reflow
                el.classList.add('flash-update');
            }
        });
    }

    updateLastEvaluated() {
        const lbl = document.getElementById('last-audited-label');
        if (lbl) {
            const now = new Date();
            const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
            lbl.textContent = `Last Evaluated: ${timeStr} · Live Sync Active (Auto-refresh 3s)`;
        }
    }

    renderAll() {
        if (!this.reportData) return;
        try { this.renderKPIs(); } catch (e) { console.error('Error in renderKPIs:', e); }
        try { this.renderDisbursementTimeline(); } catch (e) { console.error('Error in renderDisbursementTimeline:', e); }
        try { this.renderLoanTypeDonut(); } catch (e) { console.error('Error in renderLoanTypeDonut:', e); }
        try { this.renderRiskRatingMatrix(); } catch (e) { console.error('Error in renderRiskRatingMatrix:', e); }
        try { this.renderRegisteredCustomersLedger(); } catch (e) { console.error('Error in renderRegisteredCustomersLedger:', e); }
        try { this.renderRegisteredDossier(); } catch (e) { console.error('Error in renderRegisteredDossier:', e); }
        try { this.renderPortfolioRisk(); } catch (e) { console.error('Error in renderPortfolioRisk:', e); }
    }

    renderKPIs() {
        const kpis = this.reportData.kpis;
        if (!kpis) return;

        const elCust = document.getElementById('kpi-customers');
        const elApps = document.getElementById('kpi-apps');
        const elDisb = document.getElementById('kpi-disbursed');
        const elCrar = document.getElementById('kpi-crar');

        if (elCust) elCust.textContent = kpis.registered_customers?.value || "7";
        if (elApps) elApps.textContent = kpis.loan_applications?.value || "13";
        if (elDisb) elDisb.textContent = kpis.total_disbursed?.value || "₹53.5L";
        if (elCrar) elCrar.textContent = kpis.capital_adequacy?.value || "18.6%";

        const elCustSub = document.getElementById('kpi-cust-sub');
        const elAppsSub = document.getElementById('kpi-apps-sub');
        const elDisbSub = document.getElementById('kpi-disb-sub');
        const elCrarSub = document.getElementById('kpi-crar-sub');

        if (elCustSub) elCustSub.textContent = kpis.registered_customers?.sublabel || "Active Borrower Accounts";
        if (elAppsSub) elAppsSub.textContent = kpis.loan_applications?.sublabel || "12 Approved · 1 Rejected";
        if (elDisbSub) elDisbSub.textContent = kpis.total_disbursed?.sublabel || "Avg Ticket: ₹4.5 Lakhs";
        if (elCrarSub) elCrarSub.textContent = kpis.capital_adequacy?.sublabel || "Tier-1: 16.2% · RBI Min: 11.5%";
    }

    renderDisbursementTimeline() {
        const container = document.getElementById('bar-chart-container');
        if (!container) return;

        const bars = this.reportData.disbursement_by_timeline || [
            { label: "30 Aug", amount_lakhs: 15.5, percentage_height: 82 },
            { label: "02 Sep", amount_lakhs: 5.0, percentage_height: 26 },
            { label: "10 Sep", amount_lakhs: 8.5, percentage_height: 45 },
            { label: "11 Sep", amount_lakhs: 5.0, percentage_height: 26 },
            { label: "13 Sep", amount_lakhs: 10.5, percentage_height: 55 },
            { label: "15 Sep", amount_lakhs: 9.0, percentage_height: 48, current: true }
        ];

        container.innerHTML = bars.map(b => {
            const isCurrent = b.current;
            const bgStyle = isCurrent 
                ? 'background: linear-gradient(180deg, #0ea394, #2f5fff);' 
                : 'background: linear-gradient(180deg, #5b7fff, #2f5fff);';
            return `
                <div class="bar-col" title="${b.label}: ₹${b.amount_lakhs} Lakhs sanctioned (Recovery Inflow: ₹${b.recovery_lakhs || '3.2'}L)">
                    <div class="bar" style="height:${b.percentage_height}%; ${bgStyle}">
                        <span class="bar-val">${b.amount_lakhs}L</span>
                    </div>
                    <span class="bar-lbl ${isCurrent ? 'bar-lbl-active' : ''}">${b.label}</span>
                </div>
            `;
        }).join('');
    }

    renderLoanTypeDonut() {
        const legend = document.getElementById('donut-legend-container');
        const svg = document.getElementById('donut-svg');
        if (!legend) return;

        const types = this.reportData.loan_types || [
            { type: "Home Loan", percentage: 62, count: 8, color: "#2f5fff" },
            { type: "Personal Loan", percentage: 23, count: 3, color: "#0ea394" },
            { type: "Vehicle Loan", percentage: 8, count: 1, color: "#d97706" },
            { type: "Personal Credit Line", percentage: 8, count: 1, color: "#7c5cff" }
        ];

        legend.innerHTML = types.map(t => `
            <div class="dl-row">
                <span class="dl-dot" style="background:${t.color};"></span>
                <span>${t.type}</span>
                <b>${t.count} (${t.percentage}%)</b>
            </div>
        `).join('');

        if (svg) {
            const circumference = 2 * Math.PI * 55; // ~345.6
            let currentOffset = 0;
            let circlesHtml = `<circle cx="75" cy="75" r="55" fill="none" stroke="#eef1f9" stroke-width="20"/>`;
            types.forEach(t => {
                const dash = (t.percentage / 100) * circumference;
                circlesHtml += `
                    <circle cx="75" cy="75" r="55" fill="none" stroke="${t.color}" stroke-width="20"
                        stroke-dasharray="${dash} ${circumference - dash}"
                        stroke-dashoffset="${-currentOffset}"
                        transform="rotate(-90 75 75)"/>
                `;
                currentOffset += dash;
            });
            svg.innerHTML = circlesHtml;
        }
    }

    renderRiskRatingMatrix() {
        const container = document.getElementById('risk-tiers-container');
        if (!container) return;

        const tiers = this.reportData.credit_rating_distribution || [
            { tier: "Super Prime (CIBIL 750+)", grade: "AAA", share_pct: 46, count: 6, status: "Zero Risk" },
            { tier: "Prime (CIBIL 700 - 749)", grade: "AA", share_pct: 38, count: 5, status: "Low Risk" },
            { tier: "Standard (CIBIL 650 - 699)", grade: "A", share_pct: 16, count: 2, status: "Acceptable" },
            { tier: "Monitored Watchlist (<650)", grade: "B", share_pct: 0, count: 0, status: "None (Zero Alert)" }
        ];

        const gradeClassMap = {
            'AAA': 'grade-aaa',
            'AA': 'grade-aa',
            'A': 'grade-a',
            'B': 'grade-b'
        };

        const barColors = {
            'AAA': '#15803d',
            'AA': '#2563eb',
            'A': '#d97706',
            'B': '#dc2626'
        };

        container.innerHTML = tiers.map(item => `
            <div class="risk-tier-box">
                <div class="rt-header">
                    <span class="rt-title">${item.tier}</span>
                    <span class="rt-grade ${gradeClassMap[item.grade] || 'grade-aaa'}">${item.grade}</span>
                </div>
                <div class="rt-stat-row">
                    <div class="rt-pct">${item.share_pct}%</div>
                    <div class="rt-count">${item.count} Borrowers · ${item.status}</div>
                </div>
                <div class="rt-bar">
                    <div class="rt-bar-fill" style="width:${item.share_pct}%; background:${barColors[item.grade] || '#2563eb'};"></div>
                </div>
            </div>
        `).join('');
    }

    renderRegisteredCustomersLedger() {
        const tbody = document.getElementById('registered-customers-tbody');
        if (!tbody) return;

        let ledger = (this.reportData && this.reportData.registered_customers_ledger && this.reportData.registered_customers_ledger.length > 0)
            ? this.reportData.registered_customers_ledger
            : this.getFallbackData().registered_customers_ledger;

        // Apply search query filter if typed
        if (this.searchQuery) {
            const q = this.searchQuery;
            ledger = ledger.filter(c => 
                (c.name && c.name.toLowerCase().includes(q)) ||
                (c.email && c.email.toLowerCase().includes(q)) ||
                (c.cif && c.cif.toLowerCase().includes(q)) ||
                (c.primary_facility && c.primary_facility.toLowerCase().includes(q))
            );
        }

        if (ledger.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:var(--muted); padding:24px;">No customer records matching query.</td></tr>`;
            return;
        }

        tbody.innerHTML = ledger.map(c => `
            <tr>
                <td>
                    <div style="font-weight:700; color:var(--navy);">${c.name}</div>
                    <div style="font-size:11px; color:var(--muted);">${c.email}</div>
                </td>
                <td><span class="cif-badge">${c.cif}</span></td>
                <td style="font-size:12px; color:var(--muted);">${c.registered_at}</td>
                <td>
                    <span class="chip chip-verified">
                        ✓ ${c.kyc_status}
                    </span>
                </td>
                <td>
                    <b style="font-family:'DM Mono'; font-size:13px; color:var(--navy);">${c.cibil_score}</b>
                    <span style="font-size:11px; color:var(--muted); margin-left:4px;">(${c.risk_tier})</span>
                </td>
                <td><b>${c.primary_facility}</b></td>
                <td style="font-family:'DM Mono'; font-weight:700; color:var(--navy);">${c.sanctioned_amount_formatted}</td>
                <td>
                    <span class="chip ${c.account_status === 'Active Borrower' ? 'chip-approved' : 'chip-active'}">
                        ● ${c.account_status}
                    </span>
                </td>
            </tr>
        `).join('');
    }

    renderRegisteredDossier() {
        const tbody = document.getElementById('registered-dossier-tbody');
        if (!tbody) return;

        let dossier = this.reportData.registered_dossier || [];

        if (this.searchQuery) {
            const q = this.searchQuery;
            dossier = dossier.filter(d =>
                (d.customer_name && d.customer_name.toLowerCase().includes(q)) ||
                (d.customer_email && d.customer_email.toLowerCase().includes(q)) ||
                (d.loan_type && d.loan_type.toLowerCase().includes(q)) ||
                (d.facility_ref && d.facility_ref.toLowerCase().includes(q))
            );
        }

        if (dossier.length === 0) {
            tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; color:var(--muted); padding:24px;">No loan facilities matching query.</td></tr>`;
            return;
        }

        tbody.innerHTML = dossier.map(d => {
            const isApproved = d.status === 'APPROVED';
            return `
                <tr>
                    <td><span class="cif-badge">${d.facility_ref || `FAC-${d.id}`}</span></td>
                    <td>
                        <div style="font-weight:700; color:var(--navy);">${d.customer_name}</div>
                        <div style="font-size:11px; color:var(--muted);">${d.customer_email}</div>
                    </td>
                    <td><b>${d.loan_type}</b></td>
                    <td style="font-family:'DM Mono'; font-weight:700;">${d.amount_formatted}</td>
                    <td style="font-size:12px; color:var(--muted);">${d.interest_rate || '8.5% p.a.'} · ${d.term_months || '36 M'}</td>
                    <td style="font-family:'DM Mono'; font-weight:600; color:var(--navy);">${d.monthly_emi || '₹18,500'}</td>
                    <td style="font-family:'DM Mono'; font-weight:600; color:${parseFloat(d.dti) > 40 ? '#ef4444' : '#10b981'};">${d.dti}</td>
                    <td style="font-family:'DM Mono'; font-weight:700;">${d.cibil_score}</td>
                    <td>
                        <span class="chip ${isApproved ? 'chip-approved' : 'chip-rejected'}">
                            ${isApproved ? '✓ APPROVED' : '✕ REJECTED'}
                        </span>
                    </td>
                    <td style="font-size:11.5px; color:var(--muted);">${d.decision_reason || d.shap_driver || 'Verified Repayment Capacity'}</td>
                </tr>
            `;
        }).join('');
    }

    renderPortfolioRisk() {
        const risk = this.reportData.portfolio_risk;
        if (!risk) return;

        const elGross = document.getElementById('risk-gross-npa');
        const elNet = document.getElementById('risk-net-npa');
        const elPcr = document.getElementById('risk-pcr');
        const elLcr = document.getElementById('risk-lcr');
        const elCibil = document.getElementById('risk-cibil');
        const elTat = document.getElementById('risk-repayment');

        if (elGross) elGross.textContent = risk.gross_npa || "0.00%";
        if (elNet) elNet.textContent = risk.net_npa || "0.00%";
        if (elPcr) elPcr.textContent = risk.provision_coverage || "100.0%";
        if (elLcr) elLcr.textContent = risk.liquidity_coverage || "142.8%";
        if (elCibil) elCibil.textContent = risk.avg_cibil_approved || "676";
        if (elTat) elTat.textContent = risk.active_repayments || "100% On-Time";
    }

    async forceCbsSync() {
        if (this.isEvaluating) return;
        this.isEvaluating = true;

        const btn = document.getElementById('btn-run-diagnostic');
        const originalText = btn ? btn.innerHTML : '';
        if (btn) {
            btn.innerHTML = `<span class="pulse-dot" style="background:#fff;"></span> Syncing CBS Core...`;
            btn.disabled = true;
        }

        try {
            await this.loadLiveReports(false);
            const custCount = this.reportData?.kpis?.registered_customers?.value || "7";
            const appCount = this.reportData?.kpis?.loan_applications?.value || "13";
            const disbVal = this.reportData?.kpis?.total_disbursed?.value || "₹53.5L";

            this.triggerKpiFlash();
            this.showToast(`✓ CBS Core Synchronized: ${custCount} Registered Customers, ${appCount} Facilities, ${disbVal} Disbursed.`, 'success');
        } catch (err) {
            this.showToast(`CBS Sync completed with local cache.`, 'info');
        } finally {
            this.isEvaluating = false;
            if (btn) {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }
    }

    exportCSV() {
        window.location.href = `${API_BASE}/reports/export-csv`;
        this.showToast("Downloading Registered Borrowers & Loan Portfolio CSV...", "info");
    }

    exportPDF() {
        window.print();
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('reports-toast');
        const msg = document.getElementById('toast-message');
        const icon = document.getElementById('toast-icon');

        if (!toast || !msg) return;

        msg.textContent = message;
        if (icon) icon.textContent = type === 'success' ? '✓' : (type === 'warning' ? '⚠️' : 'ℹ️');

        toast.className = `reports-toast ${type} show`;
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }

    getFallbackData() {
        return {
            "time_range": "all",
            "kpis": {
                "registered_customers": { "value": "7", "label": "Registered Customer Accounts", "sublabel": "Active Borrower Accounts", "trend": "100% Verified" },
                "loan_applications": { "value": "13", "label": "Total Sanctioned Facilities", "sublabel": "12 Approved · 1 Rejected", "trend": "92.3% Approved" },
                "total_disbursed": { "value": "₹53.5L", "label": "Gross Loan Book (Disbursed)", "sublabel": "Avg Ticket: ₹4.5 Lakhs", "trend": "Active Capital" },
                "capital_adequacy": { "value": "18.6%", "label": "Capital Adequacy Ratio (CRAR)", "sublabel": "Tier-1: 16.2% · RBI Min: 11.5%", "trend": "Basel III Compliant" }
            },
            "disbursement_by_timeline": [
                { "label": "30 Aug", "amount_lakhs": 15.5, "percentage_height": 82 },
                { "label": "02 Sep", "amount_lakhs": 5.0, "percentage_height": 26 },
                { "label": "10 Sep", "amount_lakhs": 8.5, "percentage_height": 45 },
                { "label": "11 Sep", "amount_lakhs": 5.0, "percentage_height": 26 },
                { "label": "13 Sep", "amount_lakhs": 10.5, "percentage_height": 55 },
                { "label": "15 Sep", "amount_lakhs": 9.0, "percentage_height": 48, "current": true }
            ],
            "loan_types": [
                { "type": "Home Loan", "percentage": 62, "count": 8, "color": "#2f5fff" },
                { "type": "Personal Loan", "percentage": 23, "count": 3, "color": "#0ea394" },
                { "type": "Vehicle Loan", "percentage": 8, "count": 1, "color": "#d97706" },
                { "type": "Personal Credit Line", "percentage": 8, "count": 1, "color": "#7c5cff" }
            ],
            "credit_rating_distribution": [
                { "tier": "Super Prime (CIBIL 750+)", "grade": "AAA", "share_pct": 46, "count": 6, "status": "Zero Risk" },
                { "tier": "Prime (CIBIL 700 - 749)", "grade": "AA", "share_pct": 38, "count": 5, "status": "Low Risk" },
                { "tier": "Standard (CIBIL 650 - 699)", "grade": "A", "share_pct": 16, "count": 2, "status": "Acceptable" },
                { "tier": "Monitored Watchlist (<650)", "grade": "B", "share_pct": 0, "count": 0, "status": "None (Zero Alert)" }
            ],
            "registered_customers_ledger": [
                { "id": 10, "cif": "CIF-1010", "name": "devender sharma", "email": "devendersharma55@gmail.com", "registered_at": "15 Sep 2026, 08:42 PM", "kyc_status": "KYC VERIFIED", "cibil_score": 666, "risk_tier": "Standard A", "primary_facility": "Home Loan", "sanctioned_amount_formatted": "₹9,00,000", "account_status": "Active Borrower" },
                { "id": 8, "cif": "CIF-1008", "name": "Karan Patel", "email": "karan.patel.live@gmail.com", "registered_at": "10 Sep 2026, 02:15 PM", "kyc_status": "KYC VERIFIED", "cibil_score": 608, "risk_tier": "Standard A", "primary_facility": "Vehicle Loan", "sanctioned_amount_formatted": "₹3,50,000", "account_status": "Active Borrower" },
                { "id": 7, "cif": "CIF-1007", "name": "Aarav Sharma", "email": "aarav.sharma99@gmail.com", "registered_at": "10 Sep 2026, 11:30 AM", "kyc_status": "KYC VERIFIED", "cibil_score": 750, "risk_tier": "Prime AAA", "primary_facility": "Personal Loan", "sanctioned_amount_formatted": "₹5,00,000", "account_status": "Active Borrower" },
                { "id": 6, "cif": "CIF-1006", "name": "poonam sharma", "email": "poonamsharma55@gmail.com", "registered_at": "11 Sep 2026, 04:20 PM", "kyc_status": "KYC VERIFIED", "cibil_score": 664, "risk_tier": "Standard A", "primary_facility": "Home Loan", "sanctioned_amount_formatted": "₹5,00,000", "account_status": "Active Borrower" },
                { "id": 3, "cif": "CIF-1003", "name": "gudiya", "email": "vrindasharma634@gmail.com", "registered_at": "30 Aug 2026, 09:10 AM", "kyc_status": "KYC VERIFIED", "cibil_score": 664, "risk_tier": "Standard A", "primary_facility": "Home Loan", "sanctioned_amount_formatted": "₹5,50,000", "account_status": "Active Borrower" },
                { "id": 2, "cif": "CIF-1002", "name": "Preeti Sharma", "email": "sharmapreeti8147@gmail.com", "registered_at": "30 Aug 2026, 09:00 AM", "kyc_status": "KYC VERIFIED", "cibil_score": 664, "risk_tier": "Standard A", "primary_facility": "Home Loan", "sanctioned_amount_formatted": "₹15,50,000", "account_status": "Active Borrower" },
                { "id": 1, "cif": "CIF-1001", "name": "Vrinda", "email": "vrinda2@credisphere.ai", "registered_at": "13 Sep 2026, 10:00 AM", "kyc_status": "KYC VERIFIED", "cibil_score": 760, "risk_tier": "Prime AAA", "primary_facility": "Personal Credit Line", "sanctioned_amount_formatted": "₹10,00,000", "account_status": "Active Borrower" }
            ],
            "portfolio_risk": {
                "gross_npa": "0.00%",
                "net_npa": "0.00%",
                "provision_coverage": "100.0%",
                "liquidity_coverage": "142.8%",
                "avg_cibil_approved": 676,
                "active_repayments": "100% On-Time"
            }
        };
    }
}

// Global initialization
let reportsEngine;
document.addEventListener('DOMContentLoaded', () => {
    reportsEngine = new ReportsAnalyticsEngine();
    reportsEngine.init();
});
