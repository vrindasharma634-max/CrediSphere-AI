document.addEventListener('DOMContentLoaded', () => {
    // Calculator elements
    const inputs = {
        income: document.getElementById('calc-income'),
        employment: document.getElementById('calc-employment'),
        emi: document.getElementById('calc-emi'),
        tenure: document.getElementById('calc-tenure')
    };
    const tenureDisplay = document.getElementById('tenure-display');

    // UI elements
    const gaugeFill = document.getElementById('score-gauge');
    const scoreText = document.getElementById('score-text');
    const scoreBand = document.getElementById('score-band');
    
    const dtiText = document.getElementById('dti-text');
    const dtiBar = document.getElementById('dti-bar');
    
    const resSanction = document.getElementById('res-sanction');
    const resRate = document.getElementById('res-rate');
    const resEmi = document.getElementById('res-emi');
    const resStatus = document.getElementById('res-status');

    // Number formatter for Indian Rupees
    const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

    let debounceTimer;

    const fetchSimulation = async () => {
        const payload = {
            income: inputs.income.value || 0,
            employment_profile: inputs.employment.value,
            existing_emi: inputs.emi.value || 0,
            requested_tenure_months: inputs.tenure.value
        };

        try {
            const res = await fetch('http://localhost:5004/api/calculator/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            updateUI(data);
        } catch (error) {
            console.error("Simulation failed", error);
        }
    };

    const updateUI = (data) => {
        // 1. Update Gauge (300 to 900)
        const score = data.score;
        const normalized = Math.max(0, Math.min(1, (score - 300) / 600));
        // Circle circumference is 628. Offset 628 = 0%, 0 = 100%
        const offset = 628 - (normalized * 628);
        gaugeFill.style.strokeDashoffset = offset;
        scoreText.textContent = score;

        // Colors
        let color = '#ef4444'; // Red
        if (score >= 750) color = '#10b981'; // Green
        else if (score >= 650) color = '#06b6d4'; // Teal
        else if (score >= 550) color = '#f59e0b'; // Amber

        gaugeFill.style.stroke = color;
        scoreText.style.color = color;
        
        // 2. Decision Logic
        const decision = data.decision;
        scoreBand.textContent = decision.band || decision.status;
        
        // 3. DTI Update
        dtiText.textContent = `${data.dti_percentage}%`;
        dtiBar.style.width = `${Math.min(100, data.dti_percentage)}%`;
        if (data.dti_percentage > 50) dtiBar.style.background = '#ef4444';
        else if (data.dti_percentage > 40) dtiBar.style.background = '#f59e0b';
        else dtiBar.style.background = '#10b981';

        // 4. Results
        if (decision.status === 'Rejected') {
            resSanction.textContent = '₹ 0';
            resRate.textContent = '-';
            resEmi.textContent = '₹ 0';
            resStatus.textContent = 'Declined';
            resStatus.style.background = 'rgba(239, 68, 68, 0.2)';
            resStatus.style.color = '#ef4444';
        } else {
            resSanction.textContent = formatCurrency(decision.max_sanction);
            resRate.textContent = `${decision.interest_rate}%`;
            resEmi.textContent = formatCurrency(decision.max_emi);
            resStatus.textContent = decision.status;
            resStatus.style.background = 'rgba(6, 182, 212, 0.2)';
            resStatus.style.color = '#06b6d4';
        }
    };

    const onInputChange = () => {
        tenureDisplay.textContent = `${inputs.tenure.value} Months`;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchSimulation, 300);
    };

    // Attach listeners
    Object.values(inputs).forEach(input => {
        if (input) input.addEventListener('input', onInputChange);
    });

    // Initial fetch
    fetchSimulation();
});
