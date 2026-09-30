"""
Sentiment Analysis System for Movie Reviews
Classifies movie reviews as positive, negative, or neutral using NLP and ML
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# ============================================================================
# 1. GENERATE SYNTHETIC MOVIE REVIEW DATASET
# ============================================================================

def generate_movie_reviews(n_reviews=1000, random_state=42):
    """Generate synthetic movie review dataset with sentiment labels"""
    np.random.seed(random_state)
    
    # Positive review templates
    positive_templates = [
        "This movie was absolutely fantastic! I loved every minute of it.",
        "Outstanding performance by the cast. Highly recommended!",
        "A masterpiece! One of the best films I've ever seen.",
        "Brilliant storytelling and amazing cinematography.",
        "Incredible movie! I was completely captivated throughout.",
        "Excellent direction and superb acting. Truly impressive!",
        "A delightful experience. Worth watching multiple times.",
        "Phenomenal! This film exceeded all my expectations.",
        "Perfect blend of action and emotion. Absolutely loved it!",
        "Wonderful movie! The plot kept me engaged from start to finish."
    ]
    
    # Negative review templates
    negative_templates = [
        "Terrible movie. A complete waste of time.",
        "Boring and predictable. Very disappointed.",
        "Awful acting and poor storyline. Not recommended.",
        "One of the worst films I've seen. Extremely disappointed.",
        "Dreadful! I couldn't even finish watching it.",
        "Horrible plot and terrible execution. Avoid at all costs.",
        "Disappointing and tedious. Not worth your time.",
        "Pathetic attempt at filmmaking. Absolutely dreadful.",
        "Unwatchable. Terrible from beginning to end.",
        "Abysmal! This movie was painfully bad."
    ]
    
    # Neutral review templates
    neutral_templates = [
        "It was an okay movie. Nothing special but not bad either.",
        "Average film. Some good parts, some not so good.",
        "Decent movie. It had its moments but also some flaws.",
        "Mediocre. Not the best but not the worst either.",
        "It was fine. Nothing to get excited about.",
        "Passable film. Had some interesting scenes.",
        "Neither great nor terrible. Just an average movie.",
        "Okay film. Some entertaining parts mixed with dull ones.",
        "Acceptable movie. It served its purpose.",
        "Standard fare. Nothing particularly memorable."
    ]
    
    reviews = []
    sentiments = []
    ratings = []
    
    for i in range(n_reviews):
        sentiment_choice = np.random.choice(['positive', 'negative', 'neutral'], p=[0.4, 0.35, 0.25])
        
        if sentiment_choice == 'positive':
            review = np.random.choice(positive_templates) + " " + np.random.choice(positive_templates)
            sentiment = 1  # Positive
            rating = np.random.randint(8, 11)
        elif sentiment_choice == 'negative':
            review = np.random.choice(negative_templates) + " " + np.random.choice(negative_templates)
            sentiment = 0  # Negative
            rating = np.random.randint(1, 4)
        else:
            review = np.random.choice(neutral_templates) + " " + np.random.choice(neutral_templates)
            sentiment = 2  # Neutral
            rating = np.random.randint(4, 8)
        
        reviews.append(review)
        sentiments.append(sentiment)
        ratings.append(rating)
    
    df = pd.DataFrame({
        'Review_ID': np.arange(1, n_reviews + 1),
        'Review_Text': reviews,
        'Sentiment': sentiments,
        'Rating': ratings,
        'Review_Length': [len(r.split()) for r in reviews],
        'Date': [datetime.now() - timedelta(days=np.random.randint(0, 365)) for _ in range(n_reviews)]
    })
    
    print("=" * 90)
    print("SENTIMENT ANALYSIS SYSTEM FOR MOVIE REVIEWS - DATASET OVERVIEW")
    print("=" * 90)
    print(f"\nTotal Reviews: {len(df)}")
    print(f"\nSentiment Distribution:")
    sentiment_counts = df['Sentiment'].value_counts()
    print(f"  Positive: {sentiment_counts.get(1, 0)} ({sentiment_counts.get(1, 0)/len(df)*100:.1f}%)")
    print(f"  Negative: {sentiment_counts.get(0, 0)} ({sentiment_counts.get(0, 0)/len(df)*100:.1f}%)")
    print(f"  Neutral: {sentiment_counts.get(2, 0)} ({sentiment_counts.get(2, 0)/len(df)*100:.1f}%)")
    print(f"\nRating Statistics:")
    print(f"  Average Rating: {df['Rating'].mean():.2f}")
    print(f"  Min Rating: {df['Rating'].min()}")
    print(f"  Max Rating: {df['Rating'].max()}")
    print(f"\nReview Length Statistics:")
    print(f"  Average Length: {df['Review_Length'].mean():.1f} words")
    print(f"  Min Length: {df['Review_Length'].min()} words")
    print(f"  Max Length: {df['Review_Length'].max()} words")
    
    return df

# ============================================================================
# 2. TEXT PREPROCESSING AND FEATURE EXTRACTION
# ============================================================================

def preprocess_and_vectorize(df):
    """Preprocess reviews and extract TF-IDF features"""
    print("\n" + "=" * 90)
    print("TEXT PREPROCESSING AND FEATURE EXTRACTION")
    print("=" * 90)
    
    # Create sentiment labels
    y = df['Sentiment']
    
    # TF-IDF Vectorization
    print("\nApplying TF-IDF Vectorization...")
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), 
                                  min_df=2, max_df=0.8, lowercase=True)
    X = vectorizer.fit_transform(df['Review_Text'])
    
    print(f"Vocabulary Size: {len(vectorizer.get_feature_names_out())}")
    print(f"Feature Matrix Shape: {X.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set size: {X_train.shape[0]} reviews")
    print(f"Test set size: {X_test.shape[0]} reviews")
    print(f"Feature scaling: TF-IDF (Term Frequency-Inverse Document Frequency)")
    
    return X_train, X_test, y_train, y_test, vectorizer, df

# ============================================================================
# 3. VISUALIZATION FUNCTIONS
# ============================================================================

def visualize_sentiment_distribution(df):
    """Visualize sentiment distribution"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Sentiment distribution
    sentiment_map = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
    sentiment_labels = [sentiment_map[s] for s in df['Sentiment']]
    sentiment_counts = pd.Series(sentiment_labels).value_counts()
    
    colors = ['#D62828', '#2E86AB', '#F18F01']
    axes[0].bar(sentiment_counts.index, sentiment_counts.values, color=colors, 
                edgecolor='black', alpha=0.8)
    axes[0].set_title('Distribution of Review Sentiments', fontweight='bold', fontsize=12)
    axes[0].set_ylabel('Number of Reviews')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Rating distribution by sentiment
    for sentiment in [0, 1, 2]:
        sentiment_data = df[df['Sentiment'] == sentiment]['Rating']
        axes[1].hist(sentiment_data, alpha=0.6, label=sentiment_map[sentiment], bins=10)
    
    axes[1].set_title('Rating Distribution by Sentiment', fontweight='bold', fontsize=12)
    axes[1].set_xlabel('Rating')
    axes[1].set_ylabel('Frequency')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/sentiment_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Sentiment distribution visualization saved")
    plt.close()

