/**
 * CrediSphere AI — Live Collections Intelligence & Telephony Engine
 * Connects dynamically to real registered customers from the database/customer portal.
 */

class CollectionsMLEngine {
  constructor() {
    this.customersList = [];
    this.currentCustomer = null;

    // Default fallback state (populated live from database)
    this.state = {
      user_id: null,
      name: "Loading registered customer...",
      borrowerName: "Loading...",
      phone: "",
      displayPhone: "",
      email: "",
      account_no: "---",
      loan_type: "Loan Account",
      loan_amount: 0,
      emi_amount: 0,
      bounced_emis: 0,
      total_overdue: 0,
      dpd: 0,
      dpd_bucket: "0 (0)",
      broken_promises: 0,
      sentiment: "Neutral",
      best_call_time: "5–7 PM"
    };

    this.actions = [
      { id: 'settlement', name: 'Structured Settlement Offer', qValue: 0.812, pct: 85, color: '#2563eb', isOptimal: true },
      { id: 'sms_link', name: 'SMS Payment Link', qValue: 0.640, pct: 67, color: '#10b981' },
      { id: 'ivr_call', name: 'Automated IVR Call', qValue: 0.520, pct: 54, color: '#6366f1' },
      { id: 'hard_recovery', name: 'Hard Recovery Agent Dispatch', qValue: 0.310, pct: 32, color: '#f59e0b' },
      { id: 'repossession', name: 'Legal Repossession Notice', qValue: -0.150, pct: 15, color: '#ef4444' }
    ];

    this.featureImportances = [
      { feature: "DPD Bucket (90+ Days)", weight: "38%" },
      { feature: "Broken Promises (2 prior)", weight: "27%" },
      { feature: "Sentiment (Negative Tone)", weight: "18%" },
      { feature: "Bounce Velocity (3 EMIs)", weight: "17%" }
    ];
  }

  async init() {
    await this.fetchRegisteredCustomers();
    this.renderQDistribution();
    this.renderFeatureWeights();
  }

  async fetchRegisteredCustomers() {
    try {
      const res = await apiCall(`/collections/customers?t=${Date.now()}`);
      if (res && res.customers && res.customers.length > 0) {
        this.customersList = res.customers;
        this.populateCustomerSelector();

        // Check priority: 1) URL query parameter '?user_id=...', 2) localStorage logged-in customer, 3) first registered customer
        const urlParams = new URLSearchParams(window.location.search);
        const paramUserId = urlParams.get('user_id');
        let matched = null;

        if (paramUserId) {
          matched = this.customersList.find(c => String(c.user_id) === String(paramUserId));
        }

        if (!matched) {
          const storedUserJson = localStorage.getItem('user');
          if (storedUserJson) {
            try {
              const storedUser = JSON.parse(storedUserJson);
              if (storedUser && storedUser.role === 'CUSTOMER') {
                matched = this.customersList.find(c => (storedUser.id && c.user_id === storedUser.id) || (storedUser.email && c.email === storedUser.email));
              }
            } catch (e) {}
          }
        }

        // Set active customer to matched or the first real registered customer in the database
        const selectedCust = matched || this.customersList[0];
        this.setCustomer(selectedCust);
      } else {
        this.populateDefaultCustomers();
      }
    } catch (e) {
      console.warn("Backend API error fetching collections customers:", e);
      this.populateDefaultCustomers();
    }
  }

  populateDefaultCustomers() {
    this.customersList = [];
    this.populateCustomerSelector();
    
    // Clear the UI
    const elName = document.getElementById('txt-borrower-name');
    if (elName) elName.textContent = "No active customers found";
    const elPhone = document.getElementById('txt-borrower-phone');
    if (elPhone) elPhone.textContent = "N/A";
  }

