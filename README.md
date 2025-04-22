# Scene-by-Scene Story Generator

A RAG-based AI system that generates educational stories with visual content scene by scene.

## Architecture

This application uses a Retrieval-Augmented Generation (RAG) architecture to create engaging, informative stories with images. The system:

1. Seeds a Qdrant vector database with knowledge about the requested subject and topic
2. Generates a story outline with logical scene progression
3. For each scene, retrieves relevant information from the vector database
4. Creates narrative text, explanatory content, and image prompts
5. Generates images using DALL-E 3
6. Presents the complete story in a beautiful Streamlit UI

## Requirements

- Python 3.8+
- OpenAI API Key
- Qdrant (can use local in-memory database or cloud instance)

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys (based on `.env.example`)

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Enter a subject (e.g., "Space Exploration") and a topic (e.g., "Mars Colonization")
3. Click "Generate Story" and wait for the system to create your scene-by-scene story
4. View the resulting story with narrative text, explanations, and images for each scene
5. Download the complete story as JSON if needed

## Configuration

- For cloud-based Qdrant, set the `QDRANT_URL` and `QDRANT_API_KEY` in your `.env` file
- The system uses GPT-4o and DALL-E 3 by default for optimal results
- You can modify the number of knowledge chunks by changing the `num_chunks` parameter in `knowledge_base.py`

## Components

- `app.py`: Main Streamlit application
- `vector_store.py`: Qdrant vector database integration
- `knowledge_base.py`: Seeds the vector database with relevant information
- `story_generator.py`: Core story generation logic

## Architecture Diagram

```
┌─────────────────┐      ┌───────────────────┐      ┌────────────────┐
│                 │      │                   │      │                │
│   User Input    │──────▶  Knowledge Base   │──────▶  Vector Store  │
│ (Subject/Topic) │      │      Seeder       │      │   (Qdrant)     │
│                 │      │                   │      │                │
└─────────────────┘      └───────────────────┘      └────────────────┘
                                                            │
                                                            ▼
┌─────────────────┐      ┌───────────────────┐      ┌────────────────┐
│                 │      │                   │      │                │
│   Streamlit     │◀─────│  Story Generator  │◀─────│  RAG Retrieval │
│     UI          │      │  (GPT-4o/DALL-E)  │      │                │
│                 │      │                   │      │                │
└─────────────────┘      └───────────────────┘      └────────────────┘
``` 