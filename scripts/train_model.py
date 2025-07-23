#!/usr/bin/env python3
"""
Churn Prediction Model Training Script

This script demonstrates the complete ML pipeline for customer churn prediction including:
- Data loading and exploration
- Feature engineering
- Model training with multiple algorithms
- MLflow experiment tracking
- Model evaluation and selection
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent hanging
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, classification_report, confusion_matrix
)
import mlflow
import mlflow.sklearn
import pickle
import os
import warnings
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings('ignore')

# Set up MLflow
mlflow.set_tracking_uri("sqlite:///mlruns.db")
mlflow.set_experiment("churn_prediction")

def create_synthetic_dataset(n_samples=1000, random_state=42):
    """
    Create synthetic churn dataset for demonstration
    
    Args:
        n_samples (int): Number of samples to generate
        random_state (int): Random seed for reproducibility
    
    Returns:
        pd.DataFrame: Synthetic churn dataset
    """
    logger.info(f"Creating synthetic dataset with {n_samples} samples...")
    
    np.random.seed(random_state)
    
    # Generate synthetic data
    data = {
        'customer_id': range(1, n_samples + 1),
        'tenure': np.random.randint(1, 73, n_samples),
        'monthly_charges': np.random.uniform(20, 120, n_samples),
        'total_charges': np.random.uniform(100, 8000, n_samples),
        'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'payment_method': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
        'internet_service': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples),
        'online_security': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'tech_support': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'streaming_tv': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'monthly_charges_ratio': np.random.uniform(0.5, 2.0, n_samples),
        'customer_service_calls': np.random.randint(0, 10, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create churn target based on features (realistic patterns)
    churn_prob = (
        (df['tenure'] < 12) * 0.3 +
        (df['monthly_charges'] > 80) * 0.2 +
        (df['contract_type'] == 'Month-to-month') * 0.3 +
        (df['customer_service_calls'] > 3) * 0.2 +
        (df['payment_method'] == 'Electronic check') * 0.1
    )
    
    # Ensure probabilities are between 0 and 1
    churn_prob = np.clip(churn_prob, 0, 1)
    
    df['churn'] = np.random.binomial(1, churn_prob)
    
    logger.info(f"Dataset created: {df.shape}")
    logger.info(f"Churn rate: {df['churn'].mean():.2%}")
    
    return df

def explore_data(df):
    """
    Perform exploratory data analysis
    
    Args:
        df (pd.DataFrame): Input dataset
    """
    logger.info("Performing exploratory data analysis...")
    
    # Create output directory for plots
    os.makedirs('data/plots', exist_ok=True)
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Churn Dataset Exploration', fontsize=16, fontweight='bold')
    
    # Tenure distribution
    axes[0, 0].hist(df['tenure'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Tenure Distribution')
    axes[0, 0].set_xlabel('Tenure (months)')
    axes[0, 0].set_ylabel('Frequency')
    
    # Monthly charges distribution
    axes[0, 1].hist(df['monthly_charges'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    axes[0, 1].set_title('Monthly Charges Distribution')
    axes[0, 1].set_xlabel('Monthly Charges ($)')
    axes[0, 1].set_ylabel('Frequency')
    
    # Churn distribution
    churn_counts = df['churn'].value_counts()
    axes[0, 2].bar(churn_counts.index, churn_counts.values, color=['lightcoral', 'lightblue'])
    axes[0, 2].set_title('Churn Distribution')
    axes[0, 2].set_xlabel('Churn')
    axes[0, 2].set_ylabel('Count')
    axes[0, 2].set_xticks([0, 1])
    axes[0, 2].set_xticklabels(['No Churn', 'Churn'])
    
    # Churn rate by contract type
    contract_churn = df.groupby('contract_type')['churn'].mean()
    axes[1, 0].bar(contract_churn.index, contract_churn.values, color='orange', alpha=0.7)
    axes[1, 0].set_title('Churn Rate by Contract Type')
    axes[1, 0].set_xlabel('Contract Type')
    axes[1, 0].set_ylabel('Churn Rate')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Churn rate by payment method
    payment_churn = df.groupby('payment_method')['churn'].mean()
    axes[1, 1].bar(payment_churn.index, payment_churn.values, color='purple', alpha=0.7)
    axes[1, 1].set_title('Churn Rate by Payment Method')
    axes[1, 1].set_xlabel('Payment Method')
    axes[1, 1].set_ylabel('Churn Rate')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    # Churn rate by internet service
    internet_churn = df.groupby('internet_service')['churn'].mean()
    axes[1, 2].bar(internet_churn.index, internet_churn.values, color='teal', alpha=0.7)
    axes[1, 2].set_title('Churn Rate by Internet Service')
    axes[1, 2].set_xlabel('Internet Service')
    axes[1, 2].set_ylabel('Churn Rate')
    axes[1, 2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('data/plots/data_exploration.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close the plot to prevent hanging
    
    logger.info("Data exploration plots saved to data/plots/data_exploration.png")

def engineer_features(df):
    """
    Perform feature engineering on the dataset
    
    Args:
        df (pd.DataFrame): Input dataset
    
    Returns:
        tuple: (processed_df, label_encoders_dict)
    """
    logger.info("Performing feature engineering...")
    
    df_processed = df.copy()
    
    # Create binary features
    df_processed['is_month_to_month'] = (df_processed['contract_type'] == 'Month-to-month').astype(int)
    df_processed['is_electronic_check'] = (df_processed['payment_method'] == 'Electronic check').astype(int)
    df_processed['has_internet'] = (df_processed['internet_service'] != 'No').astype(int)
    
    # Create interaction features
    df_processed['tenure_monthly_ratio'] = df_processed['tenure'] / df_processed['monthly_charges']
    df_processed['total_monthly_ratio'] = df_processed['total_charges'] / df_processed['monthly_charges']
    
    # Create categorical encodings
    le_contract = LabelEncoder()
    le_payment = LabelEncoder()
    le_internet = LabelEncoder()
    
    df_processed['contract_encoded'] = le_contract.fit_transform(df_processed['contract_type'])
    df_processed['payment_encoded'] = le_payment.fit_transform(df_processed['payment_method'])
    df_processed['internet_encoded'] = le_internet.fit_transform(df_processed['internet_service'])
    
    # Store label encoders
    label_encoders = {
        'contract': le_contract,
        'payment': le_payment,
        'internet': le_internet
    }
    
    logger.info("Feature engineering completed")
    
    return df_processed, label_encoders

def prepare_features(df_processed, feature_columns):
    """
    Prepare features for modeling
    
    Args:
        df_processed (pd.DataFrame): Processed dataset
        feature_columns (list): List of feature column names
    
    Returns:
        tuple: (X, y, scaler)
    """
    logger.info("Preparing features for modeling...")
    
    X = df_processed[feature_columns]
    y = df_processed['churn']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logger.info(f"Training set: {X_train.shape}")
    logger.info(f"Test set: {X_test.shape}")
    logger.info(f"Training churn rate: {y_train.mean():.2%}")
    logger.info(f"Test churn rate: {y_test.mean():.2%}")
    
    return (X_train_scaled, X_test_scaled, y_train, y_test), scaler

def train_models(X_train, X_test, y_train, y_test):
    """
    Train multiple models and track experiments with MLflow
    
    Args:
        X_train, X_test, y_train, y_test: Training and test data
    
    Returns:
        dict: Dictionary containing model results and best model
    """
    logger.info("Training models with MLflow tracking...")
    
    # Define models to train
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(probability=True, random_state=42)
    }
    
    best_model = None
    best_score = 0
    results = {}
    
    for name, model in models.items():
        logger.info(f"Training {name}...")
        
        with mlflow.start_run(run_name=f"{name}_churn_model"):
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_pred_proba)
            
            # Log parameters and metrics
            mlflow.log_param("model_type", name)
            mlflow.log_param("n_features", X_train.shape[1])
            mlflow.log_param("n_samples", X_train.shape[0])
            
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("roc_auc", auc)
            
            # Log model
            mlflow.sklearn.log_model(model, f"{name.lower().replace(' ', '_')}_model")
            
            # Store results
            results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'auc': auc,
                'model': model
            }
            
            logger.info(f"{name} Results:")
            logger.info(f"  Accuracy: {accuracy:.4f}")
            logger.info(f"  Precision: {precision:.4f}")
            logger.info(f"  Recall: {recall:.4f}")
            logger.info(f"  F1-Score: {f1:.4f}")
            logger.info(f"  ROC-AUC: {auc:.4f}")
            
            # Track best model
            if auc > best_score:
                best_score = auc
                best_model = model
    
    best_model_name = max(results.keys(), key=lambda k: results[k]['auc'])
    logger.info(f"Best model: {best_model_name}")
    logger.info(f"Best AUC: {best_score:.4f}")
    
    return results, best_model

def evaluate_models(results):
    """
    Evaluate and visualize model performance
    
    Args:
        results (dict): Dictionary containing model results
    """
    logger.info("Evaluating model performance...")
    
    # Create output directory for plots
    os.makedirs('data/plots', exist_ok=True)
    
    # Compare model performance
    metrics_df = pd.DataFrame(results).T[['accuracy', 'precision', 'recall', 'f1', 'auc']]
    logger.info("Model Performance Comparison:")
    logger.info(metrics_df.round(4))
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Model performance metrics
    metrics_df[['accuracy', 'precision', 'recall', 'f1']].plot(kind='bar', ax=ax1)
    ax1.set_title('Model Performance Metrics', fontweight='bold')
    ax1.set_xlabel('Model')
    ax1.set_ylabel('Score')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # ROC-AUC scores
    metrics_df['auc'].plot(kind='bar', color='orange', ax=ax2)
    ax2.set_title('ROC-AUC Scores', fontweight='bold')
    ax2.set_xlabel('Model')
    ax2.set_ylabel('ROC-AUC')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('data/plots/model_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    logger.info("Model comparison plots saved to data/plots/model_comparison.png")

def analyze_feature_importance(best_model, feature_columns):
    """
    Analyze feature importance for tree-based models
    
    Args:
        best_model: Trained model
        feature_columns (list): List of feature column names
    """
    logger.info("Analyzing feature importance...")
    
    # Create output directory for plots
    os.makedirs('data/plots', exist_ok=True)
    
    # Feature importance (for tree-based models)
    if hasattr(best_model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(12, 8))
        plt.barh(feature_importance['feature'], feature_importance['importance'])
        plt.title('Feature Importance', fontweight='bold')
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        plt.tight_layout()
        plt.savefig('data/plots/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Top 5 Most Important Features:")
        logger.info(feature_importance.head())
        logger.info("Feature importance plot saved to data/plots/feature_importance.png")
    else:
        logger.info("Feature importance not available for this model type")

def save_model(best_model, scaler, feature_columns, label_encoders):
    """
    Save the best model and preprocessing objects
    
    Args:
        best_model: Trained model
        scaler: Fitted scaler
        feature_columns (list): List of feature column names
        label_encoders (dict): Dictionary of label encoders
    """
    logger.info("Saving model and preprocessing objects...")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the complete model data
    model_data = {
        'model': best_model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'label_encoders': label_encoders
    }
    
    with open('models/churn_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    # Also save a simple version for the API
    os.makedirs('apps', exist_ok=True)
    with open('apps/churn_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    logger.info("Model saved successfully!")
    logger.info(f"Best model type: {type(best_model).__name__}")
    logger.info("Model saved to: models/churn_model.pkl")
    logger.info("Simple model saved to: apps/churn_model.pkl")

def main():
    """
    Main function to run the complete training pipeline
    """
    logger.info("🚀 Starting Churn Prediction Model Training Pipeline")
    logger.info("=" * 60)
    
    try:
        # 1. Create synthetic dataset
        df = create_synthetic_dataset(n_samples=1000)
        
        # 2. Explore data
        explore_data(df)
        
        # 3. Feature engineering
        df_processed, label_encoders = engineer_features(df)
        
        # 4. Define feature columns
        feature_columns = [
            'tenure', 'monthly_charges', 'total_charges', 'customer_service_calls',
            'is_month_to_month', 'is_electronic_check', 'has_internet',
            'tenure_monthly_ratio', 'total_monthly_ratio',
            'contract_encoded', 'payment_encoded', 'internet_encoded'
        ]
        
        # 5. Prepare features
        (X_train, X_test, y_train, y_test), scaler = prepare_features(df_processed, feature_columns)
        
        # 6. Train models
        results, best_model = train_models(X_train, X_test, y_train, y_test)
        
        # 7. Evaluate models
        evaluate_models(results)
        
        # 8. Analyze feature importance
        analyze_feature_importance(best_model, feature_columns)
        
        # 9. Save model
        save_model(best_model, scaler, feature_columns, label_encoders)
        
        logger.info("=" * 60)
        logger.info("🎉 Training pipeline completed successfully!")
        logger.info("=" * 60)
        
        # Print summary
        best_model_name = max(results.keys(), key=lambda k: results[k]['auc'])
        logger.info(f"Best Model: {best_model_name}")
        logger.info(f"Best AUC: {results[best_model_name]['auc']:.4f}")
        logger.info(f"Best Accuracy: {results[best_model_name]['accuracy']:.4f}")
        logger.info(f"Best F1-Score: {results[best_model_name]['f1']:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Training pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 