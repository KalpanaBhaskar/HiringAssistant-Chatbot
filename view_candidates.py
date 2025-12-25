"""
Candidate Data Viewer
View and analyze stored candidate information
"""

import gradio as gr
import json
import os
from datetime import datetime
from typing import List, Dict

def load_candidate_data() -> List[Dict]:
    """Load all candidate data from the candidate_data directory"""
    candidates = []
    
    if not os.path.exists("candidate_data"):
        return candidates
    
    for filename in os.listdir("candidate_data"):
        if filename.endswith(".json"):
            filepath = os.path.join("candidate_data", filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    candidates.append(data)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    # Sort by timestamp (most recent first)
    candidates.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return candidates


def format_candidate_list(candidates: List[Dict]) -> str:
    """Format candidate list for display"""
    if not candidates:
        return "No candidate data found. Complete some interviews first!"
    
    output = f"# 📊 Candidate Database\n\n**Total Candidates**: {len(candidates)}\n\n"
    output += "---\n\n"
    
    for idx, candidate in enumerate(candidates, 1):
        info = candidate.get("candidate_info", {})
        output += f"## {idx}. {info.get('name', 'Unknown')}\n\n"
        output += f"**Session ID**: `{candidate.get('session_id', 'N/A')}`\n\n"
        output += f"**Date**: {candidate.get('timestamp', 'N/A')[:10]}\n\n"
        output += f"- **Email**: {info.get('email', 'N/A')}\n"
        output += f"- **Phone**: {info.get('phone', 'N/A')}\n"
        output += f"- **Experience**: {info.get('experience', 'N/A')}\n"
        output += f"- **Position**: {info.get('position', 'N/A')}\n"
        output += f"- **Location**: {info.get('location', 'N/A')}\n"
        output += f"- **Tech Stack**: {info.get('tech_stack', 'N/A')}\n"
        
        # Sentiment analysis
        sentiment_data = candidate.get("sentiment_analysis", {})
        avg_sentiment = sentiment_data.get("average_sentiment", 0)
        sentiment_emoji = "😊" if avg_sentiment > 0.6 else "😐" if avg_sentiment > 0.4 else "😟"
        output += f"- **Average Sentiment**: {avg_sentiment:.2f} {sentiment_emoji}\n"
        
        output += "\n---\n\n"
    
    return output


def view_candidate_details(session_id: str) -> str:
    """View detailed information for a specific candidate"""
    if not session_id:
        return "Please enter a Session ID"
    
    filepath = f"candidate_data/candidate_{session_id}.json"
    
    if not os.path.exists(filepath):
        return f"❌ No candidate found with Session ID: {session_id}"
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        info = data.get("candidate_info", {})
        output = f"# 📋 Detailed Candidate Report\n\n"
        output += f"**Session ID**: `{session_id}`\n\n"
        output += f"**Interview Date**: {data.get('timestamp', 'N/A')}\n\n"
        
        output += "## 👤 Personal Information\n\n"
        output += f"- **Name**: {info.get('name', 'N/A')}\n"
        output += f"- **Email**: {info.get('email', 'N/A')}\n"
        output += f"- **Phone**: {info.get('phone', 'N/A')}\n"
        output += f"- **Experience**: {info.get('experience', 'N/A')}\n"
        output += f"- **Desired Position**: {info.get('position', 'N/A')}\n"
        output += f"- **Location**: {info.get('location', 'N/A')}\n\n"
        
        output += "## 💻 Technical Skills\n\n"
        output += f"**Tech Stack**: {info.get('tech_stack', 'N/A')}\n\n"
        
        output += "## 📈 Sentiment Analysis\n\n"
        sentiment_data = data.get("sentiment_analysis", {})
        avg_sentiment = sentiment_data.get("average_sentiment", 0)
        output += f"**Average Sentiment Score**: {avg_sentiment:.2f}\n\n"
        
        if avg_sentiment > 0.6:
            output += "**Assessment**: Candidate showed positive engagement throughout the interview. 😊\n\n"
        elif avg_sentiment > 0.4:
            output += "**Assessment**: Candidate maintained neutral composure during the interview. 😐\n\n"
        else:
            output += "**Assessment**: Candidate may have been nervous or uncertain. Consider follow-up. 😟\n\n"
        
        output += "## 💬 Conversation History\n\n"
        history = data.get("conversation_history", [])
        for idx, exchange in enumerate(history, 1):
            output += f"**Turn {idx}**\n\n"
            output += f"👤 **Candidate**: {exchange.get('user', 'N/A')}\n\n"
            output += f"🤖 **Assistant**: {exchange.get('bot', 'N/A')}\n\n"
            output += "---\n\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error loading candidate data: {str(e)}"


def create_viewer_interface():
    """Create the data viewer interface"""
    
    with gr.Blocks() as demo:
        gr.Markdown(
            """
            # 📊 TalentScout - Candidate Data Viewer
            ### View and analyze collected candidate information
            """
        )
        
        with gr.Tabs():
            with gr.Tab("All Candidates"):
                refresh_btn = gr.Button("🔄 Refresh List", variant="primary")
                candidate_list = gr.Markdown()
                
                # Load data on page load and refresh
                demo.load(lambda: format_candidate_list(load_candidate_data()), outputs=candidate_list)
                refresh_btn.click(lambda: format_candidate_list(load_candidate_data()), outputs=candidate_list)
            
            with gr.Tab("Detailed View"):
                gr.Markdown("Enter a Session ID to view detailed candidate information")
                session_id_input = gr.Textbox(
                    label="Session ID",
                    placeholder="e.g., 20241221_143022",
                    info="You can find Session IDs in the 'All Candidates' tab"
                )
                view_btn = gr.Button("View Details", variant="primary")
                candidate_details = gr.Markdown()
                
                view_btn.click(
                    view_candidate_details,
                    inputs=session_id_input,
                    outputs=candidate_details
                )
            
            with gr.Tab("Statistics"):
                stats_output = gr.Markdown()
                
                def generate_statistics():
                    candidates = load_candidate_data()
                    if not candidates:
                        return "No data available yet."
                    
                    total = len(candidates)
                    positions = {}
                    tech_stacks = {}
                    avg_experience = []
                    
                    for candidate in candidates:
                        info = candidate.get("candidate_info", {})
                        
                        # Count positions
                        position = info.get("position", "Unknown")
                        positions[position] = positions.get(position, 0) + 1
                        
                        # Count tech stack mentions
                        tech = info.get("tech_stack", "")
                        if tech:
                            for skill in tech.split(','):
                                skill = skill.strip()
                                if skill:
                                    tech_stacks[skill] = tech_stacks.get(skill, 0) + 1
                        
                        # Experience
                        exp = info.get("experience", "")
                        if exp and "year" in exp:
                            try:
                                years = int(''.join(filter(str.isdigit, exp)))
                                avg_experience.append(years)
                            except:
                                pass
                    
                    output = f"# 📈 Recruitment Statistics\n\n"
                    output += f"**Total Candidates Screened**: {total}\n\n"
                    
                    if avg_experience:
                        output += f"**Average Experience**: {sum(avg_experience)/len(avg_experience):.1f} years\n\n"
                    
                    output += "## 🎯 Popular Positions\n\n"
                    for pos, count in sorted(positions.items(), key=lambda x: x[1], reverse=True):
                        output += f"- **{pos}**: {count} candidate(s)\n"
                    
                    output += "\n## 💻 Most Common Technologies\n\n"
                    top_tech = sorted(tech_stacks.items(), key=lambda x: x[1], reverse=True)[:10]
                    for tech, count in top_tech:
                        output += f"- **{tech}**: {count} mention(s)\n"
                    
                    return output
                
                refresh_stats = gr.Button("🔄 Refresh Statistics", variant="primary")
                refresh_stats.click(generate_statistics, outputs=stats_output)
                demo.load(generate_statistics, outputs=stats_output)
        
        gr.Markdown(
            """
            ---
            **TalentScout Data Viewer** | Secure & Privacy-Compliant
            """
        )
    
    return demo


if __name__ == "__main__":
    demo = create_viewer_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,  # Different port from main app
        share=False
    )