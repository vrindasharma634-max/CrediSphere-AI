#!/usr/bin/env python3
import re
import os

SOURCE_PATH = "/Users/vrindasharma/Desktop/CREDISPEHERAI-PROJECT/prototype.html.bak"

with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ADD CSS STYLES
css_styles = """
/* ============ COLLECTIONS AI ENGINE & LIVE TELEPHONY STYLES ============ */
#collections-ai-view {
  animation: fadeInColl 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  display: block;
}
@keyframes fadeInColl {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Status Chips & Metrics */
.coll-chip-wrap { display: flex; gap: 8px; align-items: center; margin-top: 10px; flex-wrap: wrap; }
.coll-subchip { font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 6px; background: var(--surface-2); border: 1px solid var(--border); color: var(--muted); }
.coll-subchip.danger { background: var(--red-light); color: var(--red); border-color: rgba(224,49,49,0.2); }
.coll-subchip.warning { background: var(--amber-light); color: var(--amber); border-color: rgba(217,119,6,0.2); }

/* AI Engine Insights Toggle & Panel */
.ai-engine-btn {
  display: inline-flex; align-items: center; gap: 6px;
  background: linear-gradient(135deg, rgba(124,92,255,0.1), rgba(47,95,255,0.1));
  border: 1px solid rgba(124,92,255,0.3); color: var(--purple);
  font-size: 11.5px; font-weight: 700; padding: 6px 14px; border-radius: 20px;
  cursor: pointer; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.ai-engine-btn:hover { background: var(--purple); color: #fff; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(124,92,255,0.25); }
.ai-engine-btn .chevron-icon { transition: transform 0.2s ease; font-size: 10px; }
.ai-engine-btn.expanded .chevron-icon { transform: rotate(180deg); }

.coll-insights-panel {
  display: block; margin-top: 16px; padding: 16px;
  background: linear-gradient(180deg, #f8faff, #ffffff);
  border: 1.5px solid rgba(47,95,255,0.22); border-radius: 12px;
  box-shadow: 0 4px 16px rgba(47,95,255,0.06);
  animation: fadeInColl 0.25s ease;
}
.coll-insights-title {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 12px; font-weight: 800; color: var(--navy); margin-bottom: 10px;
  padding-bottom: 8px; border-bottom: 1px dashed var(--border);
}
.coll-model-pipeline {
  display: flex; align-items: center; gap: 8px; font-size: 11px;
  background: rgba(47,95,255,0.06); padding: 6px 10px; border-radius: 8px;
  color: var(--blue); font-weight: 700; margin-bottom: 12px;
}
.coll-stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 14px; }
.coll-stat-box { background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 8px 10px; text-align: center; }
.coll-stat-box span { font-size: 10px; color: var(--muted); font-weight: 600; display: block; margin-bottom: 2px; }
.coll-stat-box b { font-size: 13px; font-family: 'DM Mono', monospace; color: var(--navy); }

/* Q-Value distribution meters */
.q-meter-wrap { margin-top: 8px; display: flex; flex-direction: column; gap: 7px; }
.q-meter-row { display: flex; align-items: center; justify-content: space-between; font-size: 11px; gap: 10px; }
.q-meter-name { width: 155px; font-weight: 600; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.q-meter-bar-bg { flex: 1; height: 7px; background: #e5e9f3; border-radius: 10px; overflow: hidden; position: relative; }
.q-meter-bar-fill { height: 100%; border-radius: 10px; transition: width 0.5s ease; }
.q-meter-val { width: 45px; text-align: right; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 11px; }

/* Action Hub Under Recovery Recommendation */
.coll-action-hub {
  margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--border);
}
.action-hub-label {
  font-size: 11px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--muted); margin-bottom: 10px;
  display: flex; align-items: center; gap: 6px;
}
.coll-action-buttons { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.coll-action-btn {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 12px 10px; border-radius: 10px; border: 1px solid transparent;
  cursor: pointer; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); text-align: center;
}
.coll-action-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(15,26,58,0.14); }
.coll-action-btn .btn-icon { font-size: 20px; margin-bottom: 4px; }
.coll-action-btn .btn-title { font-size: 12.5px; font-weight: 700; }
.coll-action-btn .btn-subtitle { font-size: 10px; opacity: 0.85; margin-top: 2px; }

.coll-action-btn.primary {
  background: linear-gradient(135deg, var(--navy), var(--blue)); color: #fff;
  box-shadow: 0 3px 10px rgba(47,95,255,0.28);
}
.coll-action-btn.secondary {
  background: linear-gradient(135deg, #10b981, #059669); color: #fff;
  box-shadow: 0 3px 10px rgba(16,185,129,0.28);
}
.coll-action-btn.outline {
  background: #fff; border-color: var(--border); color: var(--navy);
}
.coll-action-btn.outline:hover { background: var(--surface-2); border-color: var(--blue); }

/* Live Pill */
.live-pill {
  display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px;
  font-weight: 700; color: var(--green); background: var(--green-light);
  padding: 2px 8px; border-radius: 12px;
}

/* Modals & Backdrop */
.coll-modal-backdrop {
  position: fixed; inset: 0; background: rgba(14,26,58,0.72);
  backdrop-filter: blur(5px); z-index: 9000;
  display: none; align-items: center; justify-content: center;
  animation: fadeInColl 0.2s ease;
}
.coll-modal-backdrop.open { display: flex !important; }
.coll-modal-box {
  background: #fff; border-radius: 16px; width: 100%; max-width: 540px;
  box-shadow: 0 28px 72px rgba(0,0,0,0.32); border: 1px solid rgba(255,255,255,0.5);
  overflow: hidden; animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  margin: 16px; position: relative;
}
@keyframes modalPop {
  from { opacity: 0; transform: scale(0.94); }
  to { opacity: 1; transform: scale(1); }
}

/* VoIP Call Modal Specifics */
.call-modal-header {
  background: linear-gradient(135deg, #091124, #122244); color: #fff;
  padding: 26px 24px 22px; text-align: center; position: relative;
}
.call-avatar-ring {
  width: 72px; height: 72px; border-radius: 50%; margin: 0 auto 12px;
  background: linear-gradient(135deg, var(--teal), var(--blue));
  display: flex; align-items: center; justify-content: center;
  font-size: 26px; font-weight: 800; color: #fff; position: relative;
}
.call-avatar-ring.ringing::after {
  content: ''; position: absolute; inset: -8px; border-radius: 50%;
  border: 2px solid rgba(14,163,148,0.6); animation: ringPulse 1.2s infinite;
}
@keyframes ringPulse { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(1.35); opacity: 0; } }

.call-borrower-name { font-size: 18px; font-weight: 800; margin-bottom: 3px; }
.call-borrower-num { font-size: 12px; color: rgba(255,255,255,0.75); font-family: 'DM Mono', monospace; }
.call-status-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 700;
  margin-top: 10px; background: rgba(255,255,255,0.12); color: #fff;
}
.call-status-pill.connected { background: rgba(23,163,74,0.28); color: #4ade80; border: 1px solid rgba(74,222,128,0.35); }

.call-body { padding: 18px 22px; max-height: 240px; overflow-y: auto; background: var(--surface-2); }
.transcript-bubble {
  margin-bottom: 12px; display: flex; flex-direction: column; animation: fadeInColl 0.3s ease;
}
.transcript-bubble.agent { align-items: flex-end; }
.transcript-bubble.borrower { align-items: flex-start; }
.bubble-tag { font-size: 10.5px; font-weight: 700; color: var(--muted); margin-bottom: 3px; }
.bubble-content {
  max-width: 82%; padding: 10px 14px; border-radius: 12px; font-size: 12.5px; line-height: 1.48;
}
.transcript-bubble.agent .bubble-content { background: var(--navy); color: #fff; border-bottom-right-radius: 2px; }
.transcript-bubble.borrower .bubble-content { background: #fff; border: 1px solid var(--border); color: var(--ink); border-bottom-left-radius: 2px; }

/* Call Actions Bar */
.call-controls-bar {
  display: flex; align-items: center; justify-content: space-around;
  padding: 16px 20px; background: #fff; border-top: 1px solid var(--border);
}
.ctrl-btn {
  display: flex; flex-direction: column; align-items: center; gap: 4px;
  background: none; border: none; font-size: 11px; font-weight: 700; color: var(--ink);
  cursor: pointer; transition: transform 0.15s;
}
.ctrl-btn:hover { transform: scale(1.06); }
.ctrl-icon-circle {
  width: 46px; height: 46px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 18px; background: var(--surface-2); border: 1px solid var(--border);
}
.ctrl-btn.active .ctrl-icon-circle { background: var(--amber-light); border-color: var(--amber); color: var(--amber); }
.ctrl-btn.danger .ctrl-icon-circle { background: #ef4444; color: #fff; border: none; box-shadow: 0 4px 14px rgba(239,68,68,0.35); }

/* PTP Mini Drawer in Call Modal */
.ptp-drawer {
  display: none; padding: 14px 18px; background: #fff8ea; border-top: 1.5px dashed rgba(217,119,6,0.3);
}
.ptp-drawer.open { display: block; }
.ptp-input-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
.ptp-input { width: 100%; padding: 7px 10px; border-radius: 8px; border: 1px solid #d97706; font-size: 12px; }

/* SMS / Message Modal Specifics */
.msg-modal-head {
  padding: 18px 22px; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}
.msg-modal-body { padding: 20px 22px; }
.channel-switch { display: flex; gap: 8px; margin-bottom: 14px; }
.channel-btn {
  flex: 1; padding: 9px; border-radius: 8px; border: 1.5px solid var(--border);
  background: #fff; font-size: 12px; font-weight: 700; cursor: pointer; text-align: center;
  transition: all 0.15s ease;
}
.channel-btn.active { border-color: var(--green); background: var(--green-light); color: var(--green); }
.template-select-wrap { margin-bottom: 14px; }
.template-select-wrap label { font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase; display: block; margin-bottom: 6px; }
.template-select-wrap select {
  width: 100%; padding: 9px 10px; border-radius: 8px; border: 1px solid var(--border); font-size: 12px; font-family: inherit; margin-bottom: 8px;
}
.template-textarea {
  width: 100%; height: 95px; border-radius: 10px; border: 1px solid var(--border);
  padding: 10px 12px; font-family: inherit; font-size: 12px; line-height: 1.48; resize: none;
}
.msg-preview-card {
  background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 12px; margin-top: 12px;
  font-size: 11.5px; color: #166534; display: flex; gap: 8px; align-items: flex-start;
}

/* Slide-out AI Assistant Drawer */
.ai-drawer-backdrop {
  position: fixed; inset: 0; background: rgba(14,26,58,0.55);
  backdrop-filter: blur(3px); z-index: 9500;
  display: none; justify-content: flex-end; animation: fadeInColl 0.2s ease;
}
.ai-drawer-backdrop.open { display: flex !important; }
.ai-drawer-box {
  width: 100%; max-width: 480px; height: 100%; background: #fff;
  box-shadow: -12px 0 40px rgba(0,0,0,0.22); display: flex; flex-direction: column;
  animation: slideInRight 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideInRight {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}
.ai-drawer-head {
  padding: 20px 22px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(90deg, #0e1a3a, #162a5c); color: #fff;
}
.ai-drawer-body { flex: 1; overflow-y: auto; padding: 18px 20px; }
.ai-prompt-chips { display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px; }
.ai-chip-prompt {
  background: var(--surface-2); border: 1px solid var(--border); border-radius: 10px;
  padding: 9px 13px; font-size: 12px; font-weight: 600; text-align: left; cursor: pointer;
  transition: all 0.15s ease; color: var(--ink);
}
.ai-chip-prompt:hover { background: var(--blue-light); border-color: var(--blue); color: var(--blue); transform: translateX(3px); }
.ai-chat-thread { display: flex; flex-direction: column; gap: 14px; }
.ai-msg { display: flex; flex-direction: column; animation: fadeInColl 0.25s ease; }
.ai-msg.user { align-items: flex-end; }
.ai-msg.user .msg-bubble { background: var(--blue); color: #fff; border-radius: 12px 12px 2px 12px; font-size: 12.5px; padding: 10px 14px; }
.ai-msg.bot { align-items: flex-start; }
.ai-msg.bot .msg-bubble { background: #f8fafc; border: 1px solid var(--border); border-radius: 12px 12px 12px 2px; font-size: 12px; padding: 12px 15px; line-height: 1.58; color: #1e293b; }
.ai-msg.bot .msg-bubble b { color: var(--navy); }
.ai-drawer-foot {
  padding: 14px 18px; border-top: 1px solid var(--border); display: flex; gap: 8px; background: #fff;
}
.ai-drawer-input {
  flex: 1; border: 1px solid var(--border); border-radius: 10px; padding: 9px 14px; font-size: 12.5px; font-family: inherit;
}
.ai-drawer-send {
  background: var(--blue); color: #fff; border: none; border-radius: 10px; padding: 0 18px; font-weight: 700; cursor: pointer;
}

/* Toast Notifications */
#coll-toast-container {
  position: fixed; bottom: 24px; right: 24px; z-index: 99999;
  display: flex; flex-direction: column; gap: 10px; pointer-events: none;
}
.coll-toast {
  pointer-events: auto; background: var(--navy); color: #fff;
  border-radius: 10px; padding: 12px 18px; font-size: 12.5px; font-weight: 600;
  box-shadow: 0 12px 32px rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.18);
  display: flex; align-items: center; gap: 10px; animation: toastSlide 0.3s cubic-bezier(0.16,1,0.3,1);
}
@keyframes toastSlide {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.coll-toast.success { border-left: 4px solid #10b981; }
"""

