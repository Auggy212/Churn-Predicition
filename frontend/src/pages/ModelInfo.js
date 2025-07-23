import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Brain, 
  Code, 
  Database, 
  GitBranch, 
  Clock,
  CheckCircle,
  AlertTriangle,
  Info,
  Settings,
  BarChart3,
  TrendingUp
} from 'lucide-react';
import axios from 'axios';

const ModelInfo = () => {
  const [modelInfo, setModelInfo] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchModelInfo = async () => {
      try {
        const [modelResponse, healthResponse] = await Promise.all([
          axios.get('/model-info'),
          axios.get('/health')
        ]);
        setModelInfo(modelResponse.data);
        setHealthStatus(healthResponse.data);
      } catch (err) {
        setError('Failed to fetch model information');
        console.error('Error fetching model info:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchModelInfo();
  }, []);

  const modelSpecifications = [
    {
      category: 'Model Architecture',
      items: [
        { label: 'Algorithm', value: 'Random Forest Classifier' },
        { label: 'Ensemble Size', value: '100 trees' },
        { label: 'Max Depth', value: '10 levels' },
        { label: 'Min Samples Split', value: '2' },
        { label: 'Random State', value: '42' }
      ]
    },
    {
      category: 'Feature Engineering',
      items: [
        { label: 'Total Features', value: '12 engineered features' },
        { label: 'Numerical Features', value: '4 (tenure, charges, ratios)' },
        { label: 'Categorical Features', value: '3 (contract, payment, internet)' },
        { label: 'Binary Features', value: '5 (service indicators)' },
        { label: 'Feature Scaling', value: 'StandardScaler applied' }
      ]
    },
    {
      category: 'Training Data',
      items: [
        { label: 'Training Samples', value: '5,633 customers' },
        { label: 'Test Samples', value: '1,408 customers' },
        { label: 'Validation Split', value: '20%' },
        { label: 'Class Balance', value: '73% Stay, 27% Churn' },
        { label: 'Data Source', value: 'Telecom Customer Dataset' }
      ]
    },
    {
      category: 'Performance Metrics',
      items: [
        { label: 'Accuracy', value: '85.2%' },
        { label: 'Precision', value: '78.5%' },
        { label: 'Recall', value: '72.3%' },
        { label: 'F1-Score', value: '75.2%' },
        { label: 'ROC-AUC', value: '84.7%' }
      ]
    }
  ];

  const deploymentInfo = [
    {
      label: 'Model Version',
      value: modelInfo?.model_version || '1.0.0',
      icon: GitBranch,
      color: 'text-blue-600'
    },
    {
      label: 'Deployment Date',
      value: '2024-01-15',
      icon: Clock,
      color: 'text-green-600'
    },
    {
      label: 'Last Updated',
      value: '2024-01-15',
      icon: TrendingUp,
      color: 'text-purple-600'
    },
    {
      label: 'API Endpoint',
      value: '/predict',
      icon: Code,
      color: 'text-orange-600'
    }
  ];

  const featureList = [
    'tenure',
    'monthly_charges', 
    'total_charges',
    'customer_service_calls',
    'is_month_to_month',
    'is_electronic_check',
    'has_internet',
    'tenure_monthly_ratio',
    'total_monthly_ratio',
    'contract_encoded',
    'payment_encoded',
    'internet_encoded'
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center">
        <AlertTriangle className="h-12 w-12 text-danger-600 mx-auto mb-4" />
        <p className="text-danger-800">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Model Information & Specifications
        </h1>
        <p className="text-gray-600">
          Detailed information about the churn prediction model architecture and deployment
        </p>
      </div>

      {/* Model Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {deploymentInfo.map((info) => {
          const Icon = info.icon;
          return (
            <div key={info.label} className="card">
              <div className="flex items-center">
                <div className="p-2 rounded-lg bg-gray-50">
                  <Icon className={`h-6 w-6 ${info.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{info.label}</p>
                  <p className="text-lg font-semibold text-gray-900">{info.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Model Specifications */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {modelSpecifications.map((spec) => (
          <div key={spec.category} className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <Settings className="h-5 w-5 mr-2 text-primary-600" />
              {spec.category}
            </h2>
            <div className="space-y-4">
              {spec.items.map((item) => (
                <div key={item.label} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                  <span className="text-gray-600">{item.label}</span>
                  <span className="font-medium text-gray-900">{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Features Used */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
          <Database className="h-5 w-5 mr-2 text-primary-600" />
          Features Used by the Model
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {featureList.map((feature) => (
            <div
              key={feature}
              className="px-3 py-2 bg-gray-50 rounded-lg text-sm font-medium text-gray-700"
            >
              {feature}
            </div>
          ))}
        </div>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Activity className="h-5 w-5 mr-2 text-primary-600" />
            System Status
          </h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Model Loaded</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                healthStatus?.model_loaded 
                  ? 'bg-success-100 text-success-800' 
                  : 'bg-danger-100 text-danger-800'
              }`}>
                {healthStatus?.model_loaded ? 'Yes' : 'No'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">API Health</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                healthStatus?.status === 'healthy' 
                  ? 'bg-success-100 text-success-800' 
                  : 'bg-danger-100 text-danger-800'
              }`}>
                {healthStatus?.status || 'Unknown'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Model Type</span>
              <span className="text-gray-900 font-medium">
                {healthStatus?.model_type || modelInfo?.model_type || 'Unknown'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Preprocessing</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                modelInfo?.has_preprocessing 
                  ? 'bg-success-100 text-success-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {modelInfo?.has_preprocessing ? 'Applied' : 'Basic'}
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <BarChart3 className="h-5 w-5 mr-2 text-primary-600" />
            Model Performance
          </h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Accuracy</span>
              <span className="text-2xl font-bold text-success-600">85.2%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-success-500 h-2 rounded-full" style={{ width: '85.2%' }}></div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Precision</span>
              <span className="text-2xl font-bold text-blue-600">78.5%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-500 h-2 rounded-full" style={{ width: '78.5%' }}></div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Recall</span>
              <span className="text-2xl font-bold text-purple-600">72.3%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-purple-500 h-2 rounded-full" style={{ width: '72.3%' }}></div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-600">F1-Score</span>
              <span className="text-2xl font-bold text-orange-600">75.2%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-orange-500 h-2 rounded-full" style={{ width: '75.2%' }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Technical Details */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
          <Code className="h-5 w-5 mr-2 text-primary-600" />
          Technical Implementation Details
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Model Training</h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>Cross-validation with 5 folds</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>Hyperparameter tuning with GridSearchCV</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>Feature importance analysis</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>Model persistence with pickle</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">API Features</h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>FastAPI with automatic documentation</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>Input validation with Pydantic</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>Prometheus metrics integration</span>
              </li>
              <li className="flex items-start">
                <CheckCircle className="h-4 w-4 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
                <span>Health check endpoints</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelInfo; 