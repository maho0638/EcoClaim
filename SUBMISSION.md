# EcoClaim — GenLayer Portal submission

**Category:** Developer → Intelligent Contracts

**Proposed title:** EcoClaim — Environmental Marketing Consistency Consensus

**Description:**

EcoClaim is a GenLayer Intelligent Contract that compares environmental marketing claims with the evidence excerpts disclosed by their authors. Each submission includes a product, measurable or qualitative claim, its scope, and supporting text. If no evidence is supplied, a deterministic NO_EVIDENCE result prevents an ungrounded positive outcome. Otherwise, independent validators compare the exact AI assessment: CONSISTENT, CONFLICTING, or UNCLEAR. Public immutable receipts, submitter-only one-time review, strict input limits, duplicate prevention and schema-checked AI output provide transparent decision records. This is a useful screening primitive for environmental marketing and does not falsely claim certified impact or independent document authentication. Source code and GenLayer SDK/GenVM test evidence are available in the repository.

**Repository:** https://github.com/maho0638/EcoClaim

**Proof status:** Real Studionet deployment and state read-back verified; exact links below.

## Verified public Studionet deployment — 9 November 2026

**Mandatory evidence — GitHub Repository**
https://github.com/maho0638/EcoClaim

**Mandatory evidence — GenLayer Explorer Contract**
https://explorer-studio.genlayer.com/address/0x34Fe69D0b9fd80Bceb3379E3e3A8Bf8AE58b82Fd

**Live end-to-end CI evidence**
https://github.com/maho0638/EcoClaim/actions/runs/42606522178

**Successful SDK and GenVM lint checks**
https://github.com/maho0638/EcoClaim/actions/runs/42606206539

**Observed on-chain result:** `NO_EVIDENCE and CONSISTENT`

- No-evidence registration transaction: `0x358f8e2b3f15f90a19f149d8fe6070d839255d9133783bd66560be00fb7963d1`
- No-evidence review transaction: `0x2a7f1db6767fb60946b63732361a0ad9c7bc36b91931e938fd6dfb05679ad46e`
- Evidence registration transaction: `0xb156767e63d6424167e4057950fc238d013587da6c9592092deba15ad5fc10ad`
- AI review transaction: `0xa2ac3cc95e936537cd6a66420238dc630b55f7a92984c35a14af08b2dac944b2`

Only public Studionet was used, not mainnet. No Portal submission is performed by this repository.
