import pytest
from pathlib import Path
import yaml
from agent_review_graph.parser import parse_markdown, chunk_markdown_lines

# Using raw string parsing to verify the core logic
def test_frontmatter_extraction():
    md = """---
name: TestAgent
---
# Hello
"""
    result = parse_markdown(md)
    assert result['frontmatter']['name'] == 'TestAgent'

def test_chunking_with_context():
    md = """# Setup
Some setup text.
## API Keys
The API key text.
"""
    result = parse_markdown(md)
    chunks = result['chunks']
    
    assert chunks[0]['context'] == ['Setup']
    assert "Some setup text." in chunks[0]['text']
    
    assert chunks[1]['context'] == ['Setup', 'API Keys']
    assert "The API key text." in chunks[1]['text']

def test_code_blocks_ignored():
    md = """# Rules
Rule 1.
```python
print("I am a code block, not a rule")
```
Rule 2.
"""
    result = parse_markdown(md)
    texts = [c['text'] for c in result['chunks']]
    
    assert any("Rule 1." in t for t in texts)
    assert any("Rule 2." in t for t in texts)
    assert not any("print" in t for t in texts)
