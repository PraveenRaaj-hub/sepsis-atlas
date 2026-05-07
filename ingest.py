import fitz
import os
from dotenv import load_dotenv

load_dotenv()

def parse_pdf(path: str) -> list[dict]:
    doc = fitz.open(path)
    chunks = []
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            chunks.append({
                "text": text.strip(),
                "page": page_num + 1,
                "source_file": os.path.basename(path)
            })
    return chunks

def load_all_papers(papers_dir: str = "papers") -> list[dict]:
    all_chunks = []
    papers = [f for f in os.listdir(papers_dir) if f.endswith(".pdf")]

    if not papers:
        print("No PDFs found in papers/ folder")
        return []

    for fname in papers:
        path = os.path.join(papers_dir, fname)
        chunks = parse_pdf(path)
        all_chunks.extend(chunks)
        print(f"✓ {fname}: {len(chunks)} pages extracted")

    print(f"\nTotal: {len(papers)} papers, {len(all_chunks)} pages")
    return all_chunks


if __name__ == "__main__":
    chunks = load_all_papers()