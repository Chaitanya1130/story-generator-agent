from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import json
import uuid
from datetime import datetime
import uvicorn

# Import story generator components
from story_generator import StoryGenerator
from knowledge_base import KnowledgeBaseSeeder

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Story Generator API",
    description="API service for generating educational stories scene-by-scene",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize story generator and knowledge base seeder
story_generator = StoryGenerator()
knowledge_base_seeder = KnowledgeBaseSeeder()

# Pydantic models for request/response validation
class StoryRequest(BaseModel):
    subject: str = Field(..., description="The subject of the story (e.g., Mathematics, History)")
    topic: str = Field(..., description="The specific topic to focus on (e.g., Trigonometry, World War II)")
    grade: str = Field(default="grade_6", description="The grade level (e.g., grade_5, grade_10)")
    curriculum: str = Field(default="CBSE", description="The curriculum to follow (e.g., CBSE, Common Core)")
    specific_area: Optional[str] = Field(None, description="Optional specific area within the topic")

class StoryResponse(BaseModel):
    story_id: str
    status: str
    subject: str
    topic: str
    grade: str
    curriculum: str
    started_at: str
    outline: Optional[str] = None
    scenes: Optional[List[Dict[str, Any]]] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    progress: Optional[Dict[str, Any]] = None

# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid request format",
            "errors": exc.errors(),
            "example": {
                "subject": "Mathematics",
                "topic": "trigonometry",
                "grade": "grade_5",
                "curriculum": "CBSE",
                "specific_area": "cosine theta"
            }
        }
    )

@app.exception_handler(json.JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid JSON format",
            "error": str(exc),
            "example": {
                "subject": "Mathematics",
                "topic": "trigonometry",
                "grade": "grade_5",
                "curriculum": "CBSE",
                "specific_area": "cosine theta"
            }
        }
    )

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    
    try:
        # Validate required fields
        if not request.subject or not request.topic:
            raise HTTPException(status_code=400, detail="Subject and topic are required")
        
        # Create a unique ID for this story request
        story_id = str(uuid.uuid4())
        started_at = datetime.now().isoformat()
        
        # Create initial story data
        story_data = {
            "story_id": story_id,
            "status": "processing",
            "subject": request.subject,
            "topic": request.topic,
            "grade": request.grade,
            "curriculum": request.curriculum,
            "started_at": started_at,
            "progress": {
                "current_scene": 0,
                "total_scenes": 0,
                "current_stage": "initializing"
            }
        }
        
        # Update status to indicate knowledge base seeding
        story_data["status"] = "seeding_knowledge_base"
        story_data["progress"]["current_stage"] = "seeding_knowledge_base"
        
        # Seed the knowledge base with relevant information
        full_topic = f"{request.topic} - {request.specific_area}" if request.specific_area else request.topic
        knowledge_base_seeder.seed_knowledge_base(request.subject, full_topic, request.grade, request.curriculum)
        
        # Update status to indicate story generation
        story_data["status"] = "generating_story"
        story_data["progress"]["current_stage"] = "generating_story"
        
        # Generate the complete story
        complete_story = story_generator.generate_complete_story(request.subject, full_topic, request.grade, request.curriculum)
        
        # Update the story data with the complete story
        story_data.update({
            "status": "completed",
            "outline": complete_story["outline"],
            "scenes": complete_story["scenes"],
            "completed_at": datetime.now().isoformat(),
            "progress": {
                "current_scene": len(complete_story["scenes"]),
                "total_scenes": len(complete_story["scenes"]),
                "current_stage": "completed"
            }
        })
        
        return story_data
        
    except Exception as e:
        # Handle any errors during story generation
        return {
            "story_id": story_id,
            "status": "failed",
            "subject": request.subject,
            "topic": request.topic,
            "grade": request.grade,
            "curriculum": request.curriculum,
            "started_at": started_at,
            "error": str(e),
            "progress": {
                "current_stage": "failed"
            }
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 