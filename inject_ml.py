import os
import re

modules = {
    'loan-application.html': {
        'title': 'Loan Application Form',
        'ml': 'Powered by LightGBM / CatBoost AI',
        'desc': 'Real-time applicant data validation and eligibility estimation prior to final submission.'
    },
    'kyc-upload.html': {
        'title': 'KYC Document Upload',
        'ml': 'Powered by EasyOCR/Tesseract + YOLOv8 Vision AI',
        'desc': 'Automated PAN/Aadhaar extraction and deep-learning based fake document detection.'
    },
    'credit-intelligence.html': {
        'title': 'Credit Intelligence & Loan Decision',
        'ml': 'Powered by XGBoost + Graph Neural Networks (GNN) + SHAP',
        'desc': 'Predicting default risk, detecting hidden fraud relationships, and generating explainable AI approval/rejection reports.'
    },
    'collections-ai.html': {
        'title': 'Collections AI',
        'ml': 'Powered by Random Forest + Reinforcement Learning (DQN)',
        'desc': 'Predicting repayment probabilities and recommending optimal recovery strategies and contact times.'
    },
    'risk-policy.html': {
        'title': 'Risk Policy Configuration',
        'ml': 'Powered by Rule Engine + Bayesian Optimization',
        'desc': 'Automatically recommending optimal approval thresholds and risk margins to maximize portfolio yield.'
    },
    'reports.html': {
        'title': 'Reports & Analytics',
        'ml': 'Powered by AutoML + SHAP',
        'desc': 'Generating performance metrics, feature importance tracking, and continuous model monitoring reports.'
    },
    'screen-configuration.html': {
        'title': 'Screen Configuration',
        'ml': 'Powered by Association Rule Mining (Apriori) & Collaborative Filtering',
        'desc': 'Dynamically recommending which widgets and screens should be shown to different user roles.'
    }
}

html_injection_template = """
                <div style="background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e5e9f3; margin-top: 20px;">
                    <h2 style="color: #0e1a3a; margin-bottom: 15px;">{title}</h2>
                    <div style="display: inline-block; background: #eefbf1; color: #17a34a; padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 12px; margin-bottom: 15px;">
                        🧠 {ml}
                    </div>
                    <p style="color: #66708a; font-size: 15px; line-height: 1.6;">
                        {desc}
                    </p>
                    <div style="margin-top: 30px; padding: 20px; background: #f6f8fd; border: 1px dashed #c0ccda; border-radius: 8px; text-align: center; color: #9ca3af;">
                        [ Module UI Components will render here ]
                    </div>
                </div>
"""

base_dir = '/Users/vrindasharma/Desktop/project/CrediSphere-AI/frontend/pages'

for filename, data in modules.items():
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # We replace the <!-- Content goes here --> or the empty content div
        injection = html_injection_template.format(**data)
        
        # Regex to find <div id="content">...</div>
        new_content = re.sub(r'<div id="content">.*?</div>', f'<div id="content">\n{injection}\n</div>', content, flags=re.DOTALL)
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Injected ML logic into {filename}")
    else:
        print(f"Warning: {filename} not found.")
