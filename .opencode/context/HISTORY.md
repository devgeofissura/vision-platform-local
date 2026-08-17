---
name: history
description: Histórico de mudanças, decisões e adições do kit (sempre atualizado a cada alteração)
type: decisions
version: 0.1.0
author: devtiagoabreu
---

# Histórico do Kit

## O que é

Este arquivo é o **histórico de contexto** do kit. A cada mudança relevante
(nova persona, nova skill, novo template, decisão de arquitetura), uma entrada
é adicionada aqui para que a IA sempre tenha contexto do que foi criado e por
quê.

## Entradas

### 2026-08-10 — Educação, cultura, comércio, direito, política e qualidade

- **Adicionadas 39 personas** em novas categorias: `education` (11 professores
  + alfabetização + vestibular), `music` (músico, método Suzuki), `arts`
  (maquiador, estilista, cabeleireiro, bailarina, coreógrafo, roteirista),
  `sports` (personal-trainer), `automotive` (mecânico, mecânico de avião),
  `commercial` (tecelagem, plásticos, e-commerce, relacionamento com cliente),
  `languages` (professor de idiomas), `ai` (especialista em LLMs gratuitos) e
  nas existentes `humanities` (geopolítica, análise política, advogado
  trabalhista, criminalista), `marketing` (marketeiro político, criador de
  jingles políticos), `planner` (orquestrador).
- **Adicionadas 35 skills** em novas categorias: `education` (planejamento de
  aulas, métodos, avaliação, evidências, vestibular), `music`, `arts`, `sports`,
  `automotive`, `commercial`, `languages` e `ai` (LLMs gratuitos), além de
  `health/nutrition` e `humanities` (geopolítica, análise política, marketing
  político, jingles políticos).
- **Orquestrador:** novo agente `planner/orquestrador` que planeja, delega aos
  agentes certos, mostra a procedência das ferramentas e pergunta ao usuário.
- **Procedência (provenance):** frontmatter com `provenance` (fonte, URL,
  licença MIT, data de verificação) em todos os 208 assets; script
  `scripts/add-provenance.sh` + índice `context/provenance.md`.
- **Módulo de testes de qualidade:** `tests/quality/test-asset-quality.sh`
  cobrindo 6 dimensões (Acessibilidade, Segurança, Intuitividade, UI,
  Eficiência, Eficácia) para skills e agents.
- **Decisão:** personas jurídicas e políticas com caráter educativo/informativo
  (sem substituir OAB, legislação eleitoral do TSE respeitada); conteúdo em
  português com cabeçalhos compatíveis com os testes do kit.

### 2026-08-08 — Personas de domínio e certificações

- **Adicionadas 31 personas** em 12 novas categorias (construction, finance,
  marketing, science, humanities, engineering, logistics, web, health,
  management, cloud) e na categoria existente `design`.
- **Foco:** cada persona de domínio colabora com as personas de tecnologia,
  fornecendo parâmetros técnicos da sua área de acordo com o que o usuário
  está criando (seção "Como ajuda as personas de tecnologia").
- **Skills novas** para as áreas: construção, finanças, marketing, ciências,
  engenharia, web/scraping, looker studio, logística, lean, saúde, AWS e
  Google Cloud.
- **Decisão:** conteúdo em português para personas de domínio (público BR),
  mantendo os cabeçalhos compatíveis com os testes do kit
  (Persona/Pessoa, Habilidades/Capacidades, Exemplos/Exemplos de Uso).

### 2026-08-08 — Skills de contexto LLM

- **Adicionadas 5 skills** de contexto/LLM: `doc-to-markdown` (MarkItDown),
  `repo-to-llm` (gittomd/llms.txt), `code-knowledge-graph` (Graphify),
  `context-optimization` (Repomix/token economy), `skill-spector`
  (NVIDIA SkillSpector).
- **Decisão:** incluir automaticamente na instalação via `assets/skills/**`
  (o CLI copia recursivamente, sem configuração extra).

### 2026-07-18 — Fundação

- Estrutura inicial: skills, agents, prompts, templates, context, core
  (registry/discovery/resolver/version/plugin/security/quality), CI e testes.
- Versão 0.1.0 (semver).