# Insert CSS
css_needle = "/* ============ COLLECTIONS AI (admin) ============ */"
html = html.replace(css_needle, css_needle + "\n" + css_styles)

# 2. UPDATE PROTOBAR: Set Collections AI as ACTIVE by default
# remove active from login button
html = html.replace(
    '<button class="pb-tab active" data-frame="login" onclick="showFrame(\'login\',this)">Login</button>',
    '<button class="pb-tab" data-frame="login" onclick="showFrame(\'login\',this)">Login</button>'
)

# add active and data-target to collections button
html = html.replace(
    '<button class="pb-tab" data-frame="collections" onclick="showFrame(\'collections\',this)">Collections AI</button>',
    '<button class="pb-tab active nav-link" data-frame="collections" data-target="collections-ai" onclick="showFrame(\'collections\',this)">Collections AI</button>'
)

# update frame-login: remove active
html = html.replace(
    '<div class="frame active" id="frame-login">',
    '<div class="frame" id="frame-login">'
)

# update all sidebar collections links
html = html.replace(
    '<div class="sb-item" onclick="showFrameById(\'collections\')"><span class="ic">📞</span> Collections AI</div>',
    '<div class="sb-item sidebar-menu-item" data-view="collections-ai" onclick="showFrameById(\'collections\')"><span class="ic">📞</span> Collections AI</div>'
)

