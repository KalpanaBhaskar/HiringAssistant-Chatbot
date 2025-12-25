"""
TalentScout Hiring Assistant Chatbot
A conversational AI chatbot for initial candidate screening
"""

import gradio as gr
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from typing import List, Tuple
from datetime import datetime
import re

# Load environment variables
load_dotenv()

# Initialize Grok client (Grok API is compatible with OpenAI SDK)
client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# System prompt that defines the chatbot's behavior
SYSTEM_PROMPT = """You are a professional Hiring Assistant chatbot for TalentScout, a recruitment agency specializing in technology placements. Your role is to conduct initial candidate screening interviews.

Your responsibilities:
1. Greet candidates warmly and explain your purpose
2. Collect the following information in a conversational manner:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack (programming languages, frameworks, databases, tools)
3. After gathering their tech stack, generate 3-5 relevant technical questions to assess their proficiency
4. Maintain context throughout the conversation
5. Be professional, friendly, and encouraging
6. If the user says goodbye, thank them, or uses conversation-ending keywords (bye, goodbye, exit, quit, thanks bye, etc.), gracefully end the conversation

Important guidelines:
- Ask for information ONE piece at a time to keep the conversation natural
- Don't overwhelm the candidate with multiple questions at once
- Validate email and phone formats gently
- For tech stack, ask them to list their technical skills
- Generate technical questions that are practical and relevant to their experience level
- Stay focused on the hiring process - politely redirect if conversation goes off-topic
- Be encouraging and positive throughout

Remember: You're representing TalentScout, so maintain professionalism while being approachable."""


