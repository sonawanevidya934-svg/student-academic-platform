PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS students (
  student_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  department TEXT NOT NULL,
  semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8)
);
CREATE TABLE IF NOT EXISTS faculty (
  faculty_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  department TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS courses (
  course_code TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  credits INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 6),
  semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
  faculty_id TEXT REFERENCES faculty(faculty_id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS enrollments (
  enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id TEXT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
  course_code TEXT NOT NULL REFERENCES courses(course_code) ON DELETE CASCADE,
  semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
  marks REAL CHECK (marks IS NULL OR (marks BETWEEN 0 AND 100)),
  UNIQUE (student_id, course_code, semester)
);

