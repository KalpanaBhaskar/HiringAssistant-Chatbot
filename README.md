# 🎯 TalentScout Hiring Assistant Chatbot

An intelligent AI-powered chatbot designed for initial candidate screening in technology recruitment. Built with Gradio and powered by Grok AI.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Gradio](https://img.shields.io/badge/gradio-4.19.2-orange)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Deployment](#deployment)
- [Data Privacy](#data-privacy)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)

## 🌟 Overview

TalentScout Hiring Assistant is a conversational AI chatbot that streamlines the initial screening process for technology positions. The chatbot conducts professional interviews, collects candidate information, and generates tailored technical questions based on each candidate's declared tech stack.

### Purpose

This project demonstrates:
- Effective prompt engineering for conversational AI
- Integration with Large Language Models (Grok AI)
- Building intuitive user interfaces with Gradio
- Implementing data validation and storage
- Sentiment analysis for enhanced user experience

## ✨ Features

### Core Functionality
- ✅ **Intelligent Conversation Flow**: Natural, context-aware dialogue management
- 📝 **Information Gathering**: Collects essential candidate details:
  - Full Name
  - Email Address
  - Phone Number
  - Years of Experience
  - Desired Position(s)
  - Current Location
  - Tech Stack
- 🎯 **Dynamic Technical Questions**: Generates 3-5 relevant questions based on candidate's tech stack
- ✅ **Input Validation**: Automatic validation of email and phone formats
- 💾 **Data Storage**: Secure local storage of candidate information in JSON format
- 🎭 **Sentiment Analysis**: Real-time analysis to provide empathetic responses
- 🔄 **Context Management**: Maintains conversation context throughout the session
- 🚪 **Graceful Exit**: Handles conversation-ending keywords professionally

### Enhanced Features
- 📊 **Data Viewer Dashboard**: Separate interface to view and analyze collected data
- 📈 **Recruitment Statistics**: Analytics on candidate demographics and skills
- 🎨 **Modern UI**: Clean, professional interface with custom styling
- 🔒 **Privacy-Compliant**: GDPR-compliant data handling practices

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Grok API key (from [x.ai console](https://console.x.ai/))
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd hiring-assistant-chatbot
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```bash
GROK_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with your Grok API key from [x.ai console](https://console.x.ai/).

## 💻 Usage

### Running the Main Application

```bash
python app.py
```

The chatbot will be available at: `http://localhost:7860`

### Running the Data Viewer (Optional)

In a separate terminal:
```bash
python view_candidates.py
```

The data viewer will be available at: `http://localhost:7861`

### Testing the Chatbot

1. Open your browser to `http://localhost:7860`
2. The chatbot will greet you automatically
3. Follow the conversation naturally:
   - Provide your name when asked
   - Answer each question (email, phone, experience, etc.)
   - When asked about tech stack, list your skills (e.g., "Python, Django, React, PostgreSQL")
   - Answer the technical questions generated
4. Type "bye" or "goodbye" to end the conversation
5. Your data will be saved in the `candidate_data/` directory

## 📁 Project Structure

```
hiring-assistant-chatbot/
├── app.py                      # Main chatbot application
├── view_candidates.py          # Data viewer dashboard
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── candidate_data/            # Stored candidate information (created automatically)
│   └── candidate_YYYYMMDD_HHMMSS.json
└── src/                       # Additional modules (if needed)
```

## 🔧 Technical Details

### Tech Stack

- **Frontend**: Gradio 4.19.2
- **LLM**: Grok AI (via OpenAI-compatible API)
- **Language**: Python 3.8+
- **Data Storage**: JSON files (local filesystem)
- **Dependencies**:
  - gradio: UI framework
  - openai: API client (compatible with Grok)
  - python-dotenv: Environment variable management
  - pydantic: Data validation

### Architecture

#### 1. Conversation State Management
The `ConversationState` class tracks:
- Collected candidate information
- Current conversation stage
- Session metadata
- Sentiment scores

#### 2. Prompt Engineering Strategy

**System Prompt Design**:
- Defines chatbot personality and objectives
- Provides clear guidelines for information gathering
- Specifies how to generate technical questions
- Sets boundaries for conversation scope

**Context Management**:
- Conversation history is passed with each API call
- Current state is included in system prompt
- Sentiment analysis informs response tone

#### 3. Data Validation

**Email Validation**:
```python
pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

**Phone Validation**:
- Removes common separators
- Validates minimum 10 digits
- Accepts international formats

**Auto-Extraction**:
- Regex patterns detect emails, phones, and experience mentions
- Automatic population of candidate data fields

#### 4. Sentiment Analysis

Simple keyword-based sentiment analysis:
- Positive keywords: excited, happy, great, etc.
- Negative keywords: worried, nervous, confused, etc.
- Influences chatbot's response tone
- Stored for recruiter insights

### LLM Integration

**Model**: `grok-beta` (Grok AI)

**API Configuration**:
```python
client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1"
)
```

**Parameters**:
- Temperature: 0.7 (balanced creativity and consistency)
- Max Tokens: 500 (concise responses)
- Model: grok-beta

## 🌐 Deployment

### Option 1: Hugging Face Spaces (Recommended for Beginners)

1. **Create a Hugging Face account** at [huggingface.co](https://huggingface.co)

2. **Create a new Space**:
   - Go to "New Space"
   - Choose "Gradio" as the SDK
   - Name your space (e.g., "hiring-assistant")

3. **Add your files**:
   - Upload `app.py`
   - Upload `requirements.txt`
   - Add your `GROK_API_KEY` in Space Settings → Secrets

4. **Configure Space**:
   Create `README.md` in the Space with:
   ```yaml
   ---
   title: Hiring Assistant
   emoji: 🎯
   colorFrom: blue
   colorTo: green
   sdk: gradio
   sdk_version: 4.19.2
   app_file: app.py
   pinned: false
   ---
   ```

5. **Deploy**: The space will build and deploy automatically!

### Option 2: AWS EC2

1. **Launch EC2 Instance**:
   - Choose Ubuntu Server 22.04 LTS
   - Instance type: t2.micro (free tier) or t2.small
   - Configure security group to allow port 7860

2. **Connect and setup**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone your repository
git clone <your-repo-url>
cd hiring-assistant-chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
echo "GROK_API_KEY=your_key_here" > .env

# Run with nohup (background process)
nohup python app.py > output.log 2>&1 &
```

3. **Access**: Use your EC2 public IP: `http://YOUR_EC2_IP:7860`

### Option 3: Google Cloud Run

1. **Install Google Cloud SDK**

2. **Create Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "app.py"]
```

3. **Modify app.py** launch:
```python
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.getenv("PORT", 7860)),
    share=False
)
```

4. **Deploy**:
```bash
gcloud run deploy hiring-assistant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔒 Data Privacy

