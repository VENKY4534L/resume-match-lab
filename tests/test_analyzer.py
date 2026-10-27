import unittest
from app.analyzer import analyze_resume

class AnalyzerTests(unittest.TestCase):
    def test_detects_matched_and_missing_skills(self):
        result = analyze_resume(
            "Python, Flask, SQL, and unit testing experience.",
            "Required: Python, Flask, SQL, Docker, and unit testing."
        )
        self.assertIn("python", result["matched_skills"])
        self.assertIn("flask", result["matched_skills"])
        self.assertIn("docker", result["missing_skills"])

    def test_score_is_bounded(self):
        result = analyze_resume("Python developer with SQL", "Python SQL Docker")
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            analyze_resume("", "Python developer")

    def test_note_disclaims_hiring_prediction(self):
        result = analyze_resume("Python", "Python developer")
        self.assertIn("not an ATS score", result["note"])

if __name__ == "__main__":
    unittest.main()
