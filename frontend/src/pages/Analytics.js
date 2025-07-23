import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { 
  TrendingUp, 
  Users, 
  AlertTriangle, 
  CheckCircle,
  Activity,
  Clock
} from 'lucide-react';
import axios from 'axios';

const Analytics = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock data for demonstration - in real app, this would come from API
  const churnDistribution = [
    { name: 'Low Risk', value: 65, color: '#22c55e' },
    { name: 'Medium Risk', value: 25, color: '#eab308' },
    { name: 'High Risk', value: 10, color: '#ef4444' }
  ];

  const monthlyTrends = [
    { month: 'Jan', churnRate: 12, predictions: 150 },
    { month: 'Feb', churnRate: 15, predictions: 180 },
    { month: 'Mar', churnRate: 11, predictions: 165 },
    { month: 'Apr', churnRate: 18, predictions: 200 },
    { month: 'May', churnRate: 14, predictions: 175 },
    { month: 'Jun', churnRate: 16, predictions: 190 }
  ];

  const featureImportance = [
    { feature: 'Tenure', importance: 85 },
    { feature: 'Monthly Charges', importance: 72 },
    { feature: 'Contract Type', importance: 68 },
    { feature: 'Payment Method', importance: 45 },
    { feature: 'Internet Service', importance: 38 },
    { feature: 'Customer Service Calls', importance: 32 }
  ];

  const modelPerformance = [
    { metric: 'Accuracy', value: 85.2, target: 80 },
    { metric: 'Precision', value: 78.5, target: 75 },
    { metric: 'Recall', value: 72.3, target: 70 },
    { metric: 'F1-Score', value: 75.2, target: 72 },
    { metric: 'ROC-AUC', value: 84.7, target: 80 }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

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
          Model Analytics & Performance
        </h1>
        <p className="text-gray-600">
          Comprehensive insights into model performance and prediction patterns
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 rounded-lg bg-success-50">
              <CheckCircle className="h-6 w-6 text-success-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">85.2%</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 rounded-lg bg-primary-50">
              <Users className="h-6 w-6 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Predictions</p>
              <p className="text-2xl font-bold text-gray-900">1,260</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 rounded-lg bg-yellow-50">
              <AlertTriangle className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Churn Rate</p>
              <p className="text-2xl font-bold text-gray-900">14.3%</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 rounded-lg bg-purple-50">
              <Activity className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Model Version</p>
              <p className="text-2xl font-bold text-gray-900">1.0.0</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Churn Distribution */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Churn Risk Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={churnDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {churnDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Monthly Trends */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Monthly Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="churnRate"
                stroke="#ef4444"
                strokeWidth={2}
                name="Churn Rate (%)"
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="predictions"
                stroke="#3b82f6"
                strokeWidth={2}
                name="Predictions"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Feature Importance */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Feature Importance</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={featureImportance} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} />
              <YAxis dataKey="feature" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="importance" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Model Performance */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Model Performance Metrics</h2>
          <div className="space-y-4">
            {modelPerformance.map((metric) => (
              <div key={metric.metric} className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium text-gray-700">{metric.metric}</span>
                  <span className="text-gray-600">{metric.value}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      metric.value >= metric.target ? 'bg-success-500' : 'bg-yellow-500'
                    }`}
                    style={{ width: `${Math.min(metric.value, 100)}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500">
                  Target: {metric.target}%
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Additional Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Key Insights</h2>
          <ul className="space-y-3 text-gray-700">
            <li className="flex items-start">
              <CheckCircle className="h-5 w-5 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Model accuracy exceeds target by 5.2%</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="h-5 w-5 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Tenure is the most important feature (85% importance)</span>
            </li>
            <li className="flex items-start">
              <AlertTriangle className="h-5 w-5 text-yellow-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Churn rate increased in April (18%) - needs investigation</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="h-5 w-5 text-success-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>65% of customers are classified as low churn risk</span>
            </li>
          </ul>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recommendations</h2>
          <ul className="space-y-3 text-gray-700">
            <li className="flex items-start">
              <TrendingUp className="h-5 w-5 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Focus retention efforts on customers with short tenure</span>
            </li>
            <li className="flex items-start">
              <TrendingUp className="h-5 w-5 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Monitor high monthly charge customers more closely</span>
            </li>
            <li className="flex items-start">
              <TrendingUp className="h-5 w-5 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Investigate April churn spike for root cause</span>
            </li>
            <li className="flex items-start">
              <TrendingUp className="h-5 w-5 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Consider model retraining with recent data</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Analytics; 