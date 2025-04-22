import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import openai
from vector_store import VectorStore

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class KnowledgeBaseSeeder:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm_model = "gpt-4o"
        
        # Detailed grade level guidelines for knowledge complexity for each individual grade
        self.grade_guidelines = {
            # Pre-K and Kindergarten
            "pre_k": {
                "complexity": "extremely simple concepts directly related to immediate sensory experiences",
                "vocabulary": "basic words (500-1000 word vocabulary) using concrete nouns and simple action verbs",
                "chunk_length": "very short paragraphs (30-50 words)",
                "examples": "examples using familiar objects, animals, and everyday experiences"
            },
            "kindergarten": {
                "complexity": "simple, concrete concepts with clear cause-effect relationships",
                "vocabulary": "basic vocabulary (2000-3000 words) with new words immediately explained",
                "chunk_length": "short paragraphs (40-70 words)",
                "examples": "examples from daily life and familiar experiences"
            },
            
            # Elementary School (Grades 1-5)
            "grade_1": {
                "complexity": "basic concepts with simple explanations and immediate relevance",
                "vocabulary": "common words (4000-5000 vocabulary) with new terms defined simply",
                "chunk_length": "short paragraphs (50-80 words)",
                "examples": "examples relating to children's immediate world and experiences"
            },
            "grade_2": {
                "complexity": "straightforward concepts with clear connections to known ideas",
                "vocabulary": "everyday vocabulary (5000-6000 words) with new terms defined in context",
                "chunk_length": "short paragraphs (60-90 words)",
                "examples": "concrete examples from experiences children might have had"
            },
            "grade_3": {
                "complexity": "developing concepts with some connections between ideas",
                "vocabulary": "expanding vocabulary (6000-9000 words) with subject-specific terms defined",
                "chunk_length": "developing paragraphs (70-100 words)",
                "examples": "familiar examples with some new contexts introduced"
            },
            "grade_4": {
                "complexity": "interconnected concepts with some abstract relationships",
                "vocabulary": "growing vocabulary (9000-11000 words) with academic terms introduced",
                "chunk_length": "standard paragraphs (80-120 words)",
                "examples": "examples that connect to broader experiences and some beyond direct experience"
            },
            "grade_5": {
                "complexity": "moderately complex concepts with connections to broader principles",
                "vocabulary": "richer vocabulary (11000-14000 words) with content-specific terminology",
                "chunk_length": "developed paragraphs (100-150 words)",
                "examples": "examples that include phenomena beyond immediate experience"
            },
            
            # Middle School (Grades 6-8)
            "grade_6": {
                "complexity": "concepts with multiple factors and relationships between systems",
                "vocabulary": "expanded vocabulary (14000-17000 words) with technical terms explained",
                "chunk_length": "full paragraphs (120-170 words)",
                "examples": "real-world examples that connect to broader systems and processes"
            },
            "grade_7": {
                "complexity": "multi-faceted concepts with cause-effect relationships and system interactions",
                "vocabulary": "advanced vocabulary (17000-19000 words) with discipline-specific terminology",
                "chunk_length": "developed paragraphs (150-180 words)",
                "examples": "examples showing relationships between different systems or concepts"
            },
            "grade_8": {
                "complexity": "complex concepts with interconnections between systems and abstract principles",
                "vocabulary": "sophisticated vocabulary (19000-21000 words) with specialized terminology",
                "chunk_length": "substantial paragraphs (150-200 words)",
                "examples": "examples demonstrating underlying principles and theoretical applications"
            },
            
            # High School (Grades 9-12)
            "grade_9": {
                "complexity": "complex concepts with theoretical frameworks and system analysis",
                "vocabulary": "academic vocabulary (21000-23000 words) with specialized terminology",
                "chunk_length": "detailed paragraphs (170-220 words)",
                "examples": "examples illustrating theoretical concepts and practical applications"
            },
            "grade_10": {
                "complexity": "sophisticated concepts with analytical frameworks and critical perspectives",
                "vocabulary": "advanced academic vocabulary (23000-25000 words) with field-specific terminology",
                "chunk_length": "comprehensive paragraphs (180-230 words)",
                "examples": "examples demonstrating analytical principles and theoretical models"
            },
            "grade_11": {
                "complexity": "advanced concepts with theoretical foundations and critical analysis",
                "vocabulary": "college-preparatory vocabulary (25000-27000 words) with specialized academic language",
                "chunk_length": "detailed analytical paragraphs (200-250 words)",
                "examples": "examples with theoretical applications and underlying principles"
            },
            "grade_12": {
                "complexity": "college-level concepts with theoretical depth and critical evaluation",
                "vocabulary": "college-level vocabulary (27000+ words) with discipline-specific terminology",
                "chunk_length": "comprehensive academic paragraphs (200-250 words)",
                "examples": "sophisticated examples showing theoretical frameworks and applications"
            },
            
            # College and Adult
            "college_freshman": {
                "complexity": "advanced concepts with theoretical frameworks and methodological approaches",
                "vocabulary": "college-level academic vocabulary with field-specific terminology",
                "chunk_length": "substantive academic paragraphs (200-250 words)",
                "examples": "examples demonstrating theoretical principles and methodological applications"
            },
            "college_sophomore": {
                "complexity": "specialized concepts with theoretical depth and analytical frameworks",
                "vocabulary": "advanced academic vocabulary with discipline-specific terminology",
                "chunk_length": "detailed academic paragraphs (200-250 words)",
                "examples": "examples illustrating theoretical models and analytical approaches"
            },
            "college_junior": {
                "complexity": "specialized concepts with theoretical sophistication and analytical depth",
                "vocabulary": "specialized academic vocabulary with field-specific theoretical terminology",
                "chunk_length": "comprehensive academic paragraphs (200-300 words)",
                "examples": "sophisticated examples demonstrating theoretical principles and applications"
            },
            "college_senior": {
                "complexity": "advanced specialized concepts with theoretical integration and critical analysis",
                "vocabulary": "sophisticated academic vocabulary with specialized terminology",
                "chunk_length": "substantive academic paragraphs (200-300 words)",
                "examples": "examples showing integration of theoretical frameworks and practical applications"
            },
            "graduate": {
                "complexity": "highly specialized concepts with theoretical sophistication and original analysis",
                "vocabulary": "advanced academic vocabulary with specialized theoretical terminology",
                "chunk_length": "comprehensive academic paragraphs (250-300 words)",
                "examples": "sophisticated examples demonstrating theoretical innovation and critical analysis"
            },
            "adult": {
                "complexity": "sophisticated concepts with multiple perspectives and critical analysis",
                "vocabulary": "advanced vocabulary with specialized terminology for educated adults",
                "chunk_length": "substantial informative paragraphs (200-250 words)",
                "examples": "examples illustrating complex relationships and practical applications"
            },
            
            # Default fallback to middle school level
            "default": {
                "complexity": "foundational concepts with some detail and real-world connections",
                "vocabulary": "moderate vocabulary with technical terms defined in context",
                "chunk_length": "medium paragraphs (100-150 words)",
                "examples": "examples relevant to students' experiences and broader world understanding"
            }
        }
    
    def get_knowledge_chunks(self, subject: str, topic: str, grade: str = "grade_6", curriculum: str = "General", num_chunks: int = 10) -> List[str]:
        """Generate knowledge chunks about the subject and topic appropriate for the grade level and curriculum"""
        # Get grade-specific guidelines - use the specified grade level or empty dict if not found
        guidelines = self.grade_guidelines.get(grade, {})
        
        # Use the grade values directly if they exist, otherwise use sensible defaults
        complexity = guidelines.get("complexity", f"appropriate for {grade} level")
        vocabulary = guidelines.get("vocabulary", f"suitable for {grade} level")
        chunk_length = guidelines.get("chunk_length", "appropriate length paragraphs")
        examples = guidelines.get("examples", f"examples suitable for {grade} level")
        
        prompt = f"""
        Generate {num_chunks} detailed knowledge chunks about {subject} focusing on {topic}, tailored for {grade} level students following {curriculum} curriculum.
        
        Please follow these grade-appropriate guidelines:
        - Complexity: {complexity}
        - Vocabulary: {vocabulary}
        - Length: {chunk_length}
        - Examples: {examples}
        
        Each chunk should explain a specific aspect of the topic in a way that's educational, factual, and engaging for {grade} level students.
        Ensure the content aligns with {curriculum} curriculum standards where applicable.
        
        Format: Return each chunk as a separate paragraph with a clear focus.
        """
        
        response = openai.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": f"You are a knowledgeable educator who can explain complex topics clearly to {grade} level students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        result = response.choices[0].message.content
        
        # Split into chunks - we'll treat paragraphs as separate chunks
        chunks = [chunk.strip() for chunk in result.split("\n\n") if chunk.strip()]
        
        # If we don't have enough chunks, split the existing ones
        if len(chunks) < num_chunks:
            more_chunks = []
            for chunk in chunks:
                sentences = [s.strip() for s in chunk.split(".") if s.strip()]
                if len(sentences) >= 2:
                    mid = len(sentences) // 2
                    more_chunks.append(".".join(sentences[:mid]) + ".")
                    more_chunks.append(".".join(sentences[mid:]) + ".")
                else:
                    more_chunks.append(chunk)
            chunks = more_chunks
        
        return chunks[:num_chunks]
    
    def seed_knowledge_base(self, subject: str, topic: str, grade: str = "grade_6", curriculum: str = "General") -> None:
        """Seed the knowledge base with information about the subject and topic appropriate for the grade level and curriculum"""
        print(f"Seeding knowledge base for {subject} on {topic} at {grade} level following {curriculum} curriculum...")
        
        # Generate knowledge chunks with the exact grade level provided
        chunks = self.get_knowledge_chunks(subject, topic, grade, curriculum)
        
        # Create metadata for each chunk
        metadata = [
            {
                "subject": subject,
                "topic": topic,
                "grade": grade,
                "curriculum": curriculum,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]
        
        # Add to vector store
        self.vector_store.add_texts(chunks, metadata)
        
        print(f"Added {len(chunks)} knowledge chunks to the vector store for {grade} level {curriculum} curriculum.") 