import fitz
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def parse_pdf(path: str) -> list[dict]:
    doc = fitz.open(path)
    chunks = []
    
    for page_num, page in enumerate(doc):
        # Extract regular text
        text = page.get_text("text")
        
        # Extract tables separately
        table_text = ""
        try:
            tables = page.find_tables()
            if tables.tables:
                for i, table in enumerate(tables.tables):
                    df = table.to_pandas()
                    table_text += f"\nTABLE {i+1}:\n"
                    table_text += df.to_string(index=False)
                    table_text += "\n"
        except Exception:
            pass
        
        # Combine text and tables
        combined = text.strip()
        if table_text:
            combined += "\n\nTABLES ON THIS PAGE:\n" + table_text
        
        if combined.strip():
            chunks.append({
                "text": combined,
                "page": page_num + 1,
                "source_file": os.path.basename(path),
                "has_table": bool(table_text)
            })
    
    return chunks

def load_all_papers(papers_dir: str = "papers") -> list[dict]:
    all_chunks = []
    papers = [f for f in os.listdir(papers_dir) 
              if f.endswith(".pdf")]
    
    if not papers:
        print("No PDFs found in papers/ folder")
        return []
    
    table_count = 0
    for fname in sorted(papers):
        path = os.path.join(papers_dir, fname)
        chunks = parse_pdf(path)
        all_chunks.extend(chunks)
        tables_in_paper = sum(1 for c in chunks if c['has_table'])
        table_count += tables_in_paper
        print(f"✓ {fname}: {len(chunks)} pages, {tables_in_paper} pages with tables")
    
    print(f"\nTotal: {len(papers)} papers")
    print(f"Total: {len(all_chunks)} pages")
    print(f"Total: {table_count} pages containing tables")
    return all_chunks

if __name__ == "__main__":
    chunks = load_all_papers()
    
    # Show a sample of a page with a table
    table_chunks = [c for c in chunks if c['has_table']]
    if table_chunks:
        print("\n--- Sample page with table ---")
        print(f"File: {table_chunks[0]['source_file']}, Page {table_chunks[0]['page']}")
        print(table_chunks[0]['text'][:600])