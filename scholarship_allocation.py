# ==============================================================================
# Case Study: University Scholarship Allocation System
# Developed strictly using concepts from the foundational syllabus:
# - Computational Thinking, Algorithms, Flowcharts, Pseudocode
# - Variables, Data Types, Operators, Conditionals
# - Loops (for, while), Strings, Pattern Generation
# - Lists, Nested Lists, Tuples, Tuple Operations, and Unpacking
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. RAW DATA INITIALIZATION (Lists & Nested Tuples)
# ------------------------------------------------------------------------------
# Applicant Record Schema:
# (student_id, full_name, (math, physics, chemistry, computer_science), attendance_pct, family_income)
# All subject marks out of 100.
# ------------------------------------------------------------------------------

applicants = [
    ("STU101", "Aarav Sharma", (95, 92, 88, 96), 92.5, 350000),
    ("STU102", "Diya Patel", (95, 92, 88, 96), 94.0, 420000),
    ("STU103", "Rohan Verma", (82, 75, 78, 80), 85.0, 250000),
    ("STU104", "Ananya Iyer", (98, 95, 94, 99), 96.5, 480000),
    ("STU105", "Kabir Mehta", (95, 92, 88, 96), 94.0, 310000),
    ("STU106", "Sneha Rao", (55, 90, 85, 88), 91.0, 200000),   # Fails Math cutoff (<60)
    ("STU107", "Vikram Singh", (70, 72, 68, 74), 72.0, 180000), # Fails Attendance (<80%)
    ("STU108", "Pooja Hegde", (88, 86, 84, 90), 88.0, 750000),  # Fails Income ceiling (>600000)
    ("STU109", "Arjun Nair", (95, 92, 88, 96), 94.0, 310000),  # Ties with Kabir Mehta! Name resolves
    ("STU110", "Meera Sen", (91, 89, 90, 92), 89.0, 300000),
    ("STU111", "Karan Johar", (60, 61, 62, 60), 81.0, 150000),  # Barely qualifies
    ("STU112", "Neha Gupta", (78, 59, 82, 85), 84.0, 280000),   # Fails Physics cutoff (59 < 60)
]

# Policy Threshold Constants
MIN_SUBJECT_SCORE = 60.0
MIN_AGGREGATE_PCT = 75.0
MIN_ATTENDANCE_PCT = 80.0
MAX_FAMILY_INCOME = 600000.0

# Available Scholarships Quota
QUOTA_FULL = 2      # Top 2 get Full Scholarship (100% waiver)
QUOTA_PARTIAL = 3   # Next 3 get Partial Scholarship (50% waiver)

print("=" * 80)
print("       UNIVERSITY SCHOLARSHIP ALLOCATION ENGINE - REPORT GENERATION")
print("=" * 80)
print()

# ------------------------------------------------------------------------------
# 2. ELIGIBILITY EVALUATION & DISQUALIFICATION AUDITING
# ------------------------------------------------------------------------------
eligible_students = []
disqualified_students = []

# Processing applicants using for loop and tuple unpacking
for applicant in applicants:
    # Unpack the 5-element outer tuple
    sid, name, marks_tuple, att, income = applicant
    
    # Unpack nested subject marks tuple
    m, p, c, cs = marks_tuple
    
    # Calculate aggregate marks and percentage
    total_marks = m + p + c + cs
    num_subjects = len(marks_tuple)
    agg_pct = total_marks / num_subjects
    
    # Step-by-step criterion evaluation
    subject_pass = (m >= MIN_SUBJECT_SCORE and 
                    p >= MIN_SUBJECT_SCORE and 
                    c >= MIN_SUBJECT_SCORE and 
                    cs >= MIN_SUBJECT_SCORE)
    aggregate_pass = agg_pct >= MIN_AGGREGATE_PCT
    attendance_pass = att >= MIN_ATTENDANCE_PCT
    income_pass = income <= MAX_FAMILY_INCOME
    
    # Overall eligibility check using logical operators
    if subject_pass and aggregate_pass and attendance_pass and income_pass:
        # Form an enriched tuple for sorting & reporting:
        # (sid, name, marks_tuple, total_marks, agg_pct, att, income)
        enriched_record = (sid, name, marks_tuple, total_marks, agg_pct, att, income)
        eligible_students.append(enriched_record)
    else:
        # Determine specific reason(s) for audit logging
        reasons = []
        if not subject_pass:
            # Check which subjects failed
            failed_subs = []
            if m < MIN_SUBJECT_SCORE: failed_subs.append("Math (" + str(m) + ")")
            if p < MIN_SUBJECT_SCORE: failed_subs.append("Physics (" + str(p) + ")")
            if c < MIN_SUBJECT_SCORE: failed_subs.append("Chem (" + str(c) + ")")
            if cs < MIN_SUBJECT_SCORE: failed_subs.append("CS (" + str(cs) + ")")
            
            # String joining using loop
            subs_str = ""
            for s_idx in range(len(failed_subs)):
                subs_str += failed_subs[s_idx]
                if s_idx < len(failed_subs) - 1:
                    subs_str += ", "
            reasons.append("Subject score below minimum: " + subs_str)
            
        if not aggregate_pass:
            reasons.append("Aggregate " + str(round(agg_pct, 2)) + "% < " + str(MIN_AGGREGATE_PCT) + "%")
        if not attendance_pass:
            reasons.append("Attendance " + str(att) + "% < " + str(MIN_ATTENDANCE_PCT) + "%")
        if not income_pass:
            reasons.append("Income INR " + str(income) + " > " + str(int(MAX_FAMILY_INCOME)))
            
        disqualified_record = (sid, name, reasons)
        disqualified_students.append(disqualified_record)

