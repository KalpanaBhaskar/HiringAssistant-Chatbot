#!/bin/bash

# Hugging Face Spaces Deployment Script
# This script helps you deploy your app to Hugging Face Spaces

echo "🚀 TalentScout - Hugging Face Spaces Deployment Helper"
echo "======================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Get Hugging Face username
echo "📝 Step 1: Configuration"
read -p "Enter your Hugging Face username: " HF_USERNAME

if [ -z "$HF_USERNAME" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

# Get space name
read -p "Enter your Space name (e.g., hiring-assistant): " SPACE_NAME

if [ -z "$SPACE_NAME" ]; then
    echo "❌ Space name cannot be empty"
    exit 1
fi

# Confirm
echo ""
echo "📋 Deployment Configuration:"
echo "   Username: $HF_USERNAME"
echo "   Space: $SPACE_NAME"
echo "   URL: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

# Create deployment directory
echo ""
echo "📁 Step 2: Preparing files..."
DEPLOY_DIR="deploy_hf"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# Copy necessary files
cp app.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/

# Create HF-specific README
cat > $DEPLOY_DIR/README.md << 'EOF'
---
title: TalentScout Hiring Assistant
emoji: 🎯
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
license: mit
---

# 🎯 TalentScout Hiring Assistant

An intelligent AI-powered chatbot for initial candidate screening in technology recruitment.

## Features

- 💬 Natural conversation flow
- 📝 Collects candidate information professionally
- 🎯 Generates technical questions based on tech stack
- 🎭 Sentiment analysis for better user experience
- ✅ Input validation (email, phone)
- 💾 Secure data storage

## How to Use

1. Start chatting with the assistant
2. Answer questions about your background
3. Share your technical skills
4. Answer the generated technical questions
5. Type "bye" when finished

## Tech Stack

- **Frontend**: Gradio
- **LLM**: Grok AI
- **Language**: Python 3.9+

## Privacy

Your data is handled securely and used only for recruitment purposes.

---

Built with ❤️ for TalentScout
EOF

cd $DEPLOY_DIR

# Initialize git repo
echo ""
echo "🔧 Step 3: Initializing git repository..."
git init
git add .
git commit -m "Initial commit: TalentScout Hiring Assistant"

# Add Hugging Face remote
HF_REPO="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
echo "🔗 Step 4: Adding Hugging Face remote..."
echo "   Repository: $HF_REPO"
git remote add origin $HF_REPO

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Create a new Space on Hugging Face:"
echo "   https://huggingface.co/new-space"
echo "   - Name: $SPACE_NAME"
echo "   - SDK: Gradio"
echo "   - Make it Public"
echo ""
echo "2. Add your GROK_API_KEY as a Secret:"
echo "   Go to: $HF_REPO/settings"
echo "   → Secrets → New Secret"
echo "   Name: GROK_API_KEY"
echo "   Value: your_api_key_here"
echo ""
echo "3. Push your code:"
echo "   cd $DEPLOY_DIR"
echo "   git push origin main"
echo ""
echo "   If it asks for credentials, use:"
echo "   Username: $HF_USERNAME"
echo "   Password: Your Hugging Face token from:"
echo "   https://huggingface.co/settings/tokens"
echo ""
echo "4. Your app will be live at:"
echo "   $HF_REPO"
echo ""
echo "🎉 Happy deploying!"