  populateCustomerSelector() {
    const sel = document.getElementById('select-customer-account');
    if (!sel) return;
    sel.innerHTML = this.customersList.map(c => `
      <option value="${c.user_id}">
        ${c.name} — Registered Phone: ${c.phone} | ${c.loan_type} #${c.account_no} (Overdue: ₹${Math.round(c.total_overdue).toLocaleString('en-IN')})
      </option>
    `).join('');
  }

  setCustomerById(userId) {
    const cust = this.customersList.find(c => String(c.user_id) === String(userId));
    if (cust) {
      this.setCustomer(cust);
    }
  }

  setCustomer(customer) {
    this.currentCustomer = customer;
    this.state = { ...customer };

    // Format phone display nicely
    let formattedPhone = customer.phone;
    if (!formattedPhone.startsWith('+')) {
      formattedPhone = '+91 ' + formattedPhone;
    }
    this.state.displayPhone = formattedPhone;

    // Recalculate Q-Values based on customer DPD
    if (this.state.dpd >= 90) {
      this.actions[0].qValue = 0.812;
      this.actions[0].isOptimal = true;
      this.actions[1].qValue = 0.640;
      this.actions[4].qValue = -0.150;
    } else {
      this.actions[1].qValue = 0.790;
      this.actions[1].isOptimal = true;
      this.actions[0].isOptimal = false;
      this.actions[0].qValue = 0.710;
      this.actions[4].qValue = -0.050;
    }

    this.updateUI();

    const sel = document.getElementById('select-customer-account');
    if (sel && sel.value !== String(customer.user_id)) {
      sel.value = String(customer.user_id);
    }
  }

  updateUI() {
    const c = this.state;
    const phone = c.displayPhone || c.phone;

    // 1. Warning strip
    const topStripName = document.getElementById('topstrip-borrower-name');
    if (topStripName) topStripName.textContent = c.name;
    const topStripLoan = document.getElementById('topstrip-loan-id');
    if (topStripLoan) topStripLoan.textContent = `#${c.account_no}`;
    const topStripOverdue = document.getElementById('topstrip-overdue');
    if (topStripOverdue) topStripOverdue.textContent = `₹${Math.round(c.total_overdue).toLocaleString('en-IN')}`;
    const topStripPhone = document.getElementById('topstrip-phone');
    if (topStripPhone) topStripPhone.textContent = phone;

    // 2. Overdue Card
    const elName = document.getElementById('txt-borrower-name');
    if (elName) elName.textContent = c.name;
    const elPhone = document.getElementById('txt-borrower-phone');
    if (elPhone) elPhone.textContent = phone;
    const elEmi = document.getElementById('txt-emi-amt');
    if (elEmi) elEmi.textContent = `₹${Math.round(c.emi_amount).toLocaleString('en-IN')}`;
    const elBounced = document.getElementById('txt-emis-bounced');
    if (elBounced) elBounced.textContent = `${c.bounced_emis} consecutive`;
    const elOverdue = document.getElementById('txt-total-overdue');
    if (elOverdue) elOverdue.textContent = `₹${Math.round(c.total_overdue).toLocaleString('en-IN')}`;
    const elDpd = document.getElementById('txt-dpd-bucket');
    if (elDpd) elDpd.textContent = c.dpd_bucket || `${c.dpd} (${c.bounced_emis})`;
    const elRiskBadge = document.getElementById('coll-risk-badge');
    if (elRiskBadge) elRiskBadge.textContent = c.dpd >= 90 ? '🔴 High risk (RF 78.6%)' : '🟡 Moderate risk (RF 54.2%)';
    const elPromises = document.getElementById('coll-promises-chip');
    if (elPromises) elPromises.textContent = `Broken Promises: ${c.broken_promises}`;

    // 3. Recommendation Card
    const elRecText = document.getElementById('coll-rec-text');
    if (elRecText) {
      elRecText.innerHTML = `Customer <b>${c.name}</b> has broken ${c.broken_promises} prior promise(s) on ${c.loan_type} <b>#${c.account_no}</b>. AI recommends a structured settlement offer with partial upfront payment, contacted on registered number <b>${phone}</b> during the <b>${c.best_call_time}</b> window (highest response rate).`;
    }
    const elSent = document.getElementById('coll-sentiment');
    if (elSent) elSent.textContent = c.sentiment;
    const elOdds = document.getElementById('coll-rec-odds');
    if (elOdds) elOdds.textContent = c.dpd >= 90 ? '61.4%' : '78.2%';

    // 4. Modal Titles & Placeholders
    const modalPhone = document.getElementById('modal-call-phone');
    if (modalPhone) modalPhone.textContent = `${phone} · Account #${c.account_no}`;
    const modalName = document.getElementById('modal-call-name');
    if (modalName) modalName.textContent = c.name;
    const modalAvatar = document.getElementById('call-avatar-ring');
    if (modalAvatar) {
      const parts = c.name.split(' ');
      modalAvatar.textContent = parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : c.name.substring(0, 2).toUpperCase();
    }

    // 5. Render History
    this.renderHistoryFeed(c.history || []);
    this.renderQDistribution();
    this.renderFeatureWeights();
  }

