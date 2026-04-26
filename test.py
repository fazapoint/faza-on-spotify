# Source - https://stackoverflow.com/a/1883251
# Posted by Carl Meyer, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-27, License - CC BY-SA 4.0

import sys


def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )


def in_virtualenv():
    return sys.prefix != get_base_prefix_compat()

print(get_base_prefix_compat())
print(in_virtualenv())