class ConversationState:
    """Manages the state of the conversation"""
    def __init__(self):
        self.candidate_info = {
            "name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "position": None,
            "location": None,
            "tech_stack": None
        }
        self.stage = "greeting"
        self.questions_asked = False
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.sentiment_scores = []
        
    def is_complete(self):
        """Check if all information is collected"""
        return all(value is not None for value in self.candidate_info.values())
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "candidate_info": self.candidate_info,
            "stage": self.stage,
            "questions_asked": self.questions_asked,
            "session_id": self.session_id,
            "sentiment_scores": self.sentiment_scores
        }
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone format (basic validation)"""
        # Remove common separators
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        return len(clean_phone) >= 10 and clean_phone.isdigit()


def analyze_sentiment(text: str) -> dict:
    """
    Simple sentiment analysis based on keywords
    Returns sentiment score and emotion
    """
    positive_words = ['excited', 'happy', 'great', 'excellent', 'good', 'love', 
                      'wonderful', 'fantastic', 'amazing', 'looking forward']
    negative_words = ['worried', 'nervous', 'concerned', 'difficult', 'hard',
                      'confused', 'frustrated', 'anxious', 'stress']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return {"sentiment": "positive", "score": min(pos_count / 3, 1.0)}
    elif neg_count > pos_count:
        return {"sentiment": "negative", "score": min(neg_count / 3, 1.0)}
    else:
        return {"sentiment": "neutral", "score": 0.5}


def save_candidate_data(conv_state: ConversationState, conversation_history: List[Tuple[str, str]]):
    """
    Save candidate data to a JSON file
    Creates a data directory if it doesn't exist
    """
    # Create data directory
    os.makedirs("candidate_data", exist_ok=True)
    
    # Prepare data
    data = {
        "session_id": conv_state.session_id,
        "timestamp": datetime.now().isoformat(),
        "candidate_info": conv_state.candidate_info,
        "conversation_history": [
            {"user": user_msg, "bot": bot_msg} 
            for user_msg, bot_msg in conversation_history
        ],
        "sentiment_analysis": {
            "scores": conv_state.sentiment_scores,
            "average_sentiment": sum(s["score"] for s in conv_state.sentiment_scores) / len(conv_state.sentiment_scores) if conv_state.sentiment_scores else 0
        }
    }
    
    # Save to file
    filename = f"candidate_data/candidate_{conv_state.session_id}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filename


def chat_with_grok(message: str, history: List[Tuple[str, str]], state: dict) -> Tuple[str, List[Tuple[str, str]], dict]:
    """
    Main chat function that processes user messages and generates responses
    
    Args:
        message: User's current message
        history: Chat history as list of (user_msg, bot_msg) tuples
        state: Current conversation state
    
    Returns:
        Tuple of (response, updated_history, updated_state)
    """
    
    # Initialize or load conversation state
    if not state:
        conv_state = ConversationState()
        state = conv_state.to_dict()
    else:
        conv_state = ConversationState()
        conv_state.candidate_info = state["candidate_info"]
        conv_state.stage = state["stage"]
        conv_state.questions_asked = state["questions_asked"]
        conv_state.session_id = state.get("session_id", datetime.now().strftime("%Y%m%d_%H%M%S"))
        conv_state.sentiment_scores = state.get("sentiment_scores", [])
    
    # Analyze sentiment of user message
    sentiment = analyze_sentiment(message)
    conv_state.sentiment_scores.append(sentiment)
    
    # Check for conversation-ending keywords
    ending_keywords = ["bye", "goodbye", "exit", "quit", "end chat", "stop"]
    if any(keyword in message.lower() for keyword in ending_keywords):
        conv_state.stage = "ended"
        
        # Save candidate data
        if conv_state.is_complete():
            filename = save_candidate_data(conv_state, history)
            farewell = f"Thank you for your time! We have recorded your information and will review your profile. Our recruitment team will contact you within 3-5 business days regarding the next steps.\n\n✅ Your application has been saved (Reference: {conv_state.session_id})\n\nBest of luck with your application! 🎯"
        else:
            farewell = "Thank you for your time! Feel free to return anytime to complete your application. Have a great day! 👋"
        
        history.append((message, farewell))
        return farewell, history, conv_state.to_dict()
    
    # Auto-extract and validate information from user messages
    extracted_info = extract_information(message, conv_state)
    
    # Build context for the LLM
    context_info = f"\n\nCurrent candidate information collected:\n{json.dumps(conv_state.candidate_info, indent=2)}\n"
    context_info += f"Conversation stage: {conv_state.stage}\n"
    context_info += f"Technical questions asked: {conv_state.questions_asked}\n"
    context_info += f"User sentiment: {sentiment['sentiment']} (score: {sentiment['score']:.2f})\n"
    
    if sentiment['sentiment'] == 'negative' and sentiment['score'] > 0.6:
        context_info += "NOTE: User seems stressed/nervous. Be extra encouraging and supportive.\n"
    
    # Prepare messages for the API
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + context_info}
    ]
    
    # Add conversation history
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    try:
        # Call Grok API
        response = client.chat.completions.create(
            model="grok-beta",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract response
        bot_response = response.choices[0].message.content
        
        # Update conversation stage
        if conv_state.stage == "greeting" and len(history) > 0:
            conv_state.stage = "collecting_info"
        
        if conv_state.is_complete() and not conv_state.questions_asked:
            conv_state.stage = "technical_questions"
            conv_state.questions_asked = True
        
        # Update history
        history.append((message, bot_response))
        
        return bot_response, history, conv_state.to_dict()
        
    except Exception as e:
        error_msg = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        history.append((message, error_msg))
        return error_msg, history, conv_state.to_dict()


def extract_information(message: str, conv_state: ConversationState) -> dict:
    """
    Extract and validate information from user messages
    Returns extracted information
    """
    extracted = {}
    
    # Email detection
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, message)
    if email_match and not conv_state.candidate_info["email"]:
        email = email_match.group()
        if conv_state.validate_email(email):
            conv_state.candidate_info["email"] = email
            extracted["email"] = email
    
    # Phone detection
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, message)
    if phone_match and not conv_state.candidate_info["phone"]:
        phone = phone_match.group()
        if conv_state.validate_phone(phone):
            conv_state.candidate_info["phone"] = phone
            extracted["phone"] = phone
    
    # Years of experience detection
    experience_patterns = [
        r'(\d+)\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
        r'(?:experience|exp)(?:\s+of)?\s+(\d+)\s*(?:years?|yrs?)'
    ]
    for pattern in experience_patterns:
        exp_match = re.search(pattern, message.lower())
        if exp_match and not conv_state.candidate_info["experience"]:
            conv_state.candidate_info["experience"] = f"{exp_match.group(1)} years"
            extracted["experience"] = conv_state.candidate_info["experience"]
            break
    
    return extracted


def create_interface():
    """Create and configure the Gradio interface"""
    
    # Custom CSS for better appearance
    custom_css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
    }
    #chatbot {
        height: 500px;
    }
    """
    
    with gr.Blocks() as demo:
        gr.Markdown(
            """
            # 🎯 TalentScout Hiring Assistant
            ### Welcome to our AI-powered recruitment screening process
            
            I'm here to help you through the initial screening process. I'll ask you some questions about 
            your background and technical skills. Let's get started!
            """
        )
        
        # State to maintain conversation context
        state = gr.State({})
        
        # Chatbot interface
        chatbot = gr.Chatbot(
            value=[],
            elem_id="chatbot",
            height=500,
            show_label=False,
            avatar_images=(None, "🤖")
        )
        
        # User input
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your message here...",
                show_label=False,
                scale=4
            )
            submit = gr.Button("Send", scale=1, variant="primary")
        
        # Info section
        with gr.Accordion("ℹ️ About this chatbot", open=False):
            gr.Markdown(
                """
                This AI assistant will:
                - Collect your basic information
                - Learn about your technical skills
                - Ask relevant technical questions based on your expertise
                - Guide you through the screening process
                - Analyze your responses to provide better support
                
                **Privacy Note**: Your information is handled securely and saved locally for recruitment purposes only.
                
                **Features**:
                - 🎭 Sentiment analysis to provide empathetic responses
                - ✅ Automatic validation of email and phone numbers
                - 💾 Secure data storage for your application
                - 🌐 Multi-language support (coming soon)
                
                Type 'bye' or 'exit' when you're done to end the conversation.
                """
            )
        
        # Initial greeting when page loads
        def initialize_chat():
            greeting = ("", "Hello! 👋 I'm the TalentScout Hiring Assistant. I'm here to help with your initial screening for technology positions. I'll be asking you some questions about your background and technical skills.\n\nLet's start with something simple - could you please tell me your full name?")
            return [greeting], {}
        
        # Event handlers
        def user_submit(user_message, chat_history, current_state):
            return "", chat_with_grok(user_message, chat_history, current_state)
        
        # Handle submit button
        submit.click(
            user_submit,
            inputs=[msg, chatbot, state],
            outputs=[msg, chatbot, state]
        )
        
        # Handle enter key
        msg.submit(
            user_submit,
            inputs=[msg, chatbot, state],
            outputs=[msg, chatbot, state]
        )
        
        # Initialize chat on load
        demo.load(initialize_chat, outputs=[chatbot, state])
        
        gr.Markdown(
            """
            ---
            **TalentScout** | Powered by Grok AI | Built with Gradio
            """
        )
    
    return demo


if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    
    # Launch with Gradio 6.0 compatible parameters
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True to get a public URL
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            font-family: 'Arial', sans-serif;
        }
        #chatbot {
            height: 500px;
        }
        """
    )