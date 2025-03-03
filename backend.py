from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datasketch import MinHash, MinHashLSH
import re
import docx
from typing import List, Dict
import uvicorn
import io
from io import BytesIO

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_docx(file):
    try:
        doc = docx.Document(BytesIO(file))
        # Extract text from the document
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    except Exception as e:
        raise ValueError(f"Error while processing DOCX file: {str(e)}")

def preprocess_text(text: str) -> str:
    """Clean and normalize text."""
    return re.sub(r'\W+', ' ', text).lower()

def split_into_passages(text: str, passage_length: int) -> List[str]:
    """Split text into fixed-length passages."""
    words = text.split()
    return [" ".join(words[i:i + passage_length]) for i in range(0, len(words), passage_length)]

def create_minhash(text: str, num_perm=128) -> MinHash:
    """Generate MinHash signature for a passage."""
    m = MinHash(num_perm=num_perm)
    for word in text.split():
        m.update(word.encode('utf8'))
    return m

@app.post("/find_similarities/")
async def find_similarities(files: List[UploadFile], passage_length: int = 50, threshold: float = 0.5, num_perm: int = 128, sim_score_threshold: float = 0.2):

    texts = []
    file_names = []

    for file in files:
        content = await file.read()
        if file.filename.endswith(".docx"):
            text = extract_text_from_docx(content)
        else:
            text = content.decode("utf-8")
        
        texts.append(preprocess_text(text))
        file_names.append(file.filename)

    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    passage_map = {}
    minhashes = {}

    # Process each text
    for doc_id, text in enumerate(texts):
        passages = split_into_passages(text, passage_length)
        passage_map[doc_id] = passages

        for i, passage in enumerate(passages):
            m = create_minhash(passage, num_perm)
            minhashes[(doc_id, i)] = m
            lsh.insert(f"{doc_id}_{i}", m)

    similar_passages = []
    for (doc1, i), m1 in minhashes.items():
        for result in lsh.query(m1):
            doc2, j = map(int, result.split("_"))
            if doc1 < doc2:  # Avoid duplicate pairs
                sim_score = m1.jaccard(minhashes[(doc2, j)])
                if sim_score > sim_score_threshold:
                    similar_passages.append({
                        "doc1": file_names[doc1], "passage1_index": i,
                        "doc2": file_names[doc2], "passage2_index": j,
                        "text1": passage_map[doc1][i], "text2": passage_map[doc2][j],
                        "score": round(sim_score, 2)
                    })

    return {"similar_passages": similar_passages, "file_names": file_names}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

