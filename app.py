import gradio as gr
import pandas as pd
import numpy as np

def predict_churn_risk(age, tenure, monthly_charges, support_calls, 
                      contract_type, payment_method, customer_type):
    """AI-powered customer churn risk prediction"""
    try:
        # Base risk score
        risk_score = 0
        
        # Age factor
        if age < 25: risk_score += 25
        elif age < 35: risk_score += 15
        elif age > 60: risk_score += 10
        
        # Tenure factor
        if tenure < 6: risk_score += 30
        elif tenure < 12: risk_score += 20
        elif tenure < 24: risk_score += 10
        
        # Monthly charges factor
        if monthly_charges > 100: risk_score += 20
        elif monthly_charges > 70: risk_score += 15
        
        # Support calls factor
        risk_score += support_calls * 8
        
        # Contract type factor
        contract_weights = {"Monthly": 25, "Quarterly": 15, "Annual": 5, "Two-Year": 0}
        risk_score += contract_weights.get(contract_type, 15)
        
        # Payment method factor
        payment_weights = {"Electronic": 0, "Credit Card": 5, "Bank Transfer": 10, "Manual": 20}
        risk_score += payment_weights.get(payment_method, 10)
        
        # Customer type adjustments
        type_weights = {"Young Professional": -5, "Family User": -10, "Senior Citizen": 5, "Student": 15, "Business User": -15}
        risk_score += type_weights.get(customer_type, 0)
        
        # Normalize risk score
        risk_score = max(0, min(100, risk_score))
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "🚨 CRITICAL"
            probability = "85-100%"
            recommendation = "• Personal call from manager\n• Special discount offer\n• Service review meeting"
        elif risk_score >= 50:
            risk_level = "⚠️ HIGH" 
            probability = "65-84%"
            recommendation = "• Loyalty program offer\n• Feature education\n• Satisfaction survey"
        elif risk_score >= 30:
            risk_level = "📊 MEDIUM"
            probability = "35-64%"
            recommendation = "• Regular check-in calls\n• Newsletter\n• Usage tips"
        else:
            risk_level = "✅ LOW"
            probability = "0-34%"
            recommendation = "• Continue excellent service\n• Upsell opportunities\n• Referral program"
        
        return f"""
**CUSTOMER CHURN RISK ASSESSMENT**

🎯 **Risk Level**: {risk_level}
📊 **Risk Score**: {risk_score}/100
📈 **Churn Probability**: {probability}

**CUSTOMER PROFILE:**
• Age: {age} years
• Tenure: {tenure} months  
• Monthly Charges: ${monthly_charges}
• Support Calls: {support_calls} this month
• Contract: {contract_type}
• Payment: {payment_method}
• Profile: {customer_type}

**💡 RETENTION STRATEGY:**
{recommendation}

---
*AI-powered business intelligence for customer retention*
"""
        
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 👥 AI Customer Churn Predictor")
    
    with gr.Row():
        with gr.Column():
            age = gr.Slider(18, 80, value=35, label="Customer Age")
            tenure = gr.Slider(1, 60, value=12, label="Tenure (Months)")
            monthly_charges = gr.Slider(20, 200, value=75, label="Monthly Charges ($)")
            support_calls = gr.Slider(0, 10, value=2, label="Support Calls")
            
            contract_type = gr.Radio(
                choices=["Monthly", "Quarterly", "Annual", "Two-Year"],
                value="Monthly",
                label="Contract Type"
            )
            
            payment_method = gr.Radio(
                choices=["Electronic", "Credit Card", "Bank Transfer", "Manual"],
                value="Credit Card", 
                label="Payment Method"
            )
            
            customer_type = gr.Dropdown(
                choices=["Young Professional", "Family User", "Senior Citizen", "Student", "Business User"],
                value="Young Professional",
                label="Customer Profile"
            )
            
            analyze_btn = gr.Button("Analyze Churn Risk", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(label="Risk Analysis Report", lines=15, show_copy_button=True)
    
    analyze_btn.click(predict_churn_risk, 
                     [age, tenure, monthly_charges, support_calls, contract_type, payment_method, customer_type], 
                     output)

if __name__ == "__main__":
    demo.launch()
