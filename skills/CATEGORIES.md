# Skill Categories

Skills are stored **flat** (one directory per skill: `skills/<name>/SKILL.md`). Grouping is encoded in the **name prefix** — this file is the index. Invocation differs per tool: **Claude Code** loads them as the `harness` plugin (`harness:<name>`); **Codex** reads `skills/<name>/SKILL.md` by path; **Antigravity** uses the `.agent/` workflows (`/harness-*`).

**Total: 1,059 skills** (40 original + 1,019 from community repos)

---

## Original Harness Skills (prefix-based)

| Group | Prefix | Default model-tier | Skills |
|---|---|---|---|
| **Workflows** — multi-agent orchestrators (entry points) | `workflow-` | strong | workflow-intake, workflow-bootstrap, workflow-onboard, workflow-feature, workflow-bugfix, workflow-prototype, workflow-qa, workflow-release-prep, workflow-review-deep |
| **Planning** — turn an idea into spec, backlog, and skeleton | `plan-` | strong | plan-architecture-agent, plan-us-backlog-generator, plan-project-skeleton-generator |
| **Development** — write the code, by component type | `dev-` | strong | dev-be-developer, dev-fe-developer, dev-cli-tool-developer, dev-batch-developer, dev-db-designer, dev-go-developer, dev-js-ts-developer, dev-design-patterns, dev-system-design, dev-detailed-design |
| **Quality** — review, test, and harden changes | `check-` | strong | check-code-review, check-security-review, check-pr-review, check-qa, check-test-gen, check-refactor, check-ba-evaluator |
| **Delivery** — commit, PR, release, deploy, package | `ship-` | **fast** (except ship-release/ship-deploy → strong) | ship-commit-msg, ship-pr-create, ship-deploy, ship-release, ship-mcp-build |
| **Core** — everyday single-agent dev tasks | `core-` | **fast** for core-file-ops; strong for rest | core-explain, core-explore, core-fix, core-feature, core-prototype, core-file-ops |

---

## Community Skills (from downloaded repos)

