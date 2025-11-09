"""Progress indicator utilities."""

import threading
import time
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, List, Optional


class ProgressDialog:
    """Progress dialog for long operations."""

    def __init__(
        self, parent: tk.Tk, title: str = "Processing", message: str = "Please wait..."
    ):
        """Initialize progress dialog.

        Args:
            parent: Parent window
            title: Dialog title
            message: Progress message
        """
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x120")
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.label = tk.Label(self.dialog, text=message, pady=10)
        self.label.pack()

        self.progress = ttk.Progressbar(self.dialog, mode="indeterminate", length=250)
        self.progress.pack(pady=10)

        self.cancel_button = tk.Button(self.dialog, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=5)

        self.cancelled = False
        self.progress.start(10)

        self._center_on_parent()

    def _center_on_parent(self) -> None:
        """Center dialog on parent window."""
        self.dialog.update_idletasks()

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        self.dialog.geometry(f"+{x}+{y}")

    def update_message(self, message: str) -> None:
        """Update progress message.

        Args:
            message: New message
        """
        self.label.config(text=message)
        self.dialog.update()

    def cancel(self) -> None:
        """Cancel operation."""
        self.cancelled = True
        self.close()

    def close(self) -> None:
        """Close progress dialog."""
        self.progress.stop()
        self.dialog.destroy()

    def is_cancelled(self) -> bool:
        """Check if operation was cancelled.

        Returns:
            True if cancelled
        """
        return self.cancelled


def run_with_progress(
    parent: tk.Tk,
    operation: Callable,
    title: str = "Processing",
    message: str = "Please wait...",
) -> Any:
    """Run operation with progress dialog.

    Args:
        parent: Parent window
        operation: Function to execute
        title: Progress dialog title
        message: Progress message

    Returns:
        Operation result or None if cancelled
    """
    result: List[Optional[Any]] = [None]
    exception: List[Optional[Exception]] = [None]

    def worker() -> None:
        try:
            result[0] = operation()
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

    progress = ProgressDialog(parent, title, message)

    while thread.is_alive() and not progress.is_cancelled():
        parent.update()
        time.sleep(0.1)

    progress.close()

    if exception[0]:
        raise exception[0]

    return result[0] if not progress.is_cancelled() else None
