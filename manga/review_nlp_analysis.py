"""
NLP Analysis Utilities for Movie Reviews
Provides utilities for text analysis, feature extraction, and sentiment insights
"""

import numpy as np
import pandas as pd
from collections import Counter
import re

class ReviewAnalyzer:
    """
    Analyzes movie reviews for linguistic and sentiment patterns
    """
    
    def __init__(self, df):
        """Initialize with review data"""
        self.df = df
        
    def extract_text_features(self):
        """Extract linguistic features from reviews"""
        features = {
            'Review_ID': self.df['Review_ID'],
            'Review_Length': self.df['Review_Length'],
            'Avg_Word_Length': [],
            'Exclamation_Count': [],
            'Question_Count': [],
            'Capital_Ratio': [],
            'Sentiment': self.df['Sentiment']
        }
        
        for review in self.df['Review_Text']:
            # Average word length
            words = review.split()
            avg_word_len = np.mean([len(w) for w in words]) if words else 0
            features['Avg_Word_Length'].append(avg_word_len)
            
            # Exclamation marks
            exclamations = review.count('!')
            features['Exclamation_Count'].append(exclamations)
            
            # Questions
            questions = review.count('?')
            features['Question_Count'].append(questions)
            
            # Capital letter ratio
            capitals = sum(1 for c in review if c.isupper())
            capital_ratio = capitals / len(review) if review else 0
            features['Capital_Ratio'].append(capital_ratio)
        
        return pd.DataFrame(features)
    
    def analyze_sentiment_words(self):
        """Analyze most common words by sentiment"""
        positive_words = []
        negative_words = []
        neutral_words = []
        
        for idx, row in self.df.iterrows():
            words = row['Review_Text'].lower().split()
            if row['Sentiment'] == 1:  # Positive
                positive_words.extend(words)
            elif row['Sentiment'] == 0:  # Negative
                negative_words.extend(words)
            else:  # Neutral
                neutral_words.extend(words)
        
        return {
            'Positive_Top_Words': Counter(positive_words).most_common(10),
            'Negative_Top_Words': Counter(negative_words).most_common(10),
            'Neutral_Top_Words': Counter(neutral_words).most_common(10)
        }
    
    def calculate_sentiment_metrics(self):
        """Calculate comprehensive sentiment metrics"""
        metrics = {
            'Total_Reviews': len(self.df),
            'Positive_Reviews': (self.df['Sentiment'] == 1).sum(),
            'Negative_Reviews': (self.df['Sentiment'] == 0).sum(),
            'Neutral_Reviews': (self.df['Sentiment'] == 2).sum(),
            'Positive_Percentage': (self.df['Sentiment'] == 1).sum() / len(self.df) * 100,
            'Negative_Percentage': (self.df['Sentiment'] == 0).sum() / len(self.df) * 100,
            'Neutral_Percentage': (self.df['Sentiment'] == 2).sum() / len(self.df) * 100,
            'Avg_Rating': self.df['Rating'].mean(),
            'Avg_Review_Length': self.df['Review_Length'].mean(),
            'Avg_Rating_Positive': self.df[self.df['Sentiment'] == 1]['Rating'].mean(),
            'Avg_Rating_Negative': self.df[self.df['Sentiment'] == 0]['Rating'].mean(),
            'Avg_Rating_Neutral': self.df[self.df['Sentiment'] == 2]['Rating'].mean()
        }
        
        return metrics
    
    def analyze_rating_sentiment_correlation(self):
        """Analyze correlation between ratings and sentiments"""
        correlation_data = []
        
        for rating in range(1, 11):
            rating_reviews = self.df[self.df['Rating'] == rating]
            if len(rating_reviews) > 0:
                positive_pct = (rating_reviews['Sentiment'] == 1).sum() / len(rating_reviews) * 100
                negative_pct = (rating_reviews['Sentiment'] == 0).sum() / len(rating_reviews) * 100
                neutral_pct = (rating_reviews['Sentiment'] == 2).sum() / len(rating_reviews) * 100
                
                correlation_data.append({
                    'Rating': rating,
                    'Review_Count': len(rating_reviews),
                    'Positive_Percentage': positive_pct,
                    'Negative_Percentage': negative_pct,
                    'Neutral_Percentage': neutral_pct
                })
        
        return pd.DataFrame(correlation_data)
    
    def identify_review_patterns(self):
        """Identify patterns in review writing"""
        patterns = {
            'Short_Reviews': len(self.df[self.df['Review_Length'] < 10]),
            'Medium_Reviews': len(self.df[(self.df['Review_Length'] >= 10) & (self.df['Review_Length'] < 20)]),
            'Long_Reviews': len(self.df[self.df['Review_Length'] >= 20]),
            'High_Rating_Reviews': len(self.df[self.df['Rating'] >= 8]),
            'Low_Rating_Reviews': len(self.df[self.df['Rating'] <= 3]),
            'Mid_Rating_Reviews': len(self.df[(self.df['Rating'] > 3) & (self.df['Rating'] < 8)])
        }
        
        return patterns
    
    def generate_sentiment_summary(self):
        """Generate summary statistics for each sentiment"""
        summaries = {}
        
        for sentiment in [0, 1, 2]:
            sentiment_name = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}[sentiment]
            sentiment_data = self.df[self.df['Sentiment'] == sentiment]
            
            summaries[sentiment_name] = {
                'Count': len(sentiment_data),
                'Percentage': len(sentiment_data) / len(self.df) * 100,
                'Avg_Length': sentiment_data['Review_Length'].mean(),
                'Avg_Rating': sentiment_data['Rating'].mean(),
                'Min_Rating': sentiment_data['Rating'].min(),
                'Max_Rating': sentiment_data['Rating'].max()
            }
        
        return summaries


