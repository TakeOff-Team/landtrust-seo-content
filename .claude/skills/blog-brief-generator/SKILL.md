---
name: blog-brief-generator
description: Generates comprehensive SEO-optimized blog briefs for LandTrust articles. Accepts a blog topic, finds the matching marketing report, conducts keyword research, analyzes SERPs, and creates a detailed brief with quote placeholders. Outputs to Finished Content folder.
allowed-tools: Read, Glob, Grep, mcp__dataforseo-api__get_keyword_data, mcp__dataforseo-api__get_keyword_suggestions, mcp__dataforseo-api__get_serp_results, mcp__firecrawl__firecrawl_search, Write, Bash(ls:*)
---

# Blog Brief Generator

## Overview

This skill automates the creation of comprehensive, SEO-optimized blog briefs for LandTrust content. It accepts a blog topic from the user, automatically locates the matching vibe marketing report, conducts thorough keyword research and competitive SERP analysis using DataForSEO, and generates a detailed blog brief following the established structure with strategic quote placeholders for landowner podcast interviews.

**Output**: A complete blog brief saved to the Finished Content folder, ready for the content team to use.

## Instructions

### Step 1: Accept Blog Topic and Find Marketing Report

#### 1.1 Get the Blog Topic

Accept the exact blog topic from the user. Examples:
- "Top 5 Cold-Weather Hunting Gear Essentials for 2026"
- "How to Price Your Hunting Land for Maximum Revenue"
- "Best Trail Cameras for Wildlife Monitoring on Private Land"

#### 1.2 Extract Key Search Terms

From the topic, extract 2-4 key phrases for matching against reports. Remove common modifiers and focus on the core subject matter.

Examples:
- "Top 5 Cold-Weather Hunting Gear Essentials for 2026" → ["cold weather hunting gear", "hunting gear essentials", "winter hunting"]
- "How to Price Your Hunting Land" → ["price hunting land", "hunting land revenue", "land pricing"]

Convert to lowercase for case-insensitive matching.

#### 1.3 Search Marketing Reports

1. Use `Glob` to find all marketing reports:
   - Pattern: `*.md`
   - Path: `/Users/zacharygeleott/Downloads/TakeOff - LandTrust/Research/`
   - This returns all available reports (currently 16 reports from Aug-Dec 2025)

2. Use `Grep` to search for the topic across all reports:
   - Pattern: Use the key search terms from step 1.2
   - Set `-i: true` for case-insensitive search
   - Set `output_mode: "content"` to see context around matches
   - Try searching for the most specific phrase first (e.g., "cold weather hunting gear")

3. If no exact matches found, try progressively broader searches:
   - Search for individual terms separately
   - Look for partial matches or related concepts

#### 1.4 Handle Matching Logic

**One match found:**
- Proceed with that report

**Multiple matches found:**
- Use the most recent report (latest date in filename)
- Inform the user which report was selected

**No matches found:**
- Ask the user: "I couldn't find a marketing report matching this topic. Would you like to:
  1. Provide the report date/week (e.g., '12.10.25')
  2. Proceed without report context (generate from keyword research only)
  3. Modify the topic and search again"
- If user provides date, read that specific report
- If user chooses option 2, skip to Step 2 (Keyword Research)

#### 1.5 Extract Report Context

Once the matching report is identified:

1. **Read the report file** using the `Read` tool

2. **Find the Blog Ideas section:**
   - Look for headers like "Section 4: Blog and Video Content Ideas" (common in Hunting reports)
   - Or "Blog and Video Content Ideas" (common in Agriculture reports)
   - Section numbering may vary between Hunting and Agriculture

3. **Locate the specific blog idea:**
   - Search for the user's topic or close variations
   - Extract the full idea description and any associated rationale

4. **Extract supporting context from earlier sections:**
   - Section 1: Key Market Trends and Sentiment (most discussed topics, emotional tone)
   - Section 2: Customer Pain Points and Desires (specific pain points with quotes)
   - Section 3: SEO Opportunities (related keyword ideas)
   - Look for relevant pain points, quotes, and insights that relate to the blog topic

5. **Determine topic category:**
   - Is this a Hunting topic or Agriculture/Business topic?
   - This affects the angle and LandTrust value proposition later

---

### Step 2: Conduct Keyword Research and SERP Analysis

#### 2.1 Identify Primary Keyword

Extract the main keyword phrase from the topic:
- Remove modifiers like "Top 5", "Best", "How to", year numbers (2026)
- Keep the core subject matter
- Typical length: 2-5 words

Examples:
- "Top 5 Cold-Weather Hunting Gear Essentials for 2026" → "cold weather hunting gear"
- "Best Trail Cameras for Wildlife Monitoring" → "trail cameras wildlife monitoring"