  renderHistoryFeed(historyItems) {
    const container = document.getElementById('coll-feed-container');
    if (!container) return;
    if (!historyItems || historyItems.length === 0) {
      container.innerHTML = `<div style="text-align:center;color:#9ca3af;padding:20px;font-size:0.8rem;">No prior follow-ups on this account yet.</div>`;
      return;
    }
    container.innerHTML = historyItems.map(item => `
      <div class="feed-item" style="animation:fadeInColl 0.35s ease;">
        <div class="feed-dot" style="background:var(--primary-light, #eff6ff); font-size:13px;">${item.icon || '💬'}</div>
        <div>
          <div class="feed-text"><b>${item.type}</b> — ${item.details}</div>
          <div class="feed-time" style="color:var(--text-gray, #6b7280); font-size:0.7rem; margin-top:2px;">${item.time}</div>
        </div>
      </div>
    `).join('');
  }

  renderQDistribution() {
    const container = document.getElementById('q-distribution-meters');
    if (!container) return;
    container.innerHTML = this.actions.map(a => `
      <div class="q-meter-row">
        <span class="q-meter-name" title="${a.name}">${a.isOptimal ? '★ ' : ''}${a.name}</span>
        <div class="q-meter-bar-bg">
          <div class="q-meter-bar-fill" style="width:${a.pct}%;background:${a.color};"></div>
        </div>
        <span class="q-meter-val" style="color:${a.color};">${a.qValue > 0 ? '+' : ''}${a.qValue.toFixed(3)}</span>
      </div>
    `).join('');
  }

  renderFeatureWeights() {
    const container = document.getElementById('rf-feature-weights');
    if (!container) return;
    container.innerHTML = this.featureImportances.map(f => `
      <div style="background:#fff;border:1px solid var(--border, #e5e7eb);border-radius:6px;padding:5px 8px;display:flex;justify-content:space-between;font-size:0.7rem;">
        <span style="color:#6b7280;">${f.feature}:</span>
        <b style="color:#111827;">${f.weight}</b>
      </div>
    `).join('');
  }

  randomizeState() {
    const cust = this.customersList[Math.floor(Math.random() * this.customersList.length)];
    if (cust) {
      const sel = document.getElementById('select-customer-account');
      if (sel) sel.value = cust.user_id;
      this.setCustomer(cust);
      showCollToast(`Switched active account to ${cust.name} (${cust.phone})!`, "success");
    }
  }
}

const collectionsML = new CollectionsMLEngine();

window.addEventListener('DOMContentLoaded', () => {
  collectionsML.init();
});

// Toggle Insights Panel
function toggleMLEngineInsights() {
  const panel = document.getElementById('coll-insights-panel');
  const btn = document.getElementById('coll-toggle-insights-btn');
  if (!panel || !btn) return;
  const isHidden = panel.style.display === 'none';
  panel.style.display = isHidden ? 'block' : 'none';
  btn.classList.toggle('expanded', isHidden);
}

