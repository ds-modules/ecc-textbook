"""Reusable ipywidgets chat UI for notebook-based chatbot demos."""

from __future__ import annotations

import html
from typing import Any, Dict, List

import ipywidgets as widgets
from IPython.display import HTML


def _render_history(messages: List[Dict[str, str]]) -> str:
    """Convert chat history into basic HTML for notebook display."""
    chunks = []
    for msg in messages:
        role = html.escape(msg.get("role", "assistant"))
        content = html.escape(msg.get("content", ""))
        color = "#1f77b4" if role == "user" else "#2ca02c" if role == "assistant" else "#555"
        chunks.append(
            (
                "<div style='margin: 8px 0; padding: 8px; border-radius: 8px; "
                "background: #f7f7f7;'>"
                f"<strong style='color: {color};'>{role.title()}:</strong><br>"
                f"<span>{content}</span>"
                "</div>"
            )
        )
    return "".join(chunks) or "<em>No messages yet.</em>"


def launch_chat_ui(client: Any, model: str, system_prompt: str) -> widgets.VBox:
    """Return an interactive chat widget backed by OpenAI chat completions."""
    if client is None:
        raise ValueError("`client` must be an initialized OpenAI client.")

    state: Dict[str, List[Dict[str, str]]] = {
        "messages": [{"role": "system", "content": system_prompt}]
    }

    title = widgets.HTML("<h4 style='margin:0 0 8px 0;'>Interactive Chatbot</h4>")
    transcript = widgets.HTML(value=_render_history([]))
    user_input = widgets.Text(
        value="",
        placeholder="Type a message and press Enter...",
        description="You:",
        layout=widgets.Layout(width="100%"),
    )
    send_button = widgets.Button(description="Send", button_style="primary")
    reset_button = widgets.Button(description="Reset chat", button_style="")
    status = widgets.HTML("<span style='color:#666;'>Ready.</span>")

    def _call_model() -> str:
        completion = client.chat.completions.create(
            model=model,
            messages=state["messages"],
            temperature=0.3,
        )
        return completion.choices[0].message.content or ""

    def _refresh() -> None:
        transcript.value = _render_history(
            [m for m in state["messages"] if m.get("role") != "system"]
        )

    def _send(_=None) -> None:
        text = user_input.value.strip()
        if not text:
            status.value = "<span style='color:#aa5500;'>Enter a message first.</span>"
            return

        user_input.value = ""
        status.value = "<span style='color:#666;'>Thinking...</span>"
        state["messages"].append({"role": "user", "content": text})
        _refresh()

        try:
            answer = _call_model()
            state["messages"].append({"role": "assistant", "content": answer})
            status.value = "<span style='color:#22863a;'>Response received.</span>"
        except Exception as exc:  # pragma: no cover - notebook runtime behavior
            state["messages"].append(
                {
                    "role": "assistant",
                    "content": (
                        "I ran into an API error. Check your key, model name, or network and try again."
                    ),
                }
            )
            status.value = (
                "<span style='color:#b00020;'>Error: "
                f"{html.escape(str(exc))}</span>"
            )
        _refresh()

    def _reset(_=None) -> None:
        state["messages"] = [{"role": "system", "content": system_prompt}]
        _refresh()
        status.value = "<span style='color:#666;'>Chat reset.</span>"

    send_button.on_click(_send)
    reset_button.on_click(_reset)
    user_input.on_submit(_send)

    controls = widgets.HBox(
        [send_button, reset_button], layout=widgets.Layout(justify_content="flex-start")
    )
    container = widgets.VBox([title, transcript, user_input, controls, status])
    return container
