"""
Custom exceptions for LVMeteo library.
"""


class LVMeteoError(Exception):
    """Base exception for LVMeteo library."""
    pass


class APIError(LVMeteoError):
    """Raised when API request fails."""
    pass


class DataNotFoundError(LVMeteoError):
    """Raised when requested data is not found."""
    pass


class ValidationError(LVMeteoError):
    """Raised when input validation fails."""
    pass


class ConfigurationError(LVMeteoError):
    """Raised when configuration is invalid."""
    pass