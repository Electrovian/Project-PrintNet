param(
    [string]$ClusterName = "printnet-dev",
    [string]$Namespace = "printnet",
    [string]$ReleaseName = "printnet",
    [string]$ChartPath = "deploy/helm/printnet"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

k3d cluster create $ClusterName --wait
helm upgrade --install $ReleaseName $ChartPath --namespace $Namespace --create-namespace