# 3. REPLACE FRAME-COLLECTIONS WITH ACTIVE STATE AND RICH UI
old_coll_frame = r'<div class="frame" id="frame-collections">.*?<footer class="proto-foot">CrediSphere AI · Collections Intelligence Module · MCA Project Prototype</footer>\s*</div>\s*</div>\s*</div>'

new_coll_frame = """<!-- ================= COLLECTIONS AI ================= -->
<div class="frame active" id="frame-collections" data-view="collections-ai">
  <div id="collections-ai-view">
    <div class="app-shell">
      <aside class="sidebar">
        <div class="sb-brand"><div class="logo-mark">CS</div><div><b>CrediSphere</b><span>Lender Console</span></div></div>
        <div class="sb-section-label">Overview</div>
        <div class="sb-item" onclick="showFrameById('admin')"><span class="ic">📊</span> Dashboard</div>
        <div class="sb-item" onclick="showFrameById('credit')"><span class="ic">🧠</span> Credit Intelligence</div>
        <div class="sb-item" onclick="showFrameById('apply')"><span class="ic">📄</span> Loan Applications</div>
        <div class="sb-section-label">Recovery</div>
        <div class="sb-item active sidebar-menu-item" data-view="collections-ai" onclick="showFrameById('collections')"><span class="ic">📞</span> Collections AI</div>
        <div class="sb-item"><span class="ic">⚖️</span> Legal &amp; Repossession</div>
        <div class="sb-section-label">Management</div>
        <div class="sb-item"><span class="ic">👥</span> Customers</div>
        <div class="sb-item" onclick="showFrameById('reports')"><span class="ic">📈</span> Reports</div>
        <div class="sb-item" onclick="showFrameById('policy')"><span class="ic">⚙️</span> Risk Policy Config</div>
        <div class="sb-item" onclick="showFrameById('screenconfig')"><span class="ic">🖥️</span> Screen Configuration</div>
        <div class="sb-bottom">
          <div class="sb-user"><div class="sb-avatar">AK</div><div><b>Anita Kapoor</b><span>Credit Ops Admin</span></div></div>
        </div>
      </aside>

      <div class="main">
        <div class="coll-topstrip">
          <span class="pdot"></span> High-risk account — Farid Sheikh flagged for accelerated recovery action
          <span style="margin-left:auto;font-size:11.5px;color:var(--muted);font-weight:500;">
            Loan: <b style="font-family:'DM Mono',monospace;color:var(--navy);">#LN-2024-88492</b> &nbsp;·&nbsp; Overdue: <b style="color:var(--red);">₹3,72,000</b>
          </span>
        </div>
        <div class="content">
          <div class="page-head">
            <div>
              <h1>Collections Intelligence &amp; Telephony Hub</h1>
              <p>AI-recommended recovery strategy for overdue accounts · Powered by Random Forest + DQN Agent</p>
            </div>
            <div style="display:flex;gap:10px;">
              <button class="btn-sm" onclick="collectionsML.randomizeState()" style="display:flex;align-items:center;gap:6px;">
                🔄 <span>Live Re-simulate</span>
              </button>
              <button class="btn-sm dark" id="btn-ask-ai-coll" onclick="openCollAIDrawer()">🤖 Ask AI assistant</button>
            </div>
          </div>

          <div class="grid-2" style="grid-template-columns:1fr 1.35fr 1fr;gap:18px;">
            <!-- CARD 1: OVERDUE DETAILS -->
            <div class="card" id="coll-overdue-card">
              <div class="card-head" style="display:flex;justify-content:space-between;align-items:center;">
                <h3>📋 Overdue details</h3>
                <span class="subchip" style="font-size:10.5px;background:var(--surface-2);border:1px solid var(--border);padding:2px 8px;border-radius:6px;font-weight:700;">DPD 90+</span>
              </div>
              <div class="card-body">
                <div class="factor-row"><div class="factor-top"><b>Borrower Name</b><span id="txt-borrower-name">Farid Sheikh</span></div></div>
                <div class="factor-row"><div class="factor-top"><b>Contact Number</b><span style="font-family:'DM Mono',monospace;" id="txt-borrower-phone">+91 98765-43210</span></div></div>
                <div class="factor-row"><div class="factor-top"><b>EMI amount</b><span id="txt-emi-amt">₹1,20,000</span></div></div>
                <div class="factor-row"><div class="factor-top"><b>EMIs bounced</b><span id="txt-emis-bounced">3 consecutive</span></div></div>
                <div class="factor-row"><div class="factor-top"><b>Total overdue</b><span style="color:var(--red);font-weight:700;font-size:14px;" id="txt-total-overdue">₹3,72,000</span></div></div>
                <div class="factor-row"><div class="factor-top"><b>DPD bucket</b><span style="color:var(--red);font-weight:700;" id="txt-dpd-bucket">90 (3)</span></div></div>
                
                <div class="coll-chip-wrap">
                  <span class="chip chip-rejected" id="coll-risk-badge">🔴 High risk (RF Risk 78.6%)</span>
                  <span class="coll-subchip warning" id="coll-promises-chip">Broken Promises: 2</span>
                </div>

                <div style="margin-top:16px;padding-top:12px;border-top:1px dashed var(--border);display:flex;justify-content:space-between;align-items:center;">
                  <span style="font-size:11px;color:var(--muted);">RF Default Probability:</span>
                  <b style="font-size:12.5px;font-family:'DM Mono',monospace;color:var(--red);" id="coll-rf-prob">78.6%</b>
                </div>
              </div>
            </div>

            <!-- CARD 2: RECOVERY RECOMMENDATION -->
            <div class="card" id="coll-rec-card">
              <div class="card-head" style="display:flex;align-items:center;justify-content:space-between;">
                <h3><span class="ai-chip">AI</span> &nbsp;Recovery recommendation</h3>
                <button class="ai-engine-btn expanded" id="coll-toggle-insights-btn" onclick="toggleMLEngineInsights()">
                  <span>🧠</span> AI Engine Insights <span class="chevron-icon">▾</span>
                </button>
              </div>
              <div class="card-body">
                <p id="coll-rec-text" style="font-size:13px;line-height:1.65;color:#374151;margin-bottom:14px;">
                  Customer has broken 2 prior promises. AI recommends a structured settlement offer with partial upfront payment, contacted during the <b>5–7 PM</b> window (highest response rate).
                </p>

                <div class="bureau-grid" style="margin-bottom:14px;">
                  <div class="bureau-box"><span>Best call time</span><b style="font-size:13px;" id="coll-best-time">5–7 PM</b></div>
                  <div class="bureau-box"><span>Recovery odds</span><b style="font-size:13px;color:var(--amber);" id="coll-rec-odds">61.4%</b></div>
                  <div class="bureau-box"><span>Sentiment</span><b style="font-size:13px;color:var(--red);" id="coll-sentiment">Negative</b></div>
                </div>

                <!-- LIVE ACTION HUBS (CALLS, SMS & SETTLEMENT) -->
                <div class="coll-action-hub">
                  <div class="action-hub-label">⚡ Live Telephony &amp; Recovery Interventions</div>
                  <div class="coll-action-buttons">
                    <button class="coll-action-btn primary" onclick="openLiveCallModal()">
                      <span class="btn-icon">📞</span>
                      <span class="btn-title">Simulate Call</span>
                      <span class="btn-subtitle">Live VoIP Telephony</span>
                    </button>
                    <button class="coll-action-btn secondary" onclick="openSMSModal()">
                      <span class="btn-icon">💬</span>
                      <span class="btn-title">Send Payment Link</span>
                      <span class="btn-subtitle">SMS / WhatsApp</span>
                    </button>
                    <button class="coll-action-btn outline" onclick="openSettlementModal()">
                      <span class="btn-icon">📑</span>
                      <span class="btn-title">Structure Settlement</span>
                      <span class="btn-subtitle">₹40,000 Upfront Token</span>
                    </button>
                  </div>
                </div>

                <!-- EXPANDABLE AI ENGINE INSIGHTS BADGE & DIAGNOSTICS PANEL -->
                <div class="coll-insights-panel" id="coll-insights-panel">
                  <div class="coll-insights-title">
                    <span>🔬 ML/RL Diagnostic Insights</span>
                    <span style="font-size:10px;color:var(--green);font-weight:700;">● Active Policy</span>
                  </div>
                  <div class="coll-model-pipeline">
                    <span>⚙️</span>
                    <span>Model Pipeline: Random Forest (Risk Scoring) + DQN Agent (Dynamic Policy Optimization)</span>
                  </div>
                  <div class="coll-stats-row">
                    <div class="coll-stat-box">
                      <span>Confidence</span>
                      <b style="color:var(--green);" id="diag-conf">87.4%</b>
                    </div>
                    <div class="coll-stat-box">
                      <span>Exploit (ε)</span>
                      <b id="diag-epsilon">0.05</b>
                    </div>
                    <div class="coll-stat-box">
                      <span>Optimal Q</span>
                      <b style="color:var(--blue);" id="diag-qval">+0.812</b>
                    </div>
                  </div>

                  <div style="font-size:11px;font-weight:700;color:var(--navy);margin-bottom:6px;">DQN Action-Value Q(s, a) Distribution:</div>
                  <div class="q-meter-wrap" id="q-distribution-meters">
                    <!-- Populated by CollectionsMLEngine -->
                  </div>

                  <div style="font-size:11px;font-weight:700;color:var(--navy);margin-top:12px;margin-bottom:6px;">Random Forest Feature Weights:</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:10.5px;" id="rf-feature-weights">
                    <!-- Populated by CollectionsMLEngine -->
                  </div>
                </div>
              </div>
            </div>

            <!-- CARD 3: FOLLOW-UP HISTORY -->
            <div class="card" id="coll-history-card">
              <div class="card-head" style="display:flex;align-items:center;justify-content:space-between;">
                <h3>🕒 Follow-up history</h3>
                <span class="live-pill"><span class="pdot3"></span> Live Feed</span>
              </div>
              <div class="card-body">
                <div id="coll-feed-container">
                  <div class="feed-item"><div class="feed-dot" style="background:var(--green-light);">💬</div><div><div class="feed-text"><b>Kept promise</b> — ₹12,89,800 received via UPI</div><div class="feed-time">09 Nov 2025</div></div></div>
                  <div class="feed-item"><div class="feed-dot" style="background:var(--amber-light);">📞</div><div><div class="feed-text"><b>PTP</b> — ₹12,800 promised, next action 09-Dec</div><div class="feed-time">05 Nov 2025</div></div></div>
                  <div class="feed-item"><div class="feed-dot" style="background:var(--blue-light);">📩</div><div><div class="feed-text"><b>Long term promise</b> — repayment plan discussed</div><div class="feed-time">13 Oct 2025</div></div></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <footer class="proto-foot">CrediSphere AI · Collections Intelligence Module · MCA Project Prototype</footer>
      </div>
    </div>
  </div>
</div>"""