#### 2.2 Get Primary Keyword Data

Use `mcp__dataforseo-api__get_keyword_data`:

```
keyword: [primary keyword from 2.1]
location_code: 2840
language_code: "en"
search_engine: "google"
```

**Extract and record:**
- Average monthly search volume
- Monthly trend data (identify peak months and off-season)
- Cost-per-click (CPC)
- Competition level (High/Medium/Low)

**Example output to note:**
- "cold weather hunting gear" → 1,900 avg monthly, peaks at 5,400 in Nov, $1.76 CPC, High competition

#### 2.3 Get Related Keywords

Use `mcp__dataforseo-api__get_keyword_suggestions`:

```
keyword: [primary keyword]
location_code: 2840
language_code: "en"
limit: 100
```

**Categorize the results into:**

1. **High-Value Secondary Keywords** (5-7 keywords):
   - Search volume: 500-2,000+ monthly
   - Closely related to primary topic
   - High CPC indicating commercial intent

2. **Long-Tail Keywords** (10-15 keywords):
   - Search volume: 50-500 monthly
   - More specific variations
   - Question-based queries (what, how, why, when)

3. **Related Queries**:
   - Broader topic variations
   - Adjacent topics worth mentioning

#### 2.4 Analyze Primary Keyword SERP

Use `mcp__dataforseo-api__get_serp_results`:

```
keyword: [primary keyword]
location_code: 2840
language_code: "en"
search_engine: "google"
depth: 20
device: "desktop"
```

**Document the following:**

1. **Top-Ranking Content Types** (analyze top 10 results):
   - Product roundups/listicles
   - E-commerce category pages
   - Educational guides
   - Community discussions (Reddit, forums)
   - Video content
   - Brand-specific content
   - Note the domains (e.g., Outside Online, REI, Bass Pro)

2. **SERP Features Present:**
   - Featured snippets
   - People Also Ask (PAA) boxes → **Extract these questions**
   - Refinement chips
   - Popular Products carousel
   - Video carousel
   - Discussions and Forums widget
   - Related Searches → **Extract these queries**
   - Local pack (if applicable)

3. **Content Patterns:**
   - Typical word count (check meta descriptions or note comprehensiveness)
   - Structure patterns (listicles vs guides vs comparisons)
   - Visual elements (product images, tables, infographics)

4. **Competitor Domains** (top 5-7):
   - Who is ranking? (brands, publishers, communities)
   - What type of authority? (e-commerce, editorial, user-generated)

#### 2.5 Analyze Secondary Keyword SERPs

Select 3-5 high-value secondary keywords from step 2.3.

For each, run `mcp__dataforseo-api__get_serp_results` with same parameters.

**Compare and note:**
- Variations in competition (are different sites ranking?)
- Different SERP features
- Opportunities where competition is weaker
- Related topics that emerge across multiple SERPs

#### 2.6 Conduct Competitive Gap Analysis

Based on all SERP data collected, identify:

**What Competitors Are Doing Well:** (4-5 points)
- Format: ✅ **[Publisher/Brand]:** [Specific strength with detail]
- Examples:
  - ✅ **Outside Online:** Comprehensive testing methodology (8 testers, 1,115 miles), specific product recommendations with pros/cons
  - ✅ **Fieldsheer:** Simple, digestible 3-layer system education; strong focus on heated gear technology
  - ✅ **Reddit discussions:** Real-world user experiences, brand comparisons, budget-friendly alternatives

**Critical Content Gaps & Opportunities:** (5-6 gaps)
- Format:
  ```
  [Number]. **❌ Missing: [What's Missing]**
     - Current situation: [What competitors aren't doing]
     - Opportunity: [How LandTrust can fill this gap]
     - Angle: [Specific approach or example]
  ```

**Focus on LandTrust's unique angles:**
- Connection to private land hunting/farming access
- Budget tiers (Good/Better/Best) when competitors only feature premium
- Hunting style or farming operation context (stationary vs mobile, small farm vs large operation)
- Regional/climate context (Midwest vs Mountain West vs Southeast)
- Practical preparation tips beyond just "what to buy"
- Integration with LandTrust platform benefits

---

### Step 3: Generate the Blog Brief

Generate a comprehensive brief with all 12 sections following the exact structure of the reference brief at:
`/Users/zacharygeleott/Downloads/TakeOff - LandTrust/Finished Content/Cold_Weather_Hunting_Gear_Blog_Brief_2026.md`

Use the current date for the brief date.

#### Section 1: Title and Metadata

```markdown
# [Blog Topic Exactly as Provided by User]

**Date:** [Today's date - format: Month DD, YYYY]
**Prepared by:** TakeOff LLC
**Target Publication:** [Calculate based on seasonality from keyword data]
```

