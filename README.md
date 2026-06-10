# NexaEdge Network

<div align="center">

**A protocol to aggregate idle smartphone compute into a distributed edge AI inference network.**

[![Waitlist](https://img.shields.io/badge/Waitlist-Open-22C55E?style=for-the-badge)](https://nexaedge.streamlit.app)
[![Node Portal](https://img.shields.io/badge/Node_Portal-Live-22C55E?style=for-the-badge)](https://nexaedge-web-port.streamlit.app)
[![Solana](https://img.shields.io/badge/Solana-SPL_Token-9945FF?style=for-the-badge)](https://solana.com)
[![Stage](https://img.shields.io/badge/Stage-Pre--Seed_Concept-FF6B35?style=for-the-badge)](#)

</div>

-----

## The Problem

6.8 billion smartphones exist worldwide. Each contains a dedicated Neural Processing Unit (NPU) capable of running state-of-the-art small language models. Every night, they sit on charge doing nothing.

Meanwhile, enterprise AI inference costs $2–4/hr on H100 GPUs, latency exceeds 150ms across datacenter hops, and data sovereignty regulations make cloud AI legally problematic in many markets.

**The compute already exists. No protocol has been built to use it.**

-----

## What NexaEdge Does

NexaEdge is a three-layer protocol:

```
AI Buyers  →  Solana BFT Settlement  →  Device Node Cluster
(pay NEXA)     (verify + reward)         (NPU executes inference)
```

|Layer       |Component    |Function                                           |
|------------|-------------|---------------------------------------------------|
|Demand      |AI Buyers API|Submit inference tasks, pay in NEXA                |
|Coordination|Solana SPL   |BFT consensus, ZK verification, reward distribution|
|Supply      |Device Nodes |WASM sandbox, NPU execution, thermal guard         |

**Design targets (unproven at this stage):**

- Sub-5ms edge inference latency
- GDPR-native by architecture (data never leaves device)
- Hardware fingerprint + ZK proof Sybil resistance
- 39°C thermal ceiling — automatic task pause to protect hardware

-----

## Current Status

> ⚠️ **Pre-Seed Concept Demo** — No production network is running. All node simulation figures are randomly generated for illustration. Real node heartbeat infrastructure is operational for testing.

|Component                     |Status                        |
|------------------------------|------------------------------|
|Protocol Architecture         |✅ Finalized                   |
|Waitlist Portal               |✅ Live                        |
|Node Registration System      |✅ Live                        |
|Browser-based Heartbeat Client|✅ Live                        |
|Admin Dashboard               |✅ Live                        |
|NEXA Token (Solana SPL)       |✅ Minted — not yet distributed|
|WASM Runtime (iOS/Android)    |🔨 Q3 2026                     |
|SLM Inference on Device NPU   |🔨 Q3 2026                     |
|Closed Beta (1,000 nodes)     |🔨 Q4 2026                     |
|Public Mainnet                |🔨 Q1 2027                     |

-----

## NEXA Token

100,000,000 NEXA tokens have been minted on Solana.

**Contract:** `D7h9MvFDkVxPYeJwSTcE7VkKXo6mygCHYph36P8oeic2`

Tokens are **not yet in public circulation**. Early waitlist members are eligible for the node airdrop snapshot at mainnet launch.

> This is not a financial instrument or investment offer. Token distribution rules will be defined at mainnet.

-----

## Repository Structure

```
nexaedge/
├── homepage.py          # Main public-facing app (waitlist, sim, market)
├── admin_console.py     # Password-protected admin dashboard
├── user_portal.py       # Node portal (login, node registration, heartbeat)
├── node_client.py       # Python heartbeat client (desktop)
├── requirements.txt
└── .streamlit/
    └── secrets.toml     # Supabase credentials (not committed)
```

-----

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Database:** Supabase (PostgreSQL)
- **Auth:** Supabase OTP (email-based, no password)
- **Blockchain:** Solana SPL
- **Heartbeat:** Browser JS → Supabase REST API
- **Hosting:** Streamlit Cloud

-----

## Roadmap

|Phase     |Timeline|Milestone                                 |
|----------|--------|------------------------------------------|
|**NOW**   |Q2 2026 |Concept validation, waitlist, token minted|
|**NEXT**  |Q3 2026 |WASM sandbox MVP, 50-device internal alpha|
|**BETA**  |Q4 2026 |1,000-node closed beta, Solana testnet    |
|**LAUNCH**|Q1 2027 |Public mainnet, 100K node target          |
|**SCALE** |2027+   |ZK-ML live, laptop/IoT expansion, Series A|

-----

## Links

|             |                                                                          |
|-------------|--------------------------------------------------------------------------|
|🌐 Main App   |[nexaedge.streamlit.app](https://nexaedge.streamlit.app)                  |
|📡 Node Portal|[nexaedge-web-port.streamlit.app](https://nexaedge-web-port.streamlit.app)|
|🐦 X / Twitter|[@nexaedge_](https://x.com/nexaedge_)                                     |
|📢 Telegram   |[t.me/NexaEdge7](https://t.me/NexaEdge7)                                  |
|🎵 TikTok     |[@nexaedge7](https://www.tiktok.com/@nexaedge7)                           |
|📸 Instagram  |[@nexaedge__](https://www.instagram.com/nexaedge__)                       |
|👥 Facebook   |[NexaEdge](https://www.facebook.com/share/18eXN6P3Ge/)                    |
|📧 Email      |[contact@nexaedge.org](mailto:contact@nexaedge.org)                       |

-----

## Disclaimer

NexaEdge is at pre-seed concept stage. All technical claims are design targets, not guarantees. No investment contract has been formed. Joining the waitlist does not create any legal right or entitlement to tokens, equity, or financial instruments.

© 2026 NexaEdge Network. All rights reserved.
