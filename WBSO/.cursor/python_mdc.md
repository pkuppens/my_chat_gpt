# Python MDC Rules

## Module Structure

### Imports

```python
# Standard library imports
import os
import sys
from typing import Any, Dict, List, Optional

# Third-party imports
import pydantic
from langchain import LLMChain

# Local imports
from .utils import helpers
from ..config import settings
```

### Type Hints

```python
from typing import TypeVar, Generic, Protocol

T = TypeVar('T')
InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')

class Processor(Protocol[InputType, OutputType]):
    def process(self, input_data: InputType) -> OutputType:
        ...
```

### Class Documentation

```python
class PDFParser:
    """PDF form parser for WBSO applications.

    This class handles the extraction and processing of PDF form fields,
    following the AI-assisted development approach.

    Attributes:
        form_path: Path to the PDF form file
        field_mappings: Dictionary mapping field names to their locations
    """

    def __init__(self, form_path: str) -> None:
        """Initialize the PDF parser.

        Args:
            form_path: Path to the PDF form file
        """
        self.form_path = form_path
        self.field_mappings: Dict[str, Any] = {}
```

### Function Documentation

```python
def extract_form_fields(pdf_path: str) -> Dict[str, Any]:
    """Extract form fields from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary containing form field names and their values

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        PDFProcessingError: If there's an error processing the PDF

    Example:
        >>> fields = extract_form_fields("form.pdf")
        >>> print(fields["project_name"])
        "WBSO Project 2024"
    """
```

## Testing

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch

def test_extract_form_fields():
    """Test form field extraction from PDF.

    This test verifies that:
    1. Form fields are correctly extracted
    2. Field values are properly parsed
    3. Error handling works as expected
    """
    # Arrange
    mock_pdf = Mock()
    mock_pdf.get_fields.return_value = {"field1": "value1"}

    # Act
    with patch("pdfplumber.open", return_value=mock_pdf):
        result = extract_form_fields("test.pdf")

    # Assert
    assert result["field1"] == "value1"
```

## Error Handling

### Custom Exceptions

```python
class PDFProcessingError(Exception):
    """Exception raised for PDF processing errors.

    Attributes:
        message: Explanation of the error
        pdf_path: Path to the PDF file that caused the error
    """

    def __init__(self, message: str, pdf_path: str) -> None:
        self.message = message
        self.pdf_path = pdf_path
        super().__init__(f"{message} (PDF: {pdf_path})")
```

### Error Handling Pattern

```python
def process_pdf(pdf_path: str) -> Dict[str, Any]:
    """Process a PDF file with proper error handling.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Processed PDF data

    Raises:
        PDFProcessingError: If processing fails
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return extract_form_fields(pdf)
    except FileNotFoundError:
        raise PDFProcessingError("PDF file not found", pdf_path)
    except Exception as e:
        raise PDFProcessingError(f"Error processing PDF: {str(e)}", pdf_path)
```

## Configuration

### Settings Class

```python
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings.

    Attributes:
        model_name: Name of the LLM model to use
        temperature: Temperature for model generation
        max_tokens: Maximum tokens for generation
    """
    model_name: str = Field(default="gpt-4")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=2000, gt=0)

    class Config:
        env_prefix = "WBSO_"
```

## Logging

### Logging Setup

```python
import logging
from typing import Optional

def setup_logging(level: Optional[int] = None) -> None:
    """Set up logging configuration.

    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level or logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```
