from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from prometheus_fastapi_instrumentator import Instrumentator
import pickle
import numpy as np
import os
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Churn Prediction API",
    description="A machine learning API for predicting customer churn",
    version="1.0.0"
)

# Initialize Prometheus monitoring
Instrumentator().instrument(app).expose(app)

class CustomerData(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    payment_method: str
    internet_service: Optional[str] = "No"
    online_security: Optional[str] = "No"
    tech_support: Optional[str] = "No"
    streaming_tv: Optional[str] = "No"
    customer_service_calls: Optional[int] = 0
    
    @validator('tenure')
    def tenure_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Tenure must be positive')
        return v
    
    @validator('monthly_charges')
    def monthly_charges_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Monthly charges must be positive')
        return v
    
    @validator('total_charges')
    def total_charges_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Total charges must be positive')
        return v

class PredictionResponse(BaseModel):
    churn_prediction: bool
    churn_probability: float
    confidence: float
    model_version: str

# Global variables for model and preprocessing objects
model = None
scaler = None
feature_columns = None
label_encoders = None

def load_model():
    """Load the trained model and preprocessing objects"""
    global model, scaler, feature_columns, label_encoders
    
    try:
        # Try to load the full model with preprocessing
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'churn_model.pkl')
        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                model_data = pickle.load(f)
                model = model_data['model']
                scaler = model_data['scaler']
                feature_columns = model_data['feature_columns']
                label_encoders = model_data['label_encoders']
                logger.info("Loaded full model with preprocessing")
        else:
            # Fallback to simple model
            model_path = os.path.join(os.path.dirname(__file__), 'churn_model.pkl')
            with open(model_path, "rb") as f:
                model = pickle.load(f)
                logger.info("Loaded simple model")
        
        logger.info(f"Model loaded successfully: {type(model).__name__}")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def prepare_features(customer: CustomerData) -> np.ndarray:
    """Prepare features for prediction"""
    try:
        # Create feature dictionary
        features = {
            'tenure': customer.tenure,
            'monthly_charges': customer.monthly_charges,
            'total_charges': customer.total_charges,
            'customer_service_calls': customer.customer_service_calls,
            'is_month_to_month': 1 if customer.contract_type == 'Month-to-month' else 0,
            'is_electronic_check': 1 if customer.payment_method == 'Electronic check' else 0,
            'has_internet': 1 if customer.internet_service != 'No' else 0,
            'tenure_monthly_ratio': customer.tenure / customer.monthly_charges if customer.monthly_charges > 0 else 0,
            'total_monthly_ratio': customer.total_charges / customer.monthly_charges if customer.monthly_charges > 0 else 0,
        }
        
        # Add encoded categorical features if label encoders are available
        if label_encoders:
            features['contract_encoded'] = label_encoders['contract'].transform([customer.contract_type])[0]
            features['payment_encoded'] = label_encoders['payment'].transform([customer.payment_method])[0]
            features['internet_encoded'] = label_encoders['internet'].transform([customer.internet_service])[0]
        else:
            # Simple encoding fallback
            contract_mapping = {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
            payment_mapping = {'Electronic check': 0, 'Mailed check': 1, 'Bank transfer': 2, 'Credit card': 3}
            internet_mapping = {'No': 0, 'DSL': 1, 'Fiber optic': 2}
            
            features['contract_encoded'] = contract_mapping.get(customer.contract_type, 0)
            features['payment_encoded'] = payment_mapping.get(customer.payment_method, 0)
            features['internet_encoded'] = internet_mapping.get(customer.internet_service, 0)
        
        # Convert to array and ensure correct order
        if feature_columns:
            feature_array = np.array([[features[col] for col in feature_columns]])
        else:
            # Fallback feature order
            feature_array = np.array([[
                features['tenure'], features['monthly_charges'], features['total_charges'],
                features['customer_service_calls'], features['is_month_to_month'],
                features['is_electronic_check'], features['has_internet'],
                features['tenure_monthly_ratio'], features['total_monthly_ratio'],
                features['contract_encoded'], features['payment_encoded'], features['internet_encoded']
            ]])
        
        # Scale features if scaler is available
        if scaler:
            feature_array = scaler.transform(feature_array)
        
        return feature_array
    
    except Exception as e:
        logger.error(f"Error preparing features: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feature preparation error: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    if not load_model():
        logger.error("Failed to load model on startup")

@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(customer: CustomerData):
    """Predict customer churn"""
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Prepare features
        features = prepare_features(customer)
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        return PredictionResponse(
            churn_prediction=bool(prediction),
            churn_probability=float(probability[1]),
            confidence=float(max(probability)),
            model_version="1.0.0"
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_type": type(model).__name__ if model else None
    }

@app.get("/model-info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "model_version": "1.0.0",
        "features_used": feature_columns if feature_columns else "Default features",
        "has_preprocessing": scaler is not None
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Churn Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "model_info": "/model-info",
            "metrics": "/metrics",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)