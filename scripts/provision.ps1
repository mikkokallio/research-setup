param(
    [string]$Location = "swedencentral"
)

$ErrorActionPreference = "Stop"

function Get-EnvValue {
    param([string]$Name)
    $value = [Environment]::GetEnvironmentVariable($Name)
    if ([string]::IsNullOrWhiteSpace($value)) {
        throw "Missing required environment variable: $Name"
    }
    return $value
}

$subscriptionId = Get-EnvValue "AZ_SUBSCRIPTION_ID"
$resourceGroup = Get-EnvValue "AZ_RG"
$acrName = Get-EnvValue "AZ_ACR"
$acaEnv = Get-EnvValue "AZ_ACA_ENV"
$webApp = Get-EnvValue "AZ_WEB_APP"
$apiApp = Get-EnvValue "AZ_API_APP"

$logWorkspace = "$resourceGroup-logs"

Write-Host "Setting subscription $subscriptionId"
az account set --subscription $subscriptionId

Write-Host "Creating resource group $resourceGroup in $Location"
az group create --name $resourceGroup --location $Location | Out-Null

Write-Host "Creating ACR $acrName"
az acr create --name $acrName --resource-group $resourceGroup --location $Location --sku Standard --admin-enabled false | Out-Null

Write-Host "Creating Log Analytics workspace $logWorkspace"
az monitor log-analytics workspace create --resource-group $resourceGroup --workspace-name $logWorkspace --location $Location | Out-Null

$workspaceId = az monitor log-analytics workspace show --resource-group $resourceGroup --workspace-name $logWorkspace --query customerId -o tsv
$workspaceKey = az monitor log-analytics workspace get-shared-keys --resource-group $resourceGroup --workspace-name $logWorkspace --query primarySharedKey -o tsv

Write-Host "Creating Container Apps environment $acaEnv"
az containerapp env create `
    --name $acaEnv `
    --resource-group $resourceGroup `
    --location $Location `
    --logs-workspace-id $workspaceId `
    --logs-workspace-key $workspaceKey | Out-Null

Write-Host "Creating Container Apps $webApp and $apiApp"
az containerapp create `
    --name $webApp `
    --resource-group $resourceGroup `
    --environment $acaEnv `
    --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest `
    --ingress external `
    --target-port 8080 `
    --min-replicas 0 `
    --max-replicas 1 | Out-Null

az containerapp create `
    --name $apiApp `
    --resource-group $resourceGroup `
    --environment $acaEnv `
    --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest `
    --ingress external `
    --target-port 8000 `
    --min-replicas 0 `
    --max-replicas 1 | Out-Null

Write-Host "Assigning managed identities"
az containerapp identity assign --name $webApp --resource-group $resourceGroup | Out-Null
az containerapp identity assign --name $apiApp --resource-group $resourceGroup | Out-Null

$acrId = az acr show --name $acrName --resource-group $resourceGroup --query id -o tsv
$acrLogin = az acr show --name $acrName --resource-group $resourceGroup --query loginServer -o tsv

$webPrincipalId = az containerapp identity show --name $webApp --resource-group $resourceGroup --query principalId -o tsv
$apiPrincipalId = az containerapp identity show --name $apiApp --resource-group $resourceGroup --query principalId -o tsv

Write-Host "Granting AcrPull to container apps"
az role assignment create --assignee $webPrincipalId --role AcrPull --scope $acrId | Out-Null
az role assignment create --assignee $apiPrincipalId --role AcrPull --scope $acrId | Out-Null

Write-Host "Configuring ACR registry for container apps"
az containerapp registry set --name $webApp --resource-group $resourceGroup --server $acrLogin --identity system | Out-Null
az containerapp registry set --name $apiApp --resource-group $resourceGroup --server $acrLogin --identity system | Out-Null

Write-Host "Setting revision mode to multiple"
az containerapp revision set-mode --name $webApp --resource-group $resourceGroup --mode multiple | Out-Null
az containerapp revision set-mode --name $apiApp --resource-group $resourceGroup --mode multiple | Out-Null

Write-Host "Provisioning complete."
