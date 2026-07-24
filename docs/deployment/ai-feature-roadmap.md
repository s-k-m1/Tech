# SK Tech - AI Feature Roadmap

## Phase 1: Current (Implemented)

- **Login Risk Analysis** — Rule-based scoring (0-1) using IP, device, failure rate
- **Anomaly Detection** — Periodic scan for traffic spikes, brute force patterns
- **Security Dashboard** — Real-time event count, severity breakdown, threat timeline
- **Automated Response** — OTP step-up, IP auto-blacklist

## Phase 2: Short-term (Next 3 months)

| Feature | Description | Priority | Effort |
|---------|-------------|----------|--------|
| **ML-based Risk Scoring** | Replace rule-based with isolation forest or logistic regression model | High | 2 weeks |
| **User Behavior Profiling** | Learn login patterns (time, location, device, IP range) per user; flag deviations | High | 3 weeks |
| **Intelligent Alerting** | Severity-based alert routing (Slack, email, SMS) with escalation paths | Medium | 1 week |
| **Automated Report Generation** | Weekly/monthly security posture PDF report with trends and recommendations | Medium | 2 weeks |

## Phase 3: Medium-term (3-6 months)

| Feature | Description | Priority | Effort |
|---------|-------------|----------|--------|
| **Predictive Threat Detection** | Time-series forecasting of attack patterns using historical SecurityEvent data | High | 4 weeks |
| **NLP-based Log Analysis** | Parse AuditLog descriptions with LLM to extract structured threat intelligence | Medium | 3 weeks |
| **Automated Incident Response** | Playbook-driven auto-response: block IP, suspend user, revoke tokens, notify SOC | High | 3 weeks |
| **AI-powered Recommendations** | Contextual security recommendations in the dashboard (e.g., "Enable 2FA for 12 users") | Medium | 2 weeks |
| **Fraud Detection** | Detect payment anomalies in Accounting module (unusual transaction patterns) | Medium | 4 weeks |

## Phase 4: Long-term (6-12 months)

| Feature | Description | Priority | Effort |
|---------|-------------|----------|--------|
| **Chatbot Assistant** | Natural language query interface for security data ("Show me failed logins this week") | Low | 6 weeks |
| **Auto-remediation** | AI applies firewall rules, updates rate limits, patches configurations automatically | Low | 8 weeks |
| **Cross-tenant Threat Intel** | Anonymized threat intelligence sharing across tenants (opt-in) | Low | 4 weeks |
| **Deep Learning IDS** | Real-time traffic analysis with neural network for zero-day attack detection | Low | 12 weeks |
| **Self-healing Infrastructure** | AI detects and resolves infrastructure issues (restart services, scale resources) | Low | 8 weeks |

## Model Serving Strategy

```
┌──────────┐     ┌──────────────┐     ┌────────────────┐
│ Training │────>│ Model Store  │────>│  Inference API │
│ (offline)│     │ (S3/DB)      │     │  (Celery task) │
└──────────┘     └──────────────┘     └───────┬────────┘
                                              │
                                        ┌─────▼─────┐
                                        │   Score   │
                                        │  returned │
                                        └───────────┘
```

- **Training:** Periodic offline (weekly) via Celery Beat
- **Storage:** Model artifacts saved to DB or S3
- **Inference:** Synchronous via Celery task with result backend
- **Fallback:** Rule-based scoring when ML model unavailable

## Metrics for Success

| KPI | Current | Target |
|-----|---------|--------|
| False positive rate | N/A | < 5% |
| Threat detection rate | 70% | > 95% |
| Mean time to detect | 5 min | < 1 min |
| Mean time to respond | Manual | < 30 sec (auto) |
| User satisfaction | N/A | > 90% |
