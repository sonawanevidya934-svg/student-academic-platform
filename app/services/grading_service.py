GRADE_SCALE = [("O", 90, 100, 10), ("A+", 80, 89.99, 9), ("A", 70, 79.99, 8), ("B+", 60, 69.99, 7), ("B", 50, 59.99, 6), ("C", 40, 49.99, 5), ("F", 0, 39.99, 0)]
def grade_for_marks(m):
    if m is None: return (None, None)
    for g, lo, hi, p in GRADE_SCALE:
        if lo <= float(m) <= hi: return (g, p)
    return (None, None)
def validate_marks(m):
    e = []
    try: v = float(m)
    except (TypeError, ValueError): return ["Marks must be a number between 0 and 100."]
    if not 0 <= v <= 100: e.append("Marks must be between 0 and 100.")
    return e
def compute_gpa(rows):
    tot_p = 0.0; tot_c = 0; graded_c = 0
    for r in rows:
        c = int(r["credits"]); tot_c += c
        if r.get("marks") is not None:
            _, p = grade_for_marks(r["marks"])
            tot_p += p * c; graded_c += c
    gpa = round(tot_p / graded_c, 2) if graded_c else None
    return {"gpa": gpa, "total_credits": tot_c, "graded_credits": graded_c}

