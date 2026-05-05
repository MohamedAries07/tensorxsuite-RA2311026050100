# RA100 TensorX - DockerHub Push Script (Windows PowerShell)
$ImageName = "ra100-tensorx"

Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host "📦 DockerHub Distribution Tool (Windows)" -ForegroundColor Cyan
Write-Host "------------------------------------------------" -ForegroundColor Cyan

# 1. Ask for DockerHub Username
$DockerUser = Read-Host "Enter your DockerHub Username"

if (-not $DockerUser) {
    Write-Host "❌ Error: Username cannot be empty." -ForegroundColor Red
    exit
}

# 2. Build the latest image
Write-Host "Building local image: $ImageName..."
docker build -t "$ImageName:latest" .

# 3. Login to DockerHub
Write-Host "Logging into DockerHub..."
docker login

# 4. Tag the image
Write-Host "Tagging image as $DockerUser/$ImageName:latest..."
docker tag "$ImageName:latest" "$DockerUser/$ImageName:latest"

# 5. Push to DockerHub
Write-Host "Pushing to DockerHub... this may take a moment."
docker push "$DockerUser/$ImageName:latest"

Write-Host "------------------------------------------------" -ForegroundColor Green
Write-Host "✅ SUCCESS!" -ForegroundColor Green
Write-Host "Your application is now public at: https://hub.docker.com/r/$DockerUser/$ImageName" -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Green
