$queries = @(
  '{\"query\": \"vintage graphic tee under $30\"}',
  '{\"query\": \"90s track jacket in size M\"}',
  '{\"query\": \"silk slip dress in midi length under $40\"}',
  '{\"query\": \"platform sneakers size 8\"}',
  '{\"query\": \"denim jacket under $50\"}',
  '{\"query\": \"oversized flannel shirt under $25\"}',
  '{\"query\": \"designer ballgown size XXS under $5\"}',
  '{\"query\": \"\"}',
  '{\"query\": \"\"}',
  '{}'
)
$i = 0
foreach ($q in $queries) {
  $i++
  Write-Host "--- request $i ---"
  curl.exe -s -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d $q | Out-Null
  Write-Host "sent"
}
Write-Host "trial done - check logs/runs.jsonl"