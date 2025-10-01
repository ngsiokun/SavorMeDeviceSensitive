# SavorMe Backend - Evidence-Based Implementation Roadmap

## Quick Overview

**What We're Building**: A system that maps user moods → nutrient targets → recipe recommendations using evidence-based nutritional science.

**Current Status**: ✅ Core infrastructure complete, ready for refinement and testing

---

## Implementation Status

### ✅ COMPLETED

#### 1. Core Architecture
- [x] FastAPI backend with proper structure
- [x] Pydantic models for all data types
- [x] API endpoint routing
- [x] Configuration management

#### 2. Evidence-Based Mapping System
- [x] `mood_mapping.json` with 12 moods
- [x] Scientific nutrient targets for each mood
- [x] Pattern-based dietary guidelines (Mediterranean)
- [x] Medical disclaimers and contraindications

#### 3. Mood Nutrition Engine
- [x] Nutrient target aggregation (multi-mood support)
- [x] Intensity weighting (a little, medium, very)
- [x] Recipe scoring algorithm (0-1.25 scale)
- [x] Nutrient canonicalization (alias resolution)
- [x] Evidence-based explainers

#### 4. API Integrations
- [x] Edamam Recipe Search client
- [x] USDA FoodData Central client
- [x] OpenRouter AI client (emotional rationale)
- [x] Nutrition calculation engine

#### 5. API Endpoints
- [x] `/api/v1/recipes/recommend` - Main recommendation engine
- [x] `/api/v1/nutrition/calculate` - Nutrition targets
- [x] `/api/v1/mood/interpret` - Mood interpretation
- [x] `/api/v1/nutrition/score-recipe` - Direct nutrient scoring
- [x] `/api/v1/nutrition/mood-targets/{mood}` - Get targets for mood
- [x] `/api/v1/health` - Health check

---

## 🚧 REMAINING WORK

### Phase 1: Testing & Validation (Priority: HIGH)

#### A. Unit Tests
```python
# app/tests/test_mood_nutrition_engine.py
- [ ] Test mood aggregation logic
- [ ] Test intensity weighting
- [ ] Test scoring algorithm
- [ ] Test nutrient canonicalization
- [ ] Test edge cases (conflicting targets)
```

#### B. Integration Tests
```python
# app/tests/test_api_integration.py
- [ ] Test end-to-end recommendation flow
- [ ] Test with real Edamam API
- [ ] Test FDC API integration
- [ ] Test error handling
```

#### C. Data Validation
- [ ] Verify nutrient aliases match Edamam codes
- [ ] Test with 20+ real recipes
- [ ] Validate unit conversions (mg/g/mcg)
- [ ] Check Mediterranean pattern detection

### Phase 2: Data Quality & Accuracy (Priority: HIGH)

#### A. Nutrient Extraction Enhancement
```python
# app/services/edamam_client.py
- [ ] Add fallback to FDC when Edamam data incomplete
- [ ] Handle missing nutrient data gracefully
- [ ] Add confidence scores for nutrient data
- [ ] Implement ingredient-level nutrient lookup
```

#### B. Scoring Algorithm Refinement
```python
# app/services/mood_nutrition_engine.py
- [ ] Add pattern bonus calculation
- [ ] Implement preference matching
- [ ] Add novelty factor
- [ ] Tune weight distributions based on testing
```

#### C. Edge Case Handling
- [ ] No recipes meet targets → relaxation strategy
- [ ] Conflicting moods → resolution logic
- [ ] Missing critical nutrients → warning system
- [ ] Contraindications → filtering

### Phase 3: UX Enhancement (Priority: MEDIUM)

#### A. Explanation Generation
```python
# app/services/explainability.py (NEW)
- [ ] Generate "Why this recipe?" narratives
- [ ] Create visual nutrient breakdowns
- [ ] Add evidence links
- [ ] Format disclaimers appropriately
```

#### B. Response Enrichment
- [ ] Add nutrition comparison visualizations
- [ ] Include alternative recipes (2nd, 3rd best)
- [ ] Suggest ingredient substitutions
- [ ] Show confidence intervals

### Phase 4: Performance & Optimization (Priority: MEDIUM)

#### A. Caching Strategy
```python
# app/services/cache.py (NEW)
- [ ] Cache FDC API responses (24h TTL)
- [ ] Cache Edamam searches (6h TTL)
- [ ] Cache nutrient calculations
- [ ] Implement Redis integration
```

#### B. Performance Tuning
- [ ] Add async/await to all I/O operations
- [ ] Batch recipe scoring
- [ ] Optimize nutrient extraction
- [ ] Add request timeouts

### Phase 5: Advanced Features (Priority: LOW)

#### A. Personalization
```python
# app/services/personalization.py (NEW)
- [ ] Learn user preferences over time
- [ ] Adjust baselines from food logs
- [ ] Temporal adjustments (time of day)
- [ ] Combination effect modeling
```

#### B. Machine Learning
- [ ] Collect user feedback data
- [ ] Build recommendation model
- [ ] A/B test different algorithms
- [ ] Optimize weights using ML

---

## Current Implementation Gaps

### 🔴 Critical Gaps

