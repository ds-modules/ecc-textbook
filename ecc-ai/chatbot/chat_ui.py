"""Reusable ipywidgets chat UI for notebook-based chatbot demos.

Design notes (JupyterHub, JupyterLab, Notebook 7):
- Enter sends. The text box uses continuous_update=False, so the browser sends
  the complete message in one update when Enter is pressed. (The older
  on_submit event races with throttled keystroke updates and can send only the
  first character when the kernel is busy.)
- No buttons. A clicked button keeps keyboard focus, and the next keystroke is
  then handled as a notebook shortcut.
- A small script keeps focus in the text box when the student clicks anywhere
  in the chat area, and ignores half-typed text when the box loses focus. In
  Notebook 7 the "o" shortcut hides cell outputs, which makes the chat vanish
  if focus has drifted out of the box. The chat still works without the script.
- Type /reset in the box to start a new conversation, or re-run the cell.
- chat_loop() is a plain input() fallback that works in any Jupyter frontend.
"""

from __future__ import annotations

import html
from typing import Any, Dict, List

import ipywidgets as widgets
from IPython.display import HTML, display

RESET_COMMAND = "/reset"
QUIT_WORDS = {"quit", "exit"}
_CHAT_CLASS = "ecc-chat-ui"

_FOCUS_SCRIPT = f"""
<script>
(function () {{
  if (window.__eccChatFocusInstalled) return;
  window.__eccChatFocusInstalled = true;
  var BOX = ".{_CHAT_CLASS}";

  function inputOf(el) {{
    if (!(el instanceof Element)) return null;
    var box = el.closest(BOX);
    return box ? box.querySelector("input[type=text]") : null;
  }}
  function isEditable(el) {{
    return el.matches("input, textarea, select, [contenteditable=true]");
  }}

  // Clicking anywhere in the chat area keeps focus in the text box.
  window.addEventListener("mousedown", function (e) {{
    var input = inputOf(e.target);
    if (!input || isEditable(e.target)) return;
    e.preventDefault();
    input.focus();
  }}, true);

  // Keys pressed on a non-editable part of the chat area are swallowed before
  // the notebook sees them, and focus moves to the text box.
  window.addEventListener("keydown", function (e) {{
    var input = inputOf(e.target);
    if (!input || isEditable(e.target)) return;
    e.stopPropagation();
    e.preventDefault();
    input.focus();
  }}, true);

  // Send on Enter only. The browser also fires "change" when the box loses
  // focus, which would send a half-typed message; swallow those.
  window.addEventListener("keydown", function (e) {{
    var input = inputOf(e.target);
    if (!input || e.target !== input) return;
    e.stopPropagation();
    if (e.key !== "Enter") return;
    input.__eccEnter = true;
    input.dispatchEvent(new Event("change", {{ bubbles: true }}));
    input.__eccEnter = false;
  }}, true);
  window.addEventListener("change", function (e) {{
    var input = inputOf(e.target);
    if (!input || e.target !== input) return;
    if (!input.__eccEnter) e.stopPropagation();
  }}, true);
}})();
</script>
"""


def _render_history(messages: List[Dict[str, str]]) -> str:
    """Convert chat history into basic HTML for notebook display."""
    chunks = []
    for msg in messages:
        role = html.escape(msg.get("role", "assistant"))
        content = html.escape(msg.get("content", "")).replace("\n", "<br>")
        color = "#1f77b4" if role == "user" else "#2ca02c" if role == "assistant" else "#555"
        chunks.append(
            "<div style='margin: 8px 0; padding: 8px; border-radius: 8px; background: #f7f7f7;'>"
            f"<strong style='color: {color};'>{role.title()}:</strong><br>"
            f"<span>{content}</span>"
            "</div>"
        )
    return "".join(chunks) or "<em>No messages yet. Type below and press Enter.</em>"


