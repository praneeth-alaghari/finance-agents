"""Prompts package for market research agents and services."""

from market_research.prompts.macro_economics import (
    MACRO_ANALYSIS_PROMPT_TEMPLATE,
    SYSTEM_INSTRUCTION as MACRO_SYSTEM_INSTRUCTION,
)
from market_research.prompts.sector_rotation import (
    SECTOR_ROTATION_PROMPT_TEMPLATE,
    SYSTEM_INSTRUCTION as SECTOR_SYSTEM_INSTRUCTION,
)

__all__ = [
    "MACRO_ANALYSIS_PROMPT_TEMPLATE",
    "MACRO_SYSTEM_INSTRUCTION",
    "SECTOR_ROTATION_PROMPT_TEMPLATE",
    "SECTOR_SYSTEM_INSTRUCTION",
]
