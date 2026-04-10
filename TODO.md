# Movie Data Pipeline - Data Enrichment TODO

Current Plan: Implement Data Enrichment using TMDb API

## TODO Steps:

### 1. **Setup Dependencies** ✅ 
- ✅ Create requirements.txt
- ✅ Create .env.example
- ✅ Install packages: `pip install -r requirements.txt`


### 2. **Configuration** 
- [ ] Create config.py or .env for TMDb API key

### 3. **Generate Base Data** ✅
- ✅ Run `python scripts/scrape_wikipedia.py` 
- ✅ Run `python scripts/clean_movies_data.py` (133 movies processed)

### 4. **Implement Enrichment Script** ✅
- ✅ Create `scripts/enrich_movies.py`
- ✅ Implement TMDb API integration (search + details)
- ✅ Add fuzzy matching for movie names (direct hi-IN, fallback en-US)
- ✅ Handle missing matches and rate limits (sleep 0.5s)

### 5. **Test & Validate**
- [ ] Test on sample movies
- [ ] Verify new columns: imdb_rating, genres, budget, etc.
- [ ] Save to `data/enriched/`

### 6. **Pipeline Integration** ✅
- ✅ Create main_pipeline.py chaining all steps
- ✅ Add logging and error handling (os.system + API key check)

### 7. **Documentation** ✅
- ✅ Update README.md (full pipeline docs + sample data)
- ✅ Add data schema docs (in README)

**Next Steps:**
1. Get TMDb API key & setup .env
2. Run `python main_pipeline.py`
3. Proceed to SQL + Viz stages

Progress will be updated as steps complete.