def visualize_review_metrics(df):
    """Visualize review metrics"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    sentiment_map = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
    
    # Review length distribution
    axes[0, 0].hist(df['Review_Length'], bins=30, color='#2E86AB', alpha=0.7, edgecolor='black')
    axes[0, 0].axvline(df['Review_Length'].mean(), color='red', linestyle='--', linewidth=2)
    axes[0, 0].set_title('Distribution of Review Length', fontweight='bold')
    axes[0, 0].set_xlabel('Number of Words')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].grid(alpha=0.3)
    
    # Rating distribution
    axes[0, 1].hist(df['Rating'], bins=10, color='#A23B72', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Distribution of Ratings', fontweight='bold')
    axes[0, 1].set_xlabel('Rating (1-10)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].grid(alpha=0.3)
    
    # Review length by sentiment
    sentiment_lengths = [df[df['Sentiment'] == s]['Review_Length'].values for s in [0, 1, 2]]
    axes[1, 0].boxplot(sentiment_lengths, labels=['Negative', 'Positive', 'Neutral'])
    axes[1, 0].set_title('Review Length by Sentiment', fontweight='bold')
    axes[1, 0].set_ylabel('Number of Words')
    axes[1, 0].grid(alpha=0.3)
    
    # Rating by sentiment
    sentiment_ratings = [df[df['Sentiment'] == s]['Rating'].values for s in [0, 1, 2]]
    axes[1, 1].boxplot(sentiment_ratings, labels=['Negative', 'Positive', 'Neutral'])
    axes[1, 1].set_title('Rating by Sentiment', fontweight='bold')
    axes[1, 1].set_ylabel('Rating (1-10)')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/review_metrics.png', dpi=300, bbox_inches='tight')
    print("✓ Review metrics visualization saved")
    plt.close()

def visualize_temporal_trends(df):
    """Visualize temporal sentiment trends"""
    df_sorted = df.sort_values('Date')
    df_sorted['Date_Only'] = df_sorted['Date'].dt.date
    
    daily_sentiment = df_sorted.groupby('Date_Only')['Sentiment'].apply(
        lambda x: pd.Series({
            'Positive': (x == 1).sum(),
            'Negative': (x == 0).sum(),
            'Neutral': (x == 2).sum()
        })
    ).fillna(0)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    if isinstance(daily_sentiment, pd.DataFrame):
        if 'Positive' in daily_sentiment.columns:
            daily_sentiment['Positive'].plot(ax=ax, label='Positive', linewidth=2, color='#2E86AB')
        if 'Negative' in daily_sentiment.columns:
            daily_sentiment['Negative'].plot(ax=ax, label='Negative', linewidth=2, color='#D62828')
        if 'Neutral' in daily_sentiment.columns:
            daily_sentiment['Neutral'].plot(ax=ax, label='Neutral', linewidth=2, color='#F18F01')
    else:
        daily_sentiment.plot(ax=ax, linewidth=2)
    
    ax.set_title('Sentiment Trends Over Time', fontweight='bold', fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Reviews')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/temporal_trends.png', dpi=300, bbox_inches='tight')
    print("✓ Temporal trends visualization saved")
    plt.close()

def visualize_model_comparison(results):
    """Visualize model performance comparison"""
    models = list(results.keys())
    accuracy = [results[m]['Accuracy'] for m in models]
    precision = [results[m]['Precision'] for m in models]
    recall = [results[m]['Recall'] for m in models]
    f1 = [results[m]['F1'] for m in models]
    
    x = np.arange(len(models))
    width = 0.2
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.bar(x - 1.5*width, accuracy, width, label='Accuracy', alpha=0.8, edgecolor='black')
    ax.bar(x - 0.5*width, precision, width, label='Precision', alpha=0.8, edgecolor='black')
    ax.bar(x + 0.5*width, recall, width, label='Recall', alpha=0.8, edgecolor='black')
    ax.bar(x + 1.5*width, f1, width, label='F1-Score', alpha=0.8, edgecolor='black')
    
    ax.set_title('Model Performance Comparison', fontweight='bold', fontsize=12)
    ax.set_ylabel('Score')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/model_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Model comparison visualization saved")
    plt.close()

def visualize_confusion_matrices(y_test, y_pred_nb, y_pred_lr, y_pred_rf):
    """Visualize confusion matrices for all models"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    models_data = [
        ('Naive Bayes', y_pred_nb),
        ('Logistic Regression', y_pred_lr),
        ('Random Forest', y_pred_rf)
    ]
    
    for idx, (name, y_pred) in enumerate(models_data):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], 
                   xticklabels=['Negative', 'Positive', 'Neutral'],
                   yticklabels=['Negative', 'Positive', 'Neutral'])
        axes[idx].set_title(f'Confusion Matrix - {name}', fontweight='bold')
        axes[idx].set_ylabel('True Label')
        axes[idx].set_xlabel('Predicted Label')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("✓ Confusion matrices visualization saved")
    plt.close()