def launch_chat_ui(client: Any, model: str, system_prompt: str) -> widgets.VBox:
    """Return an interactive chat widget backed by OpenAI chat completions.

    The returned widget also exposes ``.send(text)`` and ``.reset()`` so the
    chat can be driven from code.
    """
    if client is None:
        raise ValueError("`client` must be an initialized OpenAI client.")

    state: Dict[str, List[Dict[str, str]]] = {
        "messages": [{"role": "system", "content": system_prompt}]
    }

    title = widgets.HTML("<h4 style='margin:0 0 8px 0;'>Interactive Chatbot</h4>")
    transcript = widgets.HTML(value=_render_history([]))
    user_input = widgets.Text(
        value="",
        placeholder="Type a message and press Enter. Type /reset to start over.",
        description="You:",
        continuous_update=False,
        layout=widgets.Layout(width="100%"),
    )
    status = widgets.HTML("<span style='color:#666;'>Ready. Press Enter to send.</span>")

    def _set_status(text: str, color: str = "#666") -> None:
        status.value = f"<span style='color:{color};'>{html.escape(text)}</span>"

    def _visible_messages() -> List[Dict[str, str]]:
        return [m for m in state["messages"] if m.get("role") != "system"]

    def _focus_input() -> None:
        focus = getattr(user_input, "focus", None)  # ipywidgets >= 8
        if callable(focus):
            focus()

    def _refresh() -> None:
        transcript.value = _render_history(_visible_messages())
        _focus_input()

    def _call_model() -> str:
        completion = client.chat.completions.create(
            model=model,
            messages=state["messages"],
            temperature=0.3,
        )
        return completion.choices[0].message.content or ""

    def reset() -> None:
        state["messages"] = [{"role": "system", "content": system_prompt}]
        _refresh()
        _set_status("Chat reset. Press Enter to send.")

    def send(text: str) -> None:
        text = (text or "").strip()
        if not text:
            _set_status("Enter a message first.", "#aa5500")
            return
        if text.lower() == RESET_COMMAND:
            reset()
            return

        state["messages"].append({"role": "user", "content": text})
        _refresh()
        _set_status("Thinking...")

        try:
            answer = _call_model()
            state["messages"].append({"role": "assistant", "content": answer})
            _set_status("Response received.", "#22863a")
        except Exception as exc:  # pragma: no cover - notebook runtime behavior
            state["messages"].append(
                {
                    "role": "assistant",
                    "content": "I ran into an API error. Check your key, model name, or network and try again.",
                }
            )
            _set_status(f"Error: {exc}", "#b00020")
        _refresh()

    def _on_value(change) -> None:
        text = change["new"]
        if not text:
            return
        user_input.value = ""
        send(text)

    user_input.observe(_on_value, names="value")

    container = widgets.VBox([title, transcript, user_input, status])
    container.add_class(_CHAT_CLASS)
    container.send = send
    container.reset = reset
    container.history = _visible_messages
    display(HTML(_FOCUS_SCRIPT))
    return container


def chat_loop(client: Any, model: str, system_prompt: str) -> List[Dict[str, str]]:
    """Plain-text chat using input(). Works in every Jupyter frontend.

    Type quit or exit to stop. Returns the full message history.
    """
    if client is None:
        raise ValueError("`client` must be an initialized OpenAI client.")

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    print("Chat started. Type quit to stop.\n")
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChat ended.")
            return messages
        if not text:
            continue
        if text.lower() in QUIT_WORDS:
            print("Chat ended.")
            return messages

        messages.append({"role": "user", "content": text})
        try:
            completion = client.chat.completions.create(
                model=model, messages=messages, temperature=0.3
            )
            answer = completion.choices[0].message.content or ""
        except Exception as exc:  # pragma: no cover - notebook runtime behavior
            answer = f"I ran into an API error: {exc}"
        messages.append({"role": "assistant", "content": answer})
        print(f"Assistant: {answer}\n")
