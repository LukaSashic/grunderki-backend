# Rollout Checklist: Module 1 Required Fields Refactor

**Version:** 2.0.0
**Target Date:** TBD
**Status:** Ready for Review

---

## Pre-Deployment Checklist

### Code Quality

- [ ] All new files created:
  - [ ] `backend/app/workshop/modules/__init__.py`
  - [ ] `backend/app/workshop/modules/module1/__init__.py`
  - [ ] `backend/app/workshop/modules/module1/required_fields.py`
  - [ ] `backend/app/workshop/modules/module1/validation_ui.py`

- [ ] Code updates applied:
  - [ ] `state_machine.py` - imports new module, updated `get_completion_status()`
  - [ ] `conversation_service.py` - FIELD_NAME_MAPPING updated with all aliases

- [ ] Documentation created:
  - [ ] `docs/MODULE1_REQUIRED_FIELDS_ARCHITECTURE.md`
  - [ ] `docs/CODE_AUDIT_ROOT_CAUSES.md`

### Testing

- [ ] Unit tests pass:
  ```bash
  pytest tests/test_module1_required_fields.py -v
  ```

- [ ] Integration tests pass:
  ```bash
  pytest tests/ -v -k "module1 or completion"
  ```

- [ ] Manual testing completed:
  - [ ] Gastronomie flow (22 required fields)
  - [ ] Dienstleistung flow (17 required fields)
  - [ ] Default/unknown business type (11 fields)

### Validation

- [ ] Field counts verified:
  | Business Type | Expected | Actual |
  |---------------|----------|--------|
  | gastronomie | 22 | [ ] |
  | einzelhandel | 19 | [ ] |
  | dienstleistung_lokal | 17 | [ ] |
  | dienstleistung_online | 17 | [ ] |
  | dienstleistung_mobil | 19 | [ ] |
  | handel_online | 18 | [ ] |
  | produktion | 18 | [ ] |
  | default | 11 | [ ] |

- [ ] Completion button behavior:
  - [ ] Button appears at 90% (not 75%)
  - [ ] Button disabled below 90%
  - [ ] Can complete at 90%+

- [ ] UI feedback verified:
  - [ ] Progress bar shows correct percentage
  - [ ] Category breakdown displays correctly
  - [ ] Missing fields listed accurately
  - [ ] Next step recommendation works

### Performance

- [ ] API response times acceptable:
  - [ ] `get_completion_status` < 100ms
  - [ ] `validate_completion` < 50ms
  - [ ] No N+1 query issues

- [ ] Memory usage stable:
  - [ ] LRU cache working correctly
  - [ ] No memory leaks in validation loop

### Backward Compatibility

- [ ] Existing sessions load correctly
- [ ] Old API responses still valid
- [ ] No breaking changes to frontend contract

---

## Deployment Steps

### Step 1: Backup (5 min)

```bash
# Backup database
pg_dump $DATABASE_URL > backup_pre_module1_refactor.sql

# Note current completion rates
# (run query to get baseline metrics)
```

### Step 2: Deploy Backend (10 min)

```bash
# Deploy new code
git pull origin main
pip install -r requirements.txt

# Restart server
systemctl restart gruenderai-workshop
# or
docker-compose up -d --build
```

### Step 3: Verify Deployment (5 min)

```bash
# Check health endpoint
curl https://api.example.com/health

# Check new module is loaded
curl https://api.example.com/api/workshop-chat/completion-status/TEST_SESSION

# Verify new fields in response
# Should include: missing_required, missing_by_category, business_type
```

### Step 4: Monitor (30 min)

- [ ] Check error logs for exceptions
- [ ] Monitor completion rate metrics
- [ ] Watch for user complaints

### Step 5: Post-Deployment Verification (15 min)

- [ ] Create test session with gastronomie type
- [ ] Verify 22 fields required
- [ ] Verify 90% completion threshold
- [ ] Complete module and check text generation

---

## Monitoring

### Key Metrics to Watch

1. **Completion Rate**
   - Baseline (before): ____%
   - Expected (after): May drop initially due to stricter requirements
   - Alert if: Drops more than 30% below baseline

2. **Average Fields Filled**
   - Baseline: ____ fields
   - Expected: ____ fields (should increase)
   - Alert if: Decreases

3. **Session Duration (Module 1)**
   - Baseline: ____ minutes
   - Expected: ____ minutes (may increase slightly)
   - Alert if: Increases more than 50%

4. **Error Rate**
   - Baseline: ____%
   - Alert if: Increases more than 1%

### Log Queries

```bash
# Check for validation errors
grep "validation_errors" /var/log/gruenderai/*.log

# Check completion status calls
grep "get_completion_status" /var/log/gruenderai/*.log | tail -100

# Check for module import errors
grep "ImportError\|ModuleNotFoundError" /var/log/gruenderai/*.log
```

---

## Rollback Plan

### Trigger Conditions

Rollback if ANY of the following occur:
- [ ] Error rate exceeds 5%
- [ ] Completion rate drops more than 50%
- [ ] Critical functionality broken
- [ ] Database corruption detected

### Rollback Steps (10 min)

#### Option A: Quick Rollback (Recommended)

Change completion threshold back to 75%:

```python
# In required_fields.py, change:
COMPLETION_CRITERIA = {
    "minimum_fill_percentage": 75,  # Changed from 90
    "show_button_at": 75,           # Changed from 90
    ...
}
```

Restart server.

#### Option B: Full Code Rollback

```bash
# Revert to previous commit
git revert HEAD~1

# Redeploy
# ... deployment steps ...
```

#### Option C: Database Restore (Last Resort)

```bash
# Restore from backup
psql $DATABASE_URL < backup_pre_module1_refactor.sql
```

---

## Success Criteria

### Immediate (Day 1)

- [ ] No increase in error rate
- [ ] API responses include new fields
- [ ] Completion button appears at 90%

### Short-term (Week 1)

- [ ] Completion rate stabilizes
- [ ] Average fields filled increases
- [ ] No critical bug reports

### Long-term (Month 1)

- [ ] Business plan quality scores improve
- [ ] BA GZ approval rate improves
- [ ] User satisfaction maintained or improved

---

## Communication Plan

### Before Deployment

- [ ] Notify team of deployment window
- [ ] Alert support team of potential user questions
- [ ] Update internal documentation

### During Deployment

- [ ] Post status updates to team channel
- [ ] Monitor support queue

### After Deployment

- [ ] Send deployment complete notification
- [ ] Share initial metrics
- [ ] Document any issues encountered

---

## Known Issues / Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Users confused by stricter requirements | Medium | Medium | Clear UI messaging, helpful next-step prompts |
| Completion rate drops significantly | Medium | High | Monitor closely, ready to adjust threshold |
| Performance degradation | Low | Medium | Caching in place, monitor response times |
| Integration issues with other modules | Low | High | Thorough testing, gradual rollout |

---

## Contacts

- **Technical Lead**: [Name]
- **Product Owner**: [Name]
- **On-Call Support**: [Contact]

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |
| Product | | | |
| DevOps | | | |
