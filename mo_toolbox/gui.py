import re
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Any

from ttkwidgets import CheckboxTreeview


def return_var_name_without_counter(var) -> str:
    var_name = re.match(r"\D+", str(var))[0]
    if var_name[-1] == '-':
        return var_name[:-1]
    else:
        return var_name


def cb_disable_state(cb: tk.Checkbutton) -> None:
    cb.configure(state=tk.DISABLED)


def cb_var_uncheck(cb_var: tk.IntVar) -> None:
    cb_var.set(0)


def cb_disable_and_uncheck(cb: tk.Checkbutton, cb_var: tk.IntVar) -> None:
    cb_disable_state(cb)
    cb_var_uncheck(cb_var)


def del_entry_default(entry: ttk.Entry, var: tk.StringVar) -> None:
    var_name = return_var_name_without_counter(var=var)
    entry.bind(
        '<FocusIn>', lambda x: {
            entry.delete(0, tk.END) if var.get() == var_name else entry.configure(foreground='grey'),
            entry.configure(foreground='black') if var.get() != str(var_name) else None
        }
    )
    entry.bind(
        '<FocusOut>', lambda x: {
            entry.insert(0, str(var_name)) if var.get() == '' else entry.configure(foreground='black'),
            entry.configure(foreground='grey') if var.get() == str(var_name) else None
        }
    )


def switch_cb_state(var1: tk.IntVar, cb1: tk.Checkbutton, var2: tk.IntVar, cb2: tk.Checkbutton) -> None:
    if var1.get() == 1:
        cb2.configure(state=tk.DISABLED)
    elif var2.get() == 1:
        cb1.configure(state=tk.DISABLED)
    else:
        cb2.configure(state=tk.NORMAL)
        cb1.configure(state=tk.NORMAL)


def set_strvar_to_none(strvar: tk.StringVar) -> str:
    """Ersetzt StringVar value durch None wenn name=value. Verhindert das default Texte im Dokument landen"""
    if return_var_name_without_counter(strvar) == strvar.get():
        return None if return_var_name_without_counter(strvar) == strvar.get() else strvar.get()


def pbar_counter(progress: int | str, total: int | str) -> str:
    return f'{str(progress).zfill(len(str(total)))} / {total}'


def update_scrollregion(canvas: tk.Canvas, frame: tk.Frame) -> None:
    canvas.update()
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)
    canvas.bind("<Configure>", canvas.configure(scrollregion=canvas.bbox(tk.ALL)))


class BasicScrollFrame(tk.Canvas):
    def __init__(self, master, height=None, width=None):
        super().__init__(master=master, highlightthickness=0)
        self.v_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.configure(yscrollcommand=self.v_scrollbar.set)

        self.scrollframe = tk.Frame(master=self, height=height, width=width)
        self.scrollframe.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        self.pack(fill=tk.BOTH, expand=True)

    def update_scrollbar(self) -> None:
        update_scrollregion(canvas=self, frame=self.scrollframe)


@dataclass(kw_only=True, slots=True)
class TreeViewColumn:
    column: str
    text: str
    width: int
    stretch: bool


class BasicTreeview:
    def __init__(self, master, columns: list[TreeViewColumn], row_height: int, cb_treeview: bool = False, cb_treeview_rowheight: int = 80) -> None:
        self.columns = columns
        self.columns_names: list[str] = [column.column for column in self.columns]
        self.cb_treeview = cb_treeview

        if not self.cb_treeview:
            self.tree = ttk.Treeview(master, columns=self.columns_names, selectmode=tk.BROWSE, height=row_height)
            self.tree['show'] = 'headings'
        else:
            style = ttk.Style()
            style.configure('Checkbox.Treeview', rowheight=cb_treeview_rowheight)
            self.tree = CheckboxTreeview(master, columns=self.columns_names[1:], selectmode=tk.BROWSE, height=row_height)

        used_columns = columns if not cb_treeview else columns[1:]

        for column in used_columns:
            if cb_treeview:
                self.tree.heading(column='#0', text=columns[0].text)
                self.tree.column(column='#0', width=columns[0].width, stretch=columns[0].stretch)
            self.tree.heading(column=column.column, text=column.text)
            self.tree.column(column.column, width=column.width, stretch=column.stretch)

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=10)
        self.tree.pack_propagate(False)

        tree_scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scrollbar.pack(in_=self.tree, side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)

    def fill_rows(self, i: int, row_values: list[str | Any]) -> None:
        self.tree.insert('', tk.END,
                         iid=str(i),
                         text='Index' if not self.cb_treeview else self.columns_names[0],
                         values=row_values,
                         tags=('oddrow',) if i % 2 else ('evenrow',))
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='lightgrey')