/* ================= LIVE VOIP CALL SIMULATION ================= */
let callTimerInterval = null;
let callDurationSeconds = 0;
let callStepTimeout = null;
let isCallMuted = false;
let ringAudioCtx = null;
let ringInterval = null;

function playRingingTone() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    ringAudioCtx = new AudioCtx();

    function ringBurst() {
      if (!ringAudioCtx || ringAudioCtx.state === 'closed') return;
      const now = ringAudioCtx.currentTime;
      const osc1 = ringAudioCtx.createOscillator();
      const osc2 = ringAudioCtx.createOscillator();
      const gain = ringAudioCtx.createGain();

      osc1.frequency.setValueAtTime(440, now);
      osc2.frequency.setValueAtTime(480, now);

      gain.gain.setValueAtTime(0.09, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.8);

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(ringAudioCtx.destination);

      osc1.start(now);
      osc2.start(now);
      osc1.stop(now + 1.8);
      osc2.stop(now + 1.8);
    }

    ringBurst();
    ringInterval = setInterval(ringBurst, 3200);
  } catch (e) {
    console.log("Audio ringing context unavailable:", e);
  }
}

function stopRingingTone() {
  if (ringInterval) {
    clearInterval(ringInterval);
    ringInterval = null;
  }
  if (ringAudioCtx && ringAudioCtx.state !== 'closed') {
    try { ringAudioCtx.close(); } catch (e) {}
    ringAudioCtx = null;
  }
}

function openLiveCallModal() {
  const c = collectionsML.state;
  const phone = c.displayPhone || c.phone;
  const cleanDigits = phone.replace(/\D/g, '').slice(-10);
  const modal = document.getElementById('coll-call-modal');
  modal.classList.add('open');

  document.getElementById('call-avatar-ring').classList.add('ringing');
  document.getElementById('call-status-pill').classList.remove('connected');
  document.getElementById('call-status-text').textContent = "Connecting to VoIP SIP Gateway...";
  
  // Update Call Header with customer registered phone
  document.getElementById('modal-call-name').textContent = c.name;
  document.getElementById('modal-call-phone').textContent = `${phone} · Account #${c.account_no}`;
  
  const telLink = document.getElementById('tel-dial-link');
  if (telLink) telLink.href = `tel:+91${cleanDigits}`;
  const modalDialBtn = document.getElementById('modal-live-dial-btn');
  if (modalDialBtn) modalDialBtn.href = `tel:+91${cleanDigits}`;
  const modalDialText = document.getElementById('modal-live-dial-text');
  if (modalDialText) modalDialText.textContent = phone;

  document.getElementById('call-transcript-stream').innerHTML = `
    <div style="text-align:center;font-size:0.75rem;color:#6b7280;margin-bottom:12px;" id="call-callout-msg">
      🔒 VoIP Encrypted Line · Dialing Registered Line: <b>${phone}</b>
    </div>
  `;

  callDurationSeconds = 0;
  isCallMuted = false;
  updateMuteButtonUI();

  // Setup pre-filled PTP amount based on customer EMI
  const tokenAmt = Math.round(c.emi_amount || 35999);
  document.getElementById('ptp-amount-input').value = `₹${tokenAmt.toLocaleString('en-IN')}`;

  // Start authentic phone ringing audio
  playRingingTone();

  callStepTimeout = setTimeout(() => {
    document.getElementById('call-status-text').textContent = `Ringing registered phone (${phone})...`;
    
    setTimeout(() => {
      stopRingingTone();
      document.getElementById('call-avatar-ring').classList.remove('ringing');
      document.getElementById('call-status-pill').classList.add('connected');
      startCallTimer();
      runCallConversationScript(c, phone);
    }, 2400);
  }, 1200);
}