Sources: [anthropics/skills](https://github.com/anthropics/skills) · [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) · [theneoai/awesome-skills](https://github.com/theneoai/awesome-skills)

### 🔧 Languages & Runtime Pros

| Skill | Source |
|---|---|
| python-pro | jeffallan |
| typescript-pro | jeffallan |
| javascript-pro | jeffallan |
| golang-pro | jeffallan |
| rust-engineer | jeffallan |
| java-architect | jeffallan |
| cpp-pro | jeffallan |
| csharp-developer | jeffallan |
| kotlin-specialist | jeffallan |
| swift-expert | jeffallan |
| php-pro | jeffallan |
| sql-pro | jeffallan |
| r-statistics-expert | theneoai |

### 🌐 Web Frameworks

| Skill | Source |
|---|---|
| react-expert, react-native-expert | jeffallan |
| angular-architect | jeffallan |
| vue-expert, vue-expert-js | jeffallan |
| nextjs-developer | jeffallan |
| django-expert | jeffallan |
| fastapi-expert | jeffallan |
| spring-boot-engineer | jeffallan |
| rails-expert | jeffallan |
| laravel-specialist | jeffallan |
| nestjs-expert | jeffallan |
| dotnet-core-expert | jeffallan |
| wordpress-pro | jeffallan |
| shopify-expert | jeffallan |
| flutter-expert | jeffallan |
| frontend-design | anthropic |

### ☁️ Cloud & Infrastructure

| Skill | Source |
|---|---|
| aws-cloud-expert, azure-cloud-expert, gcp-cloud-expert | theneoai |
| cloud-architect | jeffallan |
| docker-expert | theneoai |
| kubernetes-expert, kubernetes-specialist | theneoai / jeffallan |
| helm-expert, istio-servicemesh-expert | theneoai |
| terraform-expert, terraform-engineer | theneoai / jeffallan |
| ansible-expert, pulumi-expert | theneoai |
| vercel-expert, cloudflare-expert | theneoai |

### 🗄️ Databases & Data Platform

| Skill | Source |
|---|---|
| postgresql-expert, postgres-pro | theneoai / jeffallan |
| mysql-expert, mongodb-expert, redis-expert | theneoai |
| elasticsearch-expert, clickhouse-expert, duckdb-expert | theneoai |
| database-optimizer | jeffallan |
| kafka-expert, spark-expert, spark-engineer | theneoai / jeffallan |
| airflow-expert, flink-expert, dbt-expert, lakehouse-expert | theneoai |

### 🤖 AI / ML

| Skill | Source |
|---|---|
| pytorch-expert, tensorflow-expert, sklearn-expert | theneoai |
| huggingface-expert, langchain-expert, llama-index-expert | theneoai |
| cuda-expert, wandb-expert, mlflow-expert | theneoai |
| llm-serving-expert, llm-training-engineer | theneoai |
| rag-architect, ml-pipeline, fine-tuning-expert | jeffallan |
| prompt-engineer | theneoai |

### 🔒 Security

| Skill | Source |
|---|---|
| security-reviewer, secure-code-guardian | jeffallan |
| security-engineer, ai-security-engineer | theneoai |
| container-security-expert, vault-secrets-expert | theneoai |
| nmap-expert, burpsuite-expert, metasploit-expert | theneoai |
| incident-responder, threat-intelligence-analyst | theneoai |
| privacy-computing-engineer, data-security-officer | theneoai |

### 📊 Observability & SRE

| Skill | Source |
|---|---|
| prometheus-expert, grafana-expert | theneoai |
| datadog-expert, elk-stack-expert | theneoai |
| opentelemetry-expert, pagerduty-expert | theneoai |
| monitoring-expert, sre-engineer | jeffallan |
| chaos-engineer | jeffallan |

### 🚀 CI/CD & Delivery

| Skill | Source |
|---|---|
| github-actions-expert | theneoai |
| gitlab-cicd-expert | theneoai |
| jenkins-expert | theneoai |
| devops-engineer | theneoai |

### 🏗️ Architecture & Design

| Skill | Source |
|---|---|
| architecture-designer | jeffallan |
| microservices-architect, graphql-architect | jeffallan |
| api-designer | jeffallan |
| software-architect, system-architect | theneoai |
| architecture-review | theneoai |

### 🧪 Testing & Quality

| Skill | Source |
|---|---|
| test-master | jeffallan |
| webapp-testing | anthropic |
| playwright-expert | jeffallan |
| tdd-workflow | theneoai |
| code-reviewer | jeffallan |
| code-documenter | jeffallan |

### 🐛 Debugging & Fix

| Skill | Source |
|---|---|
| debugging-wizard | jeffallan |
| debug-diagnose | theneoai |
| legacy-modernizer | jeffallan |

### 🛠️ Dev Workflows (theneoai)

| Skill | Description |
|---|---|
| tdd-workflow | Red-Green-Refactor, vertical slices |
| debug-diagnose | Structured 6-phase debugging |
| architecture-review | System architecture evaluation |
| issue-triage | Classify and prioritize issues |
| to-prd | Generate Product Requirements Docs |
| zoom-out | Big-picture analysis |

### 📦 Anthropic Official Skills

| Skill | Description |
|---|---|
| webapp-testing | Playwright web testing with helper scripts |
| skill-creator | Auto-generate new skills |
| mcp-builder | Build MCP servers |
| frontend-design | UI/UX design patterns |
| canvas-design | Canvas-based design |
| web-artifacts-builder | Build web artifacts |
| claude-api | Claude API integration |
| docx, pptx, xlsx, pdf | Document generation |
| algorithmic-art | Generative art |
| theme-factory | Theme generation |
| brand-guidelines | Brand identity systems |
| internal-comms | Internal communications |
| doc-coauthoring | Collaborative document editing |
| slack-gif-creator | Slack GIF creation |

### 👤 Persona Skills (theneoai — largest group)

Professional roles across 60+ domains including: full-stack-developer, backend-developer, frontend-developer, qa-engineer, data-engineer, data-scientist, ai-ml-engineer, mobile-app-developer, embedded-systems-engineer, site-reliability-engineer, and hundreds more across industries (finance, healthcare, education, manufacturing, etc.)

---

## Notes
- The prefix is **classification only** — every skill still runs independently (Claude Code: `harness:<name>`; Codex: by file path; Antigravity: `.agent/` workflows).
- Workflows drive the leaf skills; each `workflow-*/SKILL.md` lists the skills it uses and links to them.
- Tool-capability names used inside skills (ask-user, spawn-subagents, generate-image) are mapped per agent in [../resources/agent-tool-mapping.md](../resources/agent-tool-mapping.md).
- **Model-tier** (`fast` / `strong`) tells an orchestrator which model to spawn a skill's subagent on; see the model-tier section in [agent-tool-mapping.md](../resources/agent-tool-mapping.md). `strong` is the safe default — only the mechanical skills above default to `fast`, and any judgment step escalates to `strong` when in doubt.
- **Duplicate handling**: When multiple repos had the same skill name, the version with more content + supporting files (references/, scripts/) was kept. Existing harness skills were never overwritten.
