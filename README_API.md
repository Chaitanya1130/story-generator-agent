# Story Generator API

## Overview

The Story Generator API is a RESTful service that generates educational, scene-by-scene stories with explanations and visuals based on subject, topic, and grade level.

This API serves as an orchestrator for the story generation process, allowing clients to request stories asynchronously. The story generation process includes:

1. Seeding a knowledge base with relevant information for the subject and topic
2. Generating a story outline
3. Creating detailed scenes with narrative text, explanations, and image prompts
4. Returning the complete story to the client

## Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (see requirements.txt)
- Running instance of Qdrant vector database (or use in-memory instance)
- OpenAI API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables (create a `.env` file):
   ```
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url  # Optional, uses in-memory DB if not provided
   QDRANT_API_KEY=your_qdrant_api_key  # Optional
   ```

### Running the API

Start the API server:

```bash
python api.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the API is running, access the interactive documentation at http://localhost:8000/docs for detailed information on all endpoints.

### Key Endpoints

#### Generate a Story

```
POST /generate-story
```

Request body:
```json
{
  "subject": "Mathematics",
  "topic": "Pythagorean Theorem",
  "specific_area": "Real-world applications",
  "grade": "grade_8",
  "curriculum": "Common Core"
}
```

Response:
```json
{
  "story_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "subject": "Mathematics",
  "topic": "Pythagorean Theorem",
  "grade": "grade_8",
  "curriculum": "Common Core",
  "started_at": "2023-06-15T12:34:56.789Z"
}
```

#### Check Story Status

```
GET /story/{story_id}
```

Response (in-progress):
```json
{
  "story_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "generating_story",
  "subject": "Mathematics",
  "topic": "Pythagorean Theorem",
  "grade": "grade_8",
  "curriculum": "Common Core",
  "started_at": "2023-06-15T12:34:56.789Z"
}
```

Response (completed):
```json
{
  "story_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "subject": "Mathematics",
  "topic": "Pythagorean Theorem",
  "grade": "grade_8",
  "curriculum": "Common Core",
  "started_at": "2023-06-15T12:34:56.789Z",
  "completed_at": "2023-06-15T12:40:23.456Z",
  "outline": "...",
  "scenes": [
    {
      "narrative": "...",
      "explanation": "...",
      "image_url": "https://..."
    },
    ...
  ]
}
```

#### List All Stories

```
GET /stories
```

Returns an array of all story objects.

## Using the API Client

A command-line client is provided to interact with the API:

```bash
python api_client.py --subject "Biology" --topic "Photosynthesis" --grade "grade_7"
```

Optional parameters:
- `--curriculum`: Specify the curriculum to follow (default: "General")
- `--specific-area`: Narrow down the topic
- `--output`: Specify an output file name
- `--poll-interval`: Set the polling interval in seconds (default: 10)

Example:
```bash
python api_client.py --subject "Physics" --topic "Momentum" --grade "grade_10" --specific-area "Conservation of Momentum" --curriculum "CBSE" --output "physics_momentum.json"
```

## Integration Examples

### Web Frontend

Use the API in a web application:

```javascript
// Request a story generation
async function generateStory() {
  const response = await fetch('http://localhost:8000/generate-story', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      subject: 'Chemistry',
      topic: 'Periodic Table',
      grade: 'grade_9'
    })
  });
  
  const data = await response.json();
  const storyId = data.story_id;
  
  // Poll for completion
  checkStatus(storyId);
}

// Check story status
async function checkStatus(storyId) {
  const response = await fetch(`http://localhost:8000/story/${storyId}`);
  const story = await response.json();
  
  if (story.status === 'completed') {
    displayStory(story);
  } else if (story.status === 'failed') {
    displayError(story.error);
  } else {
    // Still processing, check again after delay
    setTimeout(() => checkStatus(storyId), 5000);
  }
}
```

## Performance Considerations

- Story generation is a resource-intensive process and may take several minutes to complete
- The API uses background tasks to handle story generation asynchronously
- For production use, consider implementing:
  - Persistent storage for generated stories
  - User authentication and rate limiting
  - Caching for frequently requested stories
  - Load balancing for horizontal scaling 