class SentimentInsights:
    """
    Generates actionable insights from sentiment analysis
    """
    
    def __init__(self, df):
        """Initialize with review data"""
        self.df = df
        self.analyzer = ReviewAnalyzer(df)
    
    def get_key_findings(self):
        """Extract key findings from the data"""
        metrics = self.analyzer.calculate_sentiment_metrics()
        
        findings = []
        
        # Finding 1: Dominant sentiment
        sentiments = {
            'Positive': metrics['Positive_Percentage'],
            'Negative': metrics['Negative_Percentage'],
            'Neutral': metrics['Neutral_Percentage']
        }
        dominant = max(sentiments, key=sentiments.get)
        findings.append(f"Dominant sentiment is {dominant} ({sentiments[dominant]:.1f}% of reviews)")
        
        # Finding 2: Rating patterns
        avg_rating = metrics['Avg_Rating']
        if avg_rating >= 7:
            findings.append("Overall movie reception is positive based on average rating")
        elif avg_rating <= 4:
            findings.append("Overall movie reception is negative based on average rating")
        else:
            findings.append("Movie reception is mixed based on average rating")
        
        # Finding 3: Sentiment-rating alignment
        pos_rating = metrics['Avg_Rating_Positive']
        neg_rating = metrics['Avg_Rating_Negative']
        if pos_rating > neg_rating + 2:
            findings.append("Strong alignment between positive sentiment and high ratings")
        
        return findings
    
    def get_improvement_areas(self):
        """Identify areas for improvement"""
        metrics = self.analyzer.calculate_sentiment_metrics()
        
        improvements = []
        
        if metrics['Negative_Percentage'] > 30:
            improvements.append("High percentage of negative reviews suggests need for quality improvements")
        
        if metrics['Avg_Rating'] < 5:
            improvements.append("Low average rating indicates significant audience dissatisfaction")
        
        return improvements
    
    def get_audience_insights(self):
        """Generate audience insights"""
        metrics = self.analyzer.calculate_sentiment_metrics()
        
        insights = []
        
        if metrics['Positive_Percentage'] > 40:
            insights.append("Strong positive audience reception indicates commercial potential")
        
        if metrics['Neutral_Percentage'] > 30:
            insights.append("Significant neutral sentiment suggests mixed audience opinions")
        
        return insights


