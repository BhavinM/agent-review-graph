import argparse
import sys
import os
import logging
from pathlib import Path

from .parser import crawl_plugin_directory, parse_skill_file
from .evaluator import evaluate_skills
from .reporter import generate_report

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("AgentReviewGraph")

def main():
    parser = argparse.ArgumentParser(description="AgentReviewGraph: AI Linter & Graph Inspector for Agent Skills")
    parser.add_argument("target", help="Path to a SKILL.md file or a plugin directory")
    parser.add_argument("--fail-on-contradiction", action="store_true", help="Exit with code 1 if critical contradictions are found")
    parser.add_argument("--threshold", type=float, default=0.0, help="Contradiction severity threshold to flag (default: 0.0)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging of Jev API payloads")
    parser.add_argument("--output-dir", default=os.getcwd(), help="Directory to save the generated JSON and HTML reports")
    
    args = parser.parse_args()
    
    if args.verbose:
        # Only set DEBUG on our own loggers — not the root logger
        # Setting the root logger to DEBUG leaks verbose output from third-party
        # libraries (e.g. markdown-it parser internals, httpx request traces)
        logging.getLogger("AgentReviewGraph").setLevel(logging.DEBUG)
        logging.getLogger("AgentReviewGraph.Evaluator").setLevel(logging.DEBUG)
        logging.getLogger("AgentReviewGraph.Parser").setLevel(logging.DEBUG)
    
    target_path = Path(args.target)
    if not target_path.exists():
        logger.error(f"Target path does not exist: {target_path}")
        sys.exit(1)
        
    try:
        logger.info(f"Analyzing target: {target_path}")
        
        parsed_files = []
        if target_path.is_dir():
            parsed_files = crawl_plugin_directory(target_path)
            logger.info(f"Discovered {len(parsed_files)} markdown files in directory.")
        else:
            parsed_files = [parse_skill_file(target_path)]
            
        logger.info(f"Building Semantic Knowledge Graph via Jev Engine (Threshold: {args.threshold})...")
        knowledge_graph = evaluate_skills(parsed_files, threshold=args.threshold)
        
        logger.info(f"Generating interactive UI report to {args.output_dir}...")
        report_path = generate_report(knowledge_graph, output_dir=args.output_dir)
        
        logger.info(f"Success! Report generated at: {report_path}")
        
        if args.fail_on_contradiction and knowledge_graph.get("has_contradictions"):
            logger.error("CRITICAL CONTRADICTIONS DETECTED. Failing CI check.")
            sys.exit(1)
            
    except Exception as e:
        logger.exception("An unexpected error occurred during execution.")
        sys.exit(1)

if __name__ == "__main__":
    main()
