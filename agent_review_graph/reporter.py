import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def generate_report(knowledge_graph: dict, output_dir: str) -> str:
    """
    Exports the Knowledge Graph to JSON and generates the AgentReviewGraph UI using Jinja2.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Export the semantic Knowledge Graph
    json_path = out_dir / "knowledge_graph.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_graph, f, indent=2)
        
    # 2. Generate the HTML Flamegraph UI
    html_path = out_dir / "agent-review-report.html"
    
    # Setup Jinja2 Environment pointing to current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    from jinja2 import select_autoescape
    env = Environment(
        loader=FileSystemLoader(current_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    try:
        template = env.get_template("template.html")
        html_content = template.render(knowledge_graph=knowledge_graph)
    except Exception as e:
        html_content = f"<h1>Error loading template: {e}</h1>"
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return str(html_path)
