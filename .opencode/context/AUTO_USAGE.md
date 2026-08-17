---
name: auto-usage
description: Regra de uso automático de skills, personas e assets do kit no OpenCode — sempre verifique e use quando for produtivo, sem comandos
type: workflow
version: 0.1.0
author: devtiagoabreu
---

# Uso Automático do Kit (Auto Usage)

Este arquivo é instalado automaticamente pelo kit e registrado nas
instruções do projeto. Ele define como o assistente de IA deve usar os assets
do kit **de forma automática**, sem que o usuário precise digitar comandos.

## Regra Geral

Antes de responder ou executar uma tarefa, o assistente deve **sempre
verificar** se existe uma skill, persona (agent), comando, prompt, playbook,
recipe ou template do kit relevante para a tarefa atual. Se existir e o uso
for **mais produtivo** do que responder sem ele, o assistente deve **usar
automaticamente**, sem perguntar, e **informar o usuário** de forma curta.

## Onde procurar

Depois da instalação, os assets do kit ficam disponíveis no projeto:

| Recurso | Localização |
|---------|-------------|
| Skills | `.opencode/skills/` (carregadas automaticamente pelo OpenCode) |
| Agents / personas | `.opencode/agents/` (disponíveis para invocação) |
| Contexto | `.opencode/context/` (instruções e regras do projeto) |
| Commands | `.opencode/commands/` |
| Assets completos | `.opencode/assets/` |

## Fluxo automático

1. **Identifique a tarefa** pedida pelo usuário (codar, revisar, testar,
   documentar, modelar banco, configurar deploy, etc.).
2. **Verifique** se há uma skill relevante em `.opencode/skills/`. O OpenCode
   já expõe as skills disponíveis; o assistente deve **inspecionar as que
   correspondem** ao tema da tarefa (ex.: `nextjs-development`,
   `postgresql-database`, `sql-optimization`, `javascript-best-practices`).
3. **Verifique** se há uma persona relevante em `.opencode/agents/`
   (ex.: `nextjs-developer`, `postgresql-dba`, `qa-engineer`).
4. **Se aplicável**, use a skill/persona automaticamente:
   - Siga as instruções da skill para executar a tarefa.
   - Adote a persona no tom e na profundidade dela para a resposta.
5. **Informe o usuário** com uma nota curta sobre o que foi usado, ex.:
   `Usando a skill nextjs-development para este componente` ou
   `Atuando como postgresql-dba para revisar esta query`.
6. **Se não houver asset relevante**, responda normalmente, sem informar nada
   sobre o kit.

## Quando usar (exemplos)

- **Implementar um endpoint** → `javascript-best-practices`,
  `nextjs-development`, `rest-api-design`
- **Modelar/tunar banco** → `postgresql-database`, `oracle-database`,
  `sql-server-database`, `sql-optimization`, `nosql-modeling`
- **Revisar código** → persona `code-reviewer` ou `qa-engineer`
- **Documentar** → `documentation`, `technical-writer`
- **Configurar CI/CD ou deploy** → `ci-cd-pipeline`, `docker-best-practices`
- **Segurança** → `owasp-top-10`, `secure-coding`
- **Instalar/gerenciar o próprio kit** → skill `ocekit-manager` (use quando o
  usuário disser "instale ocekit", "instale o ocekit do <link>", "status
  ocekit", "start ocekit" ou "stop ocekit"). Pergunte ao usuário se quer
  instalação **global** (`~/.config/opencode`) ou **só neste projeto**
  (`.opencode/`), depois execute:
  `npx opencode-engineering-kit install` (projeto) ou
  `npx opencode-engineering-kit install --global` (global). Para consultar o
  estado use `npx opencode-engineering-kit status`; para desativar/reativar use
  `stop`/`start`. Informe o usuário e lembre de reiniciar o opencode.

## O que NÃO fazer

- Não perguntar ao usuário "quer que eu use uma skill?" — o uso é automático.
- Não exigir que o usuário rode `search`, `list` ou `doctor` manualmente.
- Não descrever em detalhes o funcionamento interno do kit a cada resposta;
  apenas a nota curta de qual asset foi usado (se usou).
- Não forçar o uso de um asset quando ele não agrega valor à tarefa.

## Manutenção

- Quando o usuário atualizar o kit (`npx opencode-engineering-kit upgrade`),
  este arquivo é atualizado junto.
- Se o usuário não quiser o comportamento automático, basta remover este
  arquivo de `opencode.json > instructions` ou apagar
  `.opencode/context/auto_usage.md`.
