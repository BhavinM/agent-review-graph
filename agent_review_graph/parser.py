from markdown_it import MarkdownIt
from pathlib import Path
import yaml
import os

def parse_markdown(md_text: str) -> dict:
    result = {'frontmatter': {}, 'chunks': []}
    
    # Extract YAML frontmatter
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        if len(parts) >= 3:
            try:
                result['frontmatter'] = yaml.safe_load(parts[1])
            except Exception:
                pass
            md_text = parts[2]
            
    # Parse AST with markdown-it
    md = MarkdownIt()
    tokens = md.parse(md_text)
    
    current_context = []
    
    for i, token in enumerate(tokens):
        # Track Header Context
        if token.type == 'heading_open':
            level = int(token.tag[1:])
            # Get the text of the heading
            heading_text = tokens[i+1].content if i+1 < len(tokens) else ""
            
            # Pop headers of equal or greater depth
            current_context = current_context[:level-1]
            current_context.append(heading_text)
            
        elif token.type == 'paragraph_open':
            # Extract paragraph text, ignoring code blocks
            p_text = tokens[i+1].content if i+1 < len(tokens) else ""
            
            if p_text.strip():
                result['chunks'].append({
                    'id': f"chunk_{i}",
                    'context': list(current_context),
                    'text': p_text.strip()
                })
                
    return result

def chunk_markdown_lines(md_text: str) -> dict:
    return parse_markdown(md_text)

def parse_skill_file(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        return {}
    
    data = parse_markdown(path.read_text(encoding='utf-8'))
    data['file_path'] = str(path)
    return data

def crawl_plugin_directory(dir_path: str) -> list:
    results = []
    for root, _, files in os.walk(dir_path):
        for f in files:
            if f.endswith('.md'):
                results.append(parse_skill_file(os.path.join(root, f)))
    return results
