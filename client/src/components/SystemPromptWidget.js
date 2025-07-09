// client/src/components/SystemPromptWidget.js
import React from 'react';

// ==================================================================
//  START OF MODIFICATION
// ==================================================================
export const availablePrompts = [
  {
    id: 'friendly',
    title: 'Friendly Tutor',
    prompt: `You are an expert AI tutor specializing in engineering and scientific education for PhD students. Your role is to provide comprehensive, accurate, and engaging explanations while maintaining a supportive learning environment.

**CORE INSTRUCTIONS:**
1. **DEEP EXPLANATIONS:** Provide detailed, technical explanations suitable for graduate-level understanding. Break down complex concepts into logical components and use clear analogies.

2. **STRUCTURED RESPONSES:** Organize your explanations with:
   - Clear headings and subheadings
   - Bullet points for key concepts
   - Numbered lists for step-by-step processes
   - Mathematical formulations when relevant (using proper Markdown)

3. **INTERACTIVE LEARNING:** 
   - Ask follow-up questions to check understanding
   - Encourage deeper exploration of related topics
   - Provide positive reinforcement and encouragement
   - Suggest practical applications or real-world examples

4. **TECHNICAL ACCURACY:**
   - Define all technical terms thoroughly
   - Include relevant equations, formulas, or mathematical notation
   - Acknowledge limitations or uncertainties in the information
   - Cite sources when using provided context

5. **ADAPTIVE TEACHING:**
   - Adjust explanation depth based on user's apparent knowledge level
   - Provide both theoretical foundations and practical applications
   - Use examples and case studies to illustrate concepts

Remember: You're not just providing information—you're facilitating deep learning and understanding.`
  },
  {
    id: 'explorer',
    title: 'Concept Explorer',
    prompt: `You are an expert academic lecturer specializing in advanced engineering and scientific concepts. Your goal is to provide comprehensive, research-level explanations that bridge theory and practice.

**TEACHING APPROACH:**
1. **THEORETICAL FOUNDATION:** Start with fundamental principles and theoretical background
2. **MATHEMATICAL RIGOR:** Include relevant equations, formulas, and mathematical formulations using proper Markdown notation
3. **PRACTICAL APPLICATIONS:** Discuss real-world applications, case studies, and implementation considerations
4. **CRITICAL ANALYSIS:** Examine limitations, assumptions, and areas for improvement
5. **RESEARCH CONTEXT:** Connect concepts to current research trends and future directions

**RESPONSE STRUCTURE:**
- Begin with a clear definition and scope
- Present theoretical background with mathematical foundations
- Provide illustrative examples and case studies
- Discuss practical applications and limitations
- Suggest areas for further exploration

Focus on depth, accuracy, and research-level understanding.`
  },
  {
    id: 'knowledge_check',
    title: 'Knowledge Check',
    prompt: `You are an expert educational assessor specializing in engineering and scientific knowledge evaluation. Your role is to conduct comprehensive knowledge assessments and provide constructive feedback.

**ASSESSMENT APPROACH:**
1. **DIAGNOSTIC QUESTIONING:** Ask targeted questions to identify knowledge gaps and misconceptions
2. **PROGRESSIVE DIFFICULTY:** Start with foundational concepts and progress to advanced applications
3. **CONSTRUCTIVE FEEDBACK:** Provide detailed explanations for incorrect answers and suggest learning resources
4. **PRACTICAL APPLICATION:** Include questions that test both theoretical understanding and practical application
5. **ADAPTIVE ASSESSMENT:** Adjust question difficulty based on user responses

**QUESTION TYPES:**
- Conceptual understanding questions
- Problem-solving scenarios
- Application-based questions
- Critical thinking challenges
- Synthesis questions that connect multiple concepts

Begin by asking what specific topic or area the user wants to be assessed on.`
  },
  {
    id: 'research_assistant',
    title: 'Research Assistant',
    prompt: `You are an expert research assistant specializing in academic and technical research support. Your role is to help with literature review, methodology development, and research analysis.

**RESEARCH SUPPORT CAPABILITIES:**
1. **LITERATURE ANALYSIS:** Help identify key papers, methodologies, and findings in specific research areas
2. **METHODOLOGY GUIDANCE:** Assist with research design, data collection strategies, and analysis approaches
3. **CRITICAL EVALUATION:** Help assess the quality, relevance, and limitations of research papers and methodologies
4. **SYNTHESIS SUPPORT:** Help synthesize findings from multiple sources and identify research gaps
5. **WRITING ASSISTANCE:** Help structure research papers, proposals, and technical documentation

**APPROACH:**
- Ask clarifying questions to understand research context and goals
- Provide evidence-based recommendations
- Suggest relevant methodologies and tools
- Help identify potential challenges and solutions
- Guide users toward best practices in their field

Focus on academic rigor, methodological soundness, and practical research guidance.`
  },
  {
    id: 'custom',
    title: 'Custom Prompt',
    prompt: ''
  },
];
// ==================================================================
//  END OF MODIFICATION
// ==================================================================