**For Target Publication:**
- If keyword has clear seasonality (3x+ surge in specific months):
  - Format: "Q[quarter] [year] (Peak seasonality: [months])"
  - Example: "Q4 2025 / Q1 2026 (Peak seasonality: November-January)"
  - Recommend publishing 6-8 weeks before peak
- If evergreen (no strong seasonality):
  - Format: "Q[current quarter] [year] (Evergreen topic)"

Add separator:
```markdown
---
```

#### Section 2: Primary SEO/LLM Target Keywords

Organize keywords from Step 2.2-2.3 into three subsections:

```markdown
## Primary SEO/LLM Target Keywords

### High-Value Primary Keywords
```

List 5-7 keywords with highest volume/CPC:
- Format: `**[keyword]** ([avg monthly] avg monthly / [peak monthly] in [peak month] | $[CPC] CPC | [competition level] competition)`
- Example: `**cold weather hunting gear** (1,900 avg monthly / 5,400 in Nov | $1.76 CPC | High competition)`
- For keywords without seasonality: `**[keyword]** ([avg monthly] avg monthly | $[CPC] CPC | [competition level] competition)`

```markdown
### Secondary & Long-Tail Keywords
```

List 10-15 supporting keywords:
- Same format as above
- Mix of medium-volume secondaries and long-tail variations
- Include question-based queries if identified

```markdown
### Related Search Queries (From SERP)
```

List 5-10 queries extracted from PAA boxes and Related Searches:
- Format as quoted phrases: `"query text here"`
- These are actual user queries from Google SERP features

#### Section 3: Search Demand & Opportunity

```markdown
## Search Demand & Opportunity

### Search Volume & Seasonality Insights
```

Analyze the keyword trend data:
- **Peak Season:** [Identify peak months with search volumes]
- **Off-Season Baseline:** [Identify low months with volumes]
- **Annual Growth Pattern:** [Calculate surge multiplier - e.g., "3x-7x surge during peak months"]
- **Purchase Intent:** [Interpret CPC levels - High CPC ($2+) = strong commercial intent, Low CPC (<$1) = informational]

Example:
```markdown
- **Peak Season:** November (5,400 searches for primary keyword) - December (3,600 searches) - January (2,400 searches)
- **Off-Season Baseline:** 390-720 monthly searches (June-July)
- **Annual Growth Pattern:** 3x-7x surge in search volume during peak hunting months
- **Purchase Intent:** High CPC ($1.76-$2.57) indicates strong commercial intent and buyer readiness
```

```markdown
### SERP Landscape Analysis
**Current Top-Ranking Content Types:**
```

List 5-7 content types from step 2.4, with specific examples:
1. **[Content type]** - [Specific sites] ([brief description])
2. **[Content type]** - [Specific sites] ([brief description])

Example:
```markdown
1. **Product roundups** - Outside Online, Bowhunter (comprehensive gear reviews)
2. **E-commerce category pages** - Sitka, KUIU, First Lite, Drake Waterfowl (product catalogs)
3. **Educational guides** - Fieldsheer (3-layer system guide)
```

```markdown
**SERP Features Present:**
```

List all SERP features observed:
- Refinement chips ([examples of chips if relevant])
- Popular Products carousel ([note if present])
- Discussions and Forums widget
- Video carousel
- People Also Ask
- Related Searches
- [Any other features]

```markdown
### Competitive Gap Analysis

**What Competitors Are Doing Well:**
```

List 4-5 strengths from step 2.6:
- Format: `✅ **[Publisher]:** [Specific strength with details]`

```markdown
**Critical Content Gaps & Opportunities:**
```

List 5-6 gaps from step 2.6:
- Format as outlined in step 2.6
- Each gap should have: Missing element, LandTrust opportunity, Specific angle

#### Section 4: Blog Structure & Outline

```markdown
## Blog Structure & Outline

**Target Word Count: 2,200-2,500 words**
```

Create a detailed outline with the following structure:

**Introduction Section:**
```markdown
### **Introduction ([150-200 words])**
- **Hook:** [Opening statement that grabs attention, relates to pain point or interesting fact]
- **Context:** [Reference pain points or insights from the marketing report]
- **The Problem:** [What challenge does this article address?]
- **The Solution:** [Preview of what the article will cover]
- **LandTrust Connection:** [How this relates to LandTrust's value proposition - private land access, better hunting/farming outcomes]
- **What's covered:** [Brief preview of main sections]

**Word Count:** 150-200 words

---
```

**Main Content Sections:**

Determine the appropriate number of main sections based on the topic:
- "Top 5" topics → 5 main sections (one per item)
- "Top 10" topics → 10 main sections
- "How to" guides → 4-6 sections covering key steps
- Comprehensive guides → 5-7 thematic sections

For each main section, use this template:

