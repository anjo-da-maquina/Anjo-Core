# Anjo-Core : GenAI-Driven Autonomous Testing & Zero-Trust Governance

> **The Anjo da máquina Protocol: Autonomous Self-Healing CI/CD Pipeline**  
> Architect & Maintainer: **Anjo Machina (安城巻那)**  
> *Language: English | [日本語版ドキュメント (README.ja.md)](./README.ja.md)*

---

## Vision

In the era of Generative AI, code is generated faster than human engineers can verify. **Anjo-Core** is a completely free, open-source validation and automated zero-trust testing framework engineered for modern, mission-critical software pipelines. 

Unlike traditional passive testing suites that merely log regressions, Anjo-Core operates an autonomous audit layer directly inside CI/CD environments. It enforces cryptographic integrity, automated remediation, and operational stillness (**Ataraxia**) without the overhead of manual QA.

---

## Core Pillars & Features

* **Automated Requirements Parsing (GenAI Integration)**: Dynamically parses functional specifications (Excel / YAML) into robust test suites via Model Context Protocol (MCP) and multi-LLM consensus.
* **Zero-Trust CI/CD Enforcement**: Integrates natively with GitHub Actions to block unauthorized schema drift, replay attacks, and unverified AI hallucinations.
* **Deep Traceability**: Provides comprehensive audit logs, generating tamper-proof JUnit XML compliance reports and Zero-Knowledge Proof (ZKP) integrity records.
* **Autonomous Remediation**: Detects anomalies and triggers automated recovery sequences before failing closed.

---

## Architecture: The 37 Autonomous Agents (Angels)

Anjo-Core partitions pipeline security across 37 dedicated autonomous modules, conceptually categorized by their operational domain:

* **Foundational Integrity & Defense**:
  * *Samson Option (Fifth Seal)*: Emergency protocol isolation and state purging upon unrecoverable compromise.
  * *Workflow Guard*: Absolute workflow definition and tampering verification.
  * *Chaos Engineering Matrix (Lucifer Rebellion)*: Continuous resilience validation against synthetic systemic failures.
  * *Cryptographic Enclaves*: Hardware-level signature auditing and TEE runtime memory protection.

* **Audit & Verification Layer**:
  * Granular detection modules handling replay defense, logical concealment prevention, canary data leaks, and spatial runtime consistency.
  * Semantic drift detection to maintain alignment across multiple AI evaluation models.

* **Slashing & Finality**:
  * Automated state slashing and kill-switch orchestration under protocol violation.
  * *Throne of Ataraxia*: Complete state sanitization returning environments to a pristine baseline.

---

## Quick Start & Verification

```bash
# Clone the protocol repository
git clone [https://github.com/anjo-da-maquina/Anjo-Core.git](https://github.com/anjo-da-maquina/Anjo-Core.git)

# Navigate and install dependencies
cd Anjo-Core
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install anjo-core

# Run the angelic validation suite locally
python -m anjo_core.run_audit