def visualize_sentiment_by_rating(df):
    """Visualize sentiment distribution by rating"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sentiment_map = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
    
    for sentiment in [0, 1, 2]:
        data = df[df['Sentiment'] == sentiment].groupby('Rating').size()
        ax.plot(data.index, data.values, marker='o', linewidth=2, 
               label=sentiment_map[sentiment], markersize=8)
    
    ax.set_title('Sentiment Distribution Across Ratings', fontweight='bold', fontsize=12)
    ax.set_xlabel('Rating (1-10)')
    ax.set_ylabel('Number of Reviews')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/sentiment_by_rating.png', dpi=300, bbox_inches='tight')
    print("✓ Sentiment by rating visualization saved")
    plt.close()

# ============================================================================
# 4. MODEL BUILDING AND TRAINING
# ============================================================================

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple classification models"""
    print("\n" + "=" * 90)
    print("MODEL TRAINING")
    print("=" * 90)
    
    results = {}
    models = {}
    
    # Naive Bayes
    print("\nTraining Multinomial Naive Bayes...")
    nb_model = MultinomialNB()
    nb_model.fit(X_train, y_train)
    y_pred_nb = nb_model.predict(X_test)
    
    results['Naive Bayes'] = {
        'Accuracy': accuracy_score(y_test, y_pred_nb),
        'Precision': precision_score(y_test, y_pred_nb, average='weighted'),
        'Recall': recall_score(y_test, y_pred_nb, average='weighted'),
        'F1': f1_score(y_test, y_pred_nb, average='weighted')
    }
    models['Naive Bayes'] = nb_model
    
    # Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    
    results['Logistic Regression'] = {
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr, average='weighted'),
        'Recall': recall_score(y_test, y_pred_lr, average='weighted'),
        'F1': f1_score(y_test, y_pred_lr, average='weighted')
    }
    models['Logistic Regression'] = lr_model
    
    # Random Forest
    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    results['Random Forest'] = {
        'Accuracy': accuracy_score(y_test, y_pred_rf),
        'Precision': precision_score(y_test, y_pred_rf, average='weighted'),
        'Recall': recall_score(y_test, y_pred_rf, average='weighted'),
        'F1': f1_score(y_test, y_pred_rf, average='weighted')
    }
    models['Random Forest'] = rf_model
    
    return results, models, y_pred_nb, y_pred_lr, y_pred_rf

# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "=" * 90)
    print("SENTIMENT ANALYSIS SYSTEM FOR MOVIE REVIEWS")
    print("Using Natural Language Processing and Machine Learning")
    print("=" * 90)
    
    # Generate dataset
    print("\n[Step 1] Generating Movie Review Dataset...")
    df = generate_movie_reviews(n_reviews=1000)
    
    # Preprocess and vectorize
    print("\n[Step 2] Preprocessing and Vectorizing Reviews...")
    X_train, X_test, y_train, y_test, vectorizer, df = preprocess_and_vectorize(df)
    
    # Generate visualizations
    print("\n[Step 3] Generating Visualizations...")
    print("Creating sentiment distribution visualization...")
    visualize_sentiment_distribution(df)
    
    print("Creating review metrics visualization...")
    visualize_review_metrics(df)
    
    print("Creating temporal trends visualization...")
    visualize_temporal_trends(df)
    
    print("Creating sentiment by rating visualization...")
    visualize_sentiment_by_rating(df)
    
    # Train models
    print("\n[Step 4] Training Classification Models...")
    results, models, y_pred_nb, y_pred_lr, y_pred_rf = train_models(
        X_train, X_test, y_train, y_test
    )
    
    # Print results
    print("\n" + "=" * 90)
    print("MODEL PERFORMANCE RESULTS")
    print("=" * 90)
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy: {metrics['Accuracy']:.4f}")
        print(f"  Precision: {metrics['Precision']:.4f}")
        print(f"  Recall: {metrics['Recall']:.4f}")
        print(f"  F1-Score: {metrics['F1']:.4f}")
    
    # Generate additional visualizations
    print("\n[Step 5] Generating Additional Visualizations...")
    print("Creating model comparison...")
    visualize_model_comparison(results)
    
    print("Creating confusion matrices...")
    visualize_confusion_matrices(y_test, y_pred_nb, y_pred_lr, y_pred_rf)
    
    print("\n" + "=" * 90)
    print("EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 90)
    print("\nGenerated Visualizations:")
    print("  1. sentiment_distribution.png")
    print("  2. review_metrics.png")
    print("  3. temporal_trends.png")
    print("  4. sentiment_by_rating.png")
    print("  5. model_comparison.png")
    print("  6. confusion_matrices.png")
    
    return df, X_train, X_test, y_train, y_test, results, models, vectorizer

if __name__ == "__main__":
    df, X_train, X_test, y_train, y_test, results, models, vectorizer = main()
