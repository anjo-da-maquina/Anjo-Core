# Anjo-Core : GenAI-Driven Autonomous Testing & Zero-Trust Governance

> **Protocol "Anjo da máquina": Self-Healing CI/CD Pipeline**  
> Architect/Maintainer: **Anjo Machina**  
> *Language: English | [日本語](#japanese)*

---

## Vision

In the era of Generative AI, code is written faster than human engineers can verify. **Anjo-Core** is a completely free, open-source, autonomous zero-trust testing framework designed for mission-critical software development environments.

Unlike traditional passive testing tools that merely report errors, Anjo-Core operates as an autonomous audit layer within your CI/CD environment. It eliminates manual QA overhead, enforces cryptographic integrity, executes autonomous remediation, and maintains absolute operational stillness (**Ataraxia**) within the system.

---

## Core Features & Design Philosophy

* **Automated Requirements Parsing (GenAI Integration)**: Utilizes the Model Context Protocol (MCP) and multi-LLM consensus to dynamically generate robust test suites from functional requirements (Excel / YAML).
* **Zero-Trust CI/CD Enforcement**: Natively integrated into GitHub Actions to block unauthorized schema drift, replay attacks, and unverified AI hallucinations.
* **Deep Traceability**: Provides comprehensive audit logs, generating tamper-proof JUnit XML compliance reports and cryptographic integrity records via Zero-Knowledge Proofs (ZKP).
* **Autonomous Remediation**: Executes autonomous recovery sequences upon anomaly detection before resorting to a fail-closed (forced termination) state.

---

## Architecture: 37 Autonomous Agents (The Angels)

Anjo-Core divides pipeline security into 37 autonomous modules, governing the following domains:

* **Foundational Integrity & Defense**:
  * *The Samson Option (The Fifth Seal)*: Emergency protocol isolation and total state destruction upon unavoidable compromise.
  * *Workflow Bastion*: Tamper detection and absolute integrity verification for workflow definitions.
  * *Chaos Engineering Substrate (Lucifer's Rebellion)*: Continuous resilience validation via intentional system failure injection.
  * *Cryptographic Enclave*: Hardware-level signature auditing and TEE runtime memory protection.

* **Audit & Verification Layer**:
  * High-precision detection modules monitoring replay attack defense, logic obfuscation prevention, canary data leak detection, and spatial runtime consistency.
  * Consensus layer detecting semantic drift (interpretation variance) across multiple AI evaluation models.

* **Liquidation & Finality**:
  * Automatic state slashing and kill-switch activation upon protocol violation.
  * *Throne of Ataraxia*: Purges the environment completely and forces a regression to a pure initial state.

---

## Quick Start

```bash
# Clone the protocol
git clone [https://github.com/anjo-da-maquina/Anjo-Core.git](https://github.com/anjo-da-maquina/Anjo-Core.git)

# Install dependencies and set up the environment
cd Anjo-Core
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install anjo-core

# Execute the local audit suite
python -m anjo_core.run_audit
```

---

## Global Compliance

Anjo-Core bridges the gap between advanced software engineering and absolute system sovereignty, delivering fully autonomous DevSecOps governance designed to meet rigorous enterprise standards.
