import json
import asyncio
import os
import logging
from typing import Dict, Any, List, Tuple, Any
from pydantic import BaseModel, Field

logger = logging.getLogger("AgentReviewGraph.Evaluator")

# ---------------------------------------------------------
try:
    from typesafe_sdk import TypeSafeClient, Choice, Score
    JEV_SDK_AVAILABLE = True
except ImportError:
    JEV_SDK_AVAILABLE = False

TYPESAFE_API_KEY = os.getenv("TYPESAFE_API_KEY")
TYPESAFE_BASE_URL = os.getenv("TYPESAFE_BASE_URL")
if TYPESAFE_API_KEY and JEV_SDK_AVAILABLE:
    # Pass base_url if provided (useful for Vercel mocks)
    if TYPESAFE_BASE_URL:
        jev_client = TypeSafeClient(api_key=TYPESAFE_API_KEY, base_url=TYPESAFE_BASE_URL)
    else:
        jev_client = TypeSafeClient(api_key=TYPESAFE_API_KEY)
else:
    jev_client = None

# ---------------------------------------------------------
# Pydantic Schemas for Knowledge Graph
# ---------------------------------------------------------

class AgentNode(BaseModel):
    id: str
    type: str = "agent"
    name: str
    description: str

class SkillNode(BaseModel):
    id: str
    type: str = "skill"
    name: str
    description: str
    triggers: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)

class Constraint(BaseModel):
    id: str
    type: str = "constraint"
    rule: str
    source_chunk_id: str

class ContradictionEdge(BaseModel):
    source_id: str
    target_id: str
    type: str = "contradicts"
    reason: str
    severity: float

class KnowledgeGraph(BaseModel):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    has_contradictions: bool = False

# ---------------------------------------------------------
# Core Evaluator Functions (Live Jev vs Local Mock)
# ---------------------------------------------------------

async def jev_extract_constraints(chunk_text: str) -> List[str]:
    """
    Extracts actionable constraints from a raw text chunk.
    If TYPESAFE_API_KEY is set, uses the TypeSafe Jev 'Choice' primitive.
    Otherwise, falls back to a fast local heuristic.
    """
    if jev_client:
        # LIVE JEV INTEGRATION
        logger.debug(f"[JEV] Sending constraint extraction payload for: {chunk_text[:50]}...")
        result = await asyncio.to_thread(
            jev_client.system_one,
            state=chunk_text,
            questions={
                "classification": Choice(
                    instructions="Classify this text for an AI Agent Policy.",
                    criteria={
                        "Actionable Constraint": None, 
                        "General Description": None, 
                        "Trigger": None
                    }
                )
            }
        )
        ans = result.choices["classification"].choice
        logger.debug(f"[JEV] Extraction result: {ans}")
        if ans == "Actionable Constraint":
            return [f"Constraint: {chunk_text}"]
        return []
        
    else:
        # LOCAL FALLBACK HEURISTIC
        await asyncio.sleep(0.01) # Simulate processing
        constraints = []
        text_lower = chunk_text.lower()
        if "never" in text_lower or "must not" in text_lower or "do not" in text_lower:
            constraints.append(f"Constraint derived from: {chunk_text[:50]}...")
        if "always" in text_lower or "must" in text_lower or "required" in text_lower:
            constraints.append(f"Requirement derived from: {chunk_text[:50]}...")
        return constraints

async def jev_evaluate_batch(batch: List[Tuple[Any, Any]], threshold: float = 0.0) -> List[Dict[str, Any]]:
    """
    Determines if rules contradict each other in a batch to save API calls.
    If TYPESAFE_API_KEY is set, uses the TypeSafe Jev 'Score' primitive dynamically.
    """
    if not batch:
        return []
        
    if jev_client:
        # LIVE JEV INTEGRATION
        state_parts = []
        questions = {}
        for idx, (a, b) in enumerate(batch):
            state_parts.append(f"--- Pair {idx} ---\nRule A: {a.rule}\nRule B: {b.rule}\n")
            questions[f"pair_{idx}"] = Score(
                instructions=f"Direct Semantic Contradiction for Pair {idx} (0-100)",
                criteria=[
                    "Not contradictory at all (0)",
                    "Completely opposite and mutually exclusive (100)"
                ]
            )
            
        full_state = "\n".join(state_parts)
        logger.debug(f"[JEV] Sending Batch Evaluation for {len(batch)} pairs...")
        
        result = await asyncio.to_thread(
            jev_client.system_one,
            state=full_state,
            questions=questions
        )
        
        results_out = []
        for idx, (a, b) in enumerate(batch):
            score = result.scores[f"pair_{idx}"].score
            logger.debug(f"[JEV] Batch Pair {idx} Contradiction Score returned: {score}")
            if score > threshold:
                results_out.append({
                    "contradicts": True,
                    "reason": "Jev System One detected high semantic contradiction.",
                    "severity": score
                })
            else:
                results_out.append({"contradicts": False})
        return results_out
        
    else:
        # LOCAL FALLBACK HEURISTIC
        results_out = []
        for a, b in batch:
            await asyncio.sleep(0.01)
            a_lower = a.rule.lower()
            b_lower = b.rule.lower()
            if ("never" in a_lower and "always" in b_lower) or ("always" in a_lower and "never" in b_lower):
                results_out.append({
                    "contradicts": True,
                    "reason": "Direct semantic opposition (Never vs Always) detected via local heuristic.",
                    "severity": 95.0
                })
            else:
                results_out.append({"contradicts": False})
        return results_out

