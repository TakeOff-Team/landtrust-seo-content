---
name: check-keyword-rankings
description: Checks Google search rankings for blog articles' target keywords. Use when the user wants to check keyword rankings, SEO performance, or update ranking data for articles in posted_articles.md.
allowed-tools: Read, mcp__firecrawl__firecrawl_scrape, mcp__dataforseo-api__get_serp_results
---

# Check Keyword Rankings

## Overview

This skill analyzes blog articles listed in `posted_articles.md`, extracts the top 5 target keywords from each article's content, and checks how many of those keywords rank in the top 20 Google search results for the domain landtrust.com.

## Instructions

### Step 1: Read the Articles List

Read `/Users/zacharygeleott/Downloads/TakeOff - LandTrust/Articles/posted_articles.md` to get the list of article URLs.

### Step 2: Process Each Article

For each article URL in the list:

1. **Fetch the article content** using `mcp__firecrawl__firecrawl_scrape`:
   - Set `url` to the article URL
   - Use `formats: ["markdown"]` to get clean text content
   - Filter only for landtrust.com articles (skip LinkedIn articles for ranking checks)

2. **Extract top 5 target keywords**:
   - Analyze the article title and content
   - Identify the 5 most important/relevant keywords or keyword phrases
   - Focus on:
     - Primary topic keywords from the title
     - Repeated important phrases (2-4 words)
     - Core concepts that define the article's purpose
     - Target search terms users would likely use
   - Avoid generic words like "guide", "complete", "your"

3. **Check keyword rankings** using `mcp__dataforseo-api__get_serp_results`:
   - For each of the 5 keywords:
     - Set `keyword` to the target keyword
     - Set `location_code` to 2840 (USA)
     - Set `search_engine` to "google"
     - Set `depth` to 20 (to check top 20 results)
     - Look through results for landtrust.com domain
     - Note if landtrust.com appears in positions 1-20

4. **Calculate ranking score**:
   - Count how many of the 5 keywords have landtrust.com in top 20
   - Format as: X/5 (e.g., "3/5" means 3 out of 5 keywords rank in top 20)

### Step 3: Report Results

Output results in a clean table format showing:
- Article title (extracted from URL or content)
- The 5 target keywords identified
- Ranking score (X/5)
- List results in the same order as posted_articles.md

Example output format:
```
Keyword Ranking Report
Generated: [date]

1. [Article Title]
   Keywords: keyword1, keyword2, keyword3, keyword4, keyword5
   Ranking: 3/5

2. [Article Title]
   Keywords: keyword1, keyword2, keyword3, keyword4, keyword5
   Ranking: 4/5
```

## Performance Notes

**IMPORTANT - Time Considerations:**
- This analysis is **resource-intensive** - checking all articles takes 30-60 minutes
- Each article requires: 1 article fetch + 5 keyword SERP checks = 6 API calls minimum
- For 12 articles: ~72 API calls total
- **Recommended approach**: Process ONE article at a time when requested
- Allow the user to request specific articles rather than running all at once

**Processing Guidelines:**
- Skip LinkedIn articles (they rank on linkedin.com, not landtrust.com)
- Process articles sequentially to avoid rate limiting
- If an article fails to fetch, note it and continue with others
- Consider batching keyword checks (3-4 at a time) to monitor progress

## Related Resources

- DataForSEO API for SERP data
- Firecrawl for article content extraction
