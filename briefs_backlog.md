# Briefs Backlog — Weeks 17-33 (v2 SEMRUSH)

This is the work queue for the cloud routine. Each row is one blog brief to generate.

**How the cloud routine uses this:**
1. Read this file. Find the first 2 rows with `status: pending`.
2. For each: read `seo_data/<slug>.json` for prefetched DataForSEO data, grep `Research/` for matching marketing report, generate the brief following `.claude/skills/blog-brief-generator/SKILL.md`, save to `Finished Content/v2 - SEMRUSH/Week <N>/<filename>.md`.
3. Mark the rows `status: done` here, commit, push.
4. When all rows are `done`, write `DONE.md` and disable itself.

**Output destination:** `Finished Content/v2 - SEMRUSH/Week <N>/` (use existing folders; create Week 17–33 folders if missing).

**Filename pattern:** matches existing v2 briefs — `<Topic_Words>_Blog_Brief_2026.md` (Title_Case_With_Underscores).

---

| ID    | Week | Day | Topic                                                                              | Primary Keyword                          | Slug                                    | Pillar             | Status  |
|-------|------|-----|------------------------------------------------------------------------------------|------------------------------------------|-----------------------------------------|--------------------|---------|
| W17a  | 17   | Tue | Maryland Hunting Seasons & Licensing: Your Complete 2026-2027 Reference            | maryland hunting seasons                 | maryland_hunting_seasons                | P1: State Seasons  | done    |
| W17b  | 17   | Thu | Best Choke for Duck Hunting: 12 Gauge Patterns and Recs                            | best choke for duck hunting              | best_choke_duck_hunting                 | P4: Gear           | done    |
| W18a  | 18   | Tue | New Hampshire Hunting & Fishing Seasons: Dates, Rules, and Access                  | new hampshire hunting seasons            | new_hampshire_hunting_seasons           | P1: State Seasons  | done    |
| W18b  | 18   | Thu | Best Shotgun Cleaning Kits and Maintenance Tips                                    | best shotgun cleaning kit                | best_shotgun_cleaning_kit               | P4: Gear           | done    |
| W19a  | 19   | Tue | Massachusetts Deer Hunting Season: Zones, Dates, and Tag Rules                     | massachusetts deer hunting season        | massachusetts_deer_hunting_season       | P1: State Seasons  | done    |
| W19b  | 19   | Thu | Squirrel Hunting Season: Regulations, Tips, and Why It's Underrated                | squirrel hunting season                  | squirrel_hunting_season                 | P3: Species        | done    |
| W20a  | 20   | Tue | West Virginia Hunting & Fishing Regulations: Your 2026-2027 Guide                  | west virginia hunting seasons            | west_virginia_hunting_seasons           | P1: State Seasons  | done    |
| W20b  | 20   | Thu | How to Set Rules, Pricing, and Guest Expectations on Your Land                     | hunting lease pricing                    | hunting_lease_rules_pricing             | P5: Landowner      | done    |
| W21a  | 21   | Tue | Waterfowl Hunting Seasons & Regulations: Duck and Goose Guide                      | waterfowl hunting seasons                | waterfowl_hunting_seasons               | P3: Species        | done    |
| W22a  | 22   | Tue | Deer Hunting and Management: From Habitat to Harvest                               | deer hunting and management              | deer_hunting_management                 | P3: Species        | done    |
| W22b  | 22   | Thu | North Alabama Cave and Land Trusts: Conservation Meets Recreation                  | north alabama land trust                 | north_alabama_land_trusts               | P7: Conservation   | done    |
| W23a  | 23   | Tue | Calendar of Hunting Seasons by State: When to Apply, When to Hunt                  | hunting season calendar by state         | hunting_seasons_calendar_by_state       | P2: Licenses       | done    |
| W24a  | 24   | Tue | Deer Baiting Laws by State: What's Legal and What's Not                            | deer baiting laws by state               | deer_baiting_laws_by_state              | P3: Species        | done    |
| W24b  | 24   | Thu | Private Land Wildlife Management: What Landowners Can Do                           | private land wildlife management         | private_land_wildlife_management        | P7: Conservation   | done    |
| W25a  | 25   | Tue | Delaware Hunting Seasons & Regulations: Small State, Big Opportunities             | delaware hunting seasons                 | delaware_hunting_seasons                | P1: State Seasons  | done    |
| W25b  | 25   | Thu | Where to Aim to Kill a Deer: Shot Placement Guide for Ethical Harvest              | where to shoot a deer                    | deer_shot_placement                     | P3: Species        | done    |
| W26a  | 26   | Tue | Legal Hunting Times Explained: Shooting Hours and Regulations                      | legal hunting hours                      | legal_hunting_times                     | P2: Licenses       | done    |
| W26b  | 26   | Thu | Nebraska Hunting and Land Leases: Private Access Guide                             | nebraska hunting leases                  | nebraska_hunting_land_leases            | P3: Species        | done    |
| W27a  | 27   | Tue | Arizona Upland Game Hunting Seasons: Quail, Dove, and More                         | arizona upland game hunting              | arizona_upland_game_hunting             | P1: State Seasons  | done    |
| W27b  | 27   | Thu | Iowa Hunting Land: How to Find and Access Premium Private Ground                   | iowa hunting land                        | iowa_hunting_land                       | P3: Species        | done    |
| W28a  | 28   | Tue | Arkansas Waterfowl Hunting: Seasons, Flyways, and WMA Access                       | arkansas waterfowl hunting               | arkansas_waterfowl_hunting              | P3: Species        | done    |
| W28b  | 28   | Thu | CWD and EHD Update 2026: What Hunters Need to Know This Season                     | chronic wasting disease deer             | cwd_ehd_update_2026                     | P7: Conservation   | done    |
| W29a  | 29   | Tue | Georgia Dove Hunting Season: Dates, Limits, and Where to Go                        | georgia dove hunting season              | georgia_dove_hunting_season             | P1: State Seasons  | done    |
| W29b  | 29   | Thu | How to Cook Dove Breast: Recipes and Field-to-Table Tips                           | how to cook dove breast                  | how_to_cook_dove_breast                 | P6: Lifestyle      | done    |
| W30a  | 30   | Tue | Missouri Waterfowl Hunting: Zones, Dates, and Reservation Areas                    | missouri waterfowl hunting               | missouri_waterfowl_hunting              | P3: Species        | pending |
| W30b  | 30   | Thu | Hunting Lodging Alternatives: Private Land Stays vs Airbnb                         | hunting lodging                          | hunting_lodging_alternatives            | P6: Lifestyle      | pending |
| W31a  | 31   | Tue | Mississippi Hunting & Wildlife Management Guide                                    | mississippi hunting seasons              | mississippi_hunting_wildlife            | P1: State Seasons  | pending |
| W31b  | 31   | Thu | Wild Game Processing 101: Field Dressing, Butchering, and Storage                  | wild game processing                     | wild_game_processing                    | P6: Lifestyle      | pending |
| W32a  | 32   | Tue | Washington State Hunting Seasons: What to Know for 2026-2027                       | washington state hunting seasons         | washington_state_hunting_seasons        | P1: State Seasons  | pending |
| W32b  | 32   | Thu | Montana Deer Hunting on Private Land: Access, Tags, and Tactics                    | montana deer hunting private land        | montana_deer_hunting_private_land       | P3: Species        | pending |
| W33a  | 33   | Tue | South Carolina Waterfowl Hunting Clubs and Where to Find Access                    | south carolina waterfowl hunting         | south_carolina_waterfowl_hunting        | P3: Species        | pending |
| W33b  | 33   | Thu | Indiana Public and Private Hunting Land: Finding Access                            | indiana hunting land                     | indiana_hunting_land                    | P3: Species        | pending |

**Note:** Week 21 Thu (Decoding Trail Cameras) and Week 23 Thu (Food Plot Plants) are already `[BRIEF READY]` per the Content Calendar — excluded from this backlog.

**Total:** 32 briefs to generate.