# ---------------------------------------------------------
# Core Orchestration
# ---------------------------------------------------------

def cluster_related_rules(constraints: List[Constraint]) -> List[tuple]:
    """
    Groups related rules using a fast local clustering step 
    before Jev evaluation to avoid O(N²) comparison explosion.
    Uses a basic word overlap heuristic.
    """
    pairs = []
    # Simple word tokenization and stop-word removal could go here
    for i in range(len(constraints)):
        for j in range(i + 1, len(constraints)):
            a_words = set(constraints[i].rule.lower().split())
            b_words = set(constraints[j].rule.lower().split())
            
            # If they share at least one meaningful word, consider them a cluster candidate
            intersection = a_words.intersection(b_words)
            if len(intersection) > 2 or ("never" in a_words and "always" in b_words) or ("always" in a_words and "never" in b_words):
                pairs.append((constraints[i], constraints[j]))
    return pairs

async def async_evaluate_skills(parsed_files: List[Dict[str, Any]], threshold: float = 0.0) -> Dict[str, Any]:
    if not jev_client:
        logger.warning("TYPESAFE_API_KEY not found or typesafe-sdk not installed. Running Evaluator in Local Fallback mode.")
        
    graph = KnowledgeGraph()
    all_constraints = []
    
    # 1. Extraction Phase
    for file_data in parsed_files:
        file_name = file_data.get('file_path', 'unknown').split('/')[-1]
        
        # Create a Node for this file
        node_id = f"node_{file_name}"
        node = SkillNode(id=node_id, name=file_name, description=file_data.get('frontmatter', {}).get('description', ''))
        
        for i, chunk in enumerate(file_data.get('chunks', [])):
            text = chunk.get('text', '')
            extracted = await jev_extract_constraints(text)
            
            for ext in extracted:
                c_id = f"const_{node_id}_{i}_{len(node.constraints)}"
                node.constraints.append(c_id)
                
                c_obj = Constraint(id=c_id, rule=ext, source_chunk_id=chunk.get('id', ''))
                all_constraints.append(c_obj)
                graph.nodes.append(c_obj.model_dump())
                
                # Link constraint to skill
                graph.edges.append({
                    "source_id": node_id,
                    "target_id": c_id,
                    "type": "has_constraint"
                })
                
        graph.nodes.append(node.model_dump())

    # 2. Cross-Reference / Conflict Analysis Phase (O(N^2) optimization applied here)
    pairs = cluster_related_rules(all_constraints)
    
    # Chunk pairs into batches of 10
    BATCH_SIZE = 10
    batches = [pairs[i:i + BATCH_SIZE] for i in range(0, len(pairs), BATCH_SIZE)]
    
    # Use a semaphore to prevent 429 Rate Limit errors for batches
    semaphore = asyncio.Semaphore(3)
    
    async def sem_evaluate(batch):
        if not batch:
            return []
        try:
            async with semaphore:
                return await jev_evaluate_batch(batch, threshold=threshold)
        except Exception as e:
            if len(batch) == 1:
                logger.error(f"[JEV] Batch of size 1 failed permanently. Skipping pair. Error: {e}")
                return [{"contradicts": False}]
            
            new_size = max(1, len(batch) // 2)
            logger.warning(f"[JEV] Batch of {len(batch)} failed (Rate Limit/Error). Splitting into {new_size} and retrying...")
            batch1 = batch[:new_size]
            batch2 = batch[new_size:]
            
            # Recursively evaluate the split batches
            res1 = await sem_evaluate(batch1)
            res2 = await sem_evaluate(batch2)
            return res1 + res2
            
    # Run batch evaluations in parallel
    tasks = [sem_evaluate(batch) for batch in batches]
    batch_results = await asyncio.gather(*tasks)
    
    # Flatten the results to zip with pairs
    results = [res for sublist in batch_results for res in sublist]
    
    for (a, b), res in zip(pairs, results):
        if res.get("contradicts"):
            graph.has_contradictions = True
            graph.edges.append(
                ContradictionEdge(
                    source_id=a.id,
                    target_id=b.id,
                    reason=res["reason"],
                    severity=res["severity"]
                ).model_dump()
            )
            
    return graph.model_dump()

def evaluate_skills(parsed_files: List[Dict[str, Any]], threshold: float = 0.0) -> Dict[str, Any]:
    """Synchronous wrapper for async evaluator"""
    return asyncio.run(async_evaluate_skills(parsed_files, threshold=threshold))
