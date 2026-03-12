import requests
import json
from typing import Dict, List
from datetime import datetime, timedelta
import openai
from config import OPENAI_API_KEY, NEWS_API_KEY, SERP_API_KEY

class WebResearcher:
    """Perform web-scale research on companies"""
    
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.news_api_key = NEWS_API_KEY
        self.serp_api_key = SERP_API_KEY
        
    def research_company(self, company_name: str, industry: str = None) -> Dict:
        """Comprehensive company research"""
        
        research_results = {
            'news_articles': [],
            'sentiment_analysis': {},
            'reputation_signals': {},
            'industry_analysis': {},
            'risk_factors': []
        }
        
        # Search news
        news_data = self._search_news(company_name)
        research_results['news_articles'] = news_data
        
        # Analyze sentiment
        research_results['sentiment_analysis'] = self._analyze_sentiment(news_data)
        
        # Search for risk signals
        risk_keywords = [
            f"{company_name} lawsuit",
            f"{company_name} fraud",
            f"{company_name} bankruptcy",
            f"{company_name} regulatory violation"
        ]
        
        for keyword in risk_keywords:
            risk_results = self._search_web(keyword)
            if risk_results:
                research_results['risk_factors'].extend(risk_results)
        
        # Industry analysis
        if industry:
            research_results['industry_analysis'] = self._analyze_industry(industry)
        
        # Calculate scores
        scores = self._calculate_research_scores(research_results)
        
        return {
            'raw_research': research_results,
            'scores': scores,
            'summary': self._generate_research_summary(research_results)
        }
    
    def _search_news(self, company_name: str) -> List[Dict]:
        """Search recent news about company"""
        
        url = "[newsapi.org](https://newsapi.org/v2/everything)"
        params = {
            'q': company_name,
            'from': (datetime.now() - timedelta(days=30)).isoformat(),
            'sortBy': 'relevancy',
            'apiKey': self.news_api_key,
            'pageSize': 10
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
        except Exception as e:
            print(f"News search error: {e}")
            
        return []
    
    def _search_web(self, query: str) -> List[Dict]:
        """General web search using SERP API"""
        
        # Placeholder - implement with actual SERP API
        # For now, return mock data
        return [
            {
                'title': f'Search result for {query}',
                'snippet': 'No significant issues found',
                'link': '[example.com](https://example.com)'
            }
        ]
    
    def _analyze_sentiment(self, news_articles: List[Dict]) -> Dict:
        """Analyze sentiment of news articles using LLM"""
        
        if not news_articles:
            return {'sentiment': 'neutral', 'score': 0.5}
        
        # Combine article titles and descriptions
        text_to_analyze = '\n'.join([
            f"{article.get('title', '')} - {article.get('description', '')}"
            for article in news_articles[:5]
        ])
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze the sentiment of news articles about a company. Return a JSON with 'sentiment' (positive/negative/neutral) and 'score' (0-1)."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze sentiment:\n{text_to_analyze}"
                    }
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {'sentiment': 'neutral', 'score': 0.5}
    
    def _analyze_industry(self, industry: str) -> Dict:
        """Analyze industry trends and risks"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Provide a brief industry analysis with growth outlook and risk factors. Return JSON with 'outlook', 'growth_rate', and 'risk_level' (low/medium/high)."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the {industry} industry"
                    }
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Industry analysis error: {e}")
            return {
                'outlook': 'stable',
                'growth_rate': 0.05,
                'risk_level': 'medium'
            }
    
    def _calculate_research_scores(self, research_results: Dict) -> Dict:
        """Calculate numerical scores from research"""
        
        scores = {}
        
        # News sentiment score
        sentiment = research_results['sentiment_analysis']
        scores['news_sentiment_score'] = sentiment.get('score', 0.5)
        
        # Reputation score (based on risk factors)
        risk_count = len(research_results['risk_factors'])
        scores['reputation_score'] = max(0, 1 - (risk_count * 0.1))
        
        # Industry risk
        industry_analysis = research_results['industry_analysis']
        risk_mapping = {'low': 0.2, 'medium': 0.5, 'high': 0.8}
        scores['industry_risk'] = risk_mapping.get(
            industry_analysis.get('risk_level', 'medium'), 0.5
        )
        
        # Fraud mentions
        fraud_mentions = sum(1 for risk in research_results['risk_factors'] 
                           if 'fraud' in str(risk).lower())
        scores['fraud_mentions'] = fraud_mentions
        
        # Market position (placeholder)
        scores['market_position_score'] = 0.6
        
        return scores
    
    def _generate_research_summary(self, research_results: Dict) -> str:
        """Generate executive summary of research findings"""
        
        summary_parts = []
        
        # Sentiment summary
        sentiment = research_results['sentiment_analysis']
        summary_parts.append(
            f"Recent news sentiment is {sentiment.get('sentiment', 'neutral')} "
            f"with a score of {sentiment.get('score', 0.5):.2f}"
        )
        
        # Risk factors
        if research_results['risk_factors']:
            summary_parts.append(
                f"Identified {len(research_results['risk_factors'])} potential risk factors"
            )
        
        # Industry outlook
        industry = research_results['industry_analysis']
        if industry:
            summary_parts.append(
                f"Industry outlook is {industry.get('outlook', 'stable')} "
                f"with {industry.get('risk_level', 'medium')} risk"
            )
        
        return '. '.join(summary_parts)
