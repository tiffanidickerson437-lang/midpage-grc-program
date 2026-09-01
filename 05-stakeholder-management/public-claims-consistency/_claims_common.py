#!/usr/bin/env python3
"""Shared validation primitives for the public-claims-consistency checkers.

check_metrics.py, check_retention.py, and subprocessor_consistency.py each load a
YAML observation file and validate every surface entry against the same shape
rules: a lowercase-slug id, an https:// url, an ISO `checked` date. Those rules
had already drifted independently once — check_metrics.py's validate() lacked
the audience check its two siblings had. Keeping the shared rules here means a
fix to one lands in all three, instead of three copies drifting apart again.

Each checker still owns its own DataError-raising field/type checks that are not
shared (figures vs. assertions vs. providers) — this module holds only the parts
that were byte-for-byte identical across all three files.
"""

import datetime as _dt
import re

import yaml

SLUG_RE = re.compile(r"[a-z0-9-]+")


class DataError(ValueError):
    """The observation file is malformed. A checker that guesses past bad input is
    a checker whose findings cannot be trusted, so this always stops the run."""


def load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def require_lowercase_slug(sid):
    if not re.fullmatch(SLUG_RE, str(sid)):
        raise DataError("surface id %r must be a lowercase slug" % sid)


def require_https_url(sid, url):
    if not str(url).startswith("https://"):
        raise DataError("surface %r: url must be https://" % sid)


def require_iso_date(sid, value, field="checked"):
    try:
        _dt.date.fromisoformat(str(value))
    except ValueError:
        raise DataError("surface %r: %s is not an ISO date" % (sid, field))
