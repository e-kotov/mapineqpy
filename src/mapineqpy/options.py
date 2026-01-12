"""
Configuration options for mapineqpy.

This module provides a global `options` dictionary that allows users to configure
the behavior of the library at runtime.

Keys:
    skip_filter_check (bool): If True, skips the additional validation step in `mi.data()` that checks
                              for duplicate geographic regions (which usually indicate missing filters).
                              Default is False.

Example:

```python
import mapineqpy as mi

# Disable the filter check
mi.options["skip_filter_check"] = True
```
"""

options = {
    "skip_filter_check": False,  # Default: perform filter checks
}
"""
A dictionary for global configuration options.
"""