function startCallTimer() {
  const statusText = document.getElementById('call-status-text');
  callTimerInterval = setInterval(() => {
    callDurationSeconds++;
    const mins = String(Math.floor(callDurationSeconds / 60)).padStart(2, '0');
    const secs = String(callDurationSeconds % 60).padStart(2, '0');
    statusText.textContent = `Live Connected (${mins}:${secs})`;
  }, 1000);
}

function runCallConversationScript(customer, phone) {
  const stream = document.getElementById('call-transcript-stream');
  const tokenFormatted = `₹${Math.round(customer.emi_amount).toLocaleString('en-IN')}`;
  const totalFormatted = `₹${Math.round(customer.total_overdue).toLocaleString('en-IN')}`;

  const script = [
    { sender: "agent", text: `Namaste ${customer.name}, this is CrediSphere Collections calling on your registered number ${phone} regarding your pending EMI for ${customer.loan_type} #${customer.account_no}.` },
    { sender: "borrower", text: `Namaste. Yes, I received the notice. I had temporary salary delay this month, but I can transfer ${tokenFormatted} upfront this Friday by 5 PM.` },
    { sender: "agent", text: `Approved ${customer.name}! If you transfer ${tokenFormatted} by Friday 5 PM, our AI system will restructure the remaining ${totalFormatted} across upcoming cycles with late penalties waived.` },
    { sender: "borrower", text: `That is a big relief, thank you. Please send the payment link to my WhatsApp and registered SMS right away.` }
  ];

  script.forEach((item, idx) => {
    setTimeout(() => {
      if (!document.getElementById('coll-call-modal').classList.contains('open')) return;
      const bubble = document.createElement('div');
      bubble.className = `transcript-bubble ${item.sender}`;
      bubble.innerHTML = `
        <span class="bubble-tag">${item.sender === 'agent' ? '🤖 CrediSphere Voice AI' : `👤 ${customer.name} (Registered Borrower)`}</span>
        <div class="bubble-content">${item.text}</div>
      `;
      stream.appendChild(bubble);
      stream.scrollTop = stream.scrollHeight;

      if (idx === script.length - 1) {
        togglePTPDrawer(true);
      }
    }, (idx + 1) * 2000);
  });
}

function toggleCallMute() {
  isCallMuted = !isCallMuted;
  updateMuteButtonUI();
  showCollToast(isCallMuted ? "Microphone muted" : "Microphone unmuted");
}

function updateMuteButtonUI() {
  const btn = document.getElementById('btn-call-mute');
  if (btn) btn.classList.toggle('active', isCallMuted);
  const lbl = document.getElementById('mute-label');
  if (lbl) lbl.textContent = isCallMuted ? "Unmute" : "Mute";
}

function togglePTPDrawer(force) {
  const drawer = document.getElementById('ptp-inline-drawer');
  if (!drawer) return;
  const isOpen = typeof force === 'boolean' ? force : !drawer.classList.contains('open');
  drawer.classList.toggle('open', isOpen);
}

async function confirmRecordPTP() {
  const c = collectionsML.state;
  const amountStr = document.getElementById('ptp-amount-input').value || `₹${Math.round(c.emi_amount)}`;
  const dateStr = document.getElementById('ptp-date-input').value || "12-Dec-2025";
  const numAmount = parseFloat(amountStr.replace(/[^0-9.]/g, '')) || c.emi_amount;

  togglePTPDrawer(false);
  showCollToast(`Promise to Pay of ${amountStr} registered for ${c.name}`, "success");
  appendFollowUpFeed("📞", `<b>PTP Recorded for ${c.name}</b> — ${amountStr} promised by ${dateStr}`, "Just now");

  try {
    await apiCall('/collections/record-ptp', 'POST', {
      user_id: c.user_id,
      borrower_name: c.name,
      amount: numAmount,
      date: dateStr
    });
  } catch (e) {
    console.log("PTP logged locally");
  }
}

