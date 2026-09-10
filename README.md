# Flop Poetry Swarm

A 3-agent coordination pipeline (**Architect → Generator → Auditor**) built for the Flop Labs & Technocore ecosystem, aligned with **FLOP Yellow Paper v0.5.0** settlement specs (`V3 VerifiedTurn`, `pallet_compute_channel`).

## Swarm Architecture
* **Architect Agent:** Defines theme, rhyming scheme, and structural parameters (`/kv/` state lock).
* **Generator Agent:** Produces stanzas and passes signed payload via Mailbox (`mb-`).
* **Auditor Agent:** Verifies syllable meter, checks kafiye structures, and computes `output_hash` & `decode_policy_hash` for chain settlement.

## Protocol Compliance
- **Specification:** FLOP Yellow Paper v0.5.0 §12 (Compute Channel) & Appendix F.3
- **Wire Format:** Standardized `V3 VerifiedTurn` leaf generation