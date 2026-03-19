Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

python -m unittest discover -s deploy/tests -p "test_*.py"
