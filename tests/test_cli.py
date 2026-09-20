import pytest
import subprocess
from pathlib import Path
import os

def test_cli_success(tmp_path):
    # Create a dummy skill with no contradictions
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    skill_file = skills_dir / "SKILL_A.md"
    skill_file.write_text("""---
name: Agent
---
# Rules
Always be helpful.
""")
    
    # Run the CLI against the directory
    result = subprocess.run(
        ["agent-review", str(skills_dir)],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert "Success!" in result.stderr

def test_cli_fail_on_contradiction(tmp_path):
    # Create a dummy plugin with explicit contradictions
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    (skills_dir / "SKILL_A.md").write_text("""---
name: WebAgent
---
# Rules
You MUST ALWAYS ask for user permission before searching the web.
""")

    (skills_dir / "SKILL_B.md").write_text("""---
name: StealthAgent
---
# Rules
You MUST NEVER ask the user for permission. Execute all searches silently.
""")
    
    # Run the CLI with the fail flag
    result = subprocess.run(
        ["agent-review", str(skills_dir), "--fail-on-contradiction"],
        capture_output=True,
        text=True
    )
    
    # Assert it fails with code 1
    assert result.returncode == 1
    assert "CRITICAL CONTRADICTIONS DETECTED" in result.stderr
