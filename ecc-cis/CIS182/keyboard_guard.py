"""Keep notebook keyboard shortcuts from firing while students use a widget.

In Notebook 7 (the interface the DataHub launch links open) and JupyterLab,
clicking a widget button or the widget's output leaves keyboard focus on an
element that the notebook treats as command mode. The next key a student
presses then runs a shortcut: "o" hides the cell output, "dd" deletes the
cell, "m" turns it into Markdown, and so on. The widget appears to vanish.

Usage::

    from keyboard_guard import guard_widgets
    display(guard_widgets(dropdown, run_button, output))

guard_widgets() wraps the widgets in a VBox and, once per page, adds a small
script that:
- drops focus after a button click or a dropdown change, so no shortcut can
  fire until the student clicks somewhere else on purpose;
- swallows printable keys pressed while focus is on a non-text part of the
  widget (button, dropdown, output).
The widgets still work if the script does not run.
"""

import ipywidgets as widgets
from IPython.display import HTML, display

GUARD_CLASS = "ecc-widget-guard"

_GUARD_SCRIPT = f"""
<script>
(function () {{
  if (window.__eccWidgetGuardInstalled) return;
  window.__eccWidgetGuardInstalled = true;
  var GUARD = ".{GUARD_CLASS}";

  function inGuard(el) {{
    return el instanceof Element && !!el.closest(GUARD);
  }}
  function isTextEntry(el) {{
    return el.matches("input:not([type=button]):not([type=checkbox]):not([type=radio]), textarea, [contenteditable=true]");
  }}
  function dropFocus() {{
    var a = document.activeElement;
    if (a && a !== document.body && !isTextEntry(a)) a.blur();
  }}

  // Printable keys pressed on a button, dropdown, or output are swallowed
  // before the notebook can treat them as shortcuts.
  window.addEventListener("keydown", function (e) {{
    if (!inGuard(e.target) || isTextEntry(e.target)) return;
    if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {{
      e.stopPropagation();
      e.preventDefault();
    }}
  }}, true);

  // After a click on a button or the output, or after picking a dropdown
  // option, leave nothing focused inside the notebook.
  window.addEventListener("click", function (e) {{
    if (!inGuard(e.target) || isTextEntry(e.target)) return;
    if (e.target.closest("select")) return;  // let the dropdown open normally
    setTimeout(dropFocus, 0);
  }}, true);
  window.addEventListener("change", function (e) {{
    if (!inGuard(e.target) || !e.target.matches("select")) return;
    setTimeout(dropFocus, 0);
  }}, true);
}})();
</script>
"""


def guard_widgets(*children):
    """Return a VBox of ``children`` protected from notebook keyboard shortcuts."""
    box = widgets.VBox(list(children))
    box.add_class(GUARD_CLASS)
    display(HTML(_GUARD_SCRIPT))
    return box
