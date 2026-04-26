import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src import storage
from src.month import Month
from src.card import Card
from src.report import generate_report, generate_comparison
import io
import sys

COLORS = {
    "bg": "#1e1e2e",
    "sidebar": "#181825",
    "card": "#313244",
    "accent": "#cba6f7",
    "green": "#a6e3a1",
    "red": "#f38ba8",
    "yellow": "#f9e2af",
    "text": "#cdd6f4",
    "subtext": "#a6adc8",
}

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Control")
        self.root.geometry("900x600")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(True, True)

        self.all_months = storage.load()
        self.current_month = None

        self._build_layout()
        self._show_section("meses")

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=180)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar, text="💰 Finance\nControl",
            bg=COLORS["sidebar"], fg=COLORS["accent"],
            font=("Helvetica", 14, "bold"), pady=20
        ).pack()

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10)

        self.nav_buttons = {}
        sections = [
            ("meses", "📅  Meses"),
            ("reservas", "🏦  Reservas"),
            ("mensalidades", "📱  Mensalidades"),
            ("cartoes", "💳  Cartões"),
            ("relatorio", "📊  Relatório"),
            ("comparativo", "📈  Comparativo"),
        ]

        for key, label in sections:
            btn = tk.Button(
                self.sidebar, text=label, anchor="w",
                bg=COLORS["sidebar"], fg=COLORS["text"],
                font=("Helvetica", 11), bd=0, padx=20, pady=10,
                activebackground=COLORS["card"],
                activeforeground=COLORS["accent"],
                cursor="hand2",
                command=lambda k=key: self._show_section(k)
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        # Botão salvar
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=10)
        tk.Button(
            self.sidebar, text="💾  Salvar",
            bg=COLORS["green"], fg=COLORS["bg"],
            font=("Helvetica", 11, "bold"), bd=0, padx=20, pady=10,
            cursor="hand2", command=self._save
        ).pack(fill="x", padx=10)

        # Área principal
        self.main = tk.Frame(self.root, bg=COLORS["bg"])
        self.main.pack(side="right", fill="both", expand=True)

    def _clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def _show_section(self, section):
        # Highlight botão ativo
        for key, btn in self.nav_buttons.items():
            btn.configure(
                bg=COLORS["card"] if key == section else COLORS["sidebar"],
                fg=COLORS["accent"] if key == section else COLORS["text"]
            )
        self._clear_main()

        sections = {
            "meses": self._section_meses,
            "reservas": self._section_reservas,
            "mensalidades": self._section_mensalidades,
            "cartoes": self._section_cartoes,
            "relatorio": self._section_relatorio,
            "comparativo": self._section_comparativo,
        }
        sections[section]()

    def _header(self, title):
        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="x", padx=20, pady=(20, 10))
        tk.Label(
            frame, text=title,
            bg=COLORS["bg"], fg=COLORS["accent"],
            font=("Helvetica", 16, "bold")
        ).pack(side="left")
        if self.current_month:
            tk.Label(
                frame,
                text=f"  📅 {self.current_month.name}  |  📊 Saldo: R${self.current_month.get_balance():.2f}",
                bg=COLORS["bg"], fg=COLORS["subtext"],
                font=("Helvetica", 10)
            ).pack(side="right")

    def _save(self):
        if not self.current_month:
            messagebox.showwarning("Aviso", "Nenhum mês aberto!")
            return
        self.all_months[self.current_month.name] = storage.month_to_dict(self.current_month)
        storage.save(self.all_months)
        messagebox.showinfo("Sucesso", "✅ Dados salvos!")

    # ─── SEÇÃO MESES ───────────────────────────────────────────
    def _section_meses(self):
        self._header("📅 Meses")

        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        # Lista de meses salvos
        tk.Label(frame, text="Meses salvos:", bg=COLORS["bg"],
                 fg=COLORS["subtext"], font=("Helvetica", 11)).pack(anchor="w")

        listbox_frame = tk.Frame(frame, bg=COLORS["card"], bd=0)
        listbox_frame.pack(fill="x", pady=5)

        listbox = tk.Listbox(
            listbox_frame, bg=COLORS["card"], fg=COLORS["text"],
            font=("Helvetica", 11), selectbackground=COLORS["accent"],
            selectforeground=COLORS["bg"], bd=0, height=8
        )
        listbox.pack(fill="x", padx=5, pady=5)

        for name in self.all_months:
            listbox.insert("end", name)

        def open_month():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione um mês!")
                return
            name = listbox.get(sel[0])
            self.current_month = storage.dict_to_month(self.all_months[name])
            messagebox.showinfo("Sucesso", f"✅ Mês '{name}' carregado!")
            self._show_section("relatorio")

        def delete_month():
            sel = listbox.curselection()
            if not sel:
                return
            name = listbox.get(sel[0])
            if messagebox.askyesno("Confirmar", f"Remover '{name}'?"):
                del self.all_months[name]
                storage.save(self.all_months)
                listbox.delete(sel[0])

        btn_frame = tk.Frame(frame, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=5)

        tk.Button(btn_frame, text="📂 Abrir", bg=COLORS["accent"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=open_month).pack(side="left", padx=(0, 5))

        tk.Button(btn_frame, text="🗑️ Remover", bg=COLORS["red"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=delete_month).pack(side="left")

        # Novo mês
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=15)
        tk.Label(frame, text="Criar novo mês:", bg=COLORS["bg"],
                 fg=COLORS["subtext"], font=("Helvetica", 11)).pack(anchor="w")

        fields_frame = tk.Frame(frame, bg=COLORS["bg"])
        fields_frame.pack(fill="x", pady=5)

        tk.Label(fields_frame, text="Mês/Ano:", bg=COLORS["bg"],
                 fg=COLORS["text"]).grid(row=0, column=0, sticky="w", pady=3)
        name_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=name_var, bg=COLORS["card"],
                 fg=COLORS["text"], insertbackground=COLORS["text"],
                 bd=0, font=("Helvetica", 11), width=20).grid(row=0, column=1, padx=10, pady=3)

        tk.Label(fields_frame, text="Salário:", bg=COLORS["bg"],
                 fg=COLORS["text"]).grid(row=1, column=0, sticky="w", pady=3)
        income_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=income_var, bg=COLORS["card"],
                 fg=COLORS["text"], insertbackground=COLORS["text"],
                 bd=0, font=("Helvetica", 11), width=20).grid(row=1, column=1, padx=10, pady=3)

        tk.Label(fields_frame, text="Limite (opcional):", bg=COLORS["bg"],
                 fg=COLORS["text"]).grid(row=2, column=0, sticky="w", pady=3)
        limit_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=limit_var, bg=COLORS["card"],
                 fg=COLORS["text"], insertbackground=COLORS["text"],
                 bd=0, font=("Helvetica", 11), width=20).grid(row=2, column=1, padx=10, pady=3)

        def create_month():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Aviso", "Digite o nome do mês!")
                return
            try:
                income = float(income_var.get())
            except ValueError:
                messagebox.showwarning("Aviso", "Salário inválido!")
                return
            month = Month(name)
            month.set_income(income)
            if limit_var.get():
                try:
                    month.set_limit(float(limit_var.get()))
                except ValueError:
                    pass
            self.current_month = month
            self.all_months[name] = storage.month_to_dict(month)
            storage.save(self.all_months)
            messagebox.showinfo("Sucesso", f"✅ Mês '{name}' criado!")
            self._show_section("relatorio")

        tk.Button(frame, text="✅ Criar mês", bg=COLORS["green"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=create_month).pack(anchor="w", pady=10)

    # ─── SEÇÃO RESERVAS ────────────────────────────────────────
    def _section_reservas(self):
        self._header("🏦 Reservas")
        if not self.current_month:
            tk.Label(self.main, text="Abra um mês primeiro!",
                     bg=COLORS["bg"], fg=COLORS["red"],
                     font=("Helvetica", 12)).pack(pady=20)
            return

        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        listbox = tk.Listbox(frame, bg=COLORS["card"], fg=COLORS["text"],
                             font=("Helvetica", 11), selectbackground=COLORS["accent"],
                             selectforeground=COLORS["bg"], bd=0, height=10)
        listbox.pack(fill="x", pady=5)

        def refresh():
            listbox.delete(0, "end")
            for r in self.current_month.reserves:
                listbox.insert("end", f"  {r['description']}  —  R${r['amount']:.2f}")

        refresh()

        # Formulário
        form = tk.Frame(frame, bg=COLORS["bg"])
        form.pack(fill="x", pady=10)

        tk.Label(form, text="Descrição:", bg=COLORS["bg"], fg=COLORS["text"]).grid(row=0, column=0, sticky="w")
        desc_var = tk.StringVar()
        tk.Entry(form, textvariable=desc_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, font=("Helvetica", 11),
                 width=25).grid(row=0, column=1, padx=10, pady=3)

        tk.Label(form, text="Valor: R$", bg=COLORS["bg"], fg=COLORS["text"]).grid(row=1, column=0, sticky="w")
        amount_var = tk.StringVar()
        tk.Entry(form, textvariable=amount_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, font=("Helvetica", 11),
                 width=25).grid(row=1, column=1, padx=10, pady=3)

        def add():
            try:
                self.current_month.add_reserve(desc_var.get(), float(amount_var.get()))
                desc_var.set("")
                amount_var.set("")
                refresh()
            except ValueError:
                messagebox.showwarning("Aviso", "Valor inválido!")

        def remove():
            sel = listbox.curselection()
            if not sel:
                return
            self.current_month.reserves.pop(sel[0])
            refresh()

        btn_frame = tk.Frame(frame, bg=COLORS["bg"])
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="➕ Adicionar", bg=COLORS["green"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=add).pack(side="left", padx=(0, 5))

        tk.Button(btn_frame, text="🗑️ Remover", bg=COLORS["red"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=remove).pack(side="left")

        tk.Label(frame, textvariable=tk.StringVar(
            value=f"Total: R${self.current_month.get_total_reserves():.2f}"),
            bg=COLORS["bg"], fg=COLORS["accent"],
            font=("Helvetica", 12, "bold")).pack(anchor="w", pady=10)

    # ─── SEÇÃO MENSALIDADES ────────────────────────────────────
    def _section_mensalidades(self):
        self._header("📱 Mensalidades")
        if not self.current_month:
            tk.Label(self.main, text="Abra um mês primeiro!",
                     bg=COLORS["bg"], fg=COLORS["red"],
                     font=("Helvetica", 12)).pack(pady=20)
            return

        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        listbox = tk.Listbox(frame, bg=COLORS["card"], fg=COLORS["text"],
                             font=("Helvetica", 11), selectbackground=COLORS["accent"],
                             selectforeground=COLORS["bg"], bd=0, height=10)
        listbox.pack(fill="x", pady=5)

        def refresh():
            listbox.delete(0, "end")
            for s in self.current_month.subscriptions:
                listbox.insert("end", f"  {s['description']}  —  R${s['amount']:.2f}")

        refresh()

        form = tk.Frame(frame, bg=COLORS["bg"])
        form.pack(fill="x", pady=10)

        tk.Label(form, text="Descrição:", bg=COLORS["bg"], fg=COLORS["text"]).grid(row=0, column=0, sticky="w")
        desc_var = tk.StringVar()
        tk.Entry(form, textvariable=desc_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, font=("Helvetica", 11),
                 width=25).grid(row=0, column=1, padx=10, pady=3)

        tk.Label(form, text="Valor: R$", bg=COLORS["bg"], fg=COLORS["text"]).grid(row=1, column=0, sticky="w")
        amount_var = tk.StringVar()
        tk.Entry(form, textvariable=amount_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, font=("Helvetica", 11),
                 width=25).grid(row=1, column=1, padx=10, pady=3)

        def add():
            try:
                self.current_month.add_subscription(desc_var.get(), float(amount_var.get()))
                desc_var.set("")
                amount_var.set("")
                refresh()
            except ValueError:
                messagebox.showwarning("Aviso", "Valor inválido!")

        def remove():
            sel = listbox.curselection()
            if not sel:
                return
            self.current_month.subscriptions.pop(sel[0])
            refresh()

        btn_frame = tk.Frame(frame, bg=COLORS["bg"])
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="➕ Adicionar", bg=COLORS["green"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=add).pack(side="left", padx=(0, 5))

        tk.Button(btn_frame, text="🗑️ Remover", bg=COLORS["red"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=remove).pack(side="left")

    # ─── SEÇÃO CARTÕES ─────────────────────────────────────────
    def _section_cartoes(self):
        self._header("💳 Cartões")
        if not self.current_month:
            tk.Label(self.main, text="Abra um mês primeiro!",
                     bg=COLORS["bg"], fg=COLORS["red"],
                     font=("Helvetica", 12)).pack(pady=20)
            return

        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        # Seletor de cartão
        card_names = [c.name for c in self.current_month.cards]
        selected_card = tk.StringVar(value=card_names[0] if card_names else "")

        top = tk.Frame(frame, bg=COLORS["bg"])
        top.pack(fill="x", pady=5)

        tk.Label(top, text="Cartão:", bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        card_menu = ttk.Combobox(top, textvariable=selected_card, values=card_names, width=20)
        card_menu.pack(side="left", padx=10)

        def add_card():
            name = simpledialog.askstring("Novo Cartão", "Nome do cartão:")
            if name:
                self.current_month.add_card(Card(name))
                card_names.append(name)
                card_menu["values"] = card_names
                selected_card.set(name)
                refresh()

        def remove_card():
            name = selected_card.get()
            if not name:
                return
            self.current_month.cards = [c for c in self.current_month.cards if c.name != name]
            card_names.remove(name)
            card_menu["values"] = card_names
            selected_card.set(card_names[0] if card_names else "")
            refresh()

        tk.Button(top, text="➕ Novo cartão", bg=COLORS["accent"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=10, pady=4, cursor="hand2",
                  command=add_card).pack(side="left", padx=5)

        tk.Button(top, text="🗑️", bg=COLORS["red"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=10, pady=4, cursor="hand2",
                  command=remove_card).pack(side="left")

        # Lista de gastos
        listbox = tk.Listbox(frame, bg=COLORS["card"], fg=COLORS["text"],
                             font=("Helvetica", 11), selectbackground=COLORS["accent"],
                             selectforeground=COLORS["bg"], bd=0, height=8)
        listbox.pack(fill="x", pady=5)

        total_label = tk.Label(frame, text="", bg=COLORS["bg"],
                               fg=COLORS["accent"], font=("Helvetica", 11, "bold"))
        total_label.pack(anchor="w")

        def refresh():
            listbox.delete(0, "end")
            name = selected_card.get()
            card = next((c for c in self.current_month.cards if c.name == name), None)
            if not card:
                total_label.config(text="")
                return
            for e in card.list_expenses():
                if e["installments"]:
                    listbox.insert("end", f"  {e['description']} ({e['current']}/{e['installments']}): R${e['amount']:.2f}")
                else:
                    listbox.insert("end", f"  {e['description']}: R${e['amount']:.2f}")
            total_label.config(text=f"Total {name}: R${card.get_total():.2f}")

        card_menu.bind("<<ComboboxSelected>>", lambda e: refresh())
        refresh()

        # Formulário de gasto
        form = tk.Frame(frame, bg=COLORS["bg"])
        form.pack(fill="x", pady=10)

        tk.Label(form, text="Descrição:", bg=COLORS["bg"], fg=COLORS["text"]).grid(row=0, column=0, sticky="w")
        desc_var = tk.StringVar()
        tk.Entry(form, textvariable=desc_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, width=25,
                 font=("Helvetica", 11)).grid(row=0, column=1, padx=10, pady=3)

        tk.Label(form, text="Valor: R$", bg=COLORS["bg"], fg=COLORS["text"]).grid(row=1, column=0, sticky="w")
        amount_var = tk.StringVar()
        tk.Entry(form, textvariable=amount_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, width=25,
                 font=("Helvetica", 11)).grid(row=1, column=1, padx=10, pady=3)

        parcelado_var = tk.BooleanVar()
        tk.Checkbutton(form, text="Parcelado?", variable=parcelado_var,
                       bg=COLORS["bg"], fg=COLORS["text"],
                       selectcolor=COLORS["card"],
                       activebackground=COLORS["bg"]).grid(row=2, column=0, sticky="w", pady=3)

        tk.Label(form, text="Total / Parcelas / Atual:", bg=COLORS["bg"],
                 fg=COLORS["subtext"], font=("Helvetica", 9)).grid(row=3, column=0, sticky="w")

        parc_frame = tk.Frame(form, bg=COLORS["bg"])
        parc_frame.grid(row=3, column=1, sticky="w", padx=10)

        total_var = tk.StringVar()
        inst_var = tk.StringVar()
        curr_var = tk.StringVar()

        tk.Entry(parc_frame, textvariable=total_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, width=8,
                 font=("Helvetica", 11)).pack(side="left", padx=2)
        tk.Entry(parc_frame, textvariable=inst_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, width=5,
                 font=("Helvetica", 11)).pack(side="left", padx=2)
        tk.Entry(parc_frame, textvariable=curr_var, bg=COLORS["card"], fg=COLORS["text"],
                 insertbackground=COLORS["text"], bd=0, width=5,
                 font=("Helvetica", 11)).pack(side="left", padx=2)

        def add_expense():
            name = selected_card.get()
            card = next((c for c in self.current_month.cards if c.name == name), None)
            if not card:
                messagebox.showwarning("Aviso", "Selecione um cartão!")
                return
            try:
                if parcelado_var.get():
                    total = float(total_var.get())
                    inst = int(inst_var.get())
                    curr = int(curr_var.get())
                    amount = round(total / inst, 2)
                    card.add_expense(desc_var.get(), amount, total=total, installments=inst, current=curr)
                else:
                    card.add_expense(desc_var.get(), float(amount_var.get()))
                desc_var.set("")
                amount_var.set("")
                total_var.set("")
                inst_var.set("")
                curr_var.set("")
                refresh()
            except ValueError:
                messagebox.showwarning("Aviso", "Valores inválidos!")

        def remove_expense():
            sel = listbox.curselection()
            if not sel:
                return
            name = selected_card.get()
            card = next((c for c in self.current_month.cards if c.name == name), None)
            if card:
                card.expenses.pop(sel[0])
                refresh()

        btn_frame = tk.Frame(frame, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=5)

        tk.Button(btn_frame, text="➕ Adicionar", bg=COLORS["green"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=add_expense).pack(side="left", padx=(0, 5))

        tk.Button(btn_frame, text="🗑️ Remover", bg=COLORS["red"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=remove_expense).pack(side="left")

    # ─── SEÇÃO RELATÓRIO ───────────────────────────────────────
    def _section_relatorio(self):
        self._header("📊 Relatório")
        if not self.current_month:
            tk.Label(self.main, text="Abra um mês primeiro!",
                     bg=COLORS["bg"], fg=COLORS["red"],
                     font=("Helvetica", 12)).pack(pady=20)
            return

        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        text = tk.Text(frame, bg=COLORS["card"], fg=COLORS["text"],
                       font=("Courier", 11), bd=0, padx=10, pady=10,
                       wrap="word", state="disabled")
        text.pack(fill="both", expand=True)

        # Captura o print do relatório
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        generate_report(self.current_month)
        sys.stdout = old_stdout
        output = buffer.getvalue()

        text.config(state="normal")
        text.delete("1.0", "end")
        text.insert("end", output)
        text.config(state="disabled")

    # ─── SEÇÃO COMPARATIVO ─────────────────────────────────────
    def _section_comparativo(self):
        self._header("📈 Comparativo")

        frame = tk.Frame(self.main, bg=COLORS["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        months_list = list(self.all_months.keys())

        if len(months_list) < 2:
            tk.Label(frame, text="Você precisa ter pelo menos 2 meses salvos!",
                     bg=COLORS["bg"], fg=COLORS["yellow"],
                     font=("Helvetica", 12)).pack(pady=20)
            return

        top = tk.Frame(frame, bg=COLORS["bg"])
        top.pack(fill="x", pady=10)

        tk.Label(top, text="Mês 1:", bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        m1_var = tk.StringVar(value=months_list[0])
        ttk.Combobox(top, textvariable=m1_var, values=months_list, width=15).pack(side="left", padx=10)

        tk.Label(top, text="Mês 2:", bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        m2_var = tk.StringVar(value=months_list[1])
        ttk.Combobox(top, textvariable=m2_var, values=months_list, width=15).pack(side="left", padx=10)

        text = tk.Text(frame, bg=COLORS["card"], fg=COLORS["text"],
                       font=("Courier", 11), bd=0, padx=10, pady=10,
                       wrap="word", state="disabled")
        text.pack(fill="both", expand=True, pady=10)

        def compare():
            m1 = storage.dict_to_month(self.all_months[m1_var.get()])
            m2 = storage.dict_to_month(self.all_months[m2_var.get()])
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            generate_comparison(m1, m2)
            sys.stdout = old_stdout
            output = buffer.getvalue()
            text.config(state="normal")
            text.delete("1.0", "end")
            text.insert("end", output)
            text.config(state="disabled")

        tk.Button(top, text="📊 Comparar", bg=COLORS["accent"],
                  fg=COLORS["bg"], font=("Helvetica", 10, "bold"),
                  bd=0, padx=15, pady=6, cursor="hand2",
                  command=compare).pack(side="left", padx=10)


def run_gui():
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()