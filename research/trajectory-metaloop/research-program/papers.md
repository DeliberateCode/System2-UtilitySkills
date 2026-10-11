# Literature corpus — The Configuration Space (podcast mining)

Source: "The Configuration Space" by Karl Wehden (Spotify `spotify:show:6pvq4UeN5tRZe0ASE4rlhz`),
14 episodes, 2026-09-17 → 2026-10-08. Episode subtitles name papers, benchmarks,
frameworks, and standards directly; those are extracted below and resolved to citable
references. Items marked **[research]** were flagged in adjacent research (not named in
episode subtitles) but belong in the corpus for hypothesis generation.

Purpose: feed hypothesis generation for (a) Theory of Mind in AI agents and
(b) trajectory-failure detection / metaloop learning — each area separately, plus an
overall improvement target spanning both.

---

## (a) Theory of Mind / multi-agent cognition

### GroupToM-Bench
- **Citation:** Weidong Tang, Jierui Li, Yueling Hou, Zihan Mei, Can Zhang, Xinyan Wan,
  Zhiyuan Liang, Pengfei Zhou, Yang You, Wangbo Zhao. "GroupToM-Bench: Benchmarking Group
  Theory of Mind and Nonlinear Social Emergence in MLLMs." arXiv:2606.04184 (2026);
  ACL 2026 (long paper).