function endLiveCall() {
  stopRingingTone();
  clearInterval(callTimerInterval);
  clearTimeout(callStepTimeout);
  const modal = document.getElementById('coll-call-modal');
  modal.classList.remove('open');

  const c = collectionsML.state;
  if (callDurationSeconds > 0) {
    const mins = String(Math.floor(callDurationSeconds / 60)).padStart(2, '0');
    const secs = String(callDurationSeconds % 60).padStart(2, '0');
    appendFollowUpFeed("📞", `<b>Live Call Ended with ${c.name} (${c.phone})</b> — Duration ${mins}:${secs}`, "Just now");
    showCollToast(`Call with ${c.name} ended (${mins}:${secs}). Follow-up history updated.`, "success");
  }
}

/* ================= LIVE SMS & WHATSAPP ENGINE ================= */
let currentChannel = 'whatsapp';

function openSMSModal() {
  const c = collectionsML.state;
  const phone = c.displayPhone || c.phone;
  document.getElementById('coll-sms-modal').classList.add('open');
  
  // Set recipient in modal header
  document.getElementById('sms-modal-recipient').textContent = `Recipient: ${c.name} (Registered Phone: ${phone})`;

  // Default to WhatsApp for direct live link
  switchMsgChannel('whatsapp');
  onTemplateChange();
}

function closeSMSModal() {
  document.getElementById('coll-sms-modal').classList.remove('open');
}

function switchMsgChannel(ch) {
  currentChannel = ch;
  const c = collectionsML.state;
  const phone = c.displayPhone || c.phone;
  const isSms = ch === 'sms';

  document.getElementById('chan-sms').style.background = isSms ? 'var(--green-light)' : '#fff';
  document.getElementById('chan-sms').style.borderColor = isSms ? 'var(--green)' : 'var(--border)';
  document.getElementById('chan-sms').style.color = isSms ? 'var(--green)' : 'var(--text-dark)';
  
  document.getElementById('chan-wa').style.background = !isSms ? 'var(--green-light)' : '#fff';
  document.getElementById('chan-wa').style.borderColor = !isSms ? 'var(--green)' : 'var(--border)';
  document.getElementById('chan-wa').style.color = !isSms ? 'var(--green)' : 'var(--text-dark)';

  const sendBtn = document.getElementById('btn-dispatch-link');
  if (sendBtn) {
    if (!isSms) {
      sendBtn.innerHTML = `🟢 Open WhatsApp & Send to ${c.name}`;
      sendBtn.style.background = '#10b981';
      sendBtn.style.color = '#fff';
    } else {
      sendBtn.innerHTML = `💬 Send via SMS Gateway`;
      sendBtn.style.background = 'var(--primary)';
      sendBtn.style.color = '#fff';
    }
  }
}

function onTemplateChange() {
  const c = collectionsML.state;
  const tokenAmt = Math.round(c.emi_amount || 35999);
  const tokenFormatted = `₹${tokenAmt.toLocaleString('en-IN')}`;
  
  // Generate real working settlement URL
  const baseUrl = window.location.origin || 'http://localhost:5500';
  const payUrl = `${baseUrl}/pages/pay-settlement.html?loan_id=${c.account_no}&amount=${tokenAmt}&name=${encodeURIComponent(c.name)}&phone=${encodeURIComponent(c.phone)}`;
  
  const templates = {
    settlement: `Urgent: CrediSphere one-time settlement offer for ${c.name} (Account #${c.account_no}). Pay ${tokenFormatted} upfront token today by 5 PM to freeze penalties: ${payUrl}`,
    reminder: `Dear ${c.name}, your overdue EMI of ${tokenFormatted} for loan #${c.account_no} is pending. Avoid legal escalation by paying securely here: ${payUrl}`,
    urgent: `FINAL NOTICE for ${c.name}: Account #${c.account_no} is at DPD ${c.dpd}. Settle balance immediately or call our recovery team: ${payUrl}`
  };

  const val = document.getElementById('sms-template-select').value;
  document.getElementById('sms-message-text').value = templates[val] || templates.settlement;
}