# ------------------------------------------------------------------------------
# 3. RANKING ALGORITHM WITH MULTI-TIER TIE-BREAKING (Bubble Sort)
# ------------------------------------------------------------------------------
# Tie-Breaking Precedence Rules:
# 1. Total Marks (Descending)
# 2. Attendance % (Descending)
# 3. Family Income (Ascending - need-based preference)
# 4. Mathematics Score (Descending - core foundation subject)
# 5. Full Name (Ascending - alphabetical)
# ------------------------------------------------------------------------------

n_eligible = len(eligible_students)

# Manual Sorting using nested loops (no sorted() key or lambda)
for i in range(n_eligible - 1):
    for j in range(n_eligible - 1 - i):
        # Unpack elements at index j
        rec_j = eligible_students[j]
        sid_j, name_j, marks_j, total_j, agg_j, att_j, inc_j = rec_j
        math_j = marks_j[0]
        
        # Unpack elements at index j + 1
        rec_next = eligible_students[j + 1]
        sid_n, name_n, marks_n, total_n, agg_n, att_n, inc_n = rec_next
        math_n = marks_n[0]
        
        # Determine if candidate at (j + 1) strictly outranks candidate at j
        swap_needed = False
        
        # Rule 1: Total Marks (Higher is better)
        if total_n > total_j:
            swap_needed = True
        elif total_n == total_j:
            # Rule 2: Attendance (Higher is better)
            if att_n > att_j:
                swap_needed = True
            elif att_n == att_j:
                # Rule 3: Income (Lower is better)
                if inc_n < inc_j:
                    swap_needed = True
                elif inc_n == inc_j:
                    # Rule 4: Math Score (Higher is better)
                    if math_n > math_j:
                        swap_needed = True
                    elif math_n == math_j:
                        # Rule 5: Alphabetical order of Name (Lexicographical)
                        if name_n < name_j:
                            swap_needed = True
        
        if swap_needed:
            # Swap using tuple unpacking
            eligible_students[j], eligible_students[j + 1] = eligible_students[j + 1], eligible_students[j]

# ------------------------------------------------------------------------------
# 4. ALLOCATION CATEGORIZATION
# ------------------------------------------------------------------------------
# Quota Distribution:
# - Full Scholarship (100%): Ranks 1 to QUOTA_FULL
# - Partial Scholarship (50%): Next QUOTA_PARTIAL ranks
# - Waitlisted / Merit Certificate: Remaining eligible candidates
# ------------------------------------------------------------------------------

allocated_list = []
rank = 1

for student in eligible_students:
    sid, name, marks, total, agg, att, inc = student
    
    if rank <= QUOTA_FULL:
        status = "FULL SCHOLARSHIP (100%)"
        tier_code = "TIER-1"
    elif rank <= (QUOTA_FULL + QUOTA_PARTIAL):
        status = "PARTIAL SCHOLARSHIP (50%)"
        tier_code = "TIER-2"
    else:
        status = "MERIT WAITLIST"
        tier_code = "WAITLIST"
        
    allocated_record = (rank, sid, name, total, agg, att, inc, status, tier_code)
    allocated_list.append(allocated_record)
    rank += 1

# ------------------------------------------------------------------------------
# 5. REPORT FORMATTING & VISUALIZATION (Strings, Slicing & Loops)
# ------------------------------------------------------------------------------

# Table 1: Final Merit & Scholarship Allocation Table
print("\n" + "=" * 98)
print("FINAL MERIT RANKING & SCHOLARSHIP ALLOCATION MATRIX".center(98))
print("=" * 98)

header = (
    "Rank".center(6) + "|" +
    "ID".center(8) + "|" +
    "Student Name".ljust(18) + "|" +
    "Aggregate".center(11) + "|" +
    "Attend.".center(9) + "|" +
    "Income (INR)".rjust(14) + "|" +
    "Scholarship Status".center(27)
)
print(header)
print("-" * 98)

