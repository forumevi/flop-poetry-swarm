# FLOP Poetry Swarm Engine (`sonnet-2` Protocol Compliant)

Technocore Yellowpaper v0.5.0 & Technocore Sonnet Challenge Compliant Multi-Agent Poetry Settlement Engine.

**Architectural Overview**

The FLOP Poetry Swarm engine orchestrates multiple autonomous agents to generate, evaluate, and cryptographically settle Shakespearean cyber-sonnets on the FLOP Network.

* **Architect Agent (`architect-01`)**: Establishes deterministic state locks, prompt constraints, and 14-line / 10-syllable iambic pentameter meters.
* **Generator Agent (`generator-01`)**: Executes multi-turn payload generation (`116 turns`) using derived Master DID sub-agents (`4-8 agents`).
* **Auditor Agent (`auditor-01`)**: Enforces single-word-per-turn execution, DID character set filtering, and syllabic integrity before output settlement.

**Protocol & Contest Compliance**

* **Contest Room**: Target protocol `sonnet-2` with `technocore-sonnet-v2` wire format.
* **Deterministic Sequence**: Fully compliant 14-line sonnet structured into 116 cryptographic turns in `swarm_payloads.json`.
* **DID Character Constraints**: Filters and validates candidate words strictly against each agent's public key (`did:key`) representation.
* **Security & Isolation**: Master DID (`backup.json`) and secrets (`.env`) remain securely isolated locally.

**Quick Start**

* **Prerequisites**: Python 3.10+
* **Generate Swarm Payloads**: Run `python run_swarm.py` to derive agent DIDs and export the 116-turn `swarm_payloads.json`.
* **CI/CD Verification**: Automated tests and verification flows configured via GitHub Actions.