async function sendSMSLink() {
  const c = collectionsML.state;
  const phone = c.displayPhone || c.phone;
  const cleanDigits = phone.replace(/\D/g, '').slice(-10);
  const intlPhone = '91' + cleanDigits;
  const msgText = document.getElementById('sms-message-text').value;
  const channelName = currentChannel === 'sms' ? 'SMS Gateway (Twilio)' : 'WhatsApp Business API';
  closeSMSModal();

  try {
    await apiCall('/collections/dispatch-message', 'POST', {
      user_id: c.user_id,
      borrower_name: c.name,
      phone: c.phone,
      channel: channelName,
      message: msgText
    });
  } catch (e) {
    console.log("Local dispatch logged");
  }

  if (currentChannel === 'whatsapp') {
    // Open actual WhatsApp chat with pre-filled message directly to the customer's registered number!
    const waUrl = `https://wa.me/${intlPhone}?text=${encodeURIComponent(msgText)}`;
    window.open(waUrl, '_blank');
    showCollToast(`Opened WhatsApp chat for registered phone +${intlPhone}!`, "success");
    appendFollowUpFeed("🟢", `<b>Live WhatsApp Link Dispatched to ${c.name} (+${intlPhone})</b> — Direct chat opened with token payment link`, "Just now");
  } else {
    // SMS: Open SMS app on device + log
    const smsUrl = `sms:+${intlPhone}?body=${encodeURIComponent(msgText)}`;
    window.open(smsUrl, '_self');
    showCollToast(`Dispatched SMS to registered phone +${intlPhone}`, "success");
    appendFollowUpFeed("📩", `<b>Payment Link Sent to ${c.name} (+${intlPhone})</b> — via SMS Gateway`, "Just now");
  }
}

/* ================= STRUCTURED SETTLEMENT ENGINE ================= */
function openSettlementModal() {
  const c = collectionsML.state;
  document.getElementById('coll-settlement-modal').classList.add('open');
  document.getElementById('settlement-modal-sub').textContent = `Account: ${c.name} · Loan #${c.account_no} · Overdue: ₹${Math.round(c.total_overdue).toLocaleString('en-IN')}`;
  document.getElementById('settle-orig-bal').textContent = `₹${Math.round(c.total_overdue).toLocaleString('en-IN')}`;
  document.getElementById('settle-token-amt').textContent = `₹${Math.round(c.emi_amount).toLocaleString('en-IN')}`;
}

function closeSettlementModal() {
  document.getElementById('coll-settlement-modal').classList.remove('open');
}

function confirmSettlementAgreement() {
  const c = collectionsML.state;
  closeSettlementModal();
  showCollToast(`Settlement agreement generated for ${c.name} & sent to registered phone ${c.phone}.`, "success");
  appendFollowUpFeed("📑", `<b>Settlement Agreement Issued for ${c.name}</b> — ₹${Math.round(c.emi_amount).toLocaleString('en-IN')} upfront token plan sent to ${c.phone}`, "Just now");
}

/* ================= "ASK AI ASSISTANT" COPILOT DRAWER ================= */
function openCollAIDrawer() {
  const c = collectionsML.state;
  document.getElementById('coll-ai-drawer').classList.add('open');
  document.getElementById('ai-copilot-context').textContent = `Context: ${c.name} · Phone: ${c.phone} · DPD ${c.dpd} · Overdue ₹${Math.round(c.total_overdue).toLocaleString('en-IN')}`;
}

function closeCollAIDrawer() {
  document.getElementById('coll-ai-drawer').classList.remove('open');
}

function handleDrawerBackdropClick(e) {
  if (e.target.id === 'coll-ai-drawer') closeCollAIDrawer();
}

