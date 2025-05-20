# Educational Story Generator

An AI-powered educational tool that automatically generates engaging, curriculum-aligned stories to explain educational concepts across various subjects and grade levels.

## Features

- Generate educational stories with subject matter explanations embedded naturally in the narrative
- Customize stories by subject, topic, specific area, grade level, and curriculum
- Stories include scene-by-scene breakdowns with narrative text and educational explanations
- Optional image generation for story scenes 
- Multiple interfaces:
  - Web application built with Streamlit
  - REST API built with FastAPI
  - Command-line client for API interaction

## Architecture

The system consists of several components:

1. **Knowledge Base**: Uses Qdrant vector database and sentence transformers to store and retrieve relevant educational information
2. **Story Generator**: Leverages OpenAI's GPT models to create educational stories based on retrieved knowledge
3. **Web Application**: A Streamlit interface for interactive story generation
4. **API**: A FastAPI service that provides asynchronous story generation capabilities
5. **Client**: A command-line tool for interacting with the API

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- (Optional) Qdrant vector database instance (falls back to in-memory if not provided)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/educational-story-generator.git
   cd educational-story-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url  # Optional
   QDRANT_API_KEY=your_qdrant_api_key  # Optional
   ```

## Usage

### Web Application

Run the Streamlit web application:

```bash
   streamlit run main.py
   ```

The application will be available at http://localhost:8501

### API

Start the FastAPI server:

```bash
python api.py
```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/docs

### Command-line Client

Use the client to generate stories via the API:

```bash
python api_client.py --subject "History" --topic "American Revolution" --grade "grade_5"
```

See [API Documentation](README_API.md) for more details.

## Example Workflow

### Web Application

1. Open the Streamlit app
2. Select subject, topic, and grade level
3. Click "Generate Story"
4. View the generated story with scenes and explanations
5. (Optional) Download the story in JSON format

### API

1. Send a POST request to `/generate-story` with subject, topic, and grade
2. Receive a story ID
3. Poll the `/story/{story_id}` endpoint until the story is complete
4. Retrieve the full story with all scenes and explanations

## Project Structure

```
educational-story-generator/
├── main.py                 # Streamlit web application
├── api.py                  # FastAPI service
├── api_client.py           # Command-line client for API
├── story_generator.py      # Core story generation logic
├── knowledge_base.py       # Knowledge base seeding and retrieval
├── vector_store.py         # Vector database interface
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (create this)
├── README.md               # This file
└── README_API.md           # API documentation
```

## Customization

### Adding New Subjects

The system is designed to work with any educational subject. Simply provide a subject and topic when generating a story.

### Adjusting Generation Parameters

Advanced parameters can be modified in the `story_generator.py` file:
- Model selection
- Temperature settings
- Number of scenes
- Scene complexity

## Roadmap

- [ ] Add support for multiple languages
- [ ] Implement user accounts and story saving
- [ ] Add text-to-speech for story narration
- [ ] Expand image generation capabilities
- [ ] Create exportable lesson plans around generated stories

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT models
- Qdrant for the vector database
- Streamlit and FastAPI for the application frameworks 