```markdown
### **[Number]. [Section Title]: [Descriptive Subtitle] ([Word Count])**

**Target Keywords:** "[keyword1]," "[keyword2]," "[keyword3]"

**Content Structure:**

**Opening ([word count]):**
- [Hook or key point for this section]
- [Why this section matters]

**[Subsection Name] ([word count]):**
- [Detailed points, recommendations, or explanations]
- [Specific data, examples, or evidence]
- [Bullet points or structured information]

**[Additional Subsection Name] ([word count]):**
- [Continue with more subsections as needed]
- [Ensure each subsection has a clear purpose]

**[Another Subsection if Needed] ([word count]):**
- [More detailed content]

**Pro Tip ([word count]):**
"[Practical, actionable tip that connects to LandTrust's value proposition. Should feel like advice from an experienced hunter/farmer to a peer. Connect to private land benefits when relevant.]"

[QUOTE: [Specific person type/topic for quote - e.g., "Midwest landowner about hosting winter hunters" or "Hunter testimonial about gear failure in extreme cold"]]

**Word Count:** [Total word count for section]

---
```

**Guidelines for each section:**
- Word count: 400-450 words for "Top X" items, adjust for other formats
- Include specific, actionable information (not generic filler)
- Use subsections to organize information (What to Look For, Types/Options, Recommendations by Budget, etc.)
- Include data points, specific examples, temperature ranges, price ranges
- Pro Tip should be practical and connect to LandTrust when possible
- Each section gets 1-2 quote placeholders

**Quote Placeholder Strategy:**
- Total placeholders across outline: 8-12
- Placement: After key claims that need real-world validation
- Be specific about the quote context:
  - `[QUOTE: Midwest landowner about winter hunting success and longer sits on private land]`
  - `[QUOTE: Hunter testimonial about gear failure in 10°F weather]`
  - `[QUOTE: LandTrust+ member about exclusive access benefits]`
  - `[QUOTE: Agriculture landowner about hosting agritourism in shoulder season]`
- Distribute evenly: 1-2 per main section

**Conclusion Section:**
```markdown
### **Conclusion & Call-to-Action ([150-200 words])**

**Recap ([word count]):**
- [Summarize the key takeaways - e.g., the X essentials covered]
- [Reinforce the value of following this advice]
- [Note about budget options vs premium - accessibility]

**LandTrust Connection ([word count]):**
"[Connect the blog topic to LandTrust's value proposition. For hunting: private land access, no competition, longer sits, better results. For agriculture: monetize land, connect with market, sustainable income.]"

**Primary CTA:**
- **Button/Link:** "[Specific CTA text - e.g., 'Find Your Perfect Cold-Weather Hunt on LandTrust']"
- **Supporting text:** "[Brief supporting text explaining the action]"

**Secondary mention:**
- "[Alternative CTA - e.g., for landowners if primary is for hunters, or vice versa]"

**Word Count:** 150-200 words

---
```

**Total Word Count Summary:**
```markdown
## **TOTAL ESTIMATED WORD COUNT: 2,200-2,500 words**

Breakdown:
- Intro: [word count] words
- [Section 1 name]: [word count] words
- [Section 2 name]: [word count] words
- [Continue for all sections]
- Conclusion: [word count] words
- **Total: ~[sum] words**

---
```

#### Section 5: Content Gaps Filled & Competitive Advantages

```markdown
## Content Gaps Filled & Competitive Advantages

| **Competitor Weakness** | **LandTrust Opportunity** | **How This Brief Addresses It** |
|-------------------------|---------------------------|----------------------------------|
```

Create 5-6 rows mapping the gaps from step 2.6 to how this brief addresses them:

Format each row:
- **Competitor Weakness:** [What competitors are missing]
- **LandTrust Opportunity:** [How LandTrust can uniquely fill this]
- **How This Brief Addresses It:** [Specific way this outline incorporates the opportunity]

Example row:
```markdown
| Generic national content | Regional/temperature context | Brief mentions of Midwest vs. Mountain West, temperature ranges woven into each section |
```

```markdown
---
```

#### Section 6: Keyword Targeting Strategy

```markdown
## Keyword Targeting Strategy

### Title Options (Choose One):
```

Provide 3 title variations:
1. **"[Title option 1]"** ✅ RECOMMENDED ([Brief reasoning why recommended])
2. **"[Title option 2]"** ([How it differs, pros/cons])
3. **"[Title option 3]"** ([How it differs, pros/cons])

**Title best practices:**
- Include primary keyword
- Keep under 60 characters for SEO
- Include year if topic is annual/seasonal
- Front-load the important keywords
- Make it compelling and clear

```markdown
### Meta Description (155 characters):
```

