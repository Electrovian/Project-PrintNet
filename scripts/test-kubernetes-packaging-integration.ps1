Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Kubernetes packaging integration hook placeholder."
python -m unittest discover -s deploy/tests -p "test_*.py"
