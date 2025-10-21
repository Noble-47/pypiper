Design and implement an abstract pipeline framework that enables building modular, stateful data processing pipelines. The framework should provide a foundation for creating various types of data processing workflows.

# Framework Requirements

## Core Pipeline Architecture
 *  Support sequential processing through defined steps
 *  Track and manage pipeline state, as the steps flow
 *  Persist pipeline state to the DB
 *  Enable data flow between steps

## Framework Features
 *  Error handling and propagation
 *  Ability to retry any specific step
 *  State inspection for every step

# Implementation Task
Using the framework you create, implement a document processing pipeline that demonstrates the framework’s capabilities.

## Example: 

### Document Processing Pipeline Requirements
 * **Text Classification**
    - Input: Raw text content
    - Classify text into categories:
        - Business
        - Technical
        - General
    - Output: Category and confidence score
 
 * **Keyword Extraction**
    - Input: Text category from previous step
    - Extract keywords based on the category:
        - Business: Look for financial/management terms
        - Technical: Look for technical/code terms
        - General: Look for common nouns
    - Output: List of relevant keywords

 * **Report Generation**
    - Input: Category and keywords from previous steps
    - Create summary with:
        - Detected category
        - Category-specific keywords
        - Processing metadata
    - Output: Final report

### Key Dependencies:
    - Step 2 requires category from step 1 to determine which type of keywords to extract
    - Step 3 combines results from both previous steps
    - Each step’s failure stops the pipeline

**The pipeline should demonstrate:**
 * **Clear data dependencies between steps**
 * **State management**
 * **Error handling**



