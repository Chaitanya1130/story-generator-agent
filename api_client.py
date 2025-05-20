#!/usr/bin/env python3
import requests
import json
import time
import argparse
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def generate_story(subject: str, topic: str, grade: str = "grade_6", curriculum: str = "General", specific_area: str = None) -> Dict[str, Any]:
    """
    Request a story generation from the API
    """
    # Create request payload
    payload = {
        "subject": subject,
        "topic": topic,
        "grade": grade,
        "curriculum": curriculum
    }
    
    # Add specific_area if provided
    if specific_area:
        payload["specific_area"] = specific_area
        
    # Send POST request to generate story
    response = requests.post(f"{BASE_URL}/generate-story", json=payload)
    response.raise_for_status()  # Raise exception for HTTP errors
    
    # Return the initial story data including the ID
    return response.json()

def check_story_status(story_id: str) -> Dict[str, Any]:
    """
    Check the status of a story generation request
    """
    response = requests.get(f"{BASE_URL}/story/{story_id}")
    response.raise_for_status()
    return response.json()

def wait_for_story_completion(story_id: str, polling_interval: int = 10, max_attempts: int = 30) -> Dict[str, Any]:
    """
    Poll until story generation completes or fails
    """
    attempts = 0
    while attempts < max_attempts:
        story_data = check_story_status(story_id)
        status = story_data.get("status")
        
        if status == "completed":
            print("✅ Story generation completed!")
            return story_data
        elif status == "failed":
            error_msg = story_data.get("error", "Unknown error")
            raise Exception(f"Story generation failed: {error_msg}")
        
        # Still processing - provide status update
        current_stage = status.replace("_", " ").title()
        print(f"🔄 Current status: {current_stage}... (attempt {attempts+1}/{max_attempts})")
        
        attempts += 1
        time.sleep(polling_interval)
    
    raise Exception("Timed out waiting for story completion")

def save_story_to_file(story_data: Dict[str, Any], output_file: str = None) -> str:
    """
    Save the generated story to a file
    """
    # Generate filename if not provided
    if not output_file:
        subject = story_data.get("subject", "subject")
        topic = story_data.get("topic", "topic")
        grade = story_data.get("grade", "grade")
        story_id = story_data.get("story_id", "unknown")
        output_file = f"{subject}_{topic}_{grade}_{story_id[:8]}.json"
    
    # Save to file
    with open(output_file, "w") as f:
        json.dump(story_data, f, indent=2)
    
    return output_file

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Client for Educational Story Generator API")
    parser.add_argument("--subject", "-s", required=True, help="Subject for the story (e.g., Mathematics)")
    parser.add_argument("--topic", "-t", required=True, help="Topic for the story (e.g., Fractions)")
    parser.add_argument("--grade", "-g", default="grade_6", help="Grade level (e.g., grade_6)")
    parser.add_argument("--curriculum", "-c", default="General", help="Curriculum to follow (e.g., CBSE)")
    parser.add_argument("--specific-area", "-a", help="Specific area within the topic (optional)")
    parser.add_argument("--output", "-o", help="Output file name (optional)")
    parser.add_argument("--poll-interval", "-i", type=int, default=10, help="Polling interval in seconds")
    args = parser.parse_args()
    
    try:
        # Step 1: Request story generation
        print(f"🚀 Requesting story generation for {args.subject} - {args.topic} (Grade: {args.grade})")
        initial_data = generate_story(
            args.subject, 
            args.topic,
            args.grade,
            args.curriculum,
            args.specific_area
        )
        story_id = initial_data["story_id"]
        print(f"📝 Story generation started with ID: {story_id}")
        
        # Step 2: Wait for completion
        print("⏳ Waiting for story generation to complete...")
        complete_story = wait_for_story_completion(
            story_id,
            polling_interval=args.poll_interval
        )
        
        # Step 3: Save to file
        output_file = save_story_to_file(complete_story, args.output)
        print(f"💾 Story saved to: {output_file}")
        
        # Print summary
        print("\n📖 Story Summary:")
        print(f"Title: {args.subject}: {args.topic}")
        if args.specific_area:
            print(f"Specific Area: {args.specific_area}")
        print(f"Number of scenes: {len(complete_story.get('scenes', []))}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 