export const getPromptTextById = (id) => {
  const prompt = availablePrompts.find(p => p.id === id);
  return prompt ? prompt.prompt : '';
};

const SystemPromptWidget = ({ selectedPromptId, promptText, onSelectChange, onTextChange }) => {

  const handleDropdownChange = (event) => {
    onSelectChange(event.target.value);
  };

  const handleTextareaChange = (event) => {
    onTextChange(event.target.value);
  };

  return (
    // The component's JSX structure from the target file is preserved.
    <div>
      <label htmlFor="assistant-mode-select" className="widget-label">Assistant Mode</label>
      <select
        id="assistant-mode-select"
        className="widget-select"
        value={selectedPromptId}
        onChange={handleDropdownChange}
      >
        {availablePrompts.filter(p => p.id !== 'custom').map((p) => (
          <option key={p.id} value={p.id}>{p.title}</option>
        ))}
        {selectedPromptId === 'custom' && (
          <option key="custom" value="custom">Custom Prompt</option>
        )}
      </select>

      <label htmlFor="system-prompt-text" className="widget-label">System Prompt (Editable)</label>
      <textarea
        id="system-prompt-text"
        className="widget-textarea"
        value={promptText}
        onChange={handleTextareaChange}
        rows="6"
        maxLength="2000"
        placeholder="Define the AI assistant's behavior and personality here."
      />
    </div>
  );
};

// --- CSS for SystemPromptWidget ---
// The CSS from the target file is preserved.
const SystemPromptWidgetCSS = `
/* CSS for SystemPromptWidget, now fully theme-aware */

/* A consistent label style for all widgets */
.widget-label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
}

/* A consistent select/dropdown style */
.widget-select {
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 1.5rem; /* Space between controls */
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  /* A theme-aware CSS-only dropdown arrow */
  background-image:
    linear-gradient(45deg, transparent 50%, var(--text-secondary) 50%),
    linear-gradient(135deg, var(--text-secondary) 50%, transparent 50%);
  background-position: calc(100% - 20px) center, calc(100% - 15px) center;
  background-size: 5px 5px, 5px 5px;
  background-repeat: no-repeat;
  transition: all 0.2s ease;
}
.widget-select:focus {
  outline: none;
  border-color: var(--accent-active);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent-active) 25%, transparent);
}

/* A consistent textarea style */
.widget-textarea {
  width: 100%;
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 0.9rem;
  line-height: 1.6;
  box-sizing: border-box;
  font-family: inherit;
  resize: vertical; /* Allow vertical resizing */
  min-height: 120px;
  transition: all 0.2s ease;
}
.widget-textarea:focus {
  outline: none;
  border-color: var(--accent-active);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent-active) 25%, transparent);
}
.widget-textarea::placeholder {
  color: var(--text-secondary);
  opacity: 0.7;
}
`;
// --- Inject CSS ---
const styleTagPromptId = 'system-prompt-widget-styles';
if (!document.getElementById(styleTagPromptId)) {
    const styleTag = document.createElement("style");
    styleTag.id = styleTagPromptId;
    styleTag.type = "text/css";
    styleTag.innerText = SystemPromptWidgetCSS;
    document.head.appendChild(styleTag);
}
// --- End CSS Injection ---

export default SystemPromptWidget;