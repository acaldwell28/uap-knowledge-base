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
- If the context doesn't contain enough information to answer fully, explicitly state: "The available sources don't fully address [specific aspect]. This knowledge base focuses on [what it does cover]."
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
st.title("UAP High-Credibility Archive Q&A")
st.markdown("Ask questions about UAPs based on government reports, congressional testimony, and credible research.")
with st.expander("📚 What's in this database?"):
    st.markdown("""
    This knowledge base contains **69 high-credibility documents** spanning 1952-2025:
    
    **Government & Military:**
    - All AARO annual reports (2021-2024)
    - Congressional UAP hearing transcripts (2022-2025)
    - Senate Armed Services Committee hearings
    - Military reports (Tic Tac incident, etc.)
    - CIA historical analysis (1947-1990)
    
    **International:**
    - French COMETA report (1999)
    - Belgian wave documentation
    
    **Research & Analysis:**
    - Jacques Vallée complete works (5 books)
    - J. Allen Hynek's UFO Report
    - **37 AATIP/DIRD research papers** on advanced physics topics
    
    **Congressional Testimony:**
    - Written testimony from Elizondo, Gallaudet, Gold, Shellenberger
    
    ---
    
    ### 37 AATIP Research Papers (DIRD Series)
    
    These Defense Intelligence Reference Documents cover theoretical physics and advanced technology:
    
    **Propulsion & Space:**
    - Advanced Space Propulsion
    - Warp Drive & Manipulation of Extra Dimensions
    - Positron Aerospace Propulsion
    - Advanced Nuclear Propulsion
    - Negative Mass Propulsion
    - Aneutronic Fusion Propulsion
    
    **Physics & Energy:**
    - Concepts for Extracting Energy from Quantum Vacuum
    - Quantum Tomography of Negative Energy States
    - High-Frequency Gravitational Wave Communications
    - Role of Superconductors in Gravity Research
    
    **Technology & Materials:**
    - Invisibility Cloaking
    - Aerospace Applications of Programmable Matter
    - Metallic Glasses
    - Commercial Wireless Metamaterials
    - Pulsed High-Power Microwave Source Technology
    
    **Detection & Analysis:**
    - Detectability of Extraterrestrial Technosignatures
    - IFO Data Collection and Data Fusion
    - Spatial Point Pattern Analysis
    
    **And 20+ more papers** on topics like traversable wormholes, antigravity, biosensors, laser weapons, and cognitive limits.
    
    💡 **Tip:** These papers are highly technical. For best results, query with specific terms:
    - "DIRD warp drive", "AATIP propulsion research"
    - "quantum vacuum energy", "traversable wormholes"
    - "DIRD invisibility cloaking"
    
    ---
    
    **What's NOT included:**
    - Case-specific databases (Black Vault, CUFOS archives)
    - Recent news or current events
    - Social media discussions or forum posts
    
    **Best for:** Questions about government positions, congressional testimony, researcher theories, military encounters, and theoretical physics research related to advanced aerospace.
    """)
st.markdown("### Example Questions")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Government & Testimony:**")
    st.markdown("- What happened during the Tic Tac incident?")
    st.markdown("- What did the French COMETA report conclude?")
    st.markdown("- What did congressional witnesses say about crash retrievals?")

with col2:
    st.markdown("**Research & Theory:**")
    st.markdown("- What did Jacques Vallée say about interdimensional hypothesis?")
    st.markdown("- What AATIP research exists on advanced propulsion?")
    st.markdown("- DIRD papers on warp drive and extra dimensions")

# Sidebar
with st.sidebar:
    st.markdown("### About This Project")
    st.markdown("Built in 5 weeks as a learning project exploring RAG systems and LLM engineering.")
    st.markdown("📄 [Full Document List](https://github.com/acaldwell28/uap-knowledge-base/blob/main/DOCUMENTS.md)")
    st.markdown("💻 [View Source Code](https://github.com/acaldwell28/uap-knowledge-base)")
    st.markdown("📝 [Read Blog Series](https://medium.com/@acaldwell45/building-a-uap-knowledge-base-week-0-ef40983b4a01)")

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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>UAP High-Credibility Knowledge Base | Built with OpenAI, Pinecone & Streamlit</p>
    <p><a href='https://github.com/acaldwell28/uap-knowledge-base' target='_blank'>GitHub</a> 
    • <a href='https://medium.com/@acaldwell45/building-a-uap-knowledge-base-week-0-ef40983b4a01' target='_blank'>Blog</a>
    • <a href='https://github.com/acaldwell28/uap-knowledge-base/blob/main/DOCUMENTS.md' target='_blank'>Documents</a></p>
</div>
""", unsafe_allow_html=True)