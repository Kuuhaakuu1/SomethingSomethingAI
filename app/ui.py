from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class ReplyOption:
    label: str
    text: str


def show_reply_popup(post_text: str, options: List[ReplyOption]) -> Optional[ReplyOption]:
    root = tk.Tk()
    root.title("Reply Assistant")
    root.geometry("600x400")

    selection = tk.StringVar(value=options[0].label)

    header = tk.Label(root, text="Suggested Post", font=("Arial", 12, "bold"))
    header.pack(pady=8)

    post_box = tk.Text(root, height=6, wrap="word")
    post_box.insert("1.0", post_text)
    post_box.configure(state="disabled", background="#f5f5f5")
    post_box.pack(fill="x", padx=12)

    options_frame = tk.Frame(root)
    options_frame.pack(pady=12, fill="both", expand=True)

    for option in options:
        radio = tk.Radiobutton(
            options_frame,
            text=f"{option.label}: {option.text}",
            variable=selection,
            value=option.label,
            wraplength=560,
            justify="left",
            anchor="w",
        )
        radio.pack(fill="x", padx=8, pady=4)

    result: List[Optional[ReplyOption]] = [None]

    def _confirm() -> None:
        chosen = next((opt for opt in options if opt.label == selection.get()), None)
        result[0] = chosen
        root.destroy()

    confirm_button = tk.Button(root, text="Use Selected Reply", command=_confirm)
    confirm_button.pack(pady=12)

    root.mainloop()
    return result[0]
