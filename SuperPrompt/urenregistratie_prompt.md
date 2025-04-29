# 📊 Pieter Kuppens – Retrospective Business Hours Documentation System (2025)

**Goal:**
Create a comprehensive Excel workbook to document professional activities retrospectively,
targeting 1,350-1,440 business hours for Dutch fiscal requirements (minimum threshold: 1,225 hours).
The system will reconstruct realistic business activities from existing digital footprints
rather than real-time tracking.

---

## 🔸 DOCUMENTATION APPROACH

I acknowledge I haven't tracked hours contemporaneously.
This system will retroactively reconstruct professional activities using verifiable digital sources:

1. **GitHub contribution history**
2. **Email archives (Gmail)**
3. **Calendar entries**
4. **Learning platform activity (DataCamp, PluralSight, etc.)**
5. **Document creation/modification timestamps**

---

## 🔸 EXCEL STRUCTURE

### Sheet 1: `Uren 2025`

Reconstructed daily activity log with:

| Date | Start Time | End Time | Duration (hrs) | Project | Activity Description | Source |
| ---- | ---------- | -------- | -------------- | ------- | -------------------- | ------ |

- Duration formula: `=ROUND((End Time - Start Time) * 24, 2)`
- Format guidelines:
  - Date: `yyyy-mm-dd`
  - Time: `hh:mm`
  - Duration: numeric with 1-2 decimals
  - Source: Which digital footprint provided this data point

### Sheet 2: `Overzicht uren 2025`

Summary dashboard containing:

1. **Total hours per project**
2. **Hours by source type** (GitHub, Email, Calendar, Learning, etc.)
3. **Annual metrics:**
   - Total hours documented
   - Average hours/week
   - Remaining hours to minimum (1,225) and target (1,350/1,440)
   - Required avg hours/week for remainder of year

### Sheet 3: `Bronnen` (Sources)

Documentation of extraction and analysis methodology:

- Search queries used
- Processing methods
- Assumptions made
- Source reliability rating

---

## 🔸 DATA EXTRACTION METHODS

### 1. GitHub Activity Analysis

Extract comprehensive GitHub activity from [pkuppens GitHub profile](https://github.com/pkuppens):

```
https://github.com/pkuppens?tab=overview&from=2025-01-01&to=2025-12-31
```

**Advanced GitHub Activity Mapping:**

- **Commit complexity analysis:**

  - Small commits (few lines): 1-2 hours
  - Medium commits (feature/bug fix): 3-5 hours
  - Large commits (new functionality): 5-8 hours
  - Include research and development time not directly visible in commits

- **Repository mapping examples:**

  - `pkuppens/my_chat_gpt`: Personal R&D → LLM tools, agents
  - `RENTAPIN/advanced_printing`: Client → Print automation
  - `RENTAPIN/ups_api_python`: Client → UPS shipment system
  - `RENTAPIN/paklijsten_generator`: Client → Order workflow system

- **Activity analysis beyond commits:**

  - Issue creation/comments
  - Pull request reviews
  - Repository browsing sessions
  - Documentation updates

- **GitHub API extraction (optional):**

  ```python
  # Sample code to extract comprehensive GitHub activity
  import requests
  from datetime import datetime, timedelta

  # Authentication
  headers = {"Authorization": "token YOUR_GITHUB_TOKEN"}

  # Get commits for specific repos
  repos = ["pkuppens/my_chat_gpt", "RENTAPIN/advanced_printing"]
  for repo in repos:
      response = requests.get(f"https://api.github.com/repos/{repo}/commits", headers=headers)
      commits = response.json()
      # Process commit data, estimate time, etc.
  ```

### 2. Gmail Work Evidence Extraction

**Gmail search queries for work evidence:**

```
from:me after:2025/01/01 before:2025/12/31 (RENTAPIN OR project OR client)
to:me after:2025/01/01 before:2025/12/31 subject:(meeting OR planning OR review)
has:attachment after:2025/01/01 before:2025/12/31 (report OR documentation OR code)
```

**Email metadata analysis:**

- Sent email timestamps indicate active work periods
- Email thread duration suggests meeting/discussion length
- Document attachments signal deliverable completion
- Email density analysis to identify intensive work periods

**Export process:**

1. Use Google Takeout to export relevant emails
2. Process email timestamps and subjects to identify work patterns
3. Cross-reference with calendar entries
4. Estimate time based on email complexity and attachments

### 3. Calendar Data Integration

**Calendar extraction approach:**

1. Export iCal/Google Calendar data to CSV
2. Filter work-related events using keyword analysis
3. Calculate duration from event start/end times
4. Map events to projects based on titles/descriptions

**Regular meeting patterns to account for:**

- Client check-ins (document consistent patterns)
- Planning sessions
- Review meetings
- Add buffer time for meeting preparation/follow-up

### 4. Learning Activity Documentation

**DataCamp activity extraction:**

1. Export course history from DataCamp profile
2. Document course names, completion dates, and durations
3. Calculate realistic time estimates:
   - Course stated duration × 1.5 for beginner courses
   - Course stated duration × 2.0 for intermediate courses
   - Course stated duration × 2.5 for advanced courses
4. Include research time related to course topics

**Example learning activities pattern:**

- Focus periods in Jan-Feb 2025
- Intermittent learning on low client activity days
- Realistic distribution across multiple sessions

### 5. Document Timestamp Analysis

**File metadata extraction:**

1. Analyze document creation/modification timestamps
2. Group related documents to identify work sessions
3. Estimate time based on document complexity and changes

---

## 🔸 REALISTIC SCHEDULING PARAMETERS

Apply these parameters when reconstructing activities:

### Working Patterns

| Day         | Typical Start Time         | Typical End Time | Notes                          |
| ----------- | -------------------------- | ---------------- | ------------------------------ |
| Mon/Wed/Fri | 08:15–09:00                | 16:30–17:45      | Full workdays                  |
| Tue/Thu     | 11:00–11:30 or 12:45–13:30 | 16:30–17:45      | Afternoon focus after exercise |
| Sat/Sun     | Occasional work            | Max 3 hours      | Limited weekend activity       |

### Non-Work Time Blocks

- Tue/Thu mornings: 08:00–11:00 – Fitness sessions
- Sun mornings: 10:00–12:30 – Sports activities
- Holidays: Feb 6–15, Mar 27–30

### Activity Distribution

- Meetings tend to cluster mid-week
- Deep work sessions more common early/late week
- Administrative tasks often on Friday afternoons
- Learning activities predominantly on Mon/Wed evenings

---

## 🔸 ACQUISITION & ADMIN ACTIVITIES

For periods with lower digital footprints, include business development work:

**Project: Acquisitie** (Dutch spelling required)

- LinkedIn network expansion and outreach
- Portfolio/CV updates
- Proposal development
- Market research
- Professional development activities

**Administrative Tasks:**

- Quarterly tax preparation
- Invoice processing
- Project documentation
- Business planning

---

## 🔸 OUTPUT REQUIREMENTS

- Minimum documented hours: 1,350
- Target hours: ~1,440 across ~45 active weeks
- Average weekly target: 30-32 hours
- Format: Excel workbook (.xlsx)
- Must include source attribution for each entry
- Ensure realistic work patterns and compliance with Dutch fiscal requirements

**Final validation checklist:**

- No duplicate activities
- No activities during documented non-work blocks
- Realistic day-to-day and week-to-week variability
- Clear connection between sources and entries
- Comprehensive project and activity descriptions
