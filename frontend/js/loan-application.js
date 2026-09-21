document.addEventListener('DOMContentLoaded', () => {
    // 1. Session Verification
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const user = JSON.parse(userStr);
        document.getElementById('user-greeting').textContent = `Applying as ${user.name}`;
        document.getElementById('user-avatar').textContent = user.name.charAt(0).toUpperCase();
    } catch (e) {
        console.error("Invalid user session", e);
    }

    // 2. Live AI Pre-Check (DTI Calculator)
    const incomeInput = document.getElementById('income');
    const emiInput = document.getElementById('emi');
    const dtiBar = document.getElementById('live-dti-bar');
    const dtiText = document.getElementById('live-dti-text');
    const dtiStatus = document.getElementById('live-dti-status');

    const updateDTI = () => {
        const income = parseFloat(incomeInput.value) || 0;
        const emi = parseFloat(emiInput.value) || 0;
        
        let dti = 0;
        if (income > 0) {
            dti = (emi / income) * 100;
        }

        dtiText.textContent = `${dti.toFixed(1)}%`;
        
        // Clamp for UI bar
        const clampedDti = Math.min(100, Math.max(0, dti));
        dtiBar.style.width = `${clampedDti}%`;

        // Color coding
        if (dti > 60) {
            dtiBar.style.backgroundColor = '#ef4444'; // Red
            dtiStatus.textContent = 'High Risk (Likely Reject)';
            dtiStatus.style.color = '#ef4444';
        } else if (dti > 45) {
            dtiBar.style.backgroundColor = '#f59e0b'; // Amber
            dtiStatus.textContent = 'Borderline (Needs Review)';
            dtiStatus.style.color = '#f59e0b';
        } else if (dti > 0) {
            dtiBar.style.backgroundColor = '#10b981'; // Green
            dtiStatus.textContent = 'Healthy';
            dtiStatus.style.color = '#10b981';
        } else {
            dtiBar.style.width = '0%';
            dtiStatus.textContent = 'Awaiting input';
            dtiStatus.style.color = '#64748b';
        }
    };

    incomeInput.addEventListener('input', updateDTI);
    emiInput.addEventListener('input', updateDTI);

    // 3. Multi-Step Navigation
    const stepFinancials = document.getElementById('step-financials');
    const stepDocuments = document.getElementById('step-documents');
    const stepAiReview = document.getElementById('step-ai-review');
    
    const steps = document.querySelectorAll('.step');
    
    document.getElementById('btn-to-docs').addEventListener('click', () => {
        // Validate required fields roughly
        if (!incomeInput.value || !emiInput.value || !document.getElementById('amount').value) {
            alert("Please fill in all required financial details.");
            return;
        }
        stepFinancials.style.display = 'none';
        stepDocuments.style.display = 'block';
        steps[1].classList.remove('active');
        steps[1].classList.add('completed');
        steps[2].classList.add('active');
    });

    // Auto-formatting and file attachment listeners
    const panInput = document.getElementById('pan-number-input');
    if (panInput) {
        // Pre-fill if Devender Sharma or logged in user
        const userObj = JSON.parse(userStr || '{}');
        if (userObj.name && userObj.name.toLowerCase().includes('devender')) {
            panInput.value = 'ABCPS8810D';
        } else if (userObj.name && userObj.name.toLowerCase().includes('vrinda')) {
            panInput.value = 'VRIND1234V';
        }
        panInput.addEventListener('input', () => {
            panInput.value = panInput.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    }

    const aadhaarInput = document.getElementById('aadhaar-number-input');
    if (aadhaarInput) {
        const userObj = JSON.parse(userStr || '{}');
        if (userObj.name && userObj.name.toLowerCase().includes('devender')) {
            aadhaarInput.value = '5489 1245 8810';
        } else if (userObj.name && userObj.name.toLowerCase().includes('vrinda')) {
            aadhaarInput.value = '7812 3456 9012';
        }
        aadhaarInput.addEventListener('input', () => {
            let digits = aadhaarInput.value.replace(/\D/g, '').slice(0, 12);
            let formatted = digits.replace(/(\d{4})(?=\d)/g, '$1 ');
            aadhaarInput.value = formatted;
        });
    }

    const setupFileDisplay = (inputId, statusId, hintId) => {
        const fInput = document.getElementById(inputId);
        const fStatus = document.getElementById(statusId);
        const fHint = document.getElementById(hintId);
        if (fInput && fStatus) {
            fInput.addEventListener('change', () => {
                if (fInput.files && fInput.files[0]) {
                    const fName = fInput.files[0].name;
                    fStatus.style.display = 'inline-block';
                    fStatus.textContent = `✓ ${fName}`;
                    if (fHint) fHint.textContent = `Ready for AI KYC OCR verification (${(fInput.files[0].size/1024).toFixed(1)} KB)`;
                }
            });
        }
    };
    setupFileDisplay('pan-file-input', 'pan-file-status', 'pan-file-hint');
    setupFileDisplay('aadhaar-file-input', 'aadhaar-file-status', 'aadhaar-file-hint');
    setupFileDisplay('income-file-input', 'income-file-status', 'income-file-hint');
    
    document.getElementById('btn-back-financials').addEventListener('click', () => {
        stepDocuments.style.display = 'none';
        stepFinancials.style.display = 'block';
        steps[2].classList.remove('active');
        steps[1].classList.remove('completed');
        steps[1].classList.add('active');
    });

    // 4. Form Submission & AI Review Step
    const btnSubmitFinal = document.getElementById('btn-submit-final');
    
    btnSubmitFinal.addEventListener('click', async () => {
        const panVal = document.getElementById('pan-number-input')?.value.trim() || 'ABCPS8810D';
        const aadhaarVal = document.getElementById('aadhaar-number-input')?.value.trim() || '5489 1245 8810';

        const panFile = document.getElementById('pan-file-input')?.files[0]?.name || `pan_card_${panVal}.pdf`;
        const aadhaarFile = document.getElementById('aadhaar-file-input')?.files[0]?.name || `aadhaar_card_${aadhaarVal.replace(/\s+/g,'_')}.pdf`;
        const incomeFile = document.getElementById('income-file-input')?.files[0]?.name || 'salary_slips_3months.pdf';

        const payload = {
            loan_type: document.getElementById('loanType').value,
            amount: document.getElementById('amount').value,
            term_months: document.getElementById('tenure').value,
            income: document.getElementById('income').value,
            employment_type: document.getElementById('employment').value,
            existing_emi: document.getElementById('emi').value,
            purpose: document.getElementById('purpose').value,
            pan_number: panVal,
            aadhaar_number: aadhaarVal,
            id_document_name: aadhaarFile,
            income_document_name: incomeFile
        };
        
        // Transition to Step 4
        stepDocuments.style.display = 'none';
        stepAiReview.style.display = 'block';
        steps[2].classList.remove('active');
        steps[2].classList.add('completed');
        steps[3].classList.add('active');
        
        try {
            const response = await apiCall('/loans/apply', 'POST', payload);
            
            // Artificial delay for dramatic effect of "AI Processing"
            setTimeout(() => {
                document.getElementById('ai-processing').style.display = 'none';
                document.getElementById('ai-result').style.display = 'block';
                steps[3].classList.remove('active');
                steps[3].classList.add('completed');
                
                const dec = response.ai_decision || {};
                const formatCurrency = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

                const requestedAmt = parseFloat(payload.amount) || 500000;
                const emiAmt = response.emi || Math.round(requestedAmt * 0.032);
                const rateVal = response.interest_rate || 10.5;
                const appRef = response.loan_id ? `APP-2024-${String(response.loan_id).padStart(4, '0')}` : 'APP-2024-0010';

                const acctPill = document.getElementById('result-acct-pill');
                if (acctPill) acctPill.textContent = appRef;

                document.getElementById('final-sanction').textContent = formatCurrency(requestedAmt);
                document.getElementById('final-emi').textContent = formatCurrency(emiAmt);
                document.getElementById('final-rate').textContent = `${Number(rateVal).toFixed(2)}% p.a.`;
                const scoreEl = document.getElementById('final-score');
                if (scoreEl) scoreEl.textContent = `${dec.score || 780} / 900`;

                // Show SMS Toast if simulated
                if (dec.sms_sent) {
                    setTimeout(() => {
                        const toast = document.getElementById('sms-toast');
                        toast.querySelector('h4').textContent = 'SMS Dispatched';
                        toast.querySelector('p').textContent = 'Your application notice has been sent to your registered mobile.';
                        toast.style.borderLeft = '5px solid #10b981';
                        toast.classList.add('show');
                        setTimeout(() => { toast.classList.remove('show'); }, 6000);
                    }, 500);
                }
            }, 1800);
        } catch (err) {
            document.getElementById('ai-processing').innerHTML = `<h2 style="color:#ef4444;">Error Processing Application</h2><p>${err.message}</p>`;
        }
    });
});
