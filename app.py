import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# Initialize clients
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
index = pc.Index("uap-knowledge-base")

def rag_query(question, top_k=5):
    
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=[question]
    )
    query_embedding = response.data[0].embedding
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    context = ""
    for i, match in enumerate(results['matches'], 1):
        source = match['metadata']['source']
        text = match['metadata']['text']
        context += f"[Source {i}: {source}]\n{text}\n\n"
    
    prompt = f"""You are a helpful assistant answering questions about UAPs based on a curated knowledge base of credible sources.

Context from relevant documents:
{context}

Question: {question}

Instructions:
- Answer the question based only on the provided context
- Cite your sources using [Source N] notation
- If the context doesn't contain enough information, say so
- Be concise but thorough

Answer:"""
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about UAPs based on provided documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    answer = response.choices[0].message.content
    
    return {
        'answer': answer,
        'sources': [
            {
                'source': match['metadata']['source'],
                'text': match['metadata']['text'][:200],
                'score': match['score']
            }
            for match in results['matches']
        ]
    }

# Streamlit UI
st.title("UAP High-Credibility Knowledge Base")
st.markdown("Ask questions about UAPs based on government reports, congressional testimony, and credible research.")
st.info("This knowledge base contains 69 high-credibility documents including government reports, congressional testimony, and research from Jacques Vallée and J. Allen Hynek.")
st.markdown("### Example Questions")
st.markdown("- What happened during the Tic Tac incident?")
st.markdown("- What did the French COMETA report conclude?")
st.markdown("- What theories exist about UAP origins?")
st.markdown("- What did congressional witnesses testify about crash retrieval programs?")
st.markdown("---")


# Query input
with st.form("query_form"):
    question = st.text_input("Ask a question:", placeholder="What happened during the Tic Tac incident?")
    submitted = st.form_submit_button("Search")

if submitted and question:
    with st.spinner("Searching knowledge base..."):
        result = rag_query(question)
    
    # Display answer
    st.markdown("### Answer")
    st.markdown(result['answer'])
    
    # Display sources
    st.markdown("### Sources")
    for i, source in enumerate(result['sources'], 1):
        source_name = source['source'].replace('_', ' ').replace('-', ' ')
        with st.expander(f"Source {i}: {source_name} (relevance: {source['score']:.2f})"):
            st.text(source['text'] + "...")