html = re.sub(old_coll_frame, new_coll_frame, html, flags=re.DOTALL)

# 4. MODALS & DRAWERS MARKUP
modals_markup = """
<!-- ================= COLLECTIONS AI MODALS & DRAWERS ================= -->

<!-- 1. LIVE VOIP CALL MODAL -->
<div class="coll-modal-backdrop" id="coll-call-modal">
  <div class="coll-modal-box">
    <div class="call-modal-header">
      <div class="call-avatar-ring" id="call-avatar-ring">FS</div>
      <div class="call-borrower-name">Farid Sheikh</div>
      <div class="call-borrower-num">+91 98765-43210 · Account #LN-2024-88492</div>
      <div class="call-status-pill" id="call-status-pill">
        <span class="pdot3" style="background:#4ade80;"></span>
        <span id="call-status-text">Connecting to SIP Gateway...</span>
      </div>
    </div>

    <!-- Live Call Transcript Bubble Stream -->
    <div class="call-body" id="call-transcript-stream">
      <div style="text-align:center;font-size:11px;color:var(--muted);margin-bottom:12px;" id="call-callout-msg">
        🔒 VoIP encrypted line · Simulated AI Agent Intervention
      </div>
    </div>

    <!-- Promise to Pay Inline Drawer -->
    <div class="ptp-drawer" id="ptp-inline-drawer">
      <div style="font-size:12px;font-weight:700;color:#92400e;">📝 Record Promise to Pay (PTP)</div>
      <div class="ptp-input-grid">
        <div>
          <label style="font-size:10px;font-weight:700;color:#92400e;">PROMISED AMOUNT</label>
          <input type="text" class="ptp-input" id="ptp-amount-input" value="₹40,000">
        </div>
        <div>
          <label style="font-size:10px;font-weight:700;color:#92400e;">PROMISE DATE</label>
          <input type="text" class="ptp-input" id="ptp-date-input" value="12-Dec-2025 (Friday)">
        </div>
      </div>
      <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:8px;">
        <button onclick="togglePTPDrawer(false)" style="padding:5px 10px;border-radius:6px;border:1px solid #d97706;background:#fff;font-size:11px;cursor:pointer;">Cancel</button>
        <button onclick="confirmRecordPTP()" style="padding:5px 12px;border-radius:6px;border:none;background:#d97706;color:#fff;font-weight:700;font-size:11px;cursor:pointer;">Save PTP Record</button>
      </div>
    </div>

    <!-- Controls Bar -->
    <div class="call-controls-bar">
      <button class="ctrl-btn" id="btn-call-mute" onclick="toggleCallMute()">
        <div class="ctrl-icon-circle">🎙️</div>
        <span id="mute-label">Mute</span>
      </button>

      <button class="ctrl-btn" onclick="togglePTPDrawer()">
        <div class="ctrl-icon-circle" style="color:#d97706;">📝</div>
        <span>Record PTP</span>
      </button>

      <button class="ctrl-btn danger" onclick="endLiveCall()">
        <div class="ctrl-icon-circle">📞</div>
        <span style="color:#ef4444;">End Call</span>
      </button>
    </div>
  </div>
</div>

<!-- 2. LIVE SMS / WHATSAPP DISPATCH MODAL -->
<div class="coll-modal-backdrop" id="coll-sms-modal">
  <div class="coll-modal-box">
    <div class="msg-modal-head">
      <div>
        <b style="font-size:14px;color:var(--navy);">📲 Dispatch Recovery Payment Link</b>
        <span style="display:block;font-size:11px;color:var(--muted);">Recipient: Farid Sheikh (+91 98765-43210)</span>
      </div>
      <button onclick="closeSMSModal()" style="border:none;background:none;font-size:18px;cursor:pointer;color:var(--muted);">✕</button>
    </div>

    <div class="msg-modal-body">
      <div class="channel-switch">
        <button class="channel-btn active" id="chan-sms" onclick="switchMsgChannel('sms')">💬 SMS Gateway (Twilio/Karix)</button>
        <button class="channel-btn" id="chan-wa" onclick="switchMsgChannel('whatsapp')">🟢 WhatsApp Verified Business</button>
      </div>

      <div class="template-select-wrap">
        <label>AI-Generated Message Template</label>
        <select id="sms-template-select" onchange="onTemplateChange()">
          <option value="settlement">★ Structured Settlement Token Offer (Recommended by DQN)</option>
          <option value="reminder">Standard DPD 90 Overdue Reminder</option>
          <option value="urgent">Urgent Pre-Legal Escalation Notice</option>
        </select>

        <textarea class="template-textarea" id="sms-message-text" oninput="updateSMSPreview()"></textarea>
      </div>

      <div class="msg-preview-card">
        <span style="font-size:16px;">⚡</span>
        <div>
          <b>Gateway Preview &amp; Verification:</b>
          <span style="display:block;margin-top:2px;">Dynamic payment token generated. Target link points to secure UPI/Netbanking portal with instant callback to Loan #LN-2024-88492.</span>
        </div>
      </div>

      <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:18px;">
        <button onclick="closeSMSModal()" class="btn-sm" style="padding:8px 16px;">Cancel</button>
        <button onclick="sendSMSLink()" class="btn-sm" style="background:var(--blue);color:#fff;border:none;padding:8px 20px;font-weight:700;">
          🚀 Send Now
        </button>
      </div>
    </div>
  </div>
</div>

<!-- 3. STRUCTURED SETTLEMENT CONFIGURATOR MODAL -->
<div class="coll-modal-backdrop" id="coll-settlement-modal">
  <div class="coll-modal-box">
    <div class="msg-modal-head">
      <div>
        <b style="font-size:14px;color:var(--navy);">📑 DQN Structured Settlement Agreement</b>
        <span style="display:block;font-size:11px;color:var(--muted);">Account: Farid Sheikh · Overdue ₹3,72,000</span>
      </div>
      <button onclick="closeSettlementModal()" style="border:none;background:none;font-size:18px;cursor:pointer;color:var(--muted);">✕</button>
    </div>

    <div class="msg-modal-body">
      <div style="background:var(--surface-2);border:1px solid var(--border);border-radius:10px;padding:14px;margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px;">
          <span style="color:var(--muted);">Original Outstanding Balance:</span>
          <b>₹3,72,000</b>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px;">
          <span style="color:var(--muted);">AI Recommended Upfront Token:</span>
          <b style="color:var(--green);font-size:13px;">₹40,000 (Commitment)</b>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px;">
          <span style="color:var(--muted);">Restructured Repayment:</span>
          <b>₹33,200 / month x 10 months</b>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;">
          <span style="color:var(--muted);">Penalty / Bounce Charges Waived:</span>
          <b style="color:var(--blue);">₹24,000 (Conditional Waiver)</b>
        </div>
      </div>

      <div style="font-size:12px;color:#475569;line-height:1.5;margin-bottom:14px;">
        Generating this agreement will freeze negative bureau reporting for 14 days pending token payment, maximizing expected recovery yield to <b>68.4%</b>.
      </div>

      <div style="display:flex;justify-content:flex-end;gap:10px;">
        <button onclick="closeSettlementModal()" class="btn-sm" style="padding:8px 16px;">Cancel</button>
        <button onclick="confirmSettlementAgreement()" class="btn-sm" style="background:var(--green);color:#fff;border:none;padding:8px 20px;font-weight:700;">
          ✍️ Issue Settlement Agreement
        </button>
      </div>
    </div>
  </div>
</div>

<!-- 4. SLIDE-OUT "ASK AI ASSISTANT" DRAWER -->
<div class="ai-drawer-backdrop" id="coll-ai-drawer" onclick="handleDrawerBackdropClick(event)">
  <div class="ai-drawer-box">
    <div class="ai-drawer-head">
      <div>
        <div style="display:flex;align-items:center;gap:6px;font-weight:800;font-size:13.5px;">
          <span>🤖</span> CrediSphere Collections AI Copilot
        </div>
        <span style="font-size:10.5px;opacity:0.8;">Context: Farid Sheikh · DPD 90 · Overdue ₹3,72,000</span>
      </div>
      <button onclick="closeCollAIDrawer()" style="background:none;border:none;color:#fff;font-size:18px;cursor:pointer;">✕</button>
    </div>

    <div class="ai-drawer-body" id="ai-drawer-body">
      <div style="font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;margin-bottom:8px;">
        💡 Suggested Inquiries:
      </div>
      <div class="ai-prompt-chips">
        <button class="ai-chip-prompt" onclick="askPresetQuestion('Why does RL recommend settlement over repossession?')">
          ⚖️ Why does RL recommend settlement over repossession?
        </button>
        <button class="ai-chip-prompt" onclick="askPresetQuestion('Why is 5–7 PM the optimal contact window?')">
          ⏰ Why is 5–7 PM the optimal contact window?
        </button>
        <button class="ai-chip-prompt" onclick="askPresetQuestion('What happens if Farid defaults on this PTP?')">
          🛡️ What happens if Farid defaults on this PTP?
        </button>
        <button class="ai-chip-prompt" onclick="askPresetQuestion('Explain Random Forest risk attribution')">
          🌲 Explain Random Forest risk attribution
        </button>
      </div>

      <div class="ai-chat-thread" id="ai-chat-thread">
        <div class="ai-msg bot">
          <div class="msg-bubble">
            Hello Anita! I am your <b>Collections AI Copilot</b>. I have analyzed Farid Sheikh's profile using our Random Forest default predictor and Deep Q-Network policy optimizer. How can I assist you with this account?
          </div>
        </div>
      </div>
    </div>

    <div class="ai-drawer-foot">
      <input type="text" class="ai-drawer-input" id="ai-user-query" placeholder="Ask anything about this borrower or ML strategy..." onkeydown="if(event.key==='Enter') sendCustomAIQuery()">
      <button class="ai-drawer-send" onclick="sendCustomAIQuery()">Send</button>
    </div>
  </div>
</div>

<!-- 5. TOAST NOTIFICATION CONTAINER -->
<div id="coll-toast-container"></div>
"""