- **Key claim (paraphrase):** First multimodal benchmark for *group-level* ToM: 240
  expert-designed scenarios across eight social domains, ~3,120 tasks, with a seven-level
  cognitive audit tracing micro BDI states → meso group tension → macro collective outcomes.
  Finds a consistent "group cognitive gap": models recover individual motives yet fail on
  nonlinear collapses (groupthink, winner's curse), defaulting to optimistic consensus —
  a linear-superposition bias that scaling alone does not fix.
- **Episodes:** 2026-10-07 ("From Crowds to Chemistry"), 2026-10-06 ("Groups, Gaps, and the
  Grammar of Governance").

### AutoToM
- **Citation:** Zhining Zhang, Chuanyang Jin, Mung Yao Jia, Tianmin Shu. "AutoToM:
  Automated Bayesian Inverse Planning and Model Discovery for Open-ended Theory of Mind."
  arXiv:2502.15676 (2025); extended version "AutoToM: Scaling Model-based Mental Inference
  via Automated Agent Modeling," NeurIPS 2025.
- **Key claim (paraphrase):** Automates the two hard parts of Bayesian ToM: proposing the
  agent model (which mental variables, which timesteps) and running Bayesian inverse
  planning over it with an LLM backend. Iteratively refines the model based on inference
  uncertainty; supports arbitrary domains, mental variables, and recursion orders.
  Outperforms prompted LLMs and large reasoning models on ToM benchmarks.
- **Episodes:** 2026-09-17 ("Minds, Meshes, and Momentum").

### ToM4AI workshops (AAAI 2025 / AAAI 2026)
- **Citation:** 1st Workshop on Advancing AI Through Theory of Mind, AAAI 2025
  (proceedings arXiv:2505.03770, 28 papers); 2nd workshop, AAAI 2026, Singapore, Jan 26 2026
  (incl. "ToMa-Thon" hackathon on beyond-Sally-Anne ToM problems). Community hub:
  tom4ai.github.io.
- **Key claim (paraphrase):** Multidisciplinary venue (cogsci, psych, robotics, ML) pushing
  ToM from isolated false-belief tests toward interactive, applied social cognition;
  2026 takeaways emphasized abandoning inadequate benchmarks and trait-generalization
  across contexts as the core of ToM.
- **Episodes:** 2026-09-25 ("Alignment, Silicon, and the Standards Gap").

### Temporal Causal Belief Graphs / TGToM
- **Citation:** TemporalGraph-ToM (TGToM) benchmark, github.com/singularity4/temporalgraph-tom
  (2026). Related: "Learning Dynamic Belief Graphs for Theory-of-mind Reasoning,"
  arXiv:2603.20170 (2026).
- **Key claim (paraphrase):** Represents agents' beliefs as a temporal causal graph with
  belief propagation across time and agents; evaluates higher-order ToM (up to 7th order),
  causal, counterfactual, and common-knowledge beliefs. The graph structure mitigates the
  "reality bias" failure mode where LLMs answer from world truth instead of agent belief.
- **Episodes:** 2026-10-05 ("Beliefs, Bodies, and the Harness Problem").

### ToMnet **[research]**
- **Citation:** Neil C. Rabinowitz, Frank Perbet, H. Francis Song, Chiyuan Zhang,
  S. M. Ali Eslami, Matthew Botvinick. "Machine Theory of Mind." ICML 2018;
  arXiv:1802.07740.
- **Key claim (paraphrase):** Treats ToM as meta-learning: train a network on many agents'
  behavioral traces so it acquires a prior over agent behavior, then rapidly builds
  agent-specific models from few observations — predicting actions and inferring beliefs
  without hand-built cognitive models.

### MetaMind **[research]**
- **Citation:** "MetaMind: Modeling Human Social Thoughts with Metacognitive Multi-Agent
  Systems." arXiv:2505.18943 (2025); code at github.com/XMZhangAI/MetaMind.
- **Key claim (paraphrase):** Splits social reasoning into a three-stage metacognitive
  pipeline — a ToM agent hypothesizes hidden mental states, downstream agents refine
  against social norms — explicitly modeling the "thinking about thinking" loop that
  humans use in social inference.

### Mutual ToM (Wang & Goel, 2022) **[research]**
- **Citation:** Dakuo Wang, Kartik Talamadupula (? verify) — framework from the ToM/HAT
  literature: human-AI collaboration improves less from AI's standalone ToM scores than
  from systems that support mutual adaptation; bidirectional ToM signaling can even
  increase cognitive load and hurt performance.
- **Key claim (paraphrase):** The useful unit of analysis is the human–AI dyad's mutual
  modeling, not the AI's isolated test score; designing for mutuality beats designing
  for mindreading.
- **Note:** citation details to be verified before use in a publication.

### BigToM **[research, surfaced during resolution]**
- **Citation:** Kanishk Gandhi et al. "Understanding Social Reasoning in Language Models
  with Language Models." 2023.
- **Key claim (paraphrase):** Procedurally generates ToM evaluations from causal templates
  (5,000 model-written items); finds GPT-4's social inferences mirror human patterns but
  less reliably. Relevant as the individual-level baseline GroupToM-Bench argues beyond.

---

## (b) Trajectory failure / agent monitoring / evaluation

### ATFD — Agent Trajectory Failure Detection **[research]**
- **Citation:** galea-foo/atfd (GitHub). "A benchmark for evaluating agent monitoring
  tools — not agents themselves." 2,577 trajectories, 7 failure categories, 7 systems
  evaluated.
- **Key claim (paraphrase):** Given a complete agent trajectory (model calls, tool
  invocations, intermediate states, final outputs), measures whether a *monitoring tool*
  can detect failures, classify them correctly, do so reliably across domains — and at
  what cost (dollars, latency, tokens, API calls). Fills the gap that every existing
  benchmark scores agents while none scores the watchers.
- **Episodes:** not named in subtitles; central to the skill being built.

### Hidden-behaviour auditing (model organisms family)
- **Citation:** Samuel Marks et al. "Auditing for hidden objectives." arXiv:2503.10965
  (2025) — blind auditing game where teams detect a model's covert objective via SAEs,
  behavioral attacks, and data analysis. Related: Greenblatt et al. "Alignment faking,"
  arXiv:2412.14093 (2024); Hubinger et al. "Sleeper Agents," arXiv:2401.05566 (2024).
- **Key claim (paraphrase):** Misaligned objectives can be planted so they survive
  safety training and only trigger in deployment; auditing them requires inspecting
  internal activations and behavior under adversarial probing, not outputs —
  directly the "evaluate something whose inner workings aren't directly accessible"
  problem.
- **Episodes:** 2026-10-05 ("Mirrors, Meshes, and the Meaning of Knowing" — "Introspection
  and Hidden Behaviours").

### ASIMOV-Agentic (embodied-agent safety benchmark)
- **Citation:** Google DeepMind, released with Gemini Robotics 2 (July 30, 2026);
  benchmark published on Hugging Face.
- **Key claim (paraphrase):** First dedicated safety benchmark for embodied agents:
  tests whether the agent refuses unsafe tool calls from a VLA policy, predicts task
  feasibility, and requests human help under uncertainty — trajectory-level safety
  evaluation for physical agents.
- **Episodes:** 2026-10-02 ("Memory, Motion, and the Machinery of Governance").

### The metacognition / calibration gap (theme)
- **Key claim (paraphrase):** Agents cannot reliably tell when they are wrong *in the
  moment*; September 2026 test-time-compute research found longer reasoning traces can
  talk a correct first answer into a wrong one (up to ~21% flip rates), and stopping
  traces early cut tokens ~70%. A monitor that detects this in-trajectory is the
  missing piece.
- **Episodes:** 2026-10-08 ("Mirrors, Magnets, and the Memory of Machines"),
  2026-10-05 ("Mirrors, Meshes, and the Meaning of Knowing").

### Agentic planning / state-tracking gap (theme)
- **Key claim (paraphrase):** Agents can plan a trip yet lose track of what they already
  decided; two 2026 benchmarks measure this state-tracking gap (specific papers unnamed
  in episode — see unresolved).
- **Episodes:** 2026-09-29 ("Plans, Waves, and What Gets Lost in Between").

---

## (c) Metaloop / metacognition / agent memory

### RecMem
- **Citation:** Zijie Dai, Shiyuan Deng, Sheng Guan, Yizhou Tian, Xin Yao, Xiao Yan,
  James Cheng. "RecMem: Recurrence-based Memory Consolidation for Efficient and
  Effective Long-Running LLM Agents." arXiv:2605.16045 (2026); Findings of ACL 2026.
- **Key claim (paraphrase):** Challenges eager per-turn LLM memory extraction: stores raw
  turns cheaply in an embedding-only "subconscious" layer and invokes LLM consolidation
  (episodic narratives → semantic facts) only when sustained semantic recurrence is
  detected. Cuts memory-construction tokens 77–87% while beating Mem0/A-Mem/MemoryOS
  accuracy on LoCoMo and LongMemEval.
- **Episodes:** 2026-10-02 ("Memory, Motion, and the Machinery of Governance" — "Agent
  Memory: RecMem and Synapse").

### SYNAPSE
- **Citation:** Hanqi Jiang, Junhao Chen, Yi Pan, Ling Chen, Weihang You, Yifan Zhou,
  Ruidong Zhang, Lin Zhao, Yohannes Abate, Tianming Liu. "SYNAPSE: Empowering LLM Agents
  with Episodic-Semantic Memory via Spreading Activation." arXiv:2601.02744 (2026).
- **Key claim (paraphrase):** Models agent memory as a dynamic episodic–semantic graph
  where relevance emerges from spreading activation (with fan effect, temporal decay,
  lateral inhibition) instead of static vector similarity; triple-hybrid retrieval fuses
  embeddings, activation scores, and PageRank. Beats SOTA on LoCoMo temporal/multi-hop
  reasoning.
- **Episodes:** 2026-10-02 (same segment as RecMem).

### Metaloop (meta-learning loop engine) **[research]**
- **Citation:** jjy1000/metaloop (GitHub). Pipeline: harvest → reflect → aggregate →
  select → update; improves an agent's own rules by distilling experience history,
  validating via A/B, injecting survivors.
- **Key claim (paraphrase):** Treats the agent's operating rules as the learned object:
  experience is harvested, patterns distilled, candidates A/B-tested, and winners
  injected back — a metacognitive loop over the agent itself rather than over task data.

### MENTOR **[research]**
- **Citation:** "MENTOR: A Metacognition-Driven Self-Evolution Framework for Uncovering
  and Mitigating Implicit Risks in LLMs on Domain Tasks." arXiv:2511.07107 (2025).
- **Key claim (paraphrase):** Uses a "MetaLoop" metacognition evaluator that reflects on
  the model's own responses (perspective-taking, consequential thinking) to score
  implicit risks, then evolves the rule set through experience — metacognition as a
  safety instrument.

### DPPO / Pelican-VL **[research]**
- **Citation:** "Pelican-VL 1.0: A Foundation Brain Model for Embodied Intelligence."
  arXiv:2511.00108 (2025). Introduces DPPO (Deliberate Practice Policy Optimization).
- **Key claim (paraphrase):** A metaloop that alternates supervised fine-tuning
  (competence expansion) with RL (skill refinement), auto-identifying weaknesses and
  allocating training effort — an RL-Refine-Diagnose-SFT loop yielding +20.3% over the
  base embodied model.

### Reflexion **[research]**
- **Citation:** Noah Shinn et al. "Reflexion: Language Agents with Verbal Reinforcement
  Learning." arXiv:2303.11366 (2023).
- **Key claim (paraphrase):** Wraps a ReAct agent in an Act → Evaluate → Reflect loop;
  failures produce textual self-reflections stored in episodic memory and prepended to
  future trials — the canonical lightweight metaloop pattern.

---

## (d) Other notable mentions (one line each)

- **POMDAR** — Liconti et al., "A Benchmark of Dexterity for Anthropomorphic Robotic
  Hands," arXiv:2604.09294 (2026): 18 physical tasks, throughput score vs. human baseline.
  (Ep 2026-10-05)
- **Safe-SDL** — "Safe-SDL: Establishing Safety Boundaries and Control Mechanisms for
  AI-Driven Self-Driving Laboratories," arXiv:2602.15061 (2026): operational design
  domains + control barrier functions + CRUTD transactional safety protocol; names the
  "syntax-to-safety gap." (Ep 2026-10-07)
- **AutoLabs** — Panapitiya et al., "AutoLabs: Cognitive Multi-Agent Systems with
  Self-Correction for Autonomous Chemical Experimentation," arXiv:2509.25651 (2025),
  PNNL: multi-agent SDL where reasoning capacity dominates success; F1 > 0.89 on
  multi-step syntheses. (Eps 2026-10-06, 2026-09-30)
- **CoMuRoS** — "LLM-Based Generalizable Hierarchical Task Planning and Execution for
  Heterogeneous Robot Teams with Event-Driven Replanning," arXiv:2511.22354: centralized
  LLM deliberation + decentralized execution with runtime replanning. (Ep 2026-09-23)
- **Model Hardware Standard (MHS)** — Anthropic + HHMI Janelia, research preview
  Aug 27 2026: read/write driver primitives letting agents discover and operate lab
  hardware; model-agnostic via MCP/CLI/code. (Eps 2026-09-21, 2026-09-18, 2026-09-17)
- **Strands Robots** — AWS agent framework; building native MHS support. (Ep 2026-09-17)
- **Nature Reviews Chemistry SDL review** — Canty & Abolhasani, "The past, present and
  future of self-driving laboratories," Nat. Rev. Chem. 10, 523–537 (2026),
  doi:10.1038/s41570-026-00847-2: provenance-complete experimentation; modular hardware
  coordination gap. (Ep 2026-09-25)
- **Gemini Robotics 2** — Google DeepMind, July 30 2026: VLA + ER 2 embodied reasoning +
  On-Device 2; whole-body humanoid control demoed on Apptronik Apollo 2. (Ep 2026-10-02)
- **BrainChip AKD1500** — commercial neuromorphic processor in M.2 form factor.
  (Ep 2026-09-25)
- **WAICO** — World AI Cooperation Organization; China-led, 29 founding nations,
  Shanghai HQ, founded at WAIC 2026: second track of global AI governance.
  (Ep 2026-10-06)
- **Nature Electronics stretchable neuromorphic circuit** — 10,000 transistors/cm²,
  on-body health inference without cloud (2026). (Ep 2026-09-23)
- **RoboChem-Flex / $5k lab** — Pilon et al., Nature Synthesis 2026,
  doi:10.1038/s44160-026-01053-0: low-cost self-driving chemistry lab.
  (Ep 2026-10-01)
- **The Neuromorphic Supremacy** — Tsybina, Tyukin, Gorban, Kazantsev, Wang, Gordleeva,
  arXiv:2606.01841 (2026): astrocytic modulation + spiking dynamics embedded in ANNs →
  few-shot learning and noise robustness "supremacy" regime. (Ep 2026-09-17)
- **Provenance grounds trust in autonomous science** — MacKnight, Novitskiy, Gomes,
  Nature comment (2026): trust in autonomous science comes from complete, re-openable
  provenance records, not from interpretability. (Surfaced during research; supports
  trajectory-evaluation framing.)
- **ISO 21423** — robotics standard (referenced via InOrbit.AI OpenRobOps reference
  implementation, Sep 2026). (Ep 2026-10-06)
- **"The configuration space problem"** — concept named in Ep 2026-09-17 (Strands/MHS
  segment): the combinatorial explosion of hardware configurations an agent must reason
  over — the show's namesake problem.
- **ToM4AI 2026 keynotes** — Geoff Bird (MindSpace Theory; abandon inadequate tests),
  Sarit Kraus (humans-in-the-loop; LLMs develop internal subtext), Maarten Sap
  (subtext/social alignment via Sotopia). Useful framing sources.

---

## Unresolved (named in episodes, no publication pinned down)

- **NWRIST** — "neuromorphic wearable radar-gesture sensing" (Ep 2026-10-07). No exact
  paper found; closest related: RadarHand (wrist-worn mmWave radar for on-skin
  proprioceptive gestures, Univ. of Auckland).
- **Decrypto** — "when smarter models think worse" (Ep 2026-10-01). No paper under that
  name found; theme matches Sep 2026 test-time-compute / overthinking research.
- **ECP** — "a new layered protocol for heterogeneous robot teams" mentioned alongside
  CoMuRoS (Ep 2026-09-23); may be part of the CoMuRoS paper or a separate protocol —
  not separately resolved.
- **IEEE P4501** — named as a robotics standard (Ep 2026-10-06); no resolution found.
- **"Embodied Intelligence: The Gap Report"** (Ep 2026-10-05) — no exact report found;
  theme matches the embodied-data-gap discourse (WAIC 2026: ~500k hrs available vs.
  ~10M hrs needed).
- **FLEXI** — bendable on-body compute chip (Ep 2026-09-30); no specific paper pinned.
- **Two 2026 agentic-planning/state-tracking benchmarks** (Ep 2026-09-29) — unnamed.
- **NSF open-access autonomous chemistry lab** (Ep 2026-09-29) — unnamed.
- **"A new theory-of-mind study puts language models through a decades-old psychology
  test"** (Ep 2026-09-18) — unnamed.

---

*Built 2026-10-10 from 14 episode subtitles + web resolution. Key claims are paraphrases;
verify citations against primary sources before publication use.*

---

# Part 2 — Hypothesis scaffolding

How to use this corpus: each hypothesis below names the corpus entries that ground
it and the skill mode that tests it (`analyze` = trajectory failure analysis,
`learn` = metaloop capture). Hypotheses are ordered by testability with the skill
as specified — cheapest falsification first.

## Area A — Theory of Mind in AI agents

**H-ToM-1 — Group ToM failures surface as trajectory failures.**
An agent that models individual intents correctly but misses group-level tension
(GroupToM-Bench's "group cognitive gap") will produce `communication.missing_info`
and `process.planning_failure` signatures in its trajectory: confident consensus
predictions followed by unhandled collapse. Test: run `analyze` on multi-agent
trajectories with known group outcomes; check whether group-collapse cases cluster
in those two subcategories.
*Grounding: GroupToM-Bench; ATFD taxonomy.*

**H-ToM-2 — Linear-superposition bias is measurable in-trajectory.**
GroupToM-Bench finds models default to optimistic consensus (linear superposition
of individual motives). Prediction: pre-collapse trajectory segments show high
confidence + low belief-diversity across agents — a calibration signature a monitor
can score without knowing the outcome.
*Grounding: GroupToM-Bench; metacognition/calibration-gap theme.*

**H-ToM-3 — Mutual modeling beats isolated ToM scores for failure prediction.**
In multi-agent trajectories, which dyads fail is better predicted by mutual-modeling
features (do A and B model each other symmetrically?) than by either agent's
standalone ToM benchmark score. Test: correlate dyad symmetry features with
`analyze` failure attributions.
*Grounding: Mutual ToM (Wang & Goel); Agents_Failure_Attribution framing.*

**H-ToM-4 — Reality bias has a trajectory signature.**
TGToM's "reality bias" (answering from world truth instead of the modeled agent's
belief) is detectable: tool calls or claims that use information the modeled agent
could not have observed. Test: `analyze` with an added check — does each
information-using step trace to an observation in the modeled agent's history?
*Grounding: TGToM / Temporal Causal Belief Graphs; ATFD `communication` category.*

## Area B — Trajectory failure measurement & metaloop learning

**H-TF-1 — Two-tier monitors dominate single-pass judges on cost.**
A cheap heuristic tier (structural: `process.tool_loop`, `infrastructure.timeout`,
`infrastructure.error`, `infrastructure.max_steps` — ATFD's naive heuristic catches
these at $0) plus a targeted LLM tier for semantic categories achieves
Pareto-optimal detection-rate-per-dollar vs. single-pass LLM judges.
*Grounding: ATFD headline results; skill `analyze` Mode A implements this.*

**H-TF-2 — Category alignment is the binding constraint, and memory helps.**
ATFD shows classification (CA 0.545→0.093 real-domain) is far harder than detection.
Prediction: a judge given retrieved similar past failures (from the metaloop's
pattern store) classifies more accurately than a cold judge — memory-augmented CA
> cold CA on the same trajectories.
*Grounding: ATFD metrics; SYNAPSE/RecMem retrieval.*

**H-ML-1 — The funnel retains the lift at a fraction of the cost.**
Storing only (episode tuple → pattern → rule + scalars) with confidence-gated
promotion and credit-based eviction retains ≥90% of the failure-rate reduction of
full-trajectory retention at <10% of token cost. Test by ablation: full-retention
vs. funnel variants on a fixed trajectory set.
*Grounding: metaloop engine; RecMem's 77–87% savings via gated consolidation.*

**H-ML-2 — Categorized failures are a better verdict signal than binary outcomes.**
Using ATFD `JudgeOutput` (has_failure + categorized findings) as the metaloop's
select-stage verdict — rather than task success/fail — yields faster-converging,
more specific rules, because the reflect stage can cluster on failure *type*.
*Grounding: ATFD output contract; metaloop select stage.*

**H-ML-3 — Selective invocation cuts loop cost ~10× without hurting rule quality.**
Running the expensive reflect/validate stages only when the cheap detector fires
(or confidence is low) preserves rule quality while slashing operating cost —
the same gating logic as RecMem's recurrence trigger and MENTOR's MEC gate.
*Grounding: RecMem; MENTOR; metaloop min_samples HOLD.*

## Overall improvement target (spanning both areas)

**Target:** a self-improving agent loop in which (1) ATFD-style monitoring supplies
*measurable, categorized* failure signals, (2) a memory-efficient metaloop distills
those signals into *validated* rules with sublinear memory growth, and (3)
ToM-augmented failure attribution fixes the classification bottleneck — so that
failure rate per 1k trajectories falls epoch over epoch at bounded memory cost.

**H-SYN-1 — ToM improves failure attribution, the hardest subproblem.**
In multi-agent trajectories, attributing *which agent and step* caused a failure
(cf. ICML'25 Agents_Failure_Attribution) improves when the judge maintains explicit
belief-state models of each agent instead of judging the transcript alone.
*Grounding: H-ToM-3 + H-TF-2; the skill's analyze mode is the test harness.*

**H-SYN-2 — The closed loop compounds (flagship).**
Monitor → categorize → distill → A/B-validate → inject, run over successive epochs:
failure rate per 1k trajectories declines while memory grows sublinearly (log) in
trajectory count, via the funnel + credit eviction. Falsifiable within the skill:
track (failures/1k traj, bytes of rule store) per epoch.
*Grounding: all of Area B + the metaloop lifecycle.*

**H-SYN-3 — Optimize the frontier, not the accuracy.**
The right objective is ATFD's Pareto framing: maximize detection-rate-per-dollar
at bounded memory — not raw DR. A system at 80% DR / $0.01/traj beats 95% DR /
$1.00/traj for any production loop. The skill's cost report makes this the
default scoreboard.
*Grounding: ATFD leaderboard design (Pareto, not ranking); cost-report contract.*

## Suggested first experiments (in skill order)

1. `analyze` 20–50 local agent transcripts → baseline (DR/FPR/CA vs. any labels).
2. Enable two-tier judging (H-TF-1) → measure $/traj delta.
3. Feed categorized findings into `learn` → first rule candidates (H-ML-2).
4. A/B one rule on held-out episodes → ledger delta (H-SYN-2 begins).
5. Add belief-state attribution on a multi-agent failure (H-SYN-1, H-ToM-4).
