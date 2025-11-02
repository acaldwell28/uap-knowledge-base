# UAP High-Credibility Knowledge Base

A RAG (Retrieval Augmented Generation) system for querying UAP/UFO research using semantic search.

## Live Demo
🔗 [https://uap-knowledge-base-epdyhkmj8ztavaz6gokjh5.streamlit.app/](https://uap-knowledge-base-epdyhkmj8ztavaz6gokjh5.streamlit.app/)

## What It Does

Ask questions about UAPs in natural language and get answers with citations from 69 high-credibility sources including:
- Government reports (AARO, COMETA)
- Congressional testimony
- Military encounters (Tic Tac incident)
- Researcher analyses (Jacques Vallée, J. Allen Hynek)

## How It Works

1. **Document Collection:** 69 curated documents (4,200 pages) from government, military, and research sources
2. **Chunking:** Split into 2,357 semantic chunks (~750 words each)
3. **Embedding:** Converted to 1,536-dimensional vectors using OpenAI text-embedding-3-small
4. **Vector Search:** Stored in Pinecone for semantic similarity search
5. **Generation:** GPT-4o-mini generates answers based on retrieved context with citations

## Tech Stack

- **Embeddings:** OpenAI text-embedding-3-small
- **Vector Database:** Pinecone (serverless)
- **LLM:** GPT-4o-mini
- **UI:** Streamlit
- **Deployment:** Streamlit Cloud

## Results

- 26+ unique users in first week
- Handles complex queries about government positions, congressional testimony, and researcher theories
- Cost: ~$0.003 per query

## Limitations

- Corpus coverage: Focuses on government/military sources and foundational research
- Doesn't include case-specific archives (Black Vault, CUFOS)
- No current news or recent events

## Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set up secrets in .streamlit/secrets.toml
OPENAI_API_KEY = "your-key"
PINECONE_API_KEY = "your-key"

# Run
streamlit run app.py
```

## Project Timeline

Built in 4 weeks:
- Week 1: Data collection (OCR, cleaning)
- Week 2: Embeddings and vector database
- Week 3: RAG pipeline and UI
- Week 4: Deployment and user feedback

## Blog Series

[Link to your Medium posts - all 5 of them]

## Next Steps (V2)

- Expand corpus (Black Vault, CUFOS)
- Hybrid search (semantic + keyword)
- Conversation memory
- Query decomposition for complex questions

## License

[Choose one - MIT is common for portfolio projects]