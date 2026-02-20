# Deployment Guide for HealthyFoods

This guide provides step-by-step instructions for deploying the HealthyFoods AI Agentic Web Application to Azure.

## Prerequisites

- Azure subscription
- Azure CLI installed and configured
- Docker installed (for container deployment)
- GitHub account (for CI/CD)

## Step 1: Create Azure Resources

### 1.1 Create Resource Group

```bash
az group create \
  --name healthyfoods-rg \
  --location eastus
```

### 1.2 Deploy Azure Resources

Deploy all required Azure resources using the ARM template:

```bash
az deployment group create \
  --resource-group healthyfoods-rg \
  --template-file azure-resources.json \
  --parameters appName=healthyfoods
```

This will create:
- App Service Plan
- Web App
- Azure OpenAI Service
- Azure Content Safety
- Azure Storage Account
- Azure Service Bus
- Application Insights

### 1.3 Create Azure Key Vault

```bash
az keyvault create \
  --name healthyfoods-kv \
  --resource-group healthyfoods-rg \
  --location eastus
```

## Step 2: Configure Secrets

### 2.1 Store Secrets in Key Vault

```bash
# Store OpenAI API Key
az keyvault secret set \
  --vault-name healthyfoods-kv \
  --name AZURE-OPENAI-API-KEY \
  --value "your-api-key"

# Store Content Safety Key
az keyvault secret set \
  --vault-name healthyfoods-kv \
  --name AZURE-CONTENT-SAFETY-KEY \
  --value "your-key"

# Store database connection string
az keyvault secret set \
  --vault-name healthyfoods-kv \
  --name DATABASE-URL \
  --value "your-connection-string"
```

### 2.2 Configure Managed Identity

```bash
# Enable system-assigned managed identity for Web App
az webapp identity assign \
  --resource-group healthyfoods-rg \
  --name healthyfoods

# Grant Key Vault access to Web App
az keyvault set-policy \
  --name healthyfoods-kv \
  --object-id $(az webapp identity show \
    --resource-group healthyfoods-rg \
    --name healthyfoods \
    --query principalId \
    --output tsv) \
  --secret-permissions get list
```

## Step 3: Build and Push Docker Image

### 3.1 Build Docker Image

```bash
docker build -t healthyfoods:latest .
```

### 3.2 Create Azure Container Registry

```bash
az acr create \
  --resource-group healthyfoods-rg \
  --name healthyfoodscr \
  --sku Basic
```

### 3.3 Push Image to ACR

```bash
# Login to ACR
az acr login --name healthyfoodscr

# Tag image
docker tag healthyfoods:latest healthyfoodscr.azurecr.io/healthyfoods:latest

# Push image
docker push healthyfoodscr.azurecr.io/healthyfoods:latest
```

## Step 4: Configure Web App

### 4.1 Configure Container Settings

```bash
az webapp config container set \
  --resource-group healthyfoods-rg \
  --name healthyfoods \
  --docker-custom-image-name healthyfoodscr.azurecr.io/healthyfoods:latest \
  --docker-registry-server-url https://healthyfoodscr.azurecr.io
```

### 4.2 Configure Application Settings

```bash
az webapp config appsettings set \
  --resource-group healthyfoods-rg \
  --name healthyfoods \
  --settings \
    WEBSITES_PORT=8000 \
    AZURE_KEY_VAULT_URL=https://healthyfoods-kv.vault.azure.net/ \
    APPLICATIONINSIGHTS_CONNECTION_STRING="$(az monitor app-insights component show \
      --resource-group healthyfoods-rg \
      --app healthyfoods-insights \
      --query connectionString \
      --output tsv)"
```

## Step 5: Set Up CI/CD

### 5.1 Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to repository Settings > Secrets and variables > Actions
2. Add secrets:
   - `AZURE_CREDENTIALS`: Azure service principal credentials
  - `AZURE_WEBAPP_NAME`: healthyfoods
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: Download from Azure Portal

### 5.2 Get Azure Credentials

```bash
az ad sp create-for-rbac \
  --name "healthyfoods-github" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/healthyfoods-rg \
  --sdk-auth
```

Copy the JSON output and add it as `AZURE_CREDENTIALS` secret in GitHub.

## Step 6: Configure Azure Power Automate

### 6.1 Create Power Automate Flow

1. Go to [Power Automate](https://flow.microsoft.com)
2. Create new flow "When HTTP request received"
3. Configure trigger for order processing
4. Add actions for notifications and integrations

### 6.2 Update MCP Endpoint

Add the Power Automate HTTP endpoint to your environment variables:

```bash
az webapp config appsettings set \
  --resource-group healthyfoods-rg \
  --name healthyfoods \
  --settings AZURE_MCP_ENDPOINT="your-power-automate-endpoint"
```

## Step 7: Configure Monitoring

### 7.1 Enable Application Insights

Application Insights is automatically configured through the ARM template.

### 7.2 Create Alerts

```bash
# Create alert for high error rate
az monitor metrics alert create \
  --name high-error-rate \
  --resource-group healthyfoods-rg \
  --scopes $(az webapp show \
    --resource-group healthyfoods-rg \
    --name healthyfoods \
    --query id \
    --output tsv) \
  --condition "avg requests/failed > 5" \
  --window-size 5m \
  --evaluation-frequency 1m
```

## Step 8: Verify Deployment

### 8.1 Test Endpoints

```bash
# Health check
curl https://healthyfoods.azurewebsites.net/health

# API documentation
open https://healthyfoods.azurewebsites.net/docs
```

### 8.2 Monitor Logs

```bash
# Stream logs
az webapp log tail \
  --resource-group healthyfoods-rg \
  --name healthyfoods
```

## Step 9: Post-Deployment Configuration

### 9.1 Configure Custom Domain (Optional)

```bash
az webapp config hostname add \
  --resource-group healthyfoods-rg \
  --webapp-name healthyfoods \
  --hostname www.yourdomain.com
```

### 9.2 Enable HTTPS

```bash
az webapp config ssl bind \
  --resource-group healthyfoods-rg \
  --name healthyfoods \
  --certificate-thumbprint {thumbprint} \
  --ssl-type SNI
```

## Troubleshooting

### Common Issues

1. **Container fails to start**
   - Check application logs: `az webapp log tail`
   - Verify environment variables are set correctly
   - Ensure container port is set to 8000

2. **Azure OpenAI connection fails**
   - Verify API key in Key Vault
   - Check endpoint URL format
   - Ensure managed identity has permissions

3. **Database connection errors**
   - Verify connection string
   - Check firewall rules
   - Ensure Web App IP is whitelisted

### Support

For additional support:
- Check [Azure documentation](https://docs.microsoft.com/azure)
- Contact support@rosetechcyber.com

## Cleanup

To remove all resources:

```bash
az group delete --name healthyfoods-rg --yes --no-wait
```

---

**Note**: Replace placeholder values (like `{subscription-id}`) with your actual values.
