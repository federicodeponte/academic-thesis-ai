# Data - Single Source of Truth

**DRY Principle:** All documentation metrics are generated from `metrics.json`.

## 📊 metrics.json

**Single source of truth** for all performance data, costs, and statistics across:
- README.md
- docs/BENCHMARKS.md
- Website content
- Marketing materials

### Structure

```json
{
  "meta": { ... },           // Project metadata (users, theses, dates)
  "performance": { ... },    // Speed, efficiency metrics
  "quality": { ... },        // Quality scores, accuracy
  "agents": { ... },         // AI agent counts
  "research": { ... },       // Paper databases
  "costs": { ... },          // All pricing data
  "theses": { ... },         // Individual thesis stats
  "features": { ... },       // Feature counts
  "comparisons": { ... }     // Competitive data
}
```

## 🔄 Updating Documentation

### 1. Edit metrics.json

```bash
# Edit the centralized data
vim data/metrics.json
```

### 2. Generate documentation

```bash
# Generate all docs from metrics
python3 scripts/generate_docs.py --all

# Or generate specific docs
python3 scripts/generate_docs.py --readme    # Just README sections
python3 scripts/generate_docs.py --bench     # Just BENCHMARKS.md
```

### 3. Review generated files

```bash
# Check generated sections for README
cat data/generated_readme_sections.md

# Check regenerated benchmarks
cat docs/BENCHMARKS.md
```

### 4. Update README.md manually

The script generates sections for README.md in `data/generated_readme_sections.md`.
You need to manually copy these sections into `README.md` to replace the old content.

**Sections generated:**
- `key_metrics` → "By the Numbers" table
- `comparison` → "Why OpenDraft?" comparison table
- `time_savings` → Time savings breakdown
- `success_stories` → Four thesis examples table

## ✅ Benefits

1. **DRY:** Change data once, update everywhere
2. **Consistency:** All docs always in sync
3. **Validation:** JSON schema validates data
4. **Automation:** Regenerate docs with one command
5. **Maintenance:** Easy to update metrics

## 📝 Example Workflow

```bash
# New benchmark test completed
# Update metrics.json with new timing data
vim data/metrics.json

# Regenerate all documentation
python3 scripts/generate_docs.py --all

# Review changes
git diff docs/BENCHMARKS.md data/generated_readme_sections.md

# Commit
git add data/metrics.json docs/BENCHMARKS.md
git commit -m "chore: update metrics from latest benchmark tests"
```

## 🎯 What Gets Generated

| File | Generated From | Status |
|------|---------------|--------|
| `docs/BENCHMARKS.md` | metrics.json | ✅ Auto-generated |
| `data/generated_readme_sections.md` | metrics.json | ✅ Auto-generated |
| `README.md` | generated_readme_sections.md | ⚠️ Manual update |
| Website content | metrics.json | 🔄 Future |

## 📖 Schema Documentation

See `scripts/generate_docs.py` for the complete data schema and how it's used to generate each section.

**Key fields:**
- `meta.last_updated` - Auto-updates on generation
- `performance.*` - Speed/efficiency metrics
- `costs.*` - All pricing comparisons
- `theses.*` - Individual thesis data
- `quality.*` - Quality scores

## 🚀 Future Enhancements

- [ ] JSON schema validation
- [ ] Auto-update from test results
- [ ] Website content generation
- [ ] CI/CD integration
- [ ] Historical metrics tracking

---

**Last Updated:** 2025-11-22
**Maintained By:** Federico De Ponte
