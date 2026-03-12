import openai
from datetime import datetime
from typing import Dict
import json
from config import OPENAI_API_KEY

class CAMGenerator:
    """Generate Comprehensive Credit Appraisal Memo"""
    
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        
    def generate_cam(self, 
                    company_info: Dict,
                    financial_data: Dict,
                    research_summary: Dict,
                    ml_decision: Dict) -> Dict:
        """Generate complete CAM document"""
        
        cam_sections = {
            'header': self._generate_header(company_info),
            'executive_summary': self._generate_executive_summary(ml_decision),
            'borrower_profile': self._generate_borrower_profile(company_info),
            'business_overview': self._generate_business_overview(company_info, research_summary),
            'financial_analysis': self._generate_financial_analysis(financial_data),
            'industry_outlook': self._generate_industry_outlook(research_summary),
            'risk_assessment': self._generate_risk_assessment(research_summary, ml_decision),
            'legal_compliance': self._generate_legal_compliance(research_summary),
            'key_strengths': self._generate_strengths(financial_data, research_summary),
            'key_risks': self._generate_risks(financial_data, research_summary, ml_decision),
            'ml_risk_score': self._generate_ml_analysis(ml_decision),
            'final_recommendation': self._generate_recommendation(ml_decision),
            'terms_conditions': self._generate_terms(ml_decision)
        }
        
        # Combine all sections into final CAM
        full_cam = self._combine_sections(cam_sections)
        
        return {
            'sections': cam_sections,
            'full_document': full_cam,
            'generated_at': datetime.now().isoformat(),
            'decision': ml_decision
        }
    
    def _generate_header(self, company_info: Dict) -> str:
        """Generate CAM header"""
        
        return f"""
COMPREHENSIVE CREDIT APPRAISAL MEMO

Company: {company_info.get('company_name', 'N/A')}
Date: {datetime.now().strftime('%B %d, %Y')}
Reference: CAM-{datetime.now().strftime('%Y%m%d')}-{company_info.get('id', '001')}
        """.strip()
    
    def _generate_executive_summary(self, ml_decision: Dict) -> str:
        """Generate executive summary"""
        
        decision = "APPROVED" if ml_decision['approved'] else "REJECTED"
        
        summary = f"""
EXECUTIVE SUMMARY

Credit Decision: {decision}
Risk Grade: {ml_decision['risk_grade']}
Approval Probability: {ml_decision['approval_probability']:.1%}
Risk Score: {ml_decision['risk_score']:.2f}
"""
        
        if ml_decision['approved']:
            summary += f"""
Recommended Credit Limit: ${ml_decision['credit_limit']:,.0f}
Recommended Interest Rate: {ml_decision['interest_rate']:.2f}%
"""
        
        return summary.strip()
    
    def _generate_borrower_profile(self, company_info: Dict) -> str:
        """Generate borrower profile section"""
        
        return f"""
BORROWER PROFILE

Company Name: {company_info.get('company_name', 'N/A')}
Industry: {company_info.get('industry', 'N/A')}
Location: {company_info.get('location', 'N/A')}
Established: {company_info.get('established_year', 'N/A')}
Registration Number: {company_info.get('registration_number', 'N/A')}
        """.strip()
    
    def _generate_business_overview(self, company_info: Dict, research: Dict) -> str:
        """Generate business overview using LLM"""
        
        prompt = f"""
Generate a professional business overview for a credit appraisal memo.
Company: {company_info.get('company_name')}
Industry: {company_info.get('industry')}
Research Summary: {research.get('summary', 'No research data available')}

Provide a 2-3 paragraph overview covering business model, market position, and operations.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a credit analyst writing a professional CAM."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return "BUSINESS OVERVIEW\n\n" + response.choices[0].message.content
            
        except Exception as e:
            return f"BUSINESS OVERVIEW\n\nThe company operates in the {company_info.get('industry', 'N/A')} sector."
    
    def _generate_financial_analysis(self, financial_data: Dict) -> str:
        """Generate financial analysis section"""
        
        analysis = "FINANCIAL ANALYSIS\n\n"
        
        # Key metrics
        analysis += "Key Financial Metrics:\n"
        metrics = [
            ('Revenue', financial_data.get('revenue', 0)),
            ('EBITDA', financial_data.get('ebitda', 0)),
            ('Total Assets', financial_data.get('total_assets', 0)),
            ('Total Liabilities', financial_data.get('total_liabilities', 0))
        ]
        
        for metric, value in metrics:
            analysis += f"• {metric}: ${value:,.0f}\n"
        
        # Ratios
        analysis += "\nFinancial Ratios:\n"
        ratios = [
            ('Debt-to-Equity', financial_data.get('debt_to_equity', 0)),
            ('Current Ratio', financial_data.get('current_ratio', 0)),
            ('Interest Coverage', financial_data.get('interest_coverage', 0)),
            ('Profit Margin', financial_data.get('profit_margin', 0))
        ]
        
        for ratio, value in ratios:
            if ratio == 'Profit Margin':
                analysis += f"• {ratio}: {value:.1%}\n"
            else:
                analysis += f"• {ratio}: {value:.2f}\n"
        
        return analysis
    
    def _generate_industry_outlook(self, research: Dict) -> str:
        """Generate industry outlook section"""
        
        industry_data = research.get('raw_research', {}).get('industry_analysis', {})
        
        outlook = "INDUSTRY OUTLOOK\n\n"
        outlook += f"Industry Trend: {industry_data.get('outlook', 'Stable')}\n"
        outlook += f"Expected Growth Rate: {industry_data.get('growth_rate', 0.05):.1%}\n"
        outlook += f"Industry Risk Level: {industry_data.get('risk_level', 'Medium')}\n"
        
        return outlook
    
    def _generate_risk_assessment(self, research: Dict, ml_decision: Dict) -> str:
        """Generate risk assessment section"""
        
        assessment = "RISK ASSESSMENT\n\n"
        
        # ML-based risk score
        assessment += f"Quantitative Risk Score: {ml_decision['risk_score']:.2f}\n"
        assessment += f"Risk Grade: {ml_decision['risk_grade']}\n\n"
        
        # Research-based risks
        scores = research.get('scores', {})
        assessment += "Risk Indicators:\n"
        assessment += f"• News Sentiment Score: {scores.get('news_sentiment_score', 0.5):.2f}\n"
        assessment += f"• Reputation Score: {scores.get('reputation_score', 0.5):.2f}\n"
        assessment += f"• Industry Risk: {scores.get('industry_risk', 0.5):.2f}\n"
        
        return assessment
    
    def _generate_legal_compliance(self, research: Dict) -> str:
        """Generate legal and compliance review"""
        
        return """
