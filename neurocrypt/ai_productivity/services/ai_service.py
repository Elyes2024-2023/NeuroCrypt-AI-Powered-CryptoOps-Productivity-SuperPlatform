from typing import List, Optional
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        openai.api_key = self.openai_api_key
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def generate_todo_suggestions(self, todo_title: str, todo_description: Optional[str] = None) -> List[str]:
        """Generate AI-powered suggestions for a todo item."""
        prompt = PromptTemplate(
            input_variables=["title", "description"],
            template="""Given this todo item:
            Title: {title}
            Description: {description}
            
            Please provide 3 smart suggestions to enhance this todo item, considering:
            1. Priority and urgency
            2. Potential subtasks
            3. Related resources or contacts
            
            Format the response as a list of suggestions."""
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a productivity assistant."},
                    {"role": "user", "content": prompt.format(
                        title=todo_title,
                        description=todo_description or "No description provided"
                    )}
                ]
            )
            
            content = response.choices[0].message.content
            return [suggestion.strip() for suggestion in content.split("\n") if suggestion.strip()]
        except Exception as e:
            print(f"Error generating todo suggestions: {str(e)}")
            return ["Unable to generate suggestions at this time."]

    async def analyze_journal_entry(self, content: str) -> dict:
        """Analyze a journal entry for insights and mood."""
        prompt = PromptTemplate(
            input_variables=["content"],
            template="""Analyze this journal entry and provide insights:
            {content}
            
            Please provide:
            1. Overall mood
            2. Key themes
            3. Action items or follow-ups
            4. Emotional patterns
            
            Format the response as a JSON object."""
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an empathetic journal analyzer."},
                    {"role": "user", "content": prompt.format(content=content)}
                ]
            )
            
            content = response.choices[0].message.content
            # In production, use proper JSON parsing
            import json
            try:
                return json.loads(content)
            except:
                return {
                    "mood": "neutral",
                    "themes": ["Unable to analyze"],
                    "action_items": [],
                    "emotional_patterns": []
                }
        except Exception as e:
            print(f"Error analyzing journal entry: {str(e)}")
            return {
                "mood": "neutral",
                "themes": ["Error in analysis"],
                "action_items": [],
                "emotional_patterns": []
            }

    async def suggest_goal_improvements(self, goal_title: str, goal_description: Optional[str] = None) -> dict:
        """Generate AI-powered suggestions for improving a goal."""
        prompt = PromptTemplate(
            input_variables=["title", "description"],
            template="""Analyze this goal and provide improvement suggestions:
            Title: {title}
            Description: {description}
            
            Please provide:
            1. SMART criteria analysis
            2. Potential milestones
            3. Resource recommendations
            4. Risk factors
            
            Format the response as a JSON object."""
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a goal-setting expert."},
                    {"role": "user", "content": prompt.format(
                        title=goal_title,
                        description=goal_description or "No description provided"
                    )}
                ]
            )
            
            content = response.choices[0].message.content
            # In production, use proper JSON parsing
            import json
            try:
                return json.loads(content)
            except:
                return {
                    "smart_criteria": "Unable to analyze",
                    "milestones": [],
                    "resources": [],
                    "risks": []
                }
        except Exception as e:
            print(f"Error suggesting goal improvements: {str(e)}")
            return {
                "smart_criteria": "Error in analysis",
                "milestones": [],
                "resources": [],
                "risks": []
            }

    async def get_productivity_insights(self, todos: List[dict], journal_entries: List[dict], goals: List[dict]) -> dict:
        """Generate comprehensive productivity insights based on user data."""
        prompt = PromptTemplate(
            input_variables=["todos", "journal_entries", "goals"],
            template="""Analyze this user's productivity data and provide insights:
            
            Todos: {todos}
            Journal Entries: {journal_entries}
            Goals: {goals}
            
            Please provide:
            1. Productivity patterns
            2. Areas for improvement
            3. Achievement highlights
            4. Recommended next steps
            
            Format the response as a JSON object."""
        )

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a productivity analyst."},
                    {"role": "user", "content": prompt.format(
                        todos=str(todos),
                        journal_entries=str(journal_entries),
                        goals=str(goals)
                    )}
                ]
            )
            
            content = response.choices[0].message.content
            # In production, use proper JSON parsing
            import json
            try:
                return json.loads(content)
            except:
                return {
                    "patterns": ["Unable to analyze"],
                    "improvements": [],
                    "highlights": [],
                    "next_steps": []
                }
        except Exception as e:
            print(f"Error getting productivity insights: {str(e)}")
            return {
                "patterns": ["Error in analysis"],
                "improvements": [],
                "highlights": [],
                "next_steps": []
            } 