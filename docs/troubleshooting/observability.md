# Observability

- **Prometheus**: default scrape config in `/observability/prometheus.yml`
- **Grafana**: dashboards auto-provision from `/observability/grafana/dashboards`
  - System Health
  - LLM Usage & Latency
  - Workflow Reliability
- **Langfuse**: traces from agents & tools; redaction enabled by default.

Low-Maintenance: set `ENABLE_OBSERVABILITY=false` to disable prom/grafana/langfuse.