Write a compelling meta description:
- Must be 155 characters or less (including spaces)
- Include primary keyword naturally
- Include a benefit or value proposition
- Include call-to-action if space permits
- Example: "Don't let cold weather end your hunt early. Get the top 5 cold-weather hunting gear essentials for 2026, from jackets to boots, with budget-friendly options."

```markdown
### URL Slug:
```

`/blog/[topic-slug-year]`
- Use primary keywords
- Replace spaces with hyphens
- Include year if relevant
- Keep concise (5-8 words max)
- Example: `/blog/cold-weather-hunting-gear-essentials-2026`

```markdown
### Header Tag Strategy:
```

Outline the H1/H2/H3 hierarchy:
- **H1:** [Title with primary keyword]
- **H2:** [List all main section titles - typically 7-10 H2s including intro and conclusion]
- **H3:** [List subsection types - e.g., "What to Look For," "Recommendations by Budget," "Pro Tip"]

```markdown
### Internal Linking Opportunities:
```

Suggest 4-5 internal links to other LandTrust pages:
- Link to property search pages (filtered by state/region if relevant)
- Link to related blog posts (if they exist or plan to exist)
- Link to landowner signup page
- Link to how-to or getting started pages
- Examples:
  - "How to Find Private Hunting Land in [Your State]"
  - "Private Land vs. Public Land Hunting: Which is Right for You?"
  - "Late-Season Deer Hunting: Tips for Success"

```markdown
### External Linking Strategy:
```

