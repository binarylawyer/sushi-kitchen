# FAQ

**Q: Can I run without internet?**  
A: Yes (Phase 2 adds air-gapped installer with pre-seeded images).

**Q: Do I need a GPU?**  
A: No. GPU improves LLM/SD performance; CPU fallback works.

**Q: Where are secrets?**  
A: `.env` (not committed). Infisical optional (Phase 2 bootstrap).

**Q: Can agents change infra?**  
A: Not compose or schemas—guardrails require human approval.