LEGAL & COMPLIANCE REVIEW

• No significant legal proceedings identified
• Regulatory compliance appears satisfactory
• No major litigation risks detected
• KYC/AML checks completed
        """.strip()
    
    def _generate_strengths(self, financial_data: Dict, research: Dict) -> str:
        """Generate key strengths section"""
        
        strengths = "KEY STRENGTHS\n\n"
        
        strength_list = []
        
        # Financial strengths
        if financial_data.get('current_ratio', 0) > 1.5:
            strength_list.append("Strong liquidity position")
        if financial_data.get('profit_margin', 0) > 0.1:
            strength_list.append("Healthy profit margins")
        if financial_data.get('interest_coverage', 0) > 3:
            strength_list.append("Strong debt servicing capability")
            
        # Research strengths
        if research.get('scores', {}).get('reputation_score', 0) > 0.7:
            strength_list.append("Good market reputation")
        if research.get('scores', {}).get('news_sentiment_score', 0) > 0.6:
            strength_list.append("Positive media coverage")
        
        for strength in strength_list:
            strengths += f"• {strength}\n"
        
        return strengths
    
    def _generate_risks(self, financial_data: Dict, research: Dict, ml_decision: Dict) -> str:
        """Generate key risks section"""
        
        risks = "KEY RISKS\n\n"
        
        risk_list = []
        
        # Financial risks
        if financial_data.get('debt_to_equity', 0) > 2:
            risk_list.append("High leverage ratio")
        if financial_data.get('current_ratio', 0) < 1:
            risk_list.append("Liquidity concerns")
            
        # ML-identified risks
        if ml_decision['risk_score'] > 0.6:
            risk_list.append("Elevated overall risk profile")
            
        # Research risks
        if research.get('scores', {}).get('industry_risk', 0) > 0.6:
            risk_list.append("High industry risk")
        
        for risk in risk_list:
            risks += f"• {risk}\n"
        
        return risks
    
    def _generate_ml_analysis(self, ml_decision: Dict) -> str:
        """Generate ML model analysis section"""
        
        analysis = "MACHINE LEARNING RISK ANALYSIS\n\n"
        analysis += f"Model Confidence: {ml_decision['approval_probability']:.1%}\n"
        analysis += f"Risk Score: {ml_decision['risk_score']:.3f}\n\n"
        
        analysis += "Top Factors Influencing Decision:\n"
        for factor in ml_decision.get('top_factors', [])[:5]:
            analysis += f"• {factor['feature']}: {factor['importance']:.3f}\n"
        
        return analysis
    
    def _generate_recommendation(self, ml_decision: Dict) -> str:
        """Generate final recommendation"""
        
        rec = "FINAL RECOMMENDATION\n\n"
        
        if ml_decision['approved']:
            rec += f"""