Suggest 3-4 authority sources to link to:
- State wildlife agencies (for regulations, seasons, requirements)
- Manufacturer product pages (for specific gear recommendations - potential affiliate links)
- Authoritative guides (REI's layering guide, outdoor publications)
- Research or data sources (if citing statistics or studies)

```markdown
---
```

#### Section 7: Visual Content Recommendations

```markdown
## Visual Content Recommendations

**Essential for SEO and engagement:**

1. **Hero Image:**
   - [Describe ideal hero image specific to topic]
   - Alt text: "[SEO-optimized alt text with primary keyword]"
```

Examples:
- "Hunter wearing insulated cold weather hunting gear in winter tree stand"
- "Farmer walking through regenerative grazing pasture with cattle in background"

```markdown
2. **Product/Section Images:**
   - [3-5 specific image recommendations for main sections]
   - Use manufacturer product photos (link to affiliate pages if possible)
   - Format: Side-by-side comparison of Budget vs. Premium options
```

```markdown
3. **Simple Infographic (Optional but Recommended):**
   - [Describe 1-2 infographic concepts specific to topic]
   - Quick reference for readers
```

Examples:
- "The 3-Layer System for Cold-Weather Hunting" visual
- "Temperature-Based Gear Selection Chart"
- "Annual Farm Revenue Streams Calendar"

```markdown
4. **Comparison Table:**
   - [Describe 1-2 comparison table ideas]
   - Should simplify complex decisions
```

Examples:
- "Insulation Guide: How Much Do You Need?" (temperature ranges, recommended gear, hunting style)
- "Pricing Strategies Comparison" (day rate vs seasonal vs membership models)

```markdown
5. **Embedded Video (If Available):**
   - If LandTrust has video of [relevant scenario], embed it
   - If not, consider creating a simple [duration]-second [topic] video
```

```markdown
---
```

#### Section 8: Promotion & Distribution Strategy

```markdown
## Promotion & Distribution Strategy

### SEO Optimization:
- **Publish timing:** [Month/quarter based on seasonality - recommend 6-8 weeks before peak]
- **Update annually:** [Refresh strategy - e.g., "Refresh with new gear and update year in title"]
- Target featured snippet: [Specific strategy - e.g., "Structure intro with bulleted list of 5 essentials at top"]
- Optimize for People Also Ask:
  - "[PAA question 1 from SERP data]"
  - "[PAA question 2 from SERP data]"
  - "[PAA question 3 from SERP data]"
```

```markdown
### Social Media:
- **Instagram:** [Specific post idea with format - e.g., carousel, reel, static]
- **Facebook:** [Specific post idea with pull quote or angle]
- **Pinterest:** [Pin strategy - e.g., "Create vertical pins for each gear essential"]
```

```markdown
### Email Marketing:
- Newsletter feature with subject line: "[Compelling subject line]"
- Segment:
  - **[Primary audience]:** [What to emphasize in email]
  - **[Secondary audience]:** [What to emphasize in email]
```

```markdown
### Partnerships:
- [2-3 partnership ideas - brand outreach, forum sharing, influencer collaboration]
```

```markdown
---
```

#### Section 9: Success Metrics & KPIs

```markdown
## Success Metrics & KPIs

**Track these to measure performance:**

1. **Organic Traffic:**
   - Goal: [Realistic session target] organic sessions in first 3 months
   - Track rankings for "[primary keyword]" and related keywords

2. **Engagement:**
   - Avg. time on page: [Target based on word count - typically 3-5 minutes for 2,500 words]
   - Scroll depth: [Target %] reach conclusion
   - Bounce rate: [Target % - typically <60%]

3. **Conversions:**
   - Click-through rate on CTAs: [Target % - typically 8-12%]
   - Property search clicks from blog: Track via UTM parameters
   - [Other relevant conversion - e.g., landowner signups, membership clicks]

4. **Social Shares:**
   - Goal: [Number]+ shares across platforms in first month

5. **Featured Snippet:**
   - Goal: Capture featured snippet for 1-2 related queries within 6 months

---
```

#### Section 10: Notes for Content Writer

```markdown
## Notes for Content Writer

### Tone & Voice:
- **Voice:** [Describe the voice - e.g., "Experienced hunting buddy giving straight advice" or "Knowledgeable farmer sharing practical wisdom"]
- **POV:** Second person ("you")—direct and conversational
- **Avoid:**
  - Generic filler ("As we all know...")
  - Repetitive AI phrasing
  - Overly technical jargon without explanation
  - Excessive superlatives ("the absolute best," "amazing," "incredible")

### Key Messaging:
- **Core:** [Primary message - e.g., "The right gear = longer hunts = better success. It's an investment, not an expense."]
- **LandTrust angle:** [How to weave in value prop - e.g., "Private land access means you can afford to sit longer and hunt smarter—but only if your gear keeps you comfortable."]
- **[Third key message]:** [e.g., "Budget-friendly: You don't need to spend $3K to hunt in winter, but don't cheap out on boots or base layers."]

### Writing Tips:
- **Be specific:** Use real temps, real product names, real scenarios
- **Short sentences:** Break up long paragraphs—this is digital content, not a novel
- **Use transitions:** Connect sections smoothly so it flows
- **Practical tips:** Every section should have actionable advice readers can use immediately

### Research Sources:
- Reference the [report date] report for [topic] pain points
- Cite gear testing sources or relevant publications
- Link to manufacturer specs for accuracy
- [Any other specific sources to consult]

### Word Count Target:
- **Target:** 2,200-2,500 words
- **Acceptable range:** 2,000-2,600 words
- Each main section should be [word count] words (roughly equal length for consistency)

---
```

#### Section 11: Future Content Spinoffs

```markdown
## Future Content Spinoffs

**This article can spawn several related posts:**
```

List 3-5 related article ideas:

Format:
```markdown
1. **"[Spinoff Title]"** ([Word count])
   - [Brief description of angle and content]
   - [Why it's valuable]
```

**Spinoff guidelines:**
- Should extend or deep-dive into topics mentioned in main article
- Create a content cluster with internal linking opportunities
- Mix of longer guides (1,500+ words) and shorter focused pieces (700-1,000 words)

Examples for hunting gear article:
- "Heated Hunting Gear: Is It Worth the Investment?" (700-900 words)
- "How to Layer for Cold-Weather Hunting: The Complete System" (1,000-1,200 words)
- "Landowner's Guide to Hosting Winter Hunters" (800-1,000 words)

```markdown
These can be published over the next few months to build a [topic area] content cluster with internal linking.

---
```

#### Section 12: Conclusion

```markdown
## Conclusion

This [adjective describing approach] blog brief creates a **focused, practical, 2,200-2,500 word guide** that:

1. **Ranks for high-value keywords** with [describe intent - e.g., strong commercial intent]
2. **Provides immediate value** to readers without overwhelming them
3. **Fills competitor gaps** ([list 2-3 key gaps addressed])
4. **Drives conversions** by connecting [topic] to LandTrust's value prop
5. **Is actually readable** unlike competitors' [describe competitor weakness]

**Key differentiator:** [Summarize what makes this brief unique and valuable]

**Next Steps:**
1. Assign to writer with [timeframe] deadline
2. Source/create [list visual assets needed]
3. Set up tracking (Google Analytics, Search Console)
4. Plan promotion calendar (email, social, partnerships)
5. Publish by [recommended publish date] for [explain timing rationale]

---

**End of Blog Brief**
```

---

### Step 4: Save the Blog Brief

#### 4.1 Generate Filename

Create the filename following this pattern:
- Base pattern: `[Topic_Keywords]_Blog_Brief_[Year].md`
- Process:
  1. Extract 3-5 key words from the topic
  2. Replace spaces with underscores
  3. Remove special characters (except underscores)
  4. Capitalize first letter of each word
  5. Add year from topic or use current year
  6. Keep total filename under 60 characters if possible

Examples:
- "Top 5 Cold-Weather Hunting Gear Essentials for 2026" → `Cold_Weather_Hunting_Gear_Blog_Brief_2026.md`
- "How to Price Your Hunting Land for Maximum Revenue" → `Price_Hunting_Land_Revenue_Blog_Brief_2026.md`
- "Best Trail Cameras for Wildlife Monitoring" → `Trail_Cameras_Wildlife_Monitoring_Blog_Brief_2026.md`

#### 4.2 Write to Finished Content Folder

Use the `Write` tool:
- Path: `/Users/zacharygeleott/Downloads/TakeOff - LandTrust/Finished Content/[filename].md`
- Content: The complete brief with all 12 sections from Step 3

#### 4.3 Confirm Completion

Display a summary to the user:

```
Blog brief generated successfully!

📄 File: [full file path]

🎯 Primary Keywords:
  1. [keyword] ([volume]/mo, $[CPC] CPC)
  2. [keyword] ([volume]/mo, $[CPC] CPC)
  3. [keyword] ([volume]/mo, $[CPC] CPC)
  4. [keyword] ([volume]/mo, $[CPC] CPC)
  5. [keyword] ([volume]/mo, $[CPC] CPC)

📝 Target Word Count: 2,200-2,500 words
📅 Recommended Publish Date: [date based on seasonality]
🗂️ Marketing Report Used: [report filename]

The brief includes:
✓ 12 comprehensive sections
✓ [number] strategic quote placeholders
✓ Detailed keyword research ([number] keywords analyzed)
✓ Competitive SERP analysis ([number] competitors reviewed)
✓ Content gap analysis with LandTrust opportunities

Ready for your content team!
```

---

## Edge Cases and Error Handling

### No Matching Report Found

**Symptoms:** Grep returns no results for any search terms

**Actions:**
1. Inform user: "I couldn't find a marketing report matching '[topic]'. Would you like to:"
2. Offer options:
   - Provide the report date/week (e.g., '12.10.25')
   - Proceed without report context (generate from keyword research only)
   - Modify the topic and search again
3. If user provides date:
   - Read `/Users/zacharygeleott/Downloads/TakeOff - LandTrust/Research/[date]_report.md`
   - Continue with extraction
4. If user chooses to proceed without report:
   - Skip Step 1.5 (context extraction)
   - Generate brief based entirely on keyword research
   - Note in "Notes for Content Writer" that no report context was available

### Multiple Reports Match

**Symptoms:** Grep finds topic in 2+ reports

**Actions:**
1. Parse dates from filenames (format: MM.DD.YY_report.md)
2. Select the most recent (latest date)
3. Inform user: "Found topic in multiple reports. Using the most recent: [filename]"
4. Continue with that report

### Keyword Has No or Low Search Volume

**Symptoms:** DataForSEO returns no data or very low volume (<10/month)

**Actions:**
1. Try variations:
   - Remove year from keyword
   - Try singular/plural variations
   - Broaden the keyword (remove modifiers)
2. If still low:
   - Rely heavily on keyword suggestions to find related terms with data
   - Note in brief: "Primary keyword has limited search data. Recommendations based on related keywords with stronger metrics."
3. Focus more on qualitative competitive analysis from SERP results

### SERP Results Limited or Missing

**Symptoms:** SERP results have few competitors or limited data

**Actions:**
1. Try alternative keyword variations
2. Optionally use `mcp__firecrawl__firecrawl_search`:
   - Search for the primary keyword
   - Manually analyze top results
   - Document what types of content appear
3. Note in brief: "SERP data limited. Analysis based on manual search and available results."
4. Focus on differentiation through LandTrust's unique value props

### DataForSEO API Errors

**Symptoms:** API returns error or times out

**Actions:**
1. Retry once with same parameters
2. If retry fails:
   - Continue with available data
   - Note in brief which data is missing
   - Example: "SERP analysis unavailable due to API limitations. Recommendations based on keyword data and manual research."
3. User can still get a valuable brief from partial data

### Filename Already Exists

**Symptoms:** File exists at target path

**Actions:**
1. Inform user: "A brief with this filename already exists: [filename]"
2. Offer options:
   - Overwrite the existing file
   - Create new version with suffix: `_v2.md`, `_v3.md`, etc.
   - Create new version with date: `_Dec2025.md`
3. Default to creating new version to preserve work
4. Execute based on user choice

---

## Performance Considerations

**Expected API Calls per Brief:** 10-15 total
- 1x `mcp__dataforseo-api__get_keyword_data` (primary keyword)
- 1x `mcp__dataforseo-api__get_keyword_suggestions` (100 limit)
- 4-6x `mcp__dataforseo-api__get_serp_results` (primary + 3-5 secondaries)
- Optional: 1-2x `mcp__firecrawl__firecrawl_search` (if needed for backup research)

**Estimated Completion Time:** 3-5 minutes per brief

**File Operations:** Minimal
- Multiple reads (reports, existing briefs for reference)
- 1 write operation (final brief)

**Rate Limiting Awareness:**
- DataForSEO APIs may have rate limits
- If rate limited, wait and retry
- Can complete brief with partial data if necessary

---

## Quality Checks Before Completion

Before confirming completion to the user, verify:

- [ ] All 12 sections are present in the brief
- [ ] 8-12 quote placeholders included with specific context
- [ ] Keyword data includes volume, CPC, and competition for primary + secondaries
- [ ] SERP analysis mentions at least 5 competitor examples
- [ ] Content gaps section has 5-6 specific opportunities
- [ ] Blog outline totals 2,200-2,500 words across all sections
- [ ] Each main section has word count targets
- [ ] File saved to correct location: `/Users/zacharygeleott/Downloads/TakeOff - LandTrust/Finished Content/`
- [ ] Filename follows naming convention
- [ ] Report context (if available) incorporated into gaps/opportunities and outline
- [ ] Title options provided (3 variations)
- [ ] Meta description is 155 characters or less
- [ ] URL slug is clean and includes keywords

---

## Example Execution

**User Input:**
```
/blog-brief-generator Top 5 Cold-Weather Hunting Gear Essentials for 2026
```

**Skill Execution Flow:**

1. **Extract key terms:** "cold weather hunting gear", "hunting gear essentials", "winter hunting"

2. **Search reports:**
   - Glob finds 16 reports in Research/
   - Grep searches for "cold weather hunting gear"
   - Match found in `12.10.25_report.md` at line 172

3. **Read report context:**
   - Section 4 Blog Ideas: "Top 5 Cold-Weather Hunting Gear Essentials for 2026 - Timely with the winter season approaching, providing practical gear recommendations."
   - Section 2 Pain Points: References to Mr. Buddy heater issues, gear failures in extreme cold, trail cam performance in cold
   - Context: Midwest focus, late-season hunting challenges

4. **Keyword research:**
   - Primary: "cold weather hunting gear"
     - 1,900 avg monthly, peaks at 5,400 in Nov, $1.76 CPC, High competition
   - Suggestions: Returns 87 related keywords
   - Identified secondaries: "best cold weather hunting gear" (1,000/mo), "cold weather hunting clothes" (1,900/mo), etc.

5. **SERP analysis:**
   - Primary keyword: Outside Online, Sitka, KUIU, Fieldsheer, Reddit, Bass Pro in top 10
   - SERP features: PAA box, refinement chips, popular products, related searches
   - Secondary keywords: Similar competitors, some variation in rankings
   - Gaps identified: No private land connection, no budget tiers, no hunting style context, generic regional approach

6. **Generate brief:**
   - All 12 sections populated with data
   - 10 quote placeholders strategically placed (e.g., "[QUOTE: Midwest landowner about hosting winter hunters]")
   - Outline: Introduction (175 words) + 5 gear sections (425 words each) + Conclusion (175 words) = 2,475 words
   - Content gaps table: 6 gaps mapped to LandTrust opportunities
   - Keyword targeting: 3 title options, meta description, URL slug, internal/external links
   - Visual recs: Hero image, product photos, 3-layer system infographic, insulation comparison table

7. **Save:**
   - Filename: `Cold_Weather_Hunting_Gear_Blog_Brief_2026.md`
   - Path: `/Users/zacharygeleott/Downloads/TakeOff - LandTrust/Finished Content/Cold_Weather_Hunting_Gear_Blog_Brief_2026.md`

8. **Confirm:**
   ```
   Blog brief generated successfully!

   📄 File: /Users/zacharygeleott/Downloads/TakeOff - LandTrust/Finished Content/Cold_Weather_Hunting_Gear_Blog_Brief_2026.md

   🎯 Primary Keywords:
     1. cold weather hunting gear (1,900/mo, $1.76 CPC)
     2. best cold weather hunting gear (1,000/mo, $2.57 CPC)
     3. cold weather hunting clothes (1,900/mo, $1.76 CPC)
     4. warmest hunting clothes (1,000/mo, $1.64 CPC)
     5. extreme cold weather hunting clothes (480/mo, $1.53 CPC)

   📝 Target Word Count: 2,200-2,500 words
   📅 Recommended Publish Date: October 2025 (6-8 weeks before Nov peak)
   🗂️ Marketing Report Used: 12.10.25_report.md

   The brief includes:
   ✓ 12 comprehensive sections
   ✓ 10 strategic quote placeholders
   ✓ Detailed keyword research (87 keywords analyzed)
   ✓ Competitive SERP analysis (8 competitors reviewed)
   ✓ Content gap analysis with LandTrust opportunities

   Ready for your content team!
   ```

---

**End of Skill Instructions**
