import streamlit as st
import time
import os
from dotenv import load_dotenv
from story_generator import StoryGenerator
from knowledge_base import KnowledgeBaseSeeder
import requests
from PIL import Image
from io import BytesIO
import base64
import json

# Load environment variables
load_dotenv()

# Initialize story generator and knowledge base seeder
story_generator = StoryGenerator()
knowledge_seeder = KnowledgeBaseSeeder()

# Set page config
st.set_page_config(
    page_title="Scene-by-Scene Story Generator",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .story-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 3px rgba(0,0,0,0.3);
    }
    .scene-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ffffff;
        margin-top: 2rem;
        text-shadow: 0 0 2px rgba(0,0,0,0.3);
    }
    .narrative {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #e6e6e6;
        text-align: justify;
        margin: 1rem 0;
    }
    .explanation {
        font-size: 1rem;
        background-color: rgba(52, 152, 219, 0.15);
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    .img-container {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
    }
    /* Improve overall text visibility */
    p, li, h1, h2, h3, h4, h5, h6, span, div {
        color: #e6e6e6 !important;
    }
    a {
        color: #3498db !important;
        font-weight: bold;
    }
    /* Style the expander */
    .streamlit-expanderHeader {
        color: #ffffff !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #3498db;'>📚 Scene-by-Scene Story Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #ffffff;'>Generate engaging, educational stories with visuals</p>", unsafe_allow_html=True)

# Cache for stories
if 'stories' not in st.session_state:
    st.session_state.stories = {}

# Input form
with st.form("story_form"):
    # Add curriculum selection
    curriculum_options = ["CBSE", "State Board", "ICSE", "IGCSE", "IB", "Common Core", "AP", "Other"]
    curriculum = st.selectbox("Curriculum", curriculum_options, index=0)
    
    # Add subject selection and topic inputs
    col1, col2 = st.columns(2)
    
    with col1:
        # Predefined subject options
        subject_options = [
            "Mathematics", "Physics", "Chemistry", "Biology", 
            "History", "Geography", "Literature", "Computer Science",
            "Environmental Science", "Economics", "Political Science", 
            "Psychology", "Sociology", "Art", "Music", "Physical Education",
            "Other"
        ]
        subject = st.selectbox("Subject", subject_options, index=0)
        
        # If "Other" is selected, show a text input
        if subject == "Other":
            subject = st.text_input("Enter subject", placeholder="e.g., Quantum Physics, Ancient Egypt")
    
    with col2:
        topic = st.text_input("Topic", placeholder="e.g., Trigonometry, Photosynthesis, World War II")
    
    # Add optional specific area input
    specific_area = st.text_input("Specific area (optional)", placeholder="e.g., Parts of liver, Pythagorean theorem proof, Nuclear fission")
    
    # Add detailed grade level selection
    grade_options = {
        "Grade 1": "grade_1",
        "Grade 2": "grade_2",
        "Grade 3": "grade_3",
        "Grade 4": "grade_4",
        "Grade 5": "grade_5",
        "Grade 6": "grade_6",
        "Grade 7": "grade_7",
        "Grade 8": "grade_8",
        "Grade 9": "grade_9",
        "Grade 10": "grade_10",
        "Grade 11": "grade_11",
        "Grade 12": "grade_12",
        "College Freshman": "college_freshman",
        "College Sophomore": "college_sophomore",
        "College Junior": "college_junior",
        "College Senior": "college_senior",
        "Graduate": "graduate"
    }
    
    # Create tabs for easier grade selection
    grade_tabs = st.tabs(["Elementary", "Middle School", "High School", "College"])
    
    with grade_tabs[0]:
        elementary_grades = ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"]
        elementary_grade = st.radio("Elementary School", elementary_grades, index=0)  # Default to Grade 1
    
    with grade_tabs[1]:
        middle_grades = ["Grade 6", "Grade 7", "Grade 8"]
        middle_grade = st.radio("Middle School", middle_grades, index=0)  # Default to Grade 6
    
    with grade_tabs[2]:
        high_grades = ["Grade 9", "Grade 10", "Grade 11", "Grade 12"]
        high_grade = st.radio("High School", high_grades, index=0)  # Default to Grade 9
    
    with grade_tabs[3]:
        college_grades = ["College Freshman", "College Sophomore", "College Junior", "College Senior", "Graduate"]
        college_grade = st.radio("College", college_grades, index=0)  # Default to College Freshman
    
    # Logic to determine which grade was selected
    if grade_tabs[0]._active:
        selected_grade_display = elementary_grade
    elif grade_tabs[1]._active:
        selected_grade_display = middle_grade
    elif grade_tabs[2]._active:
        selected_grade_display = high_grade
    else:
        selected_grade_display = college_grade
    
    # Convert display value to internal value
    grade = grade_options[selected_grade_display]
    
    st.markdown("<p style='font-size: 0.9rem; color: #e6e6e6;'>Generation may take a few minutes depending on the complexity of the subject and the number of scenes.</p>", unsafe_allow_html=True)
    
    submit_button = st.form_submit_button("Generate Story")

# Handle form submission
if submit_button and subject and topic:
    # We need to determine which grade was selected based on the active tab
    active_tab_index = 0
    for i, tab in enumerate(grade_tabs):
        if hasattr(tab, '_active') and tab._active:
            active_tab_index = i
            break
    
    # Set the selected grade based on active tab
    if active_tab_index == 0:
        selected_grade_display = elementary_grade
    elif active_tab_index == 1:
        selected_grade_display = middle_grade
    elif active_tab_index == 2:
        selected_grade_display = high_grade
    else:
        selected_grade_display = college_grade
    
    # Convert to internal grade value
    grade = grade_options[selected_grade_display]
    
    # Create a unique key for caching the story
    # Include the new fields in the key to ensure uniqueness
    story_key = f"{curriculum}_{subject}_{topic}_{specific_area}_{grade}" if specific_area else f"{curriculum}_{subject}_{topic}_{grade}"
    
    if story_key not in st.session_state.stories:
        with st.spinner("Seeding knowledge base with relevant information..."):
            # Include specific area if provided
            full_topic = f"{topic} - {specific_area}" if specific_area else topic
            knowledge_seeder.seed_knowledge_base(subject, full_topic, grade, curriculum)
        
        with st.spinner(f"Generating story about {subject} focused on {full_topic} for {selected_grade_display} following {curriculum} curriculum..."):
            # Generate the story
            story = story_generator.generate_complete_story(subject, full_topic, grade, curriculum)
            st.session_state.stories[story_key] = story
    
    # Display the story
    story = st.session_state.stories[story_key]
    
    # Display story title with specific area if provided
    title_text = f"{subject}: {topic}"
    if specific_area:
        title_text += f" - {specific_area}"
    
    st.markdown(f"<div class='story-title'>{title_text}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #e6e6e6;'>Tailored for {selected_grade_display} students following {curriculum} curriculum</p>", unsafe_allow_html=True)
    
    # Display outline
    with st.expander("Story Outline", expanded=False):
        st.markdown(story["outline"])
    
    # Display each scene
    for i, scene in enumerate(story["scenes"]):
        st.markdown(f"<div class='scene-title'>Scene {i+1}</div>", unsafe_allow_html=True)
        
        # Display narrative
        st.markdown(f"<div class='narrative'>{scene['narrative']}</div>", unsafe_allow_html=True)
        
        # Display explanation
        st.markdown(f"<div class='explanation'>{scene['explanation']}</div>", unsafe_allow_html=True)
        
        # Display image if available
        if scene.get("image_url"):
            st.markdown("<div class='img-container'>", unsafe_allow_html=True)
            # Replace deprecated use_column_width with use_container_width
            st.image(scene["image_url"], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Add separator between scenes
        if i < len(story["scenes"]) - 1:
            st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # Add download button
    story_json = json.dumps(story, indent=2)
    b64 = base64.b64encode(story_json.encode()).decode()
    
    # Create a more descriptive filename with the new fields
    filename = f"{curriculum}_{subject}_{topic}"
    if specific_area:
        filename += f"_{specific_area}"
    filename += f"_{grade}_story.json"
    
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">Download Story as JSON</a>'
    st.markdown(href, unsafe_allow_html=True)

elif submit_button:
    st.error("Please enter both a subject and a topic to generate a story.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #e6e6e6; font-size: 0.8rem;'>Powered by OpenAI, Qdrant Vector Database, and Streamlit</p>", unsafe_allow_html=True) 