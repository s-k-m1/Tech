# SK Tech - AI Security Workflow

## Login Risk Analysis

```
┌──────────┐     ┌──────────────────┐     ┌──────────────┐
│  Login   │────>│  Risk Analyzer   │────>│    Score     │
│ Request  │     │  (sync)          │     │   0.0 - 1.0  │
└──────────┘     └──────────────────┘     └──────┬───────┘
                                                  │
                          ┌───────────────────────┼───────────────────────┐
                          ▼                       ▼                       ▼
                    ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
                    │ Score < 0.4 │       │ 0.4-0.7      │       │ Score > 0.7  │
                    │ Allow login  │       │ Require OTP  │       │ Block login  │
                    └──────────────┘       └──────────────┘       └──────────────┘
```

### Risk Factors (weights in parentheses)

| Factor | Weight | Detection Method |
|--------|--------|-----------------|
| IP mismatch (last login) | 0.2 | Compare `user.last_login_ip` vs `request.REMOTE_ADDR` |
| Recent failed logins | 0.3 | Count `AuditLog` entries with `action~login_failed` in last 1h (capped at 3 failures) |
| Missing User-Agent | 0.1 | Empty or suspicious User-Agent header |
| Known suspicious IP | 0.2 | Check against `IPBlacklist` (geolocation, proxy/VPN detection — future) |
| Geo anomaly | 0.2 | Detect location change from previous login (future — via GeoIP) |

**Decision logic:**
- `< 0.4`: Full access granted
- `0.4 - 0.7`: Step-up authentication (OTP required)
- `> 0.7`: Login blocked, event logged as critical

## Anomaly Detection (Celery Periodic Task)

Runs every 5 minutes via Celery Beat:

```
schedule: run_security_scan.delay()
         │
         ▼
  ┌──────────────┐
  │ Anomaly      │
  │ Detector     │
  └──────┬───────┘
         │
    ┌────┴────────────────────────────┐
    ▼                                 ▼
┌──────────────┐               ┌──────────────┐
│ Traffic Spike│               │ Brute Force  │
│ >1000 req/hr │               │ >10 failed   │
│ /tenant      │               │ logins / hr  │
└──────┬───────┘               └──────┬───────┘
       │                              │
       └──────────┬───────────────────┘
                  ▼
       ┌──────────────────┐
       │ Send notification│
       │ to tenant admins │
       │ via WebSocket +  │
       │ Email            │
       └──────────────────┘
```

### Detection Rules

| Anomaly | Threshold | Severity | Action |
|---------|-----------|----------|--------|
| Traffic spike | >1000 req/tenant/hr | High | Notify admin |
| Brute force | >10 failed logins/hr | Critical | Notify admin, auto-block IPs |
| API abuse | >500 errors/hr | Medium | Rate limit tightening |
| Unusual hours | Login outside business hours | Low | Flag for review |

## AI Security Dashboard

Cache key: `security_dashboard:{tenant_id}` (TTL: 60s)

Data sources:
- `AuditLog` count (24h window) — event volume
- `SecurityEvent` severity breakdown — threat distribution
- `IPBlacklist` active count — blocked IPs
- `AnomalyDetector` results — active issues

Recommender logic:
```python
def generate_recommendations(logs):
    if critical_count > 10:
        yield "Review firewall rules — critical events elevated"
    if failed_logins > 20:
        yield "Increase rate limiting — multiple failed login attempts"
    if traffic_spike:
        yield "Investigate traffic source — possible DDoS"
```

## Response Actions

| Risk Level | Action | Implementation |
|-----------|--------|---------------|
| Low | No action | — |
| Medium | Require OTP | `AuthService.login()` checks score |
| High | Rate limit user | `rate_limit` decorator on login |
| Critical | Block + Auto-blacklist | `SecurityMiddleware._auto_block_if_needed()` |

## Future AI Enhancements

- ML-based anomaly detection (isolation forest)
- User behavior profiling (login time, location, device patterns)
- Predictive threat scoring
- Automated incident response (block IP, suspend user, notify SOC)