def generate_and_save_review_datasets(output_dir='/home/ubuntu'):
    """
    Generate and save all sample review datasets
    """
    print("Generating movie review datasets...")
    
    # Generate review dataset
    from sentiment_analysis_system import generate_movie_reviews
    
    df = generate_movie_reviews(n_reviews=1000)
    
    # Save raw dataset
    print("  Saving raw review dataset...")
    df.to_csv(f'{output_dir}/movie_reviews.csv', index=False)
    print(f"  ✓ Raw dataset saved")
    
    # Perform NLP analysis
    print("  Performing NLP analysis...")
    analyzer = ReviewAnalyzer(df)
    
    # Extract text features
    print("  Extracting text features...")
    text_features = analyzer.extract_text_features()
    text_features.to_csv(f'{output_dir}/review_text_features.csv', index=False)
    print(f"  ✓ Text features saved")
    
    # Calculate sentiment metrics
    print("  Calculating sentiment metrics...")
    metrics = analyzer.calculate_sentiment_metrics()
    
    metrics_df = pd.DataFrame({
        'Metric': list(metrics.keys()),
        'Value': list(metrics.values())
    })
    
    metrics_df.to_csv(f'{output_dir}/sentiment_metrics.csv', index=False)
    print(f"  ✓ Sentiment metrics saved")
    
    # Analyze rating-sentiment correlation
    print("  Analyzing rating-sentiment correlation...")
    correlation = analyzer.analyze_rating_sentiment_correlation()
    correlation.to_csv(f'{output_dir}/rating_sentiment_correlation.csv', index=False)
    print(f"  ✓ Rating-sentiment correlation saved")
    
    # Generate sentiment summary
    print("  Generating sentiment summary...")
    summaries = analyzer.generate_sentiment_summary()
    
    summary_df = pd.DataFrame({
        'Sentiment': list(summaries.keys()),
        'Count': [summaries[s]['Count'] for s in summaries.keys()],
        'Percentage': [summaries[s]['Percentage'] for s in summaries.keys()],
        'Avg_Length': [summaries[s]['Avg_Length'] for s in summaries.keys()],
        'Avg_Rating': [summaries[s]['Avg_Rating'] for s in summaries.keys()]
    })
    
    summary_df.to_csv(f'{output_dir}/sentiment_summary.csv', index=False)
    print(f"  ✓ Sentiment summary saved")
    
    # Generate insights
    print("  Generating insights...")
    insights = SentimentInsights(df)
    
    findings = insights.get_key_findings()
    improvements = insights.get_improvement_areas()
    audience = insights.get_audience_insights()
    
    insights_df = pd.DataFrame({
        'Type': ['Finding'] * len(findings) + ['Improvement'] * len(improvements) + ['Audience'] * len(audience),
        'Insight': findings + improvements + audience
    })
    
    insights_df.to_csv(f'{output_dir}/sentiment_insights.csv', index=False)
    print(f"  ✓ Insights saved")
    
    return df, analyzer, metrics


if __name__ == '__main__':
    df, analyzer, metrics = generate_and_save_review_datasets()
    
    print("\nDataset Summary:")
    print(f"Total Reviews: {len(df)}")
    
    print("\nSentiment Metrics:")
    for metric, value in list(metrics.items())[:5]:
        print(f"  {metric}: {value:.2f}")
    
    print("\nText Features Analysis:")
    text_features = analyzer.extract_text_features()
    print(f"  Avg Review Length: {text_features['Review_Length'].mean():.2f} words")
    print(f"  Avg Word Length: {text_features['Avg_Word_Length'].mean():.2f} characters")
    print(f"  Avg Exclamations: {text_features['Exclamation_Count'].mean():.2f}")
