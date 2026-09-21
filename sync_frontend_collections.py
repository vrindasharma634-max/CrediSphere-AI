#!/usr/bin/env python3
import re

CSS_PATH = "/Users/vrindasharma/Desktop/project/CrediSphere-AI/frontend/css/style.css"
PAGE_PATH = "/Users/vrindasharma/Desktop/project/CrediSphere-AI/frontend/pages/collections-ai.html"

with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css = f.read()

styles_to_append = """
/* ============ COLLECTIONS AI LIVE TELEPHONY & INTELLIGENCE ============ */
#collections-ai-view {
  animation: fadeInColl 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  display: block;
}
@keyframes fadeInColl {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

.coll-chip-wrap { display: flex; gap: 8px; align-items: center; margin-top: 10px; flex-wrap: wrap; }
.coll-subchip { font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 6px; background: var(--surface-2); border: 1px solid var(--border); color: var(--muted); }
.coll-subchip.danger { background: var(--red-light); color: var(--red); border-color: rgba(224,49,49,0.2); }
.coll-subchip.warning { background: var(--amber-light); color: var(--amber); border-color: rgba(217,119,6,0.2); }

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

.q-meter-wrap { margin-top: 8px; display: flex; flex-direction: column; gap: 7px; }
.q-meter-row { display: flex; align-items: center; justify-content: space-between; font-size: 11px; gap: 10px; }
.q-meter-name { width: 155px; font-weight: 600; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.q-meter-bar-bg { flex: 1; height: 7px; background: #e5e9f3; border-radius: 10px; overflow: hidden; position: relative; }
.q-meter-bar-fill { height: 100%; border-radius: 10px; transition: width 0.5s ease; }
.q-meter-val { width: 45px; text-align: right; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 11px; }

.coll-action-hub { margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--border); }
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

.live-pill {
  display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px;
  font-weight: 700; color: var(--green); background: var(--green-light);
  padding: 2px 8px; border-radius: 12px;
}

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

.ptp-drawer {
  display: none; padding: 14px 18px; background: #fff8ea; border-top: 1.5px dashed rgba(217,119,6,0.3);
}
.ptp-drawer.open { display: block; }
.ptp-input-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
.ptp-input { width: 100%; padding: 7px 10px; border-radius: 8px; border: 1px solid #d97706; font-size: 12px; }

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

if "/* ============ COLLECTIONS AI LIVE TELEPHONY & INTELLIGENCE ============" not in css:
    css += "\n" + styles_to_append
    with open(CSS_PATH, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended styles to style.css")

# Build complete standalone page for collections-ai.html
page_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrediSphere AI — Collections Intelligence &amp; Live Telephony Hub</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/style.css">
    <style>
      body { margin: 0; padding: 0; font-family: 'DM Sans', sans-serif; background: #eef1f9; }
      .app-shell { display: flex; min-height: 100vh; }
      .sidebar { width: 240px; background: #0c1427; color: #fff; padding: 24px 16px; display: flex; flex-direction: column; flex-shrink: 0; }
      .sb-brand { display: flex; align-items: center; gap: 10px; margin-bottom: 28px; padding: 0 8px; }
      .sb-brand .logo-mark { width: 34px; height: 34px; border-radius: 9px; background: linear-gradient(135deg, #0ea394, #2f5fff); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 14px; }
      .sb-brand b { font-size: 14px; display: block; }
      .sb-brand span { font-size: 10.5px; color: rgba(255,255,255,0.5); }
      .sb-section-label { font-size: 10px; font-weight: 700; text-transform: uppercase; color: rgba(255,255,255,0.4); margin: 16px 8px 8px; letter-spacing: .06em; }
      .sb-item { display: flex; align-items: center; gap: 11px; padding: 10px 12px; border-radius: 10px; font-size: 13px; font-weight: 600; color: rgba(255,255,255,.72); transition: .15s; cursor: pointer; text-decoration: none; }
      .sb-item:hover { background: rgba(255,255,255,.08); color: #fff; }
      .sb-item.active { background: linear-gradient(90deg, rgba(47,95,255,.35), rgba(47,95,255,.08)); color: #fff; box-shadow: inset 3px 0 0 #5b7fff; }
      .sb-bottom { margin-top: auto; padding-top: 14px; border-top: 1px solid rgba(255,255,255,.1); }
      .sb-user { display: flex; align-items: center; gap: 10px; padding: 8px 6px; }
      .sb-avatar { width: 32px; height: 32px; border-radius: 9px; background: linear-gradient(135deg,#0ea394,#2f5fff); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 12px; }
      .sb-user b { font-size: 12.5px; display: block; color: #fff; }
      .sb-user span { font-size: 10.5px; color: rgba(255,255,255,.5); }
      .main { flex: 1; min-width: 0; }
      .content { padding: 28px 32px; }
      .page-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
      .page-head h1 { font-size: 22px; font-weight: 800; color: #0e1a3a; margin-bottom: 4px; }
      .page-head p { font-size: 13px; color: #66708a; margin: 0; }
      .grid-2 { display: grid; }
      .card { background: #fff; border: 1px solid #e5e9f3; border-radius: 16px; box-shadow: 0 1px 3px rgba(15,26,58,.06); overflow: hidden; }
      .card-head { padding: 18px 22px; border-bottom: 1px solid #e5e9f3; }
      .card-head h3 { font-size: 14px; font-weight: 800; margin: 0; color: #0e1a3a; display: flex; align-items: center; }
      .card-body { padding: 20px 22px; }
      .factor-row { padding: 9px 0; border-bottom: 1px dashed #e5e9f3; }
      .factor-row:last-child { border-bottom: none; }
      .factor-top { display: flex; justify-content: space-between; font-size: 12.5px; }
      .factor-top b { font-weight: 600; color: #66708a; }
      .bureau-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 14px; }
      .bureau-box { background: #f6f8fd; border: 1px solid #e5e9f3; border-radius: 10px; padding: 10px 12px; text-align: center; }
      .bureau-box span { font-size: 10.5px; color: #66708a; font-weight: 600; display: block; }
      .bureau-box b { display: block; font-family: 'DM Mono', monospace; font-size: 13px; margin-top: 3px; }
      .chip { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
      .chip-rejected { background: #fef1f1; color: #e03131; }
      .ai-chip { display: inline-flex; align-items: center; gap: 4px; font-size: 10.5px; font-weight: 700; color: #7c5cff; background: #f2efff; border-radius: 20px; padding: 3px 10px; }
      .ai-chip::before { content: '✦'; }
      .feed-item { display: flex; gap: 12px; padding: 13px 0; border-bottom: 1px solid #e5e9f3; font-size: 12.5px; }
      .feed-item:last-child { border-bottom: none; }
      .feed-dot { width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 13px; }
      .feed-text b { color: #0e1a3a; }
      .feed-time { font-size: 11px; color: #66708a; margin-top: 2px; }
      .btn-sm { padding: 9px 15px; border-radius: 9px; border: 1px solid #e5e9f3; background: #fff; font-size: 12.5px; font-weight: 700; color: #101a33; cursor: pointer; }
      .btn-sm.dark { background: #0e1a3a; color: #fff; border: none; }
    </style>
</head>
<body>
  <div id="collections-ai-view">
    <div class="app-shell">
      <aside class="sidebar">
        <div class="sb-brand"><div class="logo-mark">CS</div><div><b>CrediSphere</b><span>Lender Console</span></div></div>
        <div class="sb-section-label">Overview</div>
        <a href="admin-dashboard.html" class="sb-item"><span class="ic">📊</span> Dashboard</a>
        <a href="credit-intelligence.html" class="sb-item"><span class="ic">🧠</span> Credit Intelligence</a>
        <a href="loan-application.html" class="sb-item"><span class="ic">📄</span> Loan Applications</a>
        <div class="sb-section-label">Recovery</div>
        <a href="collections-ai.html" class="sb-item active"><span class="ic">📞</span> Collections AI</a>
        <div class="sb-item"><span class="ic">⚖️</span> Legal &amp; Repossession</div>
        <div class="sb-section-label">Management</div>
        <a href="customers.html" class="sb-item"><span class="ic">👥</span> Customers</a>
        <a href="reports.html" class="sb-item"><span class="ic">📈</span> Reports</a>
        <a href="risk-policy.html" class="sb-item"><span class="ic">⚙️</span> Risk Policy Config</a>
        <a href="screen-configuration.html" class="sb-item"><span class="ic">🖥️</span> Screen Configuration</a>
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
                  <div class="q-meter-wrap" id="q-distribution-meters"></div>

                  <div style="font-size:11px;font-weight:700;color:var(--navy);margin-top:12px;margin-bottom:6px;">Random Forest Feature Weights:</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:10.5px;" id="rf-feature-weights"></div>
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
        <footer class="proto-foot" style="padding:26px;text-align:center;font-size:11.5px;color:var(--muted);">CrediSphere AI · Collections Intelligence Module · MCA Project Prototype</footer>
      </div>
    </div>
  </div>

  <!-- MODALS -->
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
      <div class="call-body" id="call-transcript-stream">
        <div style="text-align:center;font-size:11px;color:var(--muted);margin-bottom:12px;" id="call-callout-msg">
          🔒 VoIP encrypted line · Simulated AI Agent Intervention
        </div>
      </div>
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
          <button class="channel-btn active" id="chan-sms" onclick="switchMsgChannel('sms')">💬 SMS Gateway</button>
          <button class="channel-btn" id="chan-wa" onclick="switchMsgChannel('whatsapp')">🟢 WhatsApp Business</button>
        </div>
        <div class="template-select-wrap">
          <label>AI-Generated Message Template</label>
          <select id="sms-template-select" onchange="onTemplateChange()">
            <option value="settlement">★ Structured Settlement Token Offer (Recommended by DQN)</option>
            <option value="reminder">Standard DPD 90 Overdue Reminder</option>
            <option value="urgent">Urgent Pre-Legal Escalation Notice</option>
          </select>
          <textarea class="template-textarea" id="sms-message-text"></textarea>
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
          <button onclick="sendSMSLink()" class="btn-sm" style="background:var(--blue);color:#fff;border:none;padding:8px 20px;font-weight:700;">🚀 Send Now</button>
        </div>
      </div>
    </div>
  </div>

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
          <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px;"><span style="color:var(--muted);">Original Balance:</span><b>₹3,72,000</b></div>
          <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px;"><span style="color:var(--muted);">Upfront Token:</span><b style="color:var(--green);font-size:13px;">₹40,000</b></div>
          <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px;"><span style="color:var(--muted);">Restructured Repayment:</span><b>₹33,200 / mo x 10</b></div>
          <div style="display:flex;justify-content:space-between;font-size:12px;"><span style="color:var(--muted);">Penalty Waived:</span><b style="color:var(--blue);">₹24,000</b></div>
        </div>
        <div style="display:flex;justify-content:flex-end;gap:10px;">
          <button onclick="closeSettlementModal()" class="btn-sm">Cancel</button>
          <button onclick="confirmSettlementAgreement()" class="btn-sm" style="background:var(--green);color:#fff;border:none;padding:8px 20px;font-weight:700;">✍️ Issue Agreement</button>
        </div>
      </div>
    </div>
  </div>

  <div class="ai-drawer-backdrop" id="coll-ai-drawer" onclick="handleDrawerBackdropClick(event)">
    <div class="ai-drawer-box">
      <div class="ai-drawer-head">
        <div>
          <div style="display:flex;align-items:center;gap:6px;font-weight:800;font-size:13.5px;"><span>🤖</span> CrediSphere Collections AI Copilot</div>
          <span style="font-size:10.5px;opacity:0.8;">Context: Farid Sheikh · DPD 90 · Overdue ₹3,72,000</span>
        </div>
        <button onclick="closeCollAIDrawer()" style="background:none;border:none;color:#fff;font-size:18px;cursor:pointer;">✕</button>
      </div>
      <div class="ai-drawer-body" id="ai-drawer-body">
        <div class="ai-prompt-chips">
          <button class="ai-chip-prompt" onclick="askPresetQuestion('Why does RL recommend settlement over repossession?')">⚖️ Why does RL recommend settlement over repossession?</button>
          <button class="ai-chip-prompt" onclick="askPresetQuestion('Why is 5–7 PM the optimal contact window?')">⏰ Why is 5–7 PM the optimal contact window?</button>
          <button class="ai-chip-prompt" onclick="askPresetQuestion('What happens if Farid defaults on this PTP?')">🛡️ What happens if Farid defaults on this PTP?</button>
          <button class="ai-chip-prompt" onclick="askPresetQuestion('Explain Random Forest risk attribution')">🌲 Explain Random Forest risk attribution</button>
        </div>
        <div class="ai-chat-thread" id="ai-chat-thread">
          <div class="ai-msg bot"><div class="msg-bubble">Hello Anita! I am your <b>Collections AI Copilot</b>. I have evaluated Farid Sheikh with our Random Forest predictor &amp; Deep Q-Network. Ask me any question!</div></div>
        </div>
      </div>
      <div class="ai-drawer-foot">
        <input type="text" class="ai-drawer-input" id="ai-user-query" placeholder="Ask AI Copilot..." onkeydown="if(event.key==='Enter') sendCustomAIQuery()">
        <button class="ai-drawer-send" onclick="sendCustomAIQuery()">Send</button>
      </div>
    </div>
  </div>

  <div id="coll-toast-container"></div>

  <script>
  class CollectionsMLEngine {
    constructor() {
      this.state = { borrowerName: "Farid Sheikh", accountNo: "LN-2024-88492", phone: "+91 98765-43210", dpd: 90, brokenPromises: 2, bouncedEmis: 3, emiAmount: 120000, totalOverdue: 372000, sentiment: "Negative", bestCallTime: "5–7 PM" };
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
    init() { this.renderQDistribution(); this.renderFeatureWeights(); }
    randomizeState() {
      const dpds = [60, 90, 120], promises = [1, 2, 3], sentiments = ["Negative", "Hostile", "Cooperative"];
      this.state.dpd = dpds[Math.floor(Math.random() * dpds.length)];
      this.state.brokenPromises = promises[Math.floor(Math.random() * promises.length)];
      this.state.sentiment = sentiments[Math.floor(Math.random() * sentiments.length)];
      document.getElementById('txt-dpd-bucket').textContent = `${this.state.dpd} (${this.state.brokenPromises})`;
      document.getElementById('coll-sentiment').textContent = this.state.sentiment;
      document.getElementById('coll-promises-chip').textContent = `Broken Promises: ${this.state.brokenPromises}`;
      this.renderQDistribution();
      showCollToast("Live ML State re-simulated! Random Forest & DQN policies refreshed.", "success");
    }
    renderQDistribution() {
      const c = document.getElementById('q-distribution-meters'); if (!c) return;
      c.innerHTML = this.actions.map(a => `
        <div class="q-meter-row">
          <span class="q-meter-name" title="${a.name}">${a.isOptimal ? '★ ' : ''}${a.name}</span>
          <div class="q-meter-bar-bg"><div class="q-meter-bar-fill" style="width:${a.pct}%;background:${a.color};"></div></div>
          <span class="q-meter-val" style="color:${a.color};">${a.qValue > 0 ? '+' : ''}${a.qValue.toFixed(3)}</span>
        </div>
      `).join('');
    }
    renderFeatureWeights() {
      const c = document.getElementById('rf-feature-weights'); if (!c) return;
      c.innerHTML = this.featureImportances.map(f => `
        <div style="background:#fff;border:1px solid var(--border);border-radius:6px;padding:5px 8px;display:flex;justify-content:space-between;">
          <span style="color:var(--muted);">${f.feature}:</span><b style="color:var(--navy);font-family:'DM Mono',monospace;">${f.weight}</b>
        </div>
      `).join('');
    }
  }

  const collectionsML = new CollectionsMLEngine();
  window.addEventListener('load', () => collectionsML.init());

  function toggleMLEngineInsights() {
    const p = document.getElementById('coll-insights-panel');
    const b = document.getElementById('coll-toggle-insights-btn');
    if (!p || !b) return;
    const isHidden = p.style.display === 'none';
    p.style.display = isHidden ? 'block' : 'none';
    b.classList.toggle('expanded', isHidden);
  }

  let callTimerInterval = null, callDurationSeconds = 0, callStepTimeout = null, isCallMuted = false;
  function openLiveCallModal() {
    const modal = document.getElementById('coll-call-modal');
    modal.classList.add('open');
    document.getElementById('call-avatar-ring').classList.add('ringing');
    document.getElementById('call-status-pill').classList.remove('connected');
    document.getElementById('call-status-text').textContent = "Connecting to SIP Gateway...";
    document.getElementById('call-transcript-stream').innerHTML = '<div style="text-align:center;font-size:11px;color:var(--muted);margin-bottom:12px;">🔒 VoIP encrypted line · Simulated AI Agent Intervention</div>';
    callDurationSeconds = 0; isCallMuted = false; updateMuteButtonUI();

    callStepTimeout = setTimeout(() => {
      document.getElementById('call-status-text').textContent = "Ringing... (+91 98765-43210)";
      setTimeout(() => {
        document.getElementById('call-avatar-ring').classList.remove('ringing');
        document.getElementById('call-status-pill').classList.add('connected');
        startCallTimer(); runCallConversationScript();
      }, 2000);
    }, 1200);
  }

  function startCallTimer() {
    callTimerInterval = setInterval(() => {
      callDurationSeconds++;
      const m = String(Math.floor(callDurationSeconds / 60)).padStart(2, '0');
      const s = String(callDurationSeconds % 60).padStart(2, '0');
      document.getElementById('call-status-text').textContent = `Live Connected (${m}:${s})`;
    }, 1000);
  }

  function runCallConversationScript() {
    const stream = document.getElementById('call-transcript-stream');
    const script = [
      { sender: "agent", text: "Namaste Mr. Sheikh, this is CrediSphere Collections regarding your overdue EMI of ₹1,20,000." },
      { sender: "borrower", text: "Namaste. I had urgent medical expenses, but I can arrange ₹40,000 upfront this Friday if you waive late fees." },
      { sender: "agent", text: "Approved Mr. Sheikh! Pay ₹40,000 by 5 PM Friday, and we will restructure the rest across 10 months." },
      { sender: "borrower", text: "Excellent, thank you. Please send the payment link immediately." }
    ];
    script.forEach((item, idx) => {
      setTimeout(() => {
        if (!document.getElementById('coll-call-modal').classList.contains('open')) return;
        const b = document.createElement('div');
        b.className = `transcript-bubble ${item.sender}`;
        b.innerHTML = `<span class="bubble-tag">${item.sender === 'agent' ? '🤖 Voice AI' : '👤 Farid Sheikh'}</span><div class="bubble-content">${item.text}</div>`;
        stream.appendChild(b);
        stream.scrollTop = stream.scrollHeight;
        if (idx === script.length - 1) togglePTPDrawer(true);
      }, (idx + 1) * 2200);
    });
  }

  function toggleCallMute() { isCallMuted = !isCallMuted; updateMuteButtonUI(); showCollToast(isCallMuted ? "Microphone muted" : "Microphone unmuted"); }
  function updateMuteButtonUI() { const b = document.getElementById('btn-call-mute'); if (b) b.classList.toggle('active', isCallMuted); }
  function togglePTPDrawer(force) { const d = document.getElementById('ptp-inline-drawer'); if (d) d.classList.toggle('open', typeof force === 'boolean' ? force : !d.classList.contains('open')); }
  function confirmRecordPTP() {
    const amt = document.getElementById('ptp-amount-input').value || "₹40,000";
    togglePTPDrawer(false);
    appendFollowUpFeed("📞", `<b>PTP Recorded</b> — ${amt} promised by 12-Dec-2025`, "Just now");
    showCollToast(`Promise to Pay of ${amt} recorded successfully!`, "success");
  }
  function endLiveCall() {
    clearInterval(callTimerInterval); clearTimeout(callStepTimeout);
    document.getElementById('coll-call-modal').classList.remove('open');
    if (callDurationSeconds > 0) {
      appendFollowUpFeed("📞", `<b>Simulated Call Ended</b> — Borrower committed to ₹40,000 upfront token`, "Just now");
      showCollToast("Call ended. Follow-up history updated.", "success");
    }
  }

  const SMS_TEMPLATES = {
    settlement: "Urgent: CrediSphere one-time settlement offer valid until 5 PM today. Pay ₹40,000 upfront token to waive ₹24,000 penalties: https://pay.credisphere.ai/s/F92K1",
    reminder: "Dear Farid Sheikh, overdue EMI of ₹1,20,000 is pending. Avoid escalation by paying here: https://pay.credisphere.ai/pay/88492",
    urgent: "FINAL NOTICE: Account LN-2024-88492 at DPD 90. Clear balance or contact collections: https://pay.credisphere.ai/legal/88492"
  };
  let currentChannel = 'sms';
  function openSMSModal() { document.getElementById('coll-sms-modal').classList.add('open'); onTemplateChange(); }
  function closeSMSModal() { document.getElementById('coll-sms-modal').classList.remove('open'); }
  function switchMsgChannel(ch) {
    currentChannel = ch;
    document.getElementById('chan-sms').classList.toggle('active', ch === 'sms');
    document.getElementById('chan-wa').classList.toggle('active', ch === 'whatsapp');
  }
  function onTemplateChange() {
    const v = document.getElementById('sms-template-select').value;
    document.getElementById('sms-message-text').value = SMS_TEMPLATES[v] || SMS_TEMPLATES.settlement;
  }
  function sendSMSLink() {
    const ch = currentChannel === 'sms' ? 'SMS Gateway' : 'WhatsApp Business';
    closeSMSModal();
    showCollToast(`${ch} successfully dispatched (Status: Delivered · ID: msg_${Math.random().toString(36).substring(7)})`, "success");
    appendFollowUpFeed("📩", `<b>Payment Link Sent via ${ch}</b> — ₹40,000 settlement token link`, "Just now");
  }

  function openSettlementModal() { document.getElementById('coll-settlement-modal').classList.add('open'); }
  function closeSettlementModal() { document.getElementById('coll-settlement-modal').classList.remove('open'); }
  function confirmSettlementAgreement() {
    closeSettlementModal();
    showCollToast("Settlement agreement generated and queued to borrower via SMS/Email.", "success");
    appendFollowUpFeed("📑", `<b>Settlement Agreement Issued</b> — ₹40,000 upfront + ₹33,200/mo x 10 (penalties waived)`, "Just now");
  }

  const AI_COPILOT_KNOWLEDGE = {
    "Why does RL recommend settlement over repossession?": "<b>Deep Q-Network (DQN) Policy Analysis:</b><br><br>1. <b>Recovery Value:</b> At DPD 90 with 2 broken promises, repossession yields net <b>42.1%</b> after a 180+ day court freeze ($Q = -0.150$).<br><br>2. <b>Cash Velocity:</b> A structured settlement with ₹40,000 upfront locks in an expected recovery rate of <b>68.4%</b> ($Q = +0.812$).",
    "Why is 5–7 PM the optimal contact window?": "<b>Temporal Optimization Engine:</b> Answer rates jump to <b>74.2%</b> between 5:00 PM and 7:00 PM (vs 23.8% midday), leading to <b>2.3x higher PTP conversion</b>.",
    "What happens if Farid defaults on this PTP?": "<b>Next-Best-Action Transition:</b> State updates to (DPD 95, Promises 3) triggering legal arbitration notices under SARFAESI and field recovery dispatch.",
    "Explain Random Forest risk attribution": "<b>Random Forest Risk (High · 78.6%):</b><br>• DPD 90+ (38% weight)<br>• Broken Promises (27% weight)<br>• Negative Sentiment (18% weight)<br>• 3 Bounced EMIs (17% weight)"
  };
  function openCollAIDrawer() { document.getElementById('coll-ai-drawer').classList.add('open'); }
  function closeCollAIDrawer() { document.getElementById('coll-ai-drawer').classList.remove('open'); }
  function handleDrawerBackdropClick(e) { if (e.target.id === 'coll-ai-drawer') closeCollAIDrawer(); }
  function askPresetQuestion(q) {
    addChatMessage("user", q);
    setTimeout(() => {
      const a = AI_COPILOT_KNOWLEDGE[q] || "Based on historical recovery data for DPD 90 accounts, the model prioritizes structured settlement over confrontational actions.";
      addChatMessage("bot", a);
    }, 400);
  }
  function sendCustomAIQuery() {
    const inp = document.getElementById('ai-user-query');
    const q = inp.value.trim(); if (!q) return;
    addChatMessage("user", q); inp.value = '';
    setTimeout(() => {
      addChatMessage("bot", `Based on Farid Sheikh's DPD 90 profile and current state vector, our <b>DQN agent</b> strongly favors structured token settlement with contact scheduled for <b>5–7 PM</b>.`);
    }, 450);
  }
  function addChatMessage(sender, html) {
    const t = document.getElementById('ai-chat-thread');
    const m = document.createElement('div');
    m.className = `ai-msg ${sender}`;
    m.innerHTML = `<div class="msg-bubble">${html}</div>`;
    t.appendChild(m);
    t.parentElement.scrollTop = t.parentElement.scrollHeight;
  }
  function appendFollowUpFeed(icon, html, time) {
    const c = document.getElementById('coll-feed-container'); if (!c) return;
    const item = document.createElement('div');
    item.className = "feed-item"; item.style.animation = "fadeInColl 0.35s ease";
    item.innerHTML = `<div class="feed-dot" style="background:var(--blue-light);">${icon}</div><div><div class="feed-text">${html}</div><div class="feed-time" style="color:var(--blue);font-weight:700;">${time}</div></div>`;
    c.insertBefore(item, c.firstChild);
  }
  function showCollToast(msg, type) {
    const c = document.getElementById('coll-toast-container'); if (!c) return;
    const t = document.createElement('div');
    t.className = `coll-toast ${type === 'success' ? 'success' : ''}`;
    t.innerHTML = `<span>${type === 'success' ? '✅' : '🔔'}</span><span>${msg}</span>`;
    c.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 300); }, 4000);
  }
  </script>
</body>
</html>
"""

with open(PAGE_PATH, 'w', encoding='utf-8') as f:
    f.write(page_html)
print(f"Saved: {PAGE_PATH}")
