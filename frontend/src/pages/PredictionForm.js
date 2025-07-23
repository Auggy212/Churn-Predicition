import React, { useState } from 'react';
import { Brain, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import axios from 'axios';

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    tenure: '',
    monthly_charges: '',
    total_charges: '',
    contract_type: 'Month-to-month',
    payment_method: 'Electronic check',
    internet_service: 'No',
    online_security: 'No',
    tech_support: 'No',
    streaming_tv: 'No',
    customer_service_calls: '0'
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const contractTypes = ['Month-to-month', 'One year', 'Two year'];
  const paymentMethods = ['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'];
  const serviceOptions = ['No', 'DSL', 'Fiber optic'];
  const yesNoOptions = ['No', 'Yes'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // Convert numeric fields
      const requestData = {
        ...formData,
        tenure: parseInt(formData.tenure),
        monthly_charges: parseFloat(formData.monthly_charges),
        total_charges: parseFloat(formData.total_charges),
        customer_service_calls: parseInt(formData.customer_service_calls)
      };

      const response = await axios.post('/predict', requestData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while making the prediction');
    } finally {
      setLoading(false);
    }
  };

  const getChurnColor = (probability) => {
    if (probability < 0.3) return 'text-success-600';
    if (probability < 0.7) return 'text-yellow-600';
    return 'text-danger-600';
  };

  const getChurnLabel = (probability) => {
    if (probability < 0.3) return 'Low Risk';
    if (probability < 0.7) return 'Medium Risk';
    return 'High Risk';
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Customer Churn Prediction
        </h1>
        <p className="text-gray-600">
          Enter customer information to predict their likelihood of churning
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Prediction Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Brain className="h-5 w-5 mr-2 text-primary-600" />
            Customer Information
          </h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Information */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-900">Basic Information</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tenure (months)
                </label>
                <input
                  type="number"
                  name="tenure"
                  value={formData.tenure}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="12"
                  required
                  min="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Monthly Charges ($)
                </label>
                <input
                  type="number"
                  name="monthly_charges"
                  value={formData.monthly_charges}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="50.00"
                  required
                  min="0"
                  step="0.01"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Total Charges ($)
                </label>
                <input
                  type="number"
                  name="total_charges"
                  value={formData.total_charges}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="600.00"
                  required
                  min="0"
                  step="0.01"
                />
              </div>
            </div>

            {/* Contract & Payment */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-900">Contract & Payment</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contract Type
                </label>
                <select
                  name="contract_type"
                  value={formData.contract_type}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {contractTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Payment Method
                </label>
                <select
                  name="payment_method"
                  value={formData.payment_method}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {paymentMethods.map(method => (
                    <option key={method} value={method}>{method}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Services */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-900">Services</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Internet Service
                </label>
                <select
                  name="internet_service"
                  value={formData.internet_service}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {serviceOptions.map(service => (
                    <option key={service} value={service}>{service}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Online Security
                </label>
                <select
                  name="online_security"
                  value={formData.online_security}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {yesNoOptions.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tech Support
                </label>
                <select
                  name="tech_support"
                  value={formData.tech_support}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {yesNoOptions.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Streaming TV
                </label>
                <select
                  name="streaming_tv"
                  value={formData.streaming_tv}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {yesNoOptions.map(option => (
                    <option key={option} value={option}>{option}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Customer Service */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Customer Service Calls
              </label>
              <input
                type="number"
                name="customer_service_calls"
                value={formData.customer_service_calls}
                onChange={handleInputChange}
                className="input-field"
                placeholder="0"
                min="0"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 mr-2 animate-spin" />
                  Predicting...
                </>
              ) : (
                <>
                  <Brain className="h-4 w-4 mr-2" />
                  Predict Churn
                </>
              )}
            </button>
          </form>
        </div>

        {/* Prediction Results */}
        <div className="space-y-6">
          {error && (
            <div className="card border-danger-200 bg-danger-50">
              <div className="flex items-center">
                <AlertCircle className="h-5 w-5 text-danger-600 mr-2" />
                <span className="text-danger-800">{error}</span>
              </div>
            </div>
          )}

          {prediction && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                <CheckCircle className="h-5 w-5 mr-2 text-success-600" />
                Prediction Results
              </h2>

              <div className="space-y-6">
                {/* Main Prediction */}
                <div className="text-center p-6 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-gray-900 mb-2">
                    {prediction.churn_prediction ? 'Likely to Churn' : 'Likely to Stay'}
                  </div>
                  <div className={`text-lg font-semibold ${getChurnColor(prediction.churn_probability)}`}>
                    {getChurnLabel(prediction.churn_probability)}
                  </div>
                </div>

                {/* Probability Bar */}
                <div>
                  <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Churn Probability</span>
                    <span>{(prediction.churn_probability * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${
                        prediction.churn_probability < 0.3 ? 'bg-success-500' :
                        prediction.churn_probability < 0.7 ? 'bg-yellow-500' : 'bg-danger-500'
                      }`}
                      style={{ width: `${prediction.churn_probability * 100}%` }}
                    ></div>
                  </div>
                </div>

                {/* Additional Metrics */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">
                      {(prediction.confidence * 100).toFixed(1)}%
                    </div>
                    <div className="text-sm text-blue-800">Confidence</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">
                      {prediction.model_version}
                    </div>
                    <div className="text-sm text-purple-800">Model Version</div>
                  </div>
                </div>

                {/* Recommendations */}
                <div className="p-4 bg-yellow-50 rounded-lg">
                  <h3 className="font-medium text-yellow-800 mb-2">Recommendations</h3>
                  <ul className="text-sm text-yellow-700 space-y-1">
                    {prediction.churn_probability > 0.5 ? (
                      <>
                        <li>• Consider offering retention incentives</li>
                        <li>• Reach out for feedback on service quality</li>
                        <li>• Offer contract upgrades or discounts</li>
                      </>
                    ) : (
                      <>
                        <li>• Continue providing excellent service</li>
                        <li>• Consider upselling opportunities</li>
                        <li>• Monitor for any service issues</li>
                      </>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PredictionForm; 