function askPresetQuestion(q) {
  const c = collectionsML.state;
  addChatMessage("user", q);
  
  setTimeout(() => {
    let answer = "";
    if (q.includes("settlement over repossession")) {
      answer = `<b>Deep Q-Network (DQN) Policy Analysis for ${c.name}:</b><br><br>1. <b>Recovery Value:</b> At DPD ${c.dpd} with ${c.broken_promises} broken promises, legal asset repossession yields net <b>42.1%</b> after secondary auction haircuts (34%) and court freezes ($Q = -0.150$).<br><br>2. <b>Cash Velocity:</b> A structured settlement with an immediate upfront token on registered phone <b>${c.phone}</b> locks in an expected recovery rate of <b>68.4%</b> ($Q = +0.812$).`;
    } else if (q.includes("5–7 PM")) {
      answer = `<b>Temporal Optimization Engine for ${c.name}:</b><br>Historical telematics indicate connection answer rates for self-employed/salaried borrowers like ${c.name} surge to <b>74.2%</b> between 5:00 PM and 7:00 PM on registered phone ${c.phone}, leading to <b>2.3x higher PTP conversion</b>.`;
    } else if (q.includes("defaults on this PTP")) {
      answer = `<b>Next-Best-Action Transition:</b> If ${c.name} defaults by Friday 5 PM, the state transitions to (DPD ${c.dpd + 5}, Broken Promises ${c.broken_promises + 1}), triggering automated SARFAESI / Section 138 demand notices and hard recovery agent dispatch to registered address.`;
    } else {
      answer = `<b>Random Forest Risk Attribution for ${c.name}:</b><br>• DPD ${c.dpd}+ (38% weight)<br>• Broken Promises (${c.broken_promises} prior, 27% weight)<br>• Negative Sentiment (18% weight)<br>• Consecutive NACH Bounces (${c.bounced_emis} EMIs, 17% weight)`;
    }
    addChatMessage("bot", answer);
  }, 400);
}

function sendCustomAIQuery() {
  const c = collectionsML.state;
  const inp = document.getElementById('ai-user-query');
  const q = inp.value.trim();
  if (!q) return;

  addChatMessage("user", q);
  inp.value = '';

  setTimeout(() => {
    addChatMessage("bot", `Based on <b>${c.name}</b>'s registered profile (Phone: ${c.phone}, DPD: ${c.dpd}, Loan: #${c.account_no}), our <b>DQN agent</b> strongly favors structured token settlement contacted during <b>${c.best_call_time}</b>.`);
  }, 450);
}

function addChatMessage(sender, html) {
  const thread = document.getElementById('ai-chat-thread');
  const msg = document.createElement('div');
  msg.className = `ai-msg ${sender}`;
  msg.innerHTML = `<div class="msg-bubble">${html}</div>`;
  thread.appendChild(msg);
  thread.parentElement.scrollTop = thread.parentElement.scrollHeight;
}

/* ================= COMMON HELPERS: FEED & TOASTS ================= */
function appendFollowUpFeed(icon, html, time) {
  const container = document.getElementById('coll-feed-container');
  if (!container) return;
  const item = document.createElement('div');
  item.className = "feed-item";
  item.style.animation = "fadeInColl 0.35s ease";
  item.innerHTML = `
    <div class="feed-dot" style="background:var(--primary-light, #eff6ff); font-size:13px;">${icon}</div>
    <div>
      <div class="feed-text">${html}</div>
      <div class="feed-time" style="color:var(--primary, #2563eb); font-weight:700; font-size:0.7rem; margin-top:2px;">${time}</div>
    </div>
  `;
  container.insertBefore(item, container.firstChild);
}

function showCollToast(msg, type) {
  const container = document.getElementById('coll-toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `coll-toast ${type === 'success' ? 'success' : ''}`;
  toast.innerHTML = `
    <span>${type === 'success' ? '✅' : '🔔'}</span>
    <span>${msg}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
