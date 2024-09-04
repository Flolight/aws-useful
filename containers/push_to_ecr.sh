repository="my-repo"
account=$(aws sts get-caller-identity --query "Account" --output text)
region="eu-west-1"

docker build --platform linux/amd64 -t $repository:test .

aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $account.dkr.ecr.$region.amazonaws.com

repo_exists=$(aws ecr describe-repositories --repository-names $repository 2>/dev/null)

if [ -z "$repo_exists" ]; then
    echo "ECR repository doesn't exist. Creating..."
    aws ecr create-repository --repository-name $repository --region $region --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
else
    echo "ECR repository already exists. Not creating and continue."
fi

docker tag "$repository:test" "$account.dkr.ecr.$region.amazonaws.com/$repository:latest"

docker push "$account.dkr.ecr.$region.amazonaws.com/$repository:latest"
