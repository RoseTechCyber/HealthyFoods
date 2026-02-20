# HealthyFoods - AI Agentic Food Ordering Platform

[![CI/CD](https://github.com/RoseTechCyber/HealthyFoods/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/RoseTechCyber/HealthyFoods/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

HealthyFoods is an advanced AI Agentic Web Application tailored for real-time, 24/7 intelligent processing, validation, payment, routing and delivery of food orders. The platform connects customers with subscribed catering firms through an intelligent AI Agent that serves as a mediator.

## 🌟 Features

### Core Capabilities
- **24/7 Real-time Order Processing**: Continuous order handling with intelligent validation
- **AI-Powered Agent**: Autonomous decision-making for routing, validation, and optimization
- **Smart Payment Processing**: AI-driven fraud detection and secure payment handling
- **Intelligent Delivery Routing**: Optimal driver assignment and route optimization
- **Personalized Recommendations**: AI-generated food suggestions based on customer preferences

### Azure Integration
- **Azure OpenAI**: Advanced AI capabilities for intelligent decision-making
- **Azure Content Safety**: Automated content moderation and safety checks
- **Azure Power Automate**: Automated workflow management
- **Azure MCP (Model Context Protocol)**: Enhanced AI context management
- **Azure Application Insights**: Real-time monitoring and analytics
- **Azure Service Bus**: Reliable message queuing for asynchronous processing
- **Azure Storage**: Secure data persistence
- **Azure Key Vault**: Secrets and credentials management

### Security Features
- **Content Safety**: Automated content moderation using Azure Content Safety
- **Data Protection**: Encryption at rest and in transit
- **Secure Headers**: Protection against common web vulnerabilities
- **API Authentication**: Secure API access with token-based authentication

## 🏗️ Architecture

The application follows a modern microservices architecture:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Customers  │────▶│   AI Agent   │────▶│   Catering  │
│             │     │ Orchestrator │     │    Firms    │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ├──────▶ Payment Gateway
                           ├──────▶ Delivery Service
                           ├──────▶ Azure Services
                           └──────▶ Analytics Engine
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Azure subscription (for cloud features)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/RoseTechCyber/HealthyFoods.git
cd HealthyFoods
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your Azure credentials and configuration
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python -m uvicorn app.main:app --reload
```

5. **Access the API**
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Docker Deployment

```bash
docker-compose up -d
```

## 📚 API Documentation

### Core Endpoints

#### Orders
- `POST /api/v1/orders` - Create new order
- `GET /api/v1/orders/{order_id}` - Get order details
- `GET /api/v1/orders/{order_id}/track` - Track order in real-time
- `PUT /api/v1/orders/{order_id}/status` - Update order status

#### Customers
- `POST /api/v1/customers` - Register new customer
- `GET /api/v1/customers/{customer_id}` - Get customer details
- `GET /api/v1/customers/{customer_id}/recommendations` - Get AI recommendations

#### Catering Firms
- `POST /api/v1/catering-firms` - Register catering firm
- `GET /api/v1/catering-firms` - List catering firms
- `GET /api/v1/catering-firms/{firm_id}/menu` - Get firm menu

#### Payments
- `POST /api/v1/payments` - Process payment
- `GET /api/v1/payments/{payment_id}` - Get payment details

#### Delivery
- `POST /api/v1/delivery` - Assign delivery
- `GET /api/v1/delivery/{delivery_id}/track` - Track delivery in real-time

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example` for complete list):

- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI service endpoint
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_CONTENT_SAFETY_ENDPOINT`: Content Safety service endpoint
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string
- `AZURE_SERVICE_BUS_CONNECTION_STRING`: Service Bus connection string

## 🔐 Security

### Security Features Implemented

1. **Content Safety**: All user-generated content is validated using Azure Content Safety
2. **Data Encryption**: Sensitive data is encrypted using industry-standard algorithms
3. **Secure Headers**: Security headers prevent XSS, clickjacking, and other attacks
4. **API Authentication**: Token-based authentication for all API endpoints
5. **Rate Limiting**: Protection against DDoS and brute-force attacks

### Security Best Practices

- Store secrets in Azure Key Vault
- Use managed identities for Azure service authentication
- Enable HTTPS only
- Regular security audits using Azure Security Center

## 🚢 Deployment

### Azure Deployment

1. **Deploy Azure Resources**
```bash
az deployment group create \
  --resource-group healthyfoods-rg \
  --template-file azure-resources.json
```

2. **Configure CI/CD**
- Set up GitHub Actions secrets for Azure credentials
- Push to main branch to trigger automated deployment

3. **Configure Azure Web App**
```bash
az webapp config appsettings set \
  --resource-group healthyfoods-rg \
  --name healthyfoods \
  --settings @appsettings.json
```

## 🧪 Testing

Run tests:
```bash
SECRET_KEY='test-secret-key-for-ci' python -m pytest tests/ --cov=app
```

## 📊 Monitoring

### Application Insights
- Monitor application performance
- Track custom metrics
- View real-time logs

### Alerts
Configure alerts for:
- High error rates
- Performance degradation
- Security incidents

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: support@rosetechcyber.com

## 🗺️ Roadmap

- [ ] Mobile application (iOS/Android)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Integration with more payment gateways
- [ ] Enhanced AI recommendations engine
- [ ] Voice ordering capability

## 👥 Team

Developed by RoseTechCyber

---

**Note**: This application requires Azure services for full functionality. Ensure proper Azure subscription and service configuration before deployment.
