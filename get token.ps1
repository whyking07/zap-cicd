# Log in and extract token from JSON response
$LoginUrl = "http://localhost:8000/token"
$Response = Invoke-RestMethod -Uri $LoginUrl -Method Post -ContentType "application/x-www-form-urlencoded" -Body "username=demo&password=secret"

# Extract token from JSON
$Token = $Response.access_token

# Save to a file for later use
Set-Content -Path "token.txt" -Value $Token
