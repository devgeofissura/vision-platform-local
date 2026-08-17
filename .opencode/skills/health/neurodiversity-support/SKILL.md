---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: neurodiversity-support
description: Support neurodivergent learners and colleagues with inclusive communication, accessibility, and accommodations.
category: health
version: 0.1.0
author: devtiagoabreu
tags: [neurodiversity, accessibility, inclusion, wcag, communication, accommodations]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - An inclusive mindset and willingness to adjust defaults
  - Understanding of basic accessibility (WCAG) principles
  - A team, classroom, or documentation audience to apply it to
provides:
  - Inclusive written and spoken communication patterns
  - Accessible document and interface formatting (WCAG)
  - Reasonable accommodation ideas for education and work
  - Processes for gathering feedback without singling anyone out
---

# neurodiversity-support

## Overview

Neurodivergent people — including autistic people, ADHDers, and people
with dyslexia or dyspraxia — are a normal part of any classroom and
workplace. Their needs vary widely, so the best support is a set of
defaults that are inclusive for everyone: clear language, predictable
structure, and multiple ways to communicate and demonstrate work.

This skill is educational guidance about communication and
accessibility. It is not a medical resource: it does not diagnose,
assess, or treat, and it never replaces individualized advice from
healthcare or educational professionals.

## Prerequisites

- Awareness that neurodiversity varies per person; no one-size-fits-all fix
- Access to the documents, interfaces, or meetings you will improve
- Time to build feedback loops (surveys, one-to-ones) safely
- No assumption that any single strategy fits all neurodivergent people

## Usage Instructions

### 1. Inclusive Written and Spoken Communication

Use concrete language, one idea per sentence, and explicit transitions.
State the purpose and structure up front; avoid implied social norms
and vague deadlines. Preferred style:

```markdown
BAD:  "Please have a look at the report when you get a moment — the
      usual expectations apply."

GOOD: "By Friday 12:00, please review the report (link) and reply with
      one question you have. If you need an extension or another format,
      just ask — no justification required."
```

In meetings, share agendas and materials before, allow written
responses, and never treat eye contact as a measure of engagement.

### 2. Accessible Formatting (WCAG Principles)

Apply WCAG 2.2 basics to documents and interfaces: sufficient contrast,
real headings, and no color-only meaning. These benefit everyone.

```css
/* WCAG AA compliant contrast and clear focus states */
body {
  color: #1a1a1a;              /* near-black text */
  background: #ffffff;
  line-height: 1.6;
}
a:focus, button:focus {
  outline: 3px solid #005fcc;  /* visible keyboard focus */
  outline-offset: 2px;
}
/* High-contrast text alternative for emphasized words */
mark { background: #ffe9a8; }
```

For documents: use heading styles (not bolded text) for structure, add
alt text, and offer a plain-text or large-print version.

### 3. Reasonable Accommodations

Accommodations are adjustments that remove barriers; they are
reasonable when they do not cause disproportionate burden. Offer a menu,
never a single fixed option:

```yaml
options:
  - name: "Flexible communication"
    choices:
      - "Written-only replies accepted"
      - "Recorded meetings with transcripts"
      - "Extra processing time before responding"
  - name: "Environment"
    choices:
      - "Noise-cancelling headphones allowed"
      - "Quiet zone or remote option"
      - "Reduced lighting / designated break room"
  - name: "Task structure"
    choices:
      - "Written step-by-step instructions"
      - "Deadlines split into milestones"
      - "Checklists and templates provided"
```

### 4. Gather Feedback Safely

Learn what helps without forcing disclosure. An anonymous survey of the
whole group surfaces needs without singling anyone out:

```markdown
Rate each statement 1-5:
1. I can find information without asking someone.
2. I get enough time to process requests before replying.
3. The environment (noise, light) lets me work comfortably.
Open text: "One change that would help me is: ______"
```

## Best Practices

- Prefer plain language: concrete, short, and unambiguous.
- Always provide the "what, why, and by when" for any request.
- Offer choices and alternate formats; never mandate a single style.
- Keep instructions step-by-step and in writing, not just in meetings.
- Treat the person as the expert on their own needs; adjust per individual.
- Keep the disclaimer: this guidance does not replace professional health advice.

## Pitfalls / Common Mistakes

- Assuming one accommodation (e.g. "everyone gets written notes") fits all.
- Forcing participation formats that only work for one communication style.
- Using color alone (red/green) to convey meaning, excluding color-blind users.
- Judging engagement by eye contact, posture, or body language.
- Recording meetings without offering text transcripts or written alternatives.
- Framing needs as problems rather than normal human variation.

## Examples

### Example 1: Accessible email template

```text
Subject: [Action] Review attachment by Fri 12:00

Hi all,

We need one question answered about the draft roadmap (attached).

Action: reply with one open question you have.
Deadline: Friday 12:00.
Format: reply, comment in the doc, or tell me in person — your choice.
Need more time or another format? Say so, no justification needed.

Thanks,
Sam
```

### Example 2: Accessibility checklist for a new page

```markdown
- [ ] Use real heading levels (h1, h2, h3) in order
- [ ] Text contrast >= 4.5:1 (WCAG AA)
- [ ] No meaning carried by color alone
- [ ] Alt text on images; captions/transcripts on media
- [ ] Links say where they go ("See the pricing page")
- [ ] Offer a plain-text or larger-print version
```

## References

- [Neurodiversity (Wikipedia)](https://en.wikipedia.org/wiki/Neurodiversity)
- [WCAG 2.2 Overview](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/)
