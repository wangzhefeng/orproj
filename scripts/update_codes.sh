# !/bin/bash

echo "--------------------------"
echo "update TinyLLM codes..."
echo "--------------------------"
git checkout main
echo "Successfully checked out main."

git add .
git commit -m "update codes"

git pull
echo "Successfully pulled the latest changes."

git push
echo "Successfully checked out master and updated the code."