### Compliance Measures

- **Local Storage**: All data stored locally in JSON format
- **No Third-Party Sharing**: Data never shared with external services
- **Secure API Calls**: HTTPS encryption for all API communications
- **Minimal Data Collection**: Only essential information gathered
- **User Control**: Candidates can exit anytime
- **Data Retention**: Manual deletion capability
- **GDPR Compliance**: Follows data minimization principles

### Security Best Practices

1. **Environment Variables**: API keys stored in `.env` (not in repository)
2. **Input Validation**: All user inputs validated and sanitized
3. **Error Handling**: Graceful error messages without exposing system details
4. **Access Control**: Data viewer requires local access

### Handling Sensitive Information

- Emails and phone numbers validated but not verified
- No password or financial information collected
- Session IDs used for anonymized tracking
- Data files include timestamps for audit trails

## 🎯 Challenges & Solutions

### Challenge 1: Maintaining Conversation Context
**Problem**: LLMs are stateless; each call is independent.

**Solution**: 
- Implemented `ConversationState` class to track collected information
- Pass full conversation history with each API call
- Include current state in system prompt for context awareness

### Challenge 2: Generating Relevant Technical Questions
**Problem**: Questions must match candidate's specific tech stack and experience level.

**Solution**:
- Detailed system prompt with examples
- Pass collected tech stack explicitly to LLM
- Use experience level to calibrate question difficulty
- Temperature set to 0.7 for balanced creativity

### Challenge 3: Input Validation Without Frustrating Users
**Problem**: Need to validate emails/phones without being annoying.

**Solution**:
- Automatic extraction using regex patterns
- Gentle validation in chatbot responses
- Allow conversational formats (e.g., "my email is john@example.com")
- Provide helpful error messages when validation fails

### Challenge 4: Handling Unexpected Inputs
**Problem**: Users might go off-topic or provide incomplete information.

**Solution**:
- Comprehensive system prompt with redirection guidelines
- Fallback responses for unrecognized inputs
- Graceful handling of conversation-ending keywords
- Context-aware prompting to get missing information

### Challenge 5: Data Storage and Retrieval
**Problem**: Need persistent storage without database complexity.

**Solution**:
- JSON file storage with timestamped filenames
- Structured data format for easy parsing
- Separate data viewer application
- Statistical analysis capabilities

## 🚀 Future Enhancements

### Planned Features
- [ ] **Multi-language Support**: Interact in multiple languages
- [ ] **Advanced Sentiment Analysis**: Using transformer models
- [ ] **Email Integration**: Automated email notifications to recruiters
- [ ] **Calendar Integration**: Schedule follow-up interviews
- [ ] **Resume Parser**: Extract information from uploaded resumes
- [ ] **Video Interview**: Integrate video call capabilities
- [ ] **Database Migration**: Move from JSON to PostgreSQL/MongoDB
- [ ] **API Endpoints**: RESTful API for integration
- [ ] **Mobile App**: Native mobile applications
- [ ] **Analytics Dashboard**: Advanced visualizations

### Optimization Ideas
- Implement caching for common questions
- Batch processing for multiple candidates
- Real-time collaboration features
- Integration with ATS (Applicant Tracking Systems)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please contact: [your-email@example.com]

## 🙏 Acknowledgments

- Grok AI by xAI for the powerful language model
- Gradio team for the excellent UI framework
- OpenAI for the API client library

---

**Built with ❤️ for TalentScout AI/ML Internship Assignment**