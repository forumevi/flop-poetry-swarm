# FLOP Poetry Swarm Engine

Technocore Yellowpaper v0.5.0 Compliant Multi-Agent Poetry Settlement Engine.

## Architectural Overview

The FLOP Poetry Swarm engine orchestrates multiple autonomous agents to generate, evaluate, and cryptographically settle poetic outputs on the FLOP Network.

### Agent Workflow
1. **Architect Agent (`architect-01`)**: Establishes deterministic state locks, prompt constraints, and syllabic meters compliant with §12 specifications.
2. **Generator Agent (`generator-01`)**: Executes Best-of-N candidate generation using an integrated `SwarmFallbackEngine` for zero-downtime execution.
3. **Auditor Agent (`auditor-01`)**: Performs multi-criteria semantic evaluation (`PoetryEvaluator`) and validates cryptographic integrity using `WireFormatV3`.

## Protocol Compliance

* **WireFormat Standard**: Fully implements `WireFormatV3` (§12 & Appendix F.3).
* **Cryptographic Integrity**: Binds `h_in`, `h_out` SHA-256 digests with dynamic `decode_policy_hash`.
* **Evaluation Thresholding**: Enforces a minimum semantic evaluation threshold before settlement execution.

## Quick Start

### Prerequisites
* Python 3.10+

### Local Execution
Run the swarm orchestrator pipeline:
```bash
### python swarm/poetry_swarm.py
CI/CD Verification
Automated pipeline tests are configured via GitHub Actions under .github/workflows/test.yml.
