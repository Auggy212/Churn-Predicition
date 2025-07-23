import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  TrendingUp, 
  Activity, 
  BarChart3, 
  Users, 
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const [healthStatus, setHealthStatus] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [healthResponse, modelResponse] = await Promise.all([
          axios.get('/health'),
          axios.get('/model-info')
        ]);
        setHealthStatus(healthResponse.data);
        setModelInfo(modelResponse.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const stats = [
    {
      name: 'Model Status',
      value: healthStatus?.model_loaded ? 'Active' : 'Inactive',
      icon: Brain,
      color: healthStatus?.model_loaded ? 'text-success-600' : 'text-danger-600',
      bgColor: healthStatus?.model_loaded ? 'bg-success-50' : 'bg-danger-50',
    },
    {
      name: 'Model Type',
      value: modelInfo?.model_type || 'Unknown',
      icon: Activity,
      color: 'text-primary-600',
      bgColor: 'bg-primary-50',
    },
    {
      name: 'Model Version',
      value: modelInfo?.model_version || '1.0.0',
      icon: TrendingUp,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      name: 'API Status',
      value: healthStatus?.status || 'Unknown',
      icon: CheckCircle,
      color: 'text-success-600',
      bgColor: 'bg-success-50',
    },
  ];

  const quickActions = [
    {
      name: 'Make Prediction',
      description: 'Predict customer churn probability',
      href: '/predict',
      icon: Brain,
      color: 'text-primary-600',
      bgColor: 'bg-primary-50',
    },
    {
      name: 'View Analytics',
      description: 'Explore model performance metrics',
      href: '/analytics',
      icon: BarChart3,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      name: 'Model Information',
      description: 'Detailed model specifications',
      href: '/model-info',
      icon: Activity,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Churn Prediction Dashboard
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Monitor your machine learning model performance and make predictions with our comprehensive MLOps platform.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center">
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-lg font-semibold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Link
                key={action.name}
                to={action.href}
                className="card hover:shadow-md transition-shadow duration-200 group"
              >
                <div className="flex items-center mb-4">
                  <div className={`p-3 rounded-lg ${action.bgColor} group-hover:scale-110 transition-transform duration-200`}>
                    <Icon className={`h-6 w-6 ${action.color}`} />
                  </div>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {action.name}
                </h3>
                <p className="text-gray-600 text-sm">
                  {action.description}
                </p>
              </Link>
            );
          })}
        </div>
      </div>

      {/* System Status */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">System Status</h2>
        <div className="space-y-3">
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
            <span className="text-gray-600">Model Type</span>
            <span className="text-gray-900 font-medium">
              {healthStatus?.model_type || 'Unknown'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 