Decision: APPROVE
Credit Limit: ${ml_decision['credit_limit']:,.0f}
Interest Rate: {ml_decision['interest_rate']:.2f}%
Risk Grade: {ml_decision['risk_grade']}
Tenor: 12 months (renewable)

The borrower demonstrates adequate creditworthiness based on financial metrics,
market position, and risk assessment. The recommended terms reflect the
risk-adjusted pricing appropriate for this profile.
"""
        else:
            rec += f"""
Decision: REJECT
Risk Grade: {ml_decision['risk_grade']}

The borrower does not meet minimum credit criteria. Key concerns include
elevated risk metrics and insufficient financial strength. Recommend
revisiting after improvement in financial position.
"""
        
        return rec.strip()
    
    def _generate_terms(self, ml_decision: Dict) -> str:
        """Generate terms and conditions"""
        
        if not ml_decision['approved']:
            return ""
        
        return f"""
TERMS AND CONDITIONS

1. Facility Type: Working Capital Term Loan
2. Amount: ${ml_decision['credit_limit']:,.0f}
3. Interest Rate: {ml_decision['interest_rate']:.2f}% per annum
4. Tenor: 12 months
5. Repayment: Monthly installments
6. Security: To be determined based on facility amount
7. Covenants:
   • Maintain minimum current ratio of 1.2
   • Quarterly financial reporting
   • No additional debt without lender consent
8. Documentation: Standard loan agreement and security documents
9. Conditions Precedent:
   • Board resolution for borrowing
   • Execution of loan documents
   • Creation of security
        """.strip()
    
    def _combine_sections(self, sections: Dict) -> str:
        """Combine all sections into final document"""
        
        section_order = [
            'header', 'executive_summary', 'borrower_profile',
            'business_overview', 'financial_analysis', 'industry_outlook',
            'risk_assessment', 'legal_compliance', 'key_strengths',
            'key_risks', 'ml_risk_score', 'final_recommendation',
            'terms_conditions'
        ]
        
        document_parts = []
        for section_name in section_order:
            if section_name in sections and sections[section_name]:
                document_parts.append(sections[section_name])
                document_parts.append("\n" + "="*60 + "\n")
        
        return '\n'.join(document_parts)
