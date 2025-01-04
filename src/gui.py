import tkinter as tk
import tkinter.font
from rag import RAG


def centerGeometry(window: tk, width: int, height: int):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/1.5))
    return f"{width}x{height}+{x}+{y}"


class GUI:
    def __init__(self, rag: RAG):
        self.rag = rag

        self.window = tk.Tk()
        self.window.title('rag-bible-hungarian')
        self.window.geometry(centerGeometry(
            window=self.window, width=600, height=600))

        self.font = tkinter.font.Font(size=10)
        self.italic_font = tkinter.font.Font(size=10, slant="italic")

        main_frame = self.create_main_frame(master=self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)

    def create_main_frame(self, master: tk.Widget) -> tk.Frame:
        frame = tk.Frame(master=master)

        input_entry = tk.Entry(
            master=frame, font=self.font)
        input_entry.bind('<Return>', self.on_entry)
        input_entry.focus()
        input_entry.pack(fill=tk.X, expand=True,
                         side=tk.TOP, padx=8, pady=8)

        self.output_text = tk.Text(
            master=frame,  font=self.font)
        self.output_text.tag_configure("<italics>", font=self.italic_font)
        self.output_text.config(state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True,
                              side=tk.BOTTOM, padx=8, pady=8)

        return frame

    def on_entry(self, event) -> None:
        input = event.widget.get()
        if len(input.strip()) == 0:
            return

        event.widget.delete(0, tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, input + '\n\n')
        self.output_text.config(state=tk.DISABLED)

        response = self.rag.query(text=input)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, response, '<italics>')
        self.output_text.config(state=tk.DISABLED)

    def mainloop(self) -> None:
        self.window.mainloop()
