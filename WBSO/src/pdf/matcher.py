class PDFMatcher:
    def __init__(self):
        pass

    def find_matches(self, pdf_text: str, patterns: list[str]) -> list[str]:
        """Finds occurrences of patterns in the PDF text."""
        # Placeholder for actual matching logic
        matches = []
        for pattern in patterns:
            if pattern in pdf_text:
                matches.append(f"Found: {pattern}")
        return matches
