"""Reusable ipywidgets chat UI for notebook-based chatbot demos.

Design notes (JupyterHub / JupyterLab):
- No JavaScript is injected. Untrusted notebooks on the hub do not run scripts,
  so a JS-based fix never ran and its text could leak into the output.
- No buttons. Clicking a button in an output area hands keyboard focus back to
  the notebook, and the next keystroke is treated as a command-mode shortcut
  (for example "o" collapses the cell output). With Enter as the only way to
  send, focus stays in the text box while students type.
- Type /reset in the box to start a new conversation, or re-run the cell.
- chat_loop() is a plain input() fallback that works in any Jupyter frontend.
"""

from __future__ import annotations

import html
import warnings
from typing import Any, Dict, List

import ipywidgets as widgets

RESET_COMMAND = "/reset"
QUIT_WORDS = {"quit", "exit"}


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


def _bind_enter(text_widget: widgets.Text, callback) -> None:
    """Run callback when the user presses Enter in the text box.

    Uses the widget's submit event when available (ipywidgets 7 and 8), so a
    half-typed message is not sent just because the box lost focus. Falls back
    to observing value changes on versions without a submit event.
    """
    on_submit = getattr(text_widget, "on_submit", None)
    if callable(on_submit):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            on_submit(callback)
        return

    text_widget.continuous_update = False

    def _on_change(change):
        if change["new"]:
            callback(text_widget)

    text_widget.observe(_on_change, names="value")


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
        layout=widgets.Layout(width="100%"),
    )
    status = widgets.HTML("<span style='color:#666;'>Ready. Press Enter to send.</span>")

    def _set_status(text: str, color: str = "#666") -> None:
        status.value = f"<span style='color:{color};'>{html.escape(text)}</span>"

    def _visible_messages() -> List[Dict[str, str]]:
        return [m for m in state["messages"] if m.get("role") != "system"]

    def _refresh() -> None:
        transcript.value = _render_history(_visible_messages())

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

    def _on_enter(_widget=None) -> None:
        text = user_input.value
        user_input.value = ""
        send(text)

    _bind_enter(user_input, _on_enter)

    container = widgets.VBox([title, transcript, user_input, status])
    container.send = send
    container.reset = reset
    container.history = _visible_messages
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