1. **Missing Polyphenol Data**
   - Edamam doesn't provide polyphenol content
   - **Solution**: Use ingredient-based estimation or remove from scoring

2. **Added Sugar Tracking**
   - Edamam has `SUGAR.added` but often null
   - **Solution**: Use total sugars as proxy, add manual adjustments

3. **Test Coverage**
   - Zero automated tests currently
   - **Solution**: Implement test suite (see Phase 1)

### 🟡 Important Gaps

4. **FDC Integration Not Active**
   - FDC client built but not used in main flow
   - **Solution**: Add fallback logic when Edamam lacks nutrients

5. **No Caching**
   - Every request hits external APIs
   - **Solution**: Add Redis caching layer

6. **Error Handling**
   - Basic try/catch but not comprehensive
   - **Solution**: Add detailed error types and recovery

### 🟢 Nice-to-Have Gaps

7. **No Alternative Recipes**
   - Only returns single best recipe
   - **Solution**: Return top 3 with scores

8. **Limited Explainability**
   - Basic reasons provided
   - **Solution**: Richer narratives and evidence links

---

## Technical Debt

### Code Quality
- [ ] Add type hints to all functions
- [ ] Add docstrings to all classes
- [ ] Implement logging throughout
- [ ] Add input validation decorators

### Documentation
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Developer setup guide
- [ ] Deployment guide
- [ ] Contribution guidelines

### Infrastructure
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring and alerting
- [ ] Load testing

---

## Deployment Checklist

### Pre-Deployment
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] API keys configured
- [ ] Database migrations ready
- [ ] Logging configured
- [ ] Error tracking (Sentry)

### Deployment
- [ ] Deploy to staging
- [ ] Smoke test all endpoints
- [ ] Load test recommendation endpoint
- [ ] Monitor error rates
- [ ] Deploy to production
- [ ] Monitor metrics

### Post-Deployment
- [ ] User feedback collection
- [ ] A/B test tracking
- [ ] Performance monitoring
- [ ] Weekly data quality checks

---

## Risk Assessment

### High Risk
1. **API Rate Limits**: Edamam free tier = 10 req/min
   - **Mitigation**: Aggressive caching, upgrade to paid tier

2. **Data Quality**: Nutrient data incomplete/inaccurate
   - **Mitigation**: Multi-source fallbacks, confidence scores

3. **Medical Liability**: Health claims without clinical backing
   - **Mitigation**: Strong disclaimers, conservative claims

### Medium Risk
4. **User Confusion**: Complex scoring may confuse users
   - **Mitigation**: Progressive disclosure, simple default view

5. **Performance**: Multiple API calls slow response
   - **Mitigation**: Caching, async operations, timeouts

### Low Risk
6. **Edge Cases**: Rare mood combinations break system
   - **Mitigation**: Comprehensive testing, graceful degradation

---

## Success Criteria

### Week 1: Testing
- ✅ 80%+ test coverage
- ✅ All unit tests passing
- ✅ Integration tests working

### Week 2: Refinement
- ✅ Scoring algorithm validated with 50+ recipes
- ✅ Nutrient extraction 90%+ accurate
- ✅ API response time <2s average

### Week 3: Production Ready
- ✅ Error rate <1%
- ✅ Uptime >99%
- ✅ User feedback mechanism active

### Month 1: User Validation
- ✅ 100+ active users
- ✅ 4.0+ satisfaction rating
- ✅ 60%+ recipe completion rate

---

## Next Immediate Actions

### Today
1. ✅ Review MAPPING_STRATEGY.md with team
2. ⏳ Commit evidence-based system to GitHub
3. 📝 Create test plan document

### This Week
1. Write unit tests for MoodNutritionEngine
2. Test with 20 real recipes manually
3. Fix any critical bugs discovered
4. Add caching layer

### Next Week
1. Build test suite
2. Validate nutrient data quality
3. Refine scoring algorithm based on results
4. Prepare for staging deployment

---

## Questions to Answer

1. **What polyphenol estimation method should we use?**
   - Option A: Ingredient-based lookup table
   - Option B: Remove polyphenol from scoring
   - Option C: Use FDC detailed data

2. **Should we use FDC as primary or fallback?**
   - Edamam: Better recipe search, faster
   - FDC: More detailed nutrients, slower
   - **Recommendation**: Edamam primary, FDC fallback

3. **What caching strategy?**
   - Redis vs in-memory vs database
   - **Recommendation**: Redis for production, in-memory for dev

4. **How to handle insufficient evidence moods?**
   - Moods like "playful" and "charismatic" lack strong science
   - **Recommendation**: Pattern-based only, clear labeling

---

## Contact & Resources

- **Documentation**: `/documentation.md`, `/MAPPING_STRATEGY.md`
- **API Docs**: `http://localhost:8000/docs` (when running)
- **GitHub**: `https://github.com/ngsiokun/SavorMe-backend`
- **Scientific References**: See MAPPING_STRATEGY.md Section 2

---

**Last Updated**: 2025-10-01  
**Version**: 0.1.0-beta  
**Status**: Development - Evidence-based system implemented, testing phase

