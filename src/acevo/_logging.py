"""Internal logging helpers for acevo-sdk."""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any


class Component(Enum):
    """Component identifiers used in SDK log records."""

    LOG_PARSER = "LOG_PARSER"
    TELEMETRY = "TELEMETRY"


_logger = logging.getLogger("acevo")


def _log(level: int, component: Component, message: str, **kwargs: Any) -> None:
    if kwargs:
        context = " ".join(f"{key}={value}" for key, value in kwargs.items() if value is not None)
        if context:
            message = f"{message} | {context}"
    _logger.log(level, "[%s] %s", component.value, message)


def log_debug(component: Component, message: str, **kwargs: Any) -> None:
    _log(logging.DEBUG, component, message, **kwargs)


def log_info(component: Component, message: str, **kwargs: Any) -> None:
    _log(logging.INFO, component, message, **kwargs)


def log_warning(component: Component, message: str, **kwargs: Any) -> None:
    _log(logging.WARNING, component, message, **kwargs)


def log_error(component: Component, message: str, **kwargs: Any) -> None:
    _log(logging.ERROR, component, message, **kwargs)


def log_exception(component: Component, message: str, exception: Exception, **kwargs: Any) -> None:
    _logger.exception("[%s] %s | error=%s", component.value, message, exception, extra=kwargs or None)