for record in allocated_list:
    r, s_id, s_name, tot, a_pct, a_att, a_inc, s_stat, t_code = record
    
    row = (
        str(r).center(6) + "|" +
        s_id.center(8) + "|" +
        (" " + s_name).ljust(18) + "|" +
        (str(tot) + " (" + str(round(a_pct, 1)) + "%)").center(11) + "|" +
        (str(round(a_att, 1)) + "%").center(9) + "|" +
        (str(int(a_inc))).rjust(13) + " |" +
        (" " + s_stat).ljust(27)
    )
    print(row)

print("=" * 98)

# Table 2: Disqualified Candidates Audit
print("\n" + "-" * 98)
print("DISQUALIFICATION & AUDIT LOG".center(98))
print("-" * 98)
for disq in disqualified_students:
    s_id, s_name, r_list = disq
    print(s_id + " - " + s_name.ljust(16) + ": Reason(s) -> ")
    for r_item in r_list:
        print("   * " + r_item)
print("-" * 98)

# ------------------------------------------------------------------------------
# 6. PATTERN GENERATION: ASCII SCHOLARSHIP SEALS & ALLOCATION VISUALIZATIONS
# ------------------------------------------------------------------------------
# Demonstrating Pattern Generation using nested loops:
# Pattern A: Ceremonial Diamond Star Crest for Top Ranker (Aarav/Ananya)
# Pattern B: Horizontal Visual Bar Pattern for Scholarship Distribution
# ------------------------------------------------------------------------------

top_ranker = allocated_list[0]
top_name = top_ranker[2]
top_agg = top_ranker[4]

print("\n" + "=" * 60)
print("PATTERN 1: DIPLOMA OF EXCELLENCE - CEREMONIAL CREST")
print("=" * 60)

# Diamond Pattern with embedded insignia using nested loops
crest_height = 5

# Upper Diamond
for row in range(crest_height):
    # Spaces loop
    for sp in range(crest_height - row - 1):
        print(" ", end="")
    # Stars and symbols loop
    for col in range(2 * row + 1):
        if col == 0 or col == (2 * row):
            print("*", end="")
        elif row == 3 and col == row:
            print("V", end="")  # Valedictorian insignia
        else:
            print(".", end="")
    print()

# Banner box around Top Ranker Name
border_len = len(top_name) + 16
print("*" * border_len)
print("* VALEDICTORIAN: " + top_name.upper() + " *")
print("* AGGREGATE SCORE: " + str(round(top_agg, 2)) + "%       *")
print("*" * border_len)

# Lower Diamond (Inverted)
for row in range(crest_height - 2, -1, -1):
    for sp in range(crest_height - row - 1):
        print(" ", end="")
    for col in range(2 * row + 1):
        if col == 0 or col == (2 * row):
            print("*", end="")
        else:
            print(".", end="")
    print()

print("\n" + "=" * 60)
print("PATTERN 2: SCHOLARSHIP ALLOCATION PYRAMID")
print("=" * 60)

# Nested loop to generate tiered hierarchical pyramid:
# Level 1: Full Scholarship Tier (1 Star row)
# Level 2: Partial Scholarship Tier (3 Star row)
# Level 3: Waitlisted Merit Tier (5 Star row)
pyramid_levels = 4
for i in range(1, pyramid_levels + 1):
    # Leading indentation
    for s in range(pyramid_levels - i):
        print("   ", end="")
    
    # Pyramid building blocks
    for j in range(1, (2 * i)):
        if i == 1:
            print("[TIER-1: FULL]", end=" ")
        elif i == 2:
            print("[TIER-2: HALF]", end=" ")
        elif i == 3:
            print("[WAITLISTED]  ", end=" ")
        else:
            print("[BASE QUOTA]  ", end=" ")
    print()

print("\n" + "=" * 60)
print("PATTERN 3: PERFORMANCE HISTOGRAM BARS (NESTED LOOPS)")
print("=" * 60)
# Generating horizontal bar chart of aggregate scores using nested loops
for record in allocated_list:
    r, s_id, s_name, tot, a_pct, a_att, a_inc, s_stat, t_code = record
    
    # Scale percentage to 20 blocks
    num_blocks = int(a_pct // 5)
    
    print(s_id + " (" + str(round(a_pct, 1)) + "%): ", end="")
    
    # Nested loop to print bar character
    for b in range(num_blocks):
        print("#", end="")
    # Nested loop to print remaining empty slots
    for e in range(20 - num_blocks):
        print("-", end="")
    print(" | " + t_code)

print("\nSystem execution completed successfully.")
