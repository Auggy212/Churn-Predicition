# Churn Prediction Frontend

A modern React frontend for the Churn Prediction MLOps System, providing an intuitive interface for making predictions and monitoring model performance.

## 🚀 Features

- **Dashboard**: Overview of system status and quick actions
- **Prediction Form**: Interactive form for customer churn predictions
- **Analytics**: Visual charts and performance metrics
- **Model Information**: Detailed model specifications and technical details
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time API Integration**: Connects to the FastAPI backend

## 🛠️ Tech Stack

- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Beautiful and composable charts
- **Lucide React**: Beautiful & consistent icon toolkit
- **Axios**: HTTP client for API calls
- **React Router**: Client-side routing

## 📦 Installation

### Prerequisites

- Node.js 16+ and npm
- The backend API running on `http://localhost:8000`

### Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```

3. **Open your browser**:
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── Navbar.js          # Navigation component
│   ├── pages/
│   │   ├── Dashboard.js       # Main dashboard
│   │   ├── PredictionForm.js  # Churn prediction form
│   │   ├── Analytics.js       # Charts and metrics
│   │   └── ModelInfo.js       # Model specifications
│   ├── App.js                 # Main app component
│   ├── index.js               # React entry point
│   └── index.css              # Global styles
├── package.json
├── tailwind.config.js
└── postcss.config.js
```

## 🎨 Pages Overview

### Dashboard (`/`)
- System status overview
- Quick action cards
- Real-time health checks
- Model status indicators

### Prediction Form (`/predict`)
- Comprehensive customer data input form
- Real-time prediction results
- Risk assessment visualization
- Actionable recommendations

### Analytics (`/analytics`)
- Churn risk distribution charts
- Monthly trends analysis
- Feature importance visualization
- Model performance metrics
- Key insights and recommendations

### Model Information (`/model-info`)
- Detailed model specifications
- Technical implementation details
- System status monitoring
- Performance benchmarks

## 🔧 Configuration

### API Configuration

The frontend is configured to proxy requests to the backend API. The proxy is set in `package.json`:

```json
{
  "proxy": "http://localhost:8000"
}
```

### Environment Variables

Create a `.env` file in the frontend directory for custom configuration:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

### Docker Deployment

The frontend can be deployed using Docker. Add this to your `docker-compose.yml`:

```yaml
frontend:
  build: ./frontend
  ports:
    - "3000:3000"
  environment:
    - REACT_APP_API_URL=http://churn-api:8000
  depends_on:
    - churn-api
```

## 🎯 Usage Examples

### Making a Prediction

1. Navigate to the Prediction Form
2. Fill in customer information:
   - Basic details (tenure, charges)
   - Contract and payment information
   - Service preferences
   - Customer service history
3. Click "Predict Churn"
4. View results with risk assessment and recommendations

### Monitoring Analytics

1. Visit the Analytics page
2. Review key performance metrics
3. Analyze churn distribution patterns
4. Check feature importance rankings
5. Monitor monthly trends

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Error**:
   - Ensure the backend API is running on port 8000
   - Check network connectivity
   - Verify CORS settings in the backend

2. **Build Errors**:
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

3. **Styling Issues**:
   - Ensure Tailwind CSS is properly configured
   - Check for CSS conflicts

### Development Tips

- Use React Developer Tools for debugging
- Check browser console for API errors
- Monitor network tab for request/response details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 