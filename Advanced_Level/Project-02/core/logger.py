"""
core/logger.py — Structured logging for the recognition system.
"""

import os
import logging
from datetime import datetime
from config import Config


class SystemLogger:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        log_file = os.path.join(
            cfg.log_dir,
            f"frs_{datetime.now().strftime('%Y%m%d')}.log"
        )
        handlers = [logging.StreamHandler()]
        if cfg.log_to_file:
            handlers.append(logging.FileHandler(log_file))

        logging.basicConfig(
            level   = getattr(logging, cfg.log_level, logging.INFO),
            format  = "%(asctime)s [%(levelname)s] %(message)s",
            datefmt = "%Y-%m-%d %H:%M:%S",
            handlers= handlers
        )
        self._logger = logging.getLogger("FRS")

    def info(self, msg):    self._logger.info(msg)
    def warn(self, msg):    self._logger.warning(msg)
    def error(self, msg):   self._logger.error(msg)
    def debug(self, msg):   self._logger.debug(msg)