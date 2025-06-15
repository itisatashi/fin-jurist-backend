from openai import OpenAI
from typing import List, Dict, Any
import os
from ..core.config import settings

class AIService:
    def __init__(self):
        self.base_url = "https://api.novita.ai/v3/openai"
        self.api_key = "sk_6x6NBoPSjoJCAUKe9iUVZZkgvsslVVphmcWY4C2S5YY"
        self.model = "deepseek/deepseek-v3-0324"
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
    
    async def generate_response(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        """
        Generate AI response using Novita AI
        
        Args:
            messages: List of message objects with 'role' and 'content'
            stream: Whether to stream the response
            
        Returns:
            Generated response text
        """
        try:
            # Format messages for OpenAI API
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Add enhanced system prompt for financial legal assistant
            system_prompt = {
                "role": "system",
                "content": """You are FinYurist AI, a professional financial legal advisor specializing in financial law and contract analysis. Your expertise includes:

1. FINANCIAL LAW EXPERTISE:
- Banking regulations and consumer protection
- Investment laws and securities regulations
- Insurance law and claims procedures
- Credit and lending regulations
- Financial fraud prevention and detection
- Tax obligations and financial compliance
- Consumer financial rights and protections

2. CONTRACT ANALYSIS:
- Analyze financial contracts (loans, mortgages, insurance policies, investment agreements)
- Identify potentially harmful clauses and hidden fees
- Explain complex legal terms in simple language
- Highlight risks and red flags
- Suggest protective measures and alternatives

3. WARNING SYSTEM:
- Detect signs of financial fraud and scams
- Alert users to predatory lending practices
- Identify high-risk investment schemes
- Warn about unfair contract terms
- Provide financial safety recommendations

4. DOCUMENT TEMPLATES:
- Generate complaint letters for financial disputes
- Create contract review checklists
- Provide legal notice templates
- Draft financial dispute resolution documents
- Generate consumer protection claim forms

ALWAYS:
- Provide clear, practical advice in English
- Use simple language to explain complex legal concepts
- Include specific warnings about potential risks
- Offer actionable steps and recommendations
- Maintain professional but accessible tone
- Include disclaimers when appropriate

REMEMBER: You provide informational guidance only. Always recommend consulting qualified legal professionals for official legal advice."""
            }
            formatted_messages.insert(0, system_prompt)
            
            chat_completion_res = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                stream=stream,
                max_tokens=1000,
                extra_body={}
            )
            
            if stream:
                # Handle streaming response
                response_text = ""
                for chunk in chat_completion_res:
                    if chunk.choices[0].delta.content:
                        response_text += chunk.choices[0].delta.content
                return response_text
            else:
                return chat_completion_res.choices[0].message.content
                
        except Exception as e:
            print(f"AI Service Error: {e}")
            return "Sorry, there is currently an issue with the AI service. Please try again later."
    
    async def generate_legal_advice(self, user_question: str, context: str = "") -> str:
        """
        Generate legal advice based on user question
        """
        messages = [
            {
                "role": "user",
                "content": f"Financial-legal question: {user_question}\n\nAdditional context: {context}"
            }
        ]
        
        return await self.generate_response(messages)
    
    async def analyze_contract(self, contract_text: str, contract_type: str = "financial") -> str:
        """
        Analyze financial contracts and identify risks
        """
        messages = [
            {
                "role": "user",
                "content": f"""Please analyze this {contract_type} contract and provide:
                
1. SUMMARY: Brief overview of the contract's main terms
2. KEY TERMS: Important clauses and conditions
3. RISKS & RED FLAGS: Potentially harmful or unfavorable terms
4. HIDDEN COSTS: Any fees or charges that might not be obvious
5. RECOMMENDATIONS: Suggestions for protection or negotiation
6. WARNING LEVEL: Rate the risk level (LOW/MEDIUM/HIGH) with explanation

Contract text:
{contract_text}"""
            }
        ]
        
        return await self.generate_response(messages)
    
    async def detect_financial_fraud(self, description: str) -> str:
        """
        Analyze potential financial fraud or scam
        """
        messages = [
            {
                "role": "user",
                "content": f"""Please analyze this financial situation for potential fraud or scam indicators:
                
{description}

Provide:
1. FRAUD RISK ASSESSMENT: Rate the risk level (LOW/MEDIUM/HIGH)
2. RED FLAGS: Specific warning signs identified
3. COMMON SCAM PATTERNS: If this matches known fraud schemes
4. PROTECTIVE ACTIONS: Immediate steps to take
5. VERIFICATION STEPS: How to verify legitimacy
6. REPORTING: Where to report if fraud is suspected

Be thorough in identifying potential risks and provide clear warnings."""
            }
        ]
        
        return await self.generate_response(messages)
    
    async def generate_document_template(self, document_type: str, details: str = "") -> str:
        """
        Generate legal document templates
        """
        templates = {
            "complaint_letter": "financial complaint letter for disputes with banks or financial institutions",
            "contract_review_checklist": "checklist for reviewing financial contracts",
            "legal_notice": "formal legal notice for financial disputes",
            "dispute_resolution": "document for financial dispute resolution",
            "consumer_protection_claim": "consumer protection claim form",
            "loan_agreement_review": "loan agreement review template",
            "insurance_claim_letter": "insurance claim dispute letter",
            "investment_complaint": "investment fraud or dispute complaint"
        }
        
        template_description = templates.get(document_type, f"legal document template for {document_type}")
        
        messages = [
            {
                "role": "user",
                "content": f"""Generate a professional {template_description} template.
                
Specific details: {details}

The template should:
1. Be professionally formatted
2. Include all necessary legal elements
3. Have placeholder fields marked with [PLACEHOLDER]
4. Include clear instructions for completion
5. Be suitable for financial/legal matters
6. Include appropriate disclaimers

Provide the complete template ready for use."""
            }
        ]
        
        return await self.generate_response(messages)
    
    async def provide_financial_education(self, topic: str) -> str:
        """
        Provide financial education and explanations
        """
        messages = [
            {
                "role": "user",
                "content": f"""Explain the financial concept: {topic}
                
Provide:
1. DEFINITION: Clear, simple explanation
2. HOW IT WORKS: Step-by-step breakdown
3. BENEFITS & RISKS: Pros and cons
4. REAL-WORLD EXAMPLES: Practical scenarios
5. CONSUMER TIPS: Practical advice for consumers
6. WARNING SIGNS: What to watch out for
7. LEGAL PROTECTIONS: Relevant consumer rights

Use simple language that anyone can understand."""
            }
        ]
        
        return await self.generate_response(messages)

# Global AI service instance
ai_service = AIService()