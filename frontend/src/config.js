// Configuration for different environments
const config = {
  // API base URL - always use localhost since frontend is running locally
  apiBaseUrl: 'http://localhost:8000',
  
  // Environment detection
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
  isLocal: true,
  
  // API endpoints
  endpoints: {
    health: '/health',
    predict: '/predict',
    modelInfo: '/model-info',
    metrics: '/metrics',
    prometheus: '/prometheus'
  }
};

console.log('API Configuration:', {
  apiBaseUrl: config.apiBaseUrl,
  isLocal: config.isLocal,
  hostname: window.location.hostname,
  port: window.location.port
});

export default config; 