# Replace scripts completely with clean, unified engine
old_script_block = r'<script>.*?</script>'

clean_script = """<script>
/* ================= FRAME SWITCHING LOGIC ================= */
function showFrame(id, btn){
  // Normalize collections IDs
  if (id === 'collections-ai') id = 'collections';

  document.querySelectorAll('.frame').forEach(f => f.classList.remove('active'));
  const target = document.getElementById('frame-' + id);
  if (target) {
    target.classList.add('active');
  }

  document.querySelectorAll('.pb-tab').forEach(t => t.classList.remove('active'));
  if (!btn) {
    btn = document.querySelector('.pb-tab[data-frame="' + id + '"]');
  }
  if (btn) {
    btn.classList.add('active');
  }

  // Update sidebar active highlights
  document.querySelectorAll('.sb-item').forEach(item => {
    item.classList.remove('active');
    if (item.getAttribute('data-view') === id || (id === 'collections' && item.textContent.includes('Collections AI'))) {
      item.classList.add('active');
    }
  });

  if (id === 'collections') {
    const collView = document.getElementById('collections-ai-view');
    if (collView) collView.style.display = 'block';
    collectionsML.init();
  }

  window.scrollTo(0,0);
}

function showFrameById(id){
  const btn = document.querySelector('.pb-tab[data-frame="'+id+'"]');
  showFrame(id, btn);
}

/* ================= SCREEN CONFIGURATION LOGIC ================= */
function scSwitchScreen(key, tabEl){
  document.querySelectorAll('.sc-screen-tab').forEach(t=>t.classList.remove('active'));
  tabEl.classList.add('active');
  document.querySelectorAll('.sc-widget-list').forEach(l=>l.style.display='none');
  const list = document.getElementById('sc-list-'+key);
  if(list) list.style.display='block';
}

function scToggleExpand(headEl){
  const card = headEl.closest('.sc-widget-card');
  card.classList.toggle('expanded');
}

function scToggleWidget(checkbox){
  const card = checkbox.closest('.sc-widget-card');
  const badge = card.querySelector('.sc-widget-badge');
  const widgetKey = card.getAttribute('data-widget');
  const isOn = checkbox.checked;

  card.classList.toggle('off', !isOn);
  badge.textContent = isOn ? 'Visible' : 'Hidden';
  badge.classList.toggle('on', isOn);
  badge.classList.toggle('off', !isOn);

  const preview = document.getElementById('pv-'+widgetKey);
  if(preview){
    preview.classList.toggle('hidden-block', !isOn);
  }
  scUpdateCounts();
}

function scUpdateCounts(){
  const all = document.querySelectorAll('.sc-widget-card');
  let visible = 0, hidden = 0;
  all.forEach(c=>{
    if(c.classList.contains('off')) hidden++; else visible++;
  });
  const vEl = document.getElementById('sc-visible-count');
  const hEl = document.getElementById('sc-hidden-count');
  if(vEl) vEl.textContent = visible;
  if(hEl) hEl.textContent = hidden;
}

/* ==========================================================================
   COLLECTIONS INTELLIGENCE & LIVE TELEPHONY ENGINE (ML/RL + VOIP + CHANNELS)
   ========================================================================== */
class CollectionsMLEngine {
  constructor() {
    this.state = {
      borrowerName: "Farid Sheikh",
      accountNo: "LN-2024-88492",
      phone: "+91 98765-43210",
      dpd: 90,
      brokenPromises: 2,
      bouncedEmis: 3,
      emiAmount: 120000,
      totalOverdue: 372000,
      sentiment: "Negative",
      bestCallTime: "5–7 PM"
    };

    this.actions = [
      { id: 'settlement', name: 'Structured Settlement Offer', qValue: 0.812, pct: 85, color: '#2f5fff', isOptimal: true },
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

  init() {
    this.renderQDistribution();
    this.renderFeatureWeights();
  }

  randomizeState() {
    // Dynamically simulate an account variation
    const names = ["Farid Sheikh", "Rajesh Varma", "Sunil Deshmukh"];
    const sentiments = ["Negative", "Hostile", "Cooperative"];
    const dpds = [60, 90, 120];
    const promises = [1, 2, 3];

    const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
    this.state.dpd = pick(dpds);
    this.state.brokenPromises = pick(promises);
    this.state.sentiment = pick(sentiments);

    // Recalculate Q values
    if (this.state.dpd >= 90) {
      this.actions[0].qValue = 0.812;
      this.actions[4].qValue = -0.150;
    } else {
      this.actions[0].qValue = 0.740;
      this.actions[1].qValue = 0.790;
    }

    // Update UI elements
    const dpdEl = document.getElementById('txt-dpd-bucket');
    if (dpdEl) dpdEl.textContent = `${this.state.dpd} (${this.state.brokenPromises})`;
    const sentEl = document.getElementById('coll-sentiment');
    if (sentEl) sentEl.textContent = this.state.sentiment;
    const promChip = document.getElementById('coll-promises-chip');
    if (promChip) promChip.textContent = `Broken Promises: ${this.state.brokenPromises}`;

    this.renderQDistribution();
    showCollToast("Live ML State re-simulated! Random Forest & DQN policies refreshed.", "success");
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
      <div style="background:#fff;border:1px solid var(--border);border-radius:6px;padding:5px 8px;display:flex;justify-content:space-between;">
        <span style="color:var(--muted);">${f.feature}:</span>
        <b style="color:var(--navy);font-family:'DM Mono',monospace;">${f.weight}</b>
      </div>
    `).join('');
  }
}

const collectionsML = new CollectionsMLEngine();

// Initialize when DOM is ready
window.addEventListener('load', () => {
  collectionsML.init();
  // By default, activate collections frame
  showFrame('collections');
});

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

function openLiveCallModal() {
  const modal = document.getElementById('coll-call-modal');
  const avatar = document.getElementById('call-avatar-ring');
  const statusText = document.getElementById('call-status-text');
  const statusPill = document.getElementById('call-status-pill');
  const stream = document.getElementById('call-transcript-stream');

  modal.classList.add('open');
  avatar.classList.add('ringing');
  statusPill.classList.remove('connected');
  statusText.textContent = "Connecting to SIP Gateway...";
  
  stream.innerHTML = `
    <div style="text-align:center;font-size:11px;color:var(--muted);margin-bottom:12px;" id="call-callout-msg">
      🔒 VoIP encrypted line · Simulated AI Agent Intervention
    </div>
  `;

  callDurationSeconds = 0;
  isCallMuted = false;
  updateMuteButtonUI();

  callStepTimeout = setTimeout(() => {
    statusText.textContent = "Ringing... (+91 98765-43210)";
    
    setTimeout(() => {
      avatar.classList.remove('ringing');
      statusPill.classList.add('connected');
      startCallTimer();
      runCallConversationScript();
    }, 2000);
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

function runCallConversationScript() {
  const stream = document.getElementById('call-transcript-stream');
  
  const scriptDialogue = [
    { sender: "agent", text: "Namaste Mr. Sheikh, this is CrediSphere Collections regarding your pending EMI of ₹1,20,000 for account LN-2024-88492." },
    { sender: "borrower", text: "Namaste. Look, I had severe family medical expenses and lost my contract. I cannot arrange the full ₹3.72 lakh immediately." },
    { sender: "agent", text: "Understood Mr. Sheikh. Our AI model has pre-structured a recovery offer: pay a ₹40,000 upfront commitment this Friday, and we will restructure the remaining balance across 10 months with bounce penalties waived." },
    { sender: "borrower", text: "Yes! ₹40,000 this Friday by 5 PM I can manage for sure. Please send me the link on WhatsApp/SMS." }
  ];

  scriptDialogue.forEach((item, idx) => {
    setTimeout(() => {
      if (!document.getElementById('coll-call-modal').classList.contains('open')) return;
      const bubble = document.createElement('div');
      bubble.className = `transcript-bubble ${item.sender}`;
      bubble.innerHTML = `
        <span class="bubble-tag">${item.sender === 'agent' ? '🤖 CrediSphere Voice AI' : '👤 Farid Sheikh (Borrower)'}</span>
        <div class="bubble-content">${item.text}</div>
      `;
      stream.appendChild(bubble);
      stream.scrollTop = stream.scrollHeight;

      if (idx === scriptDialogue.length - 1) {
        togglePTPDrawer(true);
      }
    }, (idx + 1) * 2200);
  });
}

function toggleCallMute() {
  isCallMuted = !isCallMuted;
  updateMuteButtonUI();
  showCollToast(isCallMuted ? "Microphone muted" : "Microphone unmuted");
}

function updateMuteButtonUI() {
  const btn = document.getElementById('btn-call-mute');
  const label = document.getElementById('mute-label');
  if (!btn || !label) return;
  btn.classList.toggle('active', isCallMuted);
  label.textContent = isCallMuted ? "Unmute" : "Mute";
}

function togglePTPDrawer(forceState) {
  const drawer = document.getElementById('ptp-inline-drawer');
  if (!drawer) return;
  if (typeof forceState === 'boolean') {
    drawer.classList.toggle('open', forceState);
  } else {
    drawer.classList.toggle('open');
  }
}

function confirmRecordPTP() {
  const amount = document.getElementById('ptp-amount-input').value || "₹40,000";
  const date = document.getElementById('ptp-date-input').value || "12-Dec-2025";
  
  togglePTPDrawer(false);
  appendFollowUpFeed("📞", `<b>PTP Recorded</b> — ${amount} promised by ${date} (Agent call negotiation)`, "Just now");
  showCollToast(`Promise to Pay of ${amount} recorded successfully!`, "success");
}

function endLiveCall() {
  clearInterval(callTimerInterval);
  clearTimeout(callStepTimeout);
  
  const modal = document.getElementById('coll-call-modal');
  modal.classList.remove('open');
  
  if (callDurationSeconds > 0) {
    const mins = String(Math.floor(callDurationSeconds / 60)).padStart(2, '0');
    const secs = String(callDurationSeconds % 60).padStart(2, '0');
    appendFollowUpFeed("📞", `<b>Simulated Call Ended</b> — Duration ${mins}:${secs}, borrower committed to ₹40,000 upfront token`, "Just now");
    showCollToast(`Call ended (${mins}:${secs}). Follow-up history updated.`, "success");
  }
}

/* ================= LIVE SMS & WHATSAPP ENGINE ================= */
const SMS_TEMPLATES = {
  settlement: "Urgent: CrediSphere one-time settlement offer valid until 5 PM today. Pay ₹40,000 upfront token to waive ₹24,000 penalties: https://pay.credisphere.ai/s/F92K1",
  reminder: "Dear Farid Sheikh, overdue EMI of ₹1,20,000 is pending for account LN-2024-88492. Avoid escalation by paying here: https://pay.credisphere.ai/pay/88492",
  urgent: "FINAL NOTICE: Account LN-2024-88492 has reached DPD 90. Legal arbitration proceedings pending. Clear balance or contact collections: https://pay.credisphere.ai/legal/88492"
};

let currentChannel = 'sms';

function openSMSModal() {
  const modal = document.getElementById('coll-sms-modal');
  modal.classList.add('open');
  onTemplateChange();
}

function closeSMSModal() {
  document.getElementById('coll-sms-modal').classList.remove('open');
}

function switchMsgChannel(ch) {
  currentChannel = ch;
  document.getElementById('chan-sms').classList.toggle('active', ch === 'sms');
  document.getElementById('chan-wa').classList.toggle('active', ch === 'whatsapp');
}

function onTemplateChange() {
  const select = document.getElementById('sms-template-select');
  const textarea = document.getElementById('sms-message-text');
  const val = select.value;
  textarea.value = SMS_TEMPLATES[val] || SMS_TEMPLATES.settlement;
}

function updateSMSPreview() {}

function sendSMSLink() {
  const channelName = currentChannel === 'sms' ? 'SMS Gateway' : 'WhatsApp Business';
  closeSMSModal();

  showCollToast(`${channelName} successfully dispatched via Gateway (Status: Delivered · ID: msg_${Math.random().toString(36).substring(7)})`, "success");
  appendFollowUpFeed("📩", `<b>Payment Link Sent via ${channelName}</b> — Upfront ₹40,000 settlement token link`, "Just now");
}

/* ================= STRUCTURED SETTLEMENT ENGINE ================= */
function openSettlementModal() {
  document.getElementById('coll-settlement-modal').classList.add('open');
}
function closeSettlementModal() {
  document.getElementById('coll-settlement-modal').classList.remove('open');
}
function confirmSettlementAgreement() {
  closeSettlementModal();
  showCollToast("Settlement agreement generated and queued to borrower via SMS/Email.", "success");
  appendFollowUpFeed("📑", `<b>Settlement Agreement Issued</b> — ₹40,000 upfront + ₹33,200/mo x 10 months (penalties waived)`, "Just now");
}

/* ================= "ASK AI ASSISTANT" COPILOT DRAWER ================= */
const AI_COPILOT_KNOWLEDGE = {
  "Why does RL recommend settlement over repossession?": `
    <b>Deep Q-Network (DQN) Policy Analysis:</b><br><br>
    1. <b>Recovery Value Comparison:</b> At DPD 90 with 2 broken promises, legal asset repossession experiences a <b>34% secondary auction haircut</b> plus ₹35,000 in yard and court expenses. Expected net recovery is only <b>42.1%</b> after a 180+ day court freeze ($Q = -0.150$).<br><br>
    2. <b>Cash Velocity:</b> A structured settlement with an immediate ₹40,000 token payment secures immediate cashflow and achieves an expected net recovery rate of <b>68.4%</b> ($Q = +0.812$).<br><br>
    3. <b>Behavioral Sentiment:</b> Farid's sentiment score is <i>Negative</i>, indicating adversarial resistance to repossession threats, but historical bureau data reveals high compliance once late fees are waived.
  `,
  "Why is 5–7 PM the optimal contact window?": `
    <b>Temporal Optimization Engine:</b><br>
    Empirical telematics data across 45,000 self-employed borrowers indicates connection answer rates surge to <b>74.2%</b> between 5:00 PM and 7:00 PM (vs 23.8% during midday hours). Borrower stress levels are also significantly lower after business hours, leading to <b>2.3x higher Promise-to-Pay (PTP) conversion</b>.
  `,
  "What happens if Farid defaults on this PTP?": `
    <b>Next-Best-Action Policy Transition:</b><br>
    If the ₹40,000 upfront token is not detected by 5:00 PM Friday, the DQN state transitions to <code>(DPD: 95, BrokenPromises: 3)</code>. This triggers an automated escalation policy:
    <br>• Automated repossession notice issued under Section 138 / SARFAESI.
    <br>• Hard recovery field agent dispatched to registered business premises.
    <br>• Negative bureau flag transmitted to CIBIL/Experian.
  `,
  "Explain Random Forest risk attribution": `
    <b>Random Forest Risk Decomposition (Risk Level: High · 78.6%):</b><br>
    Ensemble of 150 gradient-boosted decision trees evaluated the following feature split:
    <br>• <b>DPD Bucket 90+ (38% weight)</b>: Crossed critical impairment barrier.
    <br>• <b>Broken Promises (27% weight)</b>: High recidivism signal.
    <br>• <b>Negative Sentiment (18% weight)</b>: Borrower vocalized severe cash shortfall.
    <br>• <b>EMI Bounce Velocity (17% weight)</b>: 3 consecutive NACH failures.
  `
};

function openCollAIDrawer() {
  document.getElementById('coll-ai-drawer').classList.add('open');
}

function closeCollAIDrawer() {
  document.getElementById('coll-ai-drawer').classList.remove('open');
}

function handleDrawerBackdropClick(e) {
  if (e.target.id === 'coll-ai-drawer') {
    closeCollAIDrawer();
  }
}

function askPresetQuestion(question) {
  addChatMessage("user", question);
  const thread = document.getElementById('ai-chat-thread');

  const typingBubble = document.createElement('div');
  typingBubble.className = "ai-msg bot";
  typingBubble.innerHTML = `<div class="msg-bubble" style="color:var(--muted);font-style:italic;">Analyzing DQN policy &amp; RF decision trees...</div>`;
  thread.appendChild(typingBubble);
  thread.parentElement.scrollTop = thread.parentElement.scrollHeight;

  setTimeout(() => {
    typingBubble.remove();
    const answer = AI_COPILOT_KNOWLEDGE[question] || "Based on historical recovery data for DPD 90 accounts, the model prioritizes structured settlement over confrontational actions.";
    addChatMessage("bot", answer);
  }, 400);
}

function sendCustomAIQuery() {
  const input = document.getElementById('ai-user-query');
  const query = input.value.trim();
  if (!query) return;

  addChatMessage("user", query);
  input.value = '';

  const thread = document.getElementById('ai-chat-thread');
  const typingBubble = document.createElement('div');
  typingBubble.className = "ai-msg bot";
  typingBubble.innerHTML = `<div class="msg-bubble" style="color:var(--muted);font-style:italic;">Querying Collections AI model engine...</div>`;
  thread.appendChild(typingBubble);
  thread.parentElement.scrollTop = thread.parentElement.scrollHeight;

  setTimeout(() => {
    typingBubble.remove();
    let reply = `Based on Farid Sheikh's DPD 90 profile and current state vector, our <b>DQN agent</b> strongly favors structured token settlement with contact scheduled for <b>5–7 PM</b>. Legal repossession or hostile recovery is penalized in the reward function due to high asset depreciation and prolonged legal turnaround.`;
    addChatMessage("bot", reply);
  }, 500);
}

function addChatMessage(sender, htmlContent) {
  const thread = document.getElementById('ai-chat-thread');
  const msg = document.createElement('div');
  msg.className = `ai-msg ${sender}`;
  msg.innerHTML = `<div class="msg-bubble">${htmlContent}</div>`;
  thread.appendChild(msg);
  thread.parentElement.scrollTop = thread.parentElement.scrollHeight;
}

/* ================= COMMON HELPERS: FEED & TOASTS ================= */
function appendFollowUpFeed(icon, contentHtml, timeStr) {
  const container = document.getElementById('coll-feed-container');
  if (!container) return;

  const item = document.createElement('div');
  item.className = "feed-item";
  item.style.animation = "fadeInColl 0.35s ease";
  item.innerHTML = `
    <div class="feed-dot" style="background:var(--blue-light);font-size:13px;">${icon}</div>
    <div>
      <div class="feed-text">${contentHtml}</div>
      <div class="feed-time" style="color:var(--blue);font-weight:700;">${timeStr}</div>
    </div>
  `;
  container.insertBefore(item, container.firstChild);
}

function showCollToast(message, type = "normal") {
  const container = document.getElementById('coll-toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `coll-toast ${type === 'success' ? 'success' : ''}`;
  toast.innerHTML = `
    <span style="font-size:16px;">${type === 'success' ? '✅' : '🔔'}</span>
    <span>${message}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4200);
}
</script>"""

html = re.sub(old_script_block, clean_script, html, flags=re.DOTALL)

# Add modals right before </body>
html = html.replace("</body>", modals_markup + "\n</body>")

# Output paths
destinations = [
    "/Users/vrindasharma/Desktop/CREDISPEHERAI-PROJECT/prototype.html",
    "/Users/vrindasharma/Desktop/project/CrediSphere-AI/prototype.html",
    "/Users/vrindasharma/Desktop/project/CrediSphere-AI/frontend/prototype.html"
]

for p in destinations:
    with open(p, 'w', encoding='utf-8') as out:
        out.write(html)
    print(f"Saved: {p} ({len(html)} bytes)")
