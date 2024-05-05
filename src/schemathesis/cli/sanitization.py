from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..runner import events
from ..sanitization import sanitize_serialized_check, sanitize_serialized_interaction
from .handlers import EventHandler

if TYPE_CHECKING:
    from .context import ExecutionContext
from ..specs.openapi._vas import logger


@dataclass
class SanitizationHandler(EventHandler):
    def handle_event(
        self, context: ExecutionContext, event: events.ExecutionEvent
    ) -> None:
        logger.debug("Goes through sanitization handler")
        if isinstance(event, events.AfterExecution):
            for check in event.result.checks:
                sanitize_serialized_check(check)
            for interaction in event.result.interactions:
                sanitize_serialized_interaction(interaction)
