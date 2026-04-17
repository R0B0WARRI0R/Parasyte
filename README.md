# PARASYTE
> An LFM that "parasites" Chrome DevTools for autonomous browser control

## Concept

```
┌─────────────────────────────────────────────────────┐
│                     PARASYTE                        │
│                                                     │
│  The LFM "attaches" to DevTools like a virus       │
│  Modifies itself minimally to control               │
│  the browser autonomously                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Biological Analogy

| Virus | Parasyte |
|-------|----------|
| Attaches to receptors | Connects via CDP |
| Injects genetic material | Sends commands |
| Cell executes | DevTools operates |
| Replication/modification | Continuous self-improvement |

## Goal

Create an autonomous agent that controls DevTools for:
- Automatic debugging
- Performance profiling
- Memory leak detection
- Network analysis
- Intelligent DOM manipulation

## Tech Stack

- **LFM**: Liquid Foundation Models (Liquid AI)
- **CDP**: Chrome DevTools Protocol
- **Target**: Chrome/Chromium with remote debugging

## Status

- [x] Deep research complete (20 topics)
- [ ] Define architecture
- [ ] Build prototype

## Structure

```
docs/           - Technical documentation
src/           - Source code
tests/         - Unit tests
```