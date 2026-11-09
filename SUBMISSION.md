# EcoClaim v2 — Portal submission (verified Studionet)

**Proposed category:** Developer → Intelligent Contracts

**Proposed title:** EcoClaim — Validator-Agreed Quantitative Green-Claim Auditor

**Description:** EcoClaim is a GenLayer Intelligent Contract for auditing the arithmetic of environmental marketing percentages against publicly committed, self-reported measurements. A report permanently records its environmental metric, baseline period, current period, quantities, and marketed reduction claim. Independent GenLayer validators extract one bounded integer percentage from the untrusted statement. The contract itself computes the measured percentage change using integer basis points and rejects overstatements through deterministic arithmetic. Unquantified statements never receive a positive result. Unlike text-versus-text environmental claim classification, the contract never delegates its final decision to AI: only the semantic number extraction needs consensus. It provides reproducible public numeric receipts with author authorization, replay prevention, bounded values, and explicit non-certification of self-reported measurements.

**Repository:** https://github.com/maho0638/EcoClaim

**Proof 1 — Required GenLayer Explorer Contract:** https://explorer-studio.genlayer.com/address/0x9880014774FfD413F434fd4849A87e819e4A8E35

**Proof 2 — Required GitHub Repository:** https://github.com/maho0638/EcoClaim

**Proof 3 — Successful public Studionet transactions and AI consensus:** https://github.com/maho0638/EcoClaim/actions/runs/42618104339

**Proof 4 — SDK tests and GenVM lint:** https://github.com/maho0638/EcoClaim/actions/runs/42615521793

**Verified outcome:** 25% claimed vs 25% calculated = NOT_OVERSTATED_VS_INPUTS; 40% claimed vs 25% calculated = OVERSTATED_VS_INPUTS. Both were read back from the real v2 contract. No mainnet deployment or environmental certification is claimed.

**Deployed code revision:** `575cb1048844b2df99b2d4dc844bc8691a12a206`.

**Note:** Portal submission must be done by the user; no submission has been sent automatically.
