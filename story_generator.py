import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import openai
from vector_store import VectorStore

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class StoryGenerator:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_model = "gpt-4o"
        
        # Detailed grade level vocabulary and complexity guidelines for each specific grade
        self.grade_guidelines = {
            # Pre-K and Kindergarten
            "pre_k": {
                "vocabulary": "very simple words (around 500-1000 word vocabulary), primarily concrete nouns and basic verbs",
                "sentence_structure": "very short, simple sentences (3-5 words), present tense, active voice",
                "narrative_style": "highly repetitive, concrete concepts only, strong visual support needed, focus on familiar objects and experiences",
                "explanation_depth": "extremely basic concepts with immediate relevance to child's experience, heavy use of visual analogies",
                "image_style": "bright, simple illustrations with minimal details, bold colors, exaggerated features, friendly characters"
            },
            "kindergarten": {
                "vocabulary": "simple, everyday words (around 2000-3000 word vocabulary), concrete nouns and basic action verbs",
                "sentence_structure": "short, simple sentences (5-7 words), mainly present tense, active voice",
                "narrative_style": "repetitive patterns, familiar settings, concrete concepts, character-focused stories with clear emotions",
                "explanation_depth": "very basic concepts connected to daily experiences, simple cause-and-effect relationships",
                "image_style": "colorful, engaging illustrations with some details, friendly characters, clear action sequences"
            },
            
            # Elementary School (Grades 1-5)
            "grade_1": {
                "vocabulary": "familiar, everyday words with gradual introduction of new terms (around 4000-5000 word vocabulary)",
                "sentence_structure": "simple sentences (5-8 words) with occasional compound sentences, primarily present tense",
                "narrative_style": "simple storylines with clear beginning-middle-end, familiar settings, concrete problems and solutions",
                "explanation_depth": "basic concepts with real-world examples from child's experience, simple step-by-step explanations",
                "image_style": "colorful illustrations with increased detail, clear expressions on characters, visual support for new concepts"
            },
            "grade_2": {
                "vocabulary": "expanding vocabulary (around 5000-6000 words) with new terms defined in context",
                "sentence_structure": "a mix of simple and compound sentences (7-10 words), introduction to past tense",
                "narrative_style": "sequential stories with minor conflicts and resolutions, introduction to character motivation",
                "explanation_depth": "concrete explanations with familiar analogies, beginning to connect related concepts",
                "image_style": "detailed illustrations that support text comprehension, visual representations of processes or sequences"
            },
            "grade_3": {
                "vocabulary": "broader vocabulary (6000-9000 words) with subject-specific terms defined clearly",
                "sentence_structure": "varied sentence types and lengths (8-12 words), introduction to paragraphing",
                "narrative_style": "more developed plots with multiple events, character development, introduction to different perspectives",
                "explanation_depth": "expanded explanations with cause and effect, beginning to connect to broader concepts",
                "image_style": "detailed illustrations with multiple elements, diagrams introduced to explain processes, realistic depictions"
            },
            "grade_4": {
                "vocabulary": "rich vocabulary (9000-11000 words) with academic terms, figurative language introduced",
                "sentence_structure": "complex and compound sentences (10-14 words), varied paragraph structures",
                "narrative_style": "multi-faceted plots, character development with internal motivations, introduction to themes",
                "explanation_depth": "detailed explanations with multiple examples, beginning to explore abstract concepts",
                "image_style": "detailed, accurate illustrations, introduction of charts and diagrams, visual metaphors"
            },
            "grade_5": {
                "vocabulary": "sophisticated vocabulary (11000-14000 words) with technical terms and figurative language",
                "sentence_structure": "varied sentence structures (12-15 words), well-developed paragraphs with supporting details",
                "narrative_style": "layered plots with subplots, nuanced character development, exploration of themes",
                "explanation_depth": "in-depth explanations connecting to prior knowledge, introduction to theoretical concepts",
                "image_style": "detailed illustrations with scientific accuracy, labeled diagrams, visual analogies for complex concepts"
            },
            
            # Middle School (Grades 6-8)
            "grade_6": {
                "vocabulary": "advanced vocabulary (14000-17000 words) with domain-specific terminology and abstract concepts",
                "sentence_structure": "complex sentence structures (12-18 words), variety of transition words, well-organized paragraphs",
                "narrative_style": "developed plots with complications, character growth and change, exploration of themes and messages",
                "explanation_depth": "comprehensive explanations with real-world applications, connections between concepts",
                "image_style": "detailed educational illustrations, more sophisticated diagrams, visual representations of complex relationships"
            },
            "grade_7": {
                "vocabulary": "extensive vocabulary (17000-19000 words) with specialized terminology and figurative expressions",
                "sentence_structure": "sophisticated sentence patterns (15-20 words), argument structures, varied paragraph organization",
                "narrative_style": "complex plots with conflict development, deeper character psychology, multiple themes",
                "explanation_depth": "detailed analysis with examples and counterexamples, exploration of underlying principles",
                "image_style": "scientifically accurate illustrations, detailed cross-sections, process diagrams, comparative visuals"
            },
            "grade_8": {
                "vocabulary": "sophisticated vocabulary (19000-21000 words) with abstract terminology and nuanced meanings",
                "sentence_structure": "varied, complex sentences (15-22 words), well-structured arguments, cohesive paragraphs",
                "narrative_style": "multi-layered plots, complex character motivations and relationships, thematic depth",
                "explanation_depth": "in-depth explanations with theoretical frameworks, connections to broader systems",
                "image_style": "detailed technical illustrations, complex diagrams with multiple elements, visual analysis of systems"
            },
            
            # High School (Grades 9-12)
            "grade_9": {
                "vocabulary": "advanced academic vocabulary (21000-23000 words) with specialized terminology",
                "sentence_structure": "sophisticated syntax (18-25 words), rhetorical devices, logical organization of complex ideas",
                "narrative_style": "exploration of complex issues, character development showing internal conflicts, thematic analysis",
                "explanation_depth": "detailed analysis with theoretical models, introduction to competing perspectives",
                "image_style": "professional-quality diagrams, models showing interactions between systems, analytical visuals"
            },
            "grade_10": {
                "vocabulary": "extensive academic vocabulary (23000-25000 words) with discipline-specific terminology",
                "sentence_structure": "complex syntactic structures (20-25 words), sophisticated transitions, logical development of arguments",
                "narrative_style": "multifaceted plots with subtle development, psychological depth in characters, thematic complexity",
                "explanation_depth": "sophisticated analysis with theoretical foundations, exploration of implications and applications",
                "image_style": "detailed scientific or technical visuals, complex systems diagrams, conceptual models with multiple layers"
            },
            "grade_11": {
                "vocabulary": "college-preparatory vocabulary (25000-27000 words) with specialized academic language",
                "sentence_structure": "varied, sophisticated syntax (20-30 words), nuanced argumentation, cohesive extended discourse",
                "narrative_style": "complex, multi-layered narratives, deep character analysis, sophisticated thematic development",
                "explanation_depth": "comprehensive analysis with theoretical frameworks, evaluation of different approaches",
                "image_style": "sophisticated visual representations of complex concepts, detailed analytical diagrams, visual models with annotations"
            },
            "grade_12": {
                "vocabulary": "college-level vocabulary (27000+ words) with field-specific terminology and academic discourse",
                "sentence_structure": "highly sophisticated syntax (20-35 words), complex argumentation, cohesive extended prose",
                "narrative_style": "nuanced narratives examining complex human experiences, sophisticated thematic exploration",
                "explanation_depth": "in-depth analysis with theoretical frameworks, critical evaluation of concepts and applications",
                "image_style": "college-level visual representations, complex models with detailed annotations, sophisticated visual analysis"
            },
            
            # College and Adult
            "college_freshman": {
                "vocabulary": "sophisticated academic vocabulary with field-specific terminology and theoretical concepts",
                "sentence_structure": "complex academic prose with varied rhetorical structures, logical argumentation",
                "narrative_style": "sophisticated exploration of complex ideas and human experiences, multiple layers of meaning",
                "explanation_depth": "rigorous analysis with theoretical frameworks, critical evaluation of concepts and methodologies",
                "image_style": "professional-grade visuals with precise detail, complex conceptual models, analytical diagrams with detailed annotations"
            },
            "college_sophomore": {
                "vocabulary": "advanced academic and discipline-specific vocabulary with theoretical terminology",
                "sentence_structure": "sophisticated academic discourse with complex logical structures and arguments",
                "narrative_style": "nuanced exploration of complex ideas with multiple perspectives and theoretical foundations",
                "explanation_depth": "detailed analysis with theoretical frameworks, critical evaluation and application of concepts",
                "image_style": "sophisticated visualizations with detailed technical elements, complex systems models, professional-level diagrams"
            },
            "college_junior": {
                "vocabulary": "specialized academic vocabulary with theoretical terminology specific to major fields",
                "sentence_structure": "advanced academic prose with discipline-specific conventions and argumentative structures",
                "narrative_style": "sophisticated exploration of complex ideas with integration of theoretical perspectives",
                "explanation_depth": "in-depth analysis with theoretical foundations, critical evaluation of competing frameworks",
                "image_style": "professional visualizations with field-specific conventions, complex analytical models, research-quality diagrams"
            },
            "college_senior": {
                "vocabulary": "specialized academic and professional vocabulary with advanced theoretical terminology",
                "sentence_structure": "sophisticated academic and professional discourse with field-specific conventions",
                "narrative_style": "complex exploration of ideas with integration of multiple theoretical perspectives",
                "explanation_depth": "comprehensive analysis with advanced theoretical frameworks, critical synthesis of concepts",
                "image_style": "professional-grade visualizations meeting field standards, complex analytical models, research-quality visuals"
            },
            "graduate": {
                "vocabulary": "highly specialized academic and professional vocabulary with advanced theoretical terminology",
                "sentence_structure": "sophisticated academic discourse with field-specific conventions and advanced argumentation",
                "narrative_style": "complex exploration of ideas with critical analysis of theoretical perspectives",
                "explanation_depth": "advanced analysis with sophisticated theoretical frameworks, original synthesis of concepts",
                "image_style": "publication-quality visualizations, complex theoretical models, research-level analytical diagrams"
            },
            "adult": {
                "vocabulary": "sophisticated vocabulary with domain-specific terminology appropriate for educated adults",
                "sentence_structure": "varied and complex structures appropriate for educated adult readers",
                "narrative_style": "mature themes with nuanced exploration of complex ideas",
                "explanation_depth": "comprehensive explanations with diverse perspectives and critical analysis",
                "image_style": "refined, detailed visualizations that capture complex relationships and subtle nuances"
            },
            
            # Default fallback to middle school level
            "default": {
                "vocabulary": "expanded vocabulary with new terms clearly defined within context",
                "sentence_structure": "mix of simple and compound sentences with some complexity",
                "narrative_style": "engaging stories with some nuance and character development",
                "explanation_depth": "moderate depth with connections to familiar concepts and practical examples",
                "image_style": "detailed illustrations that balance educational content with engaging visuals"
            }
        }
    
    def generate_story_outline(self, subject: str, topic: str, grade: str = "grade_6", curriculum: str = "General") -> str:
        """Generate a story outline based on the subject and topic appropriate for the grade level and curriculum"""
        # Get grade-specific guidelines without fallback to default
        guidelines = self.grade_guidelines.get(grade, {})
        
        # Use values directly if they exist, otherwise use sensible defaults
        vocabulary = guidelines.get("vocabulary", f"appropriate for {grade} level")
        sentence_structure = guidelines.get("sentence_structure", f"suitable for {grade} level")
        narrative_style = guidelines.get("narrative_style", f"engaging for {grade} level")
        explanation_depth = guidelines.get("explanation_depth", f"appropriate for {grade} level")
        
        prompt = f"""
        Create a detailed story outline about {subject} focusing on {topic}, tailored for {grade} level students following the {curriculum} curriculum.
        
        Please follow these grade-appropriate guidelines:
        - Vocabulary: {vocabulary}
        - Sentence structure: {sentence_structure}
        - Narrative style: {narrative_style}
        - Explanation depth: {explanation_depth}

        The outline should include:
        1. A clear introduction to the subject
        2. Key scenes or chapters that will explore different aspects of the topic
        3. A logical flow between scenes
        4. A conclusion that summarizes the key learnings
        
        Ensure the content aligns with {curriculum} curriculum standards for {grade} level.
        Format the outline with clear scene divisions.
        """
        
        response = openai.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a creative storyteller who creates educational and engaging stories tailored to specific grade levels."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    def generate_scene(self, subject: str, topic: str, scene_description: str, grade: str = "grade_6", previous_scenes: Optional[List[Dict[str, Any]]] = None, curriculum: str = "General") -> Dict[str, Any]:
        """Generate a single scene with narrative text and image prompt appropriate for the grade level and curriculum"""
        # Get grade-specific guidelines without fallback
        guidelines = self.grade_guidelines.get(grade, {})
        
        # Use values directly if they exist, otherwise use sensible defaults
        vocabulary = guidelines.get("vocabulary", f"appropriate for {grade} level")
        sentence_structure = guidelines.get("sentence_structure", f"suitable for {grade} level")
        narrative_style = guidelines.get("narrative_style", f"engaging for {grade} level")
        explanation_depth = guidelines.get("explanation_depth", f"appropriate for {grade} level")
        image_style = guidelines.get("image_style", f"visuals appropriate for {grade} level")
        
        # Get relevant information from vector store if available
        related_info = self.vector_store.search(f"{subject} {topic} {scene_description}", limit=3)
        related_info_text = "\n".join([item["text"] for item in related_info]) if related_info else ""
        
        # Context from previous scenes
        previous_context = ""
        if previous_scenes:
            previous_context = "Previous scenes:\n" + "\n".join([
                f"Scene {i+1}: {scene['narrative'][:200]}..." 
                for i, scene in enumerate(previous_scenes)
            ])
        
        prompt = f"""
        Create a detailed scene for a story about {subject} focusing on {topic}, tailored for {grade} level students following the {curriculum} curriculum.
        
        Please follow these grade-appropriate guidelines:
        - Vocabulary: {vocabulary}
        - Sentence structure: {sentence_structure}
        - Narrative style: {narrative_style}
        - Explanation depth: {explanation_depth}
        
        Scene description: {scene_description}
        
        {previous_context}
        
        Related background information:
        {related_info_text}
        
        For this scene, provide:
        1. A narrative text (300-500 words) that is engaging, educational, and explains concepts clearly at a {grade} level
        2. An explanatory section that elaborates on the key concepts or facts presented in this scene, appropriate for {grade} level students
        3. An image prompt that describes what should be visualized for this scene (detailed description for image generation) with a style appropriate for {grade} level: {image_style}
        
        For the image prompt, follow these guidelines:
        - Keep text in the image to an absolute minimum (3-5 words maximum)
        - Any text should be simple labels or short titles only
        - Don't request decorative or stylized text
        - Be specific about what content should be visualized rather than focusing on text elements
        
        Ensure the content aligns with {curriculum} curriculum standards for {grade} level.
        
        Format your response as:
        NARRATIVE: [narrative text]
        EXPLANATION: [explanatory text]
        IMAGE_PROMPT: [detailed image prompt]
        """
        
        response = openai.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": f"You are a creative storyteller who creates educational and engaging stories with vivid descriptions tailored for {grade} level students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        result = response.choices[0].message.content
        
        # Parse the response - Fixed parsing to handle multi-line sections
        narrative = ""
        explanation = ""
        image_prompt = ""
        
        # Split into sections by markers
        if "NARRATIVE:" in result and "EXPLANATION:" in result and "IMAGE_PROMPT:" in result:
            # Get positions of each marker
            narrative_pos = result.find("NARRATIVE:")
            explanation_pos = result.find("EXPLANATION:")
            image_prompt_pos = result.find("IMAGE_PROMPT:")
            
            # Extract sections based on their positions
            if narrative_pos < explanation_pos < image_prompt_pos:
                narrative = result[narrative_pos + len("NARRATIVE:"):explanation_pos].strip()
                explanation = result[explanation_pos + len("EXPLANATION:"):image_prompt_pos].strip()
                image_prompt = result[image_prompt_pos + len("IMAGE_PROMPT:"):].strip()
            elif narrative_pos < image_prompt_pos < explanation_pos:
                narrative = result[narrative_pos + len("NARRATIVE:"):image_prompt_pos].strip()
                image_prompt = result[image_prompt_pos + len("IMAGE_PROMPT:"):explanation_pos].strip()
                explanation = result[explanation_pos + len("EXPLANATION:"):].strip()
            elif explanation_pos < narrative_pos < image_prompt_pos:
                explanation = result[explanation_pos + len("EXPLANATION:"):narrative_pos].strip()
                narrative = result[narrative_pos + len("NARRATIVE:"):image_prompt_pos].strip()
                image_prompt = result[image_prompt_pos + len("IMAGE_PROMPT:"):].strip()
            # Add other possible orderings as needed
        else:
            # Fallback to the original line-by-line parsing method
            sections = result.split("\n")
            current_section = None
            
            for section in sections:
                if section.startswith("NARRATIVE:"):
                    current_section = "narrative"
                    narrative = section.replace("NARRATIVE:", "").strip()
                elif section.startswith("EXPLANATION:"):
                    current_section = "explanation"
                    explanation = section.replace("EXPLANATION:", "").strip()
                elif section.startswith("IMAGE_PROMPT:"):
                    current_section = "image_prompt"
                    image_prompt = section.replace("IMAGE_PROMPT:", "").strip()
                elif current_section == "narrative" and section:
                    narrative += "\n" + section
                elif current_section == "explanation" and section:
                    explanation += "\n" + section
                elif current_section == "image_prompt" and section:
                    image_prompt += "\n" + section
        
        # If image prompt is still empty, generate a default one
        if not image_prompt:
            image_prompt = f"A {image_style} depicting {subject} focusing on {topic}, specifically {scene_description[:100]}"
        
        return {
            "narrative": narrative,
            "explanation": explanation,
            "image_prompt": image_prompt
        }
    
    def generate_image(self, prompt: str) -> str:
        """Generate an image based on the prompt using OpenAI's DALL-E"""
        try:
            # Add a safety check to ensure prompt is not empty
            if not prompt or len(prompt.strip()) == 0:
                default_prompt = "An educational illustration with a blank canvas, representing a missing image prompt."
                print(f"Warning: Empty image prompt detected. Using default prompt instead.")
                prompt = default_prompt
            
            # Add specific instructions for text clarity
            text_clarity_instructions = """
            IMPORTANT INSTRUCTIONS FOR TEXT RENDERING:
            - Any text in the image must be crystal clear, large, and easily readable
            - Use a clear, bold font with high contrast against the background
            - Avoid stylized or decorative text that might be difficult to read
            - Maintain adequate spacing between letters and words
            - Keep text simple and minimal - only include essential labels or titles
            - Position text in uncluttered areas of the image
            - Text should be perfectly horizontal (not curved, angled, or distorted)
            """
            
            enhanced_prompt = f"{text_clarity_instructions}\n\n{prompt}"
            
            response = openai.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def generate_complete_story(self, subject: str, topic: str, grade: str = "grade_6", curriculum: str = "General") -> Dict[str, Any]:
        """Generate a complete story with multiple scenes, each with narrative, explanation, and image appropriate for the grade level and curriculum"""
        # Generate the story outline
        outline = self.generate_story_outline(subject, topic, grade, curriculum)
        
        # Parse outline to extract scenes
        scenes_descriptions = []
        current_scene = ""
        
        for line in outline.split("\n"):
            line = line.strip()
            if line.startswith("Scene") or line.startswith("Chapter") or line.startswith("Part"):
                if current_scene:
                    scenes_descriptions.append(current_scene)
                current_scene = line
            elif current_scene and line:
                current_scene += "\n" + line
        
        if current_scene:
            scenes_descriptions.append(current_scene)
        
        # If no clear scene divisions, create some
        if not scenes_descriptions:
            # Split the outline into approximately 3-5 scenes
            lines = outline.split("\n")
            chunk_size = max(1, len(lines) // 4)
            scenes_descriptions = [
                "\n".join(lines[i:i+chunk_size])
                for i in range(0, len(lines), chunk_size)
            ]
        
        # Generate each scene
        scenes = []
        for i, scene_desc in enumerate(scenes_descriptions):
            print(f"Generating scene {i+1}/{len(scenes_descriptions)}...")
            scene = self.generate_scene(subject, topic, scene_desc, grade, scenes, curriculum)
            
            # Debug print to check the image prompt
            print(f"Image prompt for scene {i+1}: {scene['image_prompt'][:100]}...")
            
            # Generate image for the scene
            image_url = self.generate_image(scene["image_prompt"])
            scene["image_url"] = image_url
            
            scenes.append(scene)
        
        return {
            "subject": subject,
            "topic": topic,
            "grade": grade,
            "curriculum": curriculum,
            "outline": outline,
            "scenes": scenes
        } 