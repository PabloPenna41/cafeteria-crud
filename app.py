import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

import requests


def _carregar_url():
    """URL do backend: variável de ambiente > servidor.txt (ao lado do .exe) > padrão XAMPP."""
    if os.environ.get("CAFETERIA_URL"):
        return os.environ["CAFETERIA_URL"]
    base = os.path.dirname(sys.executable if getattr(sys, "frozen", False)
                           else os.path.abspath(__file__))
    arquivo = os.path.join(base, "servidor.txt")
    if os.path.exists(arquivo):
        with open(arquivo, encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#"):
                    return linha.rstrip("/")
    return "http://localhost/cafeteria/php"


# Ajuste em servidor.txt (ao lado do .exe) conforme onde a pasta "php" está servida
BASE_URL = _carregar_url()
CATEGORIAS = ["Café", "Doce", "Salgado", "Bebida Gelada"]

# Paleta
BG = "#F5EDE3"        # creme
CARD = "#FFFFFF"
ESCURO = "#3B2418"    # café escuro
MARROM = "#6F4E37"
CARAMELO = "#C8863F"
CARAMELO_H = "#B3732F"
VERDE = "#4E8B5F"
VERDE_H = "#3E744E"
VERMELHO = "#B94A48"
VERMELHO_H = "#9C3B39"
CINZA = "#8A7B70"
LINHA = "#F9F3EB"
BORDA = "#E2D5C6"

FONTE = ("Segoe UI", 10)
FONTE_B = ("Segoe UI", 10, "bold")
TITULO = ("Georgia", 20, "bold")

sessao = requests.Session()


def chamar(metodo, pagina, **kwargs):
    """Faz a requisição e devolve (json, erro)."""
    try:
        r = sessao.request(metodo, f"{BASE_URL}/{pagina}", timeout=10, **kwargs)
        return r.json(), None
    except requests.RequestException as e:
        return None, f"Erro de conexão: {e}"
    except ValueError:
        return None, "Resposta inválida do servidor"


def estilizar(root):
    root.configure(bg=BG)
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure(".", font=FONTE, background=BG, foreground=ESCURO)
    s.configure("Card.TFrame", background=CARD, relief="solid", borderwidth=1,
                bordercolor=BORDA)
    s.configure("Bg.TFrame", background=BG)
    s.configure("Card.TLabel", background=CARD, foreground=MARROM, font=FONTE_B)
    s.configure("Titulo.TLabel", background=CARD, foreground=ESCURO, font=("Georgia", 13, "bold"))
    s.configure("Sub.TLabel", background=CARD, foreground=CINZA)
    s.configure("Info.TLabel", background=BG, foreground=CINZA)

    s.configure("TEntry", fieldbackground="#FFFDFA", bordercolor=BORDA, lightcolor=BORDA,
                darkcolor=BORDA, padding=6)
    s.map("TEntry", bordercolor=[("focus", CARAMELO)], lightcolor=[("focus", CARAMELO)],
          darkcolor=[("focus", CARAMELO)])
    s.configure("TCombobox", fieldbackground="#FFFDFA", bordercolor=BORDA, padding=6,
                arrowcolor=MARROM)
    s.map("TCombobox", fieldbackground=[("readonly", "#FFFDFA")],
          bordercolor=[("focus", CARAMELO)])

    def botao(nome, cor, hover):
        s.configure(nome, background=cor, foreground="white", font=FONTE_B, padding=(14, 8),
                    borderwidth=0, focusthickness=0, focuscolor=cor)
        s.map(nome, background=[("active", hover), ("pressed", hover)])

    botao("Primario.TButton", CARAMELO, CARAMELO_H)
    botao("Verde.TButton", VERDE, VERDE_H)
    botao("Perigo.TButton", VERMELHO, VERMELHO_H)
    botao("Escuro.TButton", MARROM, ESCURO)
    s.configure("Suave.TButton", background="#EFE4D6", foreground=MARROM, font=FONTE_B,
                padding=(14, 8), borderwidth=0, focusthickness=0)
    s.map("Suave.TButton", background=[("active", "#E3D3BF")])

    s.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=ESCURO,
                rowheight=34, borderwidth=0, font=FONTE)
    s.configure("Treeview.Heading", background=ESCURO, foreground="#F5EDE3",
                font=FONTE_B, padding=(8, 8), relief="flat")
    s.map("Treeview.Heading", background=[("active", MARROM)])
    s.map("Treeview", background=[("selected", "#F3D9B5")],
          foreground=[("selected", ESCURO)])
    s.configure("Vertical.TScrollbar", background="#D9C7B0", troughcolor=BG,
                bordercolor=BG, arrowcolor=MARROM)


def cabecalho(parent, direita=None):
    barra = tk.Frame(parent, bg=ESCURO, height=64)
    barra.pack(fill="x")
    barra.pack_propagate(False)
    tk.Label(barra, text="☕  Café & Cia", bg=ESCURO, fg="#F5EDE3",
             font=("Georgia", 17, "bold")).pack(side="left", padx=24)
    tk.Label(barra, text="Gestão do cardápio", bg=ESCURO, fg=CARAMELO,
             font=("Segoe UI", 10)).pack(side="left")
    if direita:
        direita(barra)
    return barra


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Café & Cia - Gestão do Cardápio")
        estilizar(self)
        self.atual = None
        self.mostrar_login()

    def trocar(self, frame_cls):
        if self.atual:
            self.atual.destroy()
        self.unbind("<Return>")
        self.atual = frame_cls(self)
        self.atual.pack(fill="both", expand=True)

    def mostrar_login(self):
        self.geometry("460x520")
        self.minsize(460, 520)
        self.trocar(TelaLogin)

    def mostrar_painel(self):
        self.geometry("1060x680")
        self.minsize(900, 600)
        self.trocar(TelaPainel)


class TelaLogin(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)
        self.app = app
        cabecalho(self)

        card = ttk.Frame(self, style="Card.TFrame", padding=30)
        card.place(relx=0.5, rely=0.55, anchor="center", width=360)

        ttk.Label(card, text="Bem-vindo!", style="Titulo.TLabel",
                  font=TITULO).pack(anchor="w")
        ttk.Label(card, text="Acesse o painel do gerente", style="Sub.TLabel").pack(
            anchor="w", pady=(2, 20))

        ttk.Label(card, text="Usuário", style="Card.TLabel").pack(anchor="w")
        self.e_usuario = ttk.Entry(card, font=FONTE)
        self.e_usuario.pack(fill="x", pady=(4, 14))

        ttk.Label(card, text="Senha", style="Card.TLabel").pack(anchor="w")
        self.e_senha = ttk.Entry(card, show="•", font=FONTE)
        self.e_senha.pack(fill="x", pady=(4, 22))

        ttk.Button(card, text="Entrar", style="Primario.TButton",
                   command=self.entrar, cursor="hand2").pack(fill="x")

        self.msg = tk.Label(card, text="", bg=CARD, fg=VERMELHO, font=("Segoe UI", 9))
        self.msg.pack(pady=(10, 0))

        app.bind("<Return>", lambda e: self.entrar())
        self.e_usuario.focus()

    def entrar(self):
        dados, erro = chamar("POST", "login.php", data={
            "usuario": self.e_usuario.get(), "senha": self.e_senha.get()})
        if erro:
            self.msg.config(text=erro)
        elif not dados.get("ok"):
            self.msg.config(text=dados.get("erro", "Falha no login"))
            self.e_senha.delete(0, "end")
        else:
            self.app.mostrar_painel()


class TelaPainel(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)
        self.app = app
        self.editando_id = None
        self.itens = []

        def direita(barra):
            ttk.Button(barra, text="Sair", style="Escuro.TButton", cursor="hand2",
                       command=self.sair).pack(side="right", padx=20)
            self.lbl_user = tk.Label(barra, text="", bg=ESCURO, fg="#F5EDE3", font=FONTE)
            self.lbl_user.pack(side="right")

        cabecalho(self, direita)

        corpo = ttk.Frame(self, style="Bg.TFrame", padding=20)
        corpo.pack(fill="both", expand=True)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        self._montar_form(corpo)
        self._montar_tabela(corpo)
        self.carregar()

    # ---------- Formulário ----------
    def _montar_form(self, corpo):
        self.form = ttk.Frame(corpo, style="Card.TFrame", padding=20)
        self.form.grid(row=0, column=0, sticky="ns", padx=(0, 18))

        self.lbl_form = ttk.Label(self.form, text="Novo item", style="Titulo.TLabel")
        self.lbl_form.pack(anchor="w")
        ttk.Label(self.form, text="Preencha os dados do produto", style="Sub.TLabel").pack(
            anchor="w", pady=(0, 14))

        def campo(rotulo):
            ttk.Label(self.form, text=rotulo, style="Card.TLabel").pack(anchor="w")

        campo("Nome do item")
        self.e_nome = ttk.Entry(self.form, width=32)
        self.e_nome.pack(fill="x", pady=(4, 12))

        campo("Categoria")
        self.c_cat = ttk.Combobox(self.form, values=CATEGORIAS, state="readonly")
        self.c_cat.current(0)
        self.c_cat.pack(fill="x", pady=(4, 12))

        campo("Descrição")
        self.t_desc = tk.Text(self.form, width=32, height=4, font=FONTE, wrap="word",
                              bg="#FFFDFA", fg=ESCURO, relief="solid", bd=1,
                              highlightthickness=1, highlightbackground=BORDA,
                              highlightcolor=CARAMELO, padx=6, pady=6, insertbackground=ESCURO)
        self.t_desc.pack(fill="x", pady=(4, 12))

        campo("Preço (R$)")
        self.e_preco = ttk.Entry(self.form)
        self.e_preco.pack(fill="x", pady=(4, 20))

        self.b_salvar = ttk.Button(self.form, text="＋  Cadastrar", style="Verde.TButton",
                                   command=self.salvar, cursor="hand2")
        self.b_salvar.pack(fill="x")
        self.b_cancelar = ttk.Button(self.form, text="Cancelar edição", style="Suave.TButton",
                                     command=self.limpar, cursor="hand2")
        # só aparece durante a edição

    # ---------- Tabela ----------
    def _montar_tabela(self, corpo):
        card = ttk.Frame(corpo, style="Card.TFrame", padding=20)
        card.grid(row=0, column=1, sticky="nsew")
        card.rowconfigure(1, weight=1)
        card.columnconfigure(0, weight=1)

        topo = ttk.Frame(card, style="Card.TFrame")
        topo.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(topo, text="Itens do cardápio", style="Titulo.TLabel").pack(side="left")
        self.lbl_total = ttk.Label(topo, text="", style="Sub.TLabel")
        self.lbl_total.pack(side="left", padx=10)

        self.busca = tk.StringVar()
        self.busca.trace_add("write", lambda *a: self.preencher())
        ttk.Entry(topo, textvariable=self.busca, width=22).pack(side="right")
        ttk.Label(topo, text="🔍", style="Sub.TLabel").pack(side="right", padx=6)

        cols = ("id", "nome", "categoria", "descricao", "preco")
        wrap = ttk.Frame(card, style="Card.TFrame")
        wrap.grid(row=1, column=0, sticky="nsew")
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="browse")
        for c, t, w, a in (("id", "#", 50, "center"), ("nome", "Nome", 180, "w"),
                           ("categoria", "Categoria", 110, "w"),
                           ("descricao", "Descrição", 260, "w"),
                           ("preco", "Preço", 90, "e")):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor=a, stretch=(c in ("nome", "descricao")))
        self.tree.tag_configure("par", background=LINHA)
        self.tree.tag_configure("impar", background=CARD)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        self.tree.bind("<Double-1>", lambda e: self.editar())

        self.vazio = ttk.Label(wrap, text="Nenhum item cadastrado ainda ☕", style="Sub.TLabel")

        acoes = ttk.Frame(card, style="Card.TFrame")
        acoes.grid(row=2, column=0, sticky="e", pady=(14, 0))
        ttk.Button(acoes, text="✎  Editar", style="Primario.TButton", cursor="hand2",
                   command=self.editar).pack(side="left", padx=(0, 8))
        ttk.Button(acoes, text="🗑  Excluir", style="Perigo.TButton", cursor="hand2",
                   command=self.excluir).pack(side="left")

    # ---------- Lógica ----------
    def carregar(self):
        dados, erro = chamar("GET", "painel.php")
        if erro or not dados.get("ok"):
            messagebox.showerror("Erro", erro or dados.get("erro"))
            return
        self.lbl_user.config(text=f"Olá, {dados.get('usuario', '')}   ")
        self.itens = dados["itens"]
        self.preencher()

    def preencher(self):
        termo = self.busca.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        n = 0
        for i in self.itens:
            if termo and termo not in f"{i['nome_item']} {i['categoria']} {i['descricao']}".lower():
                continue
            self.tree.insert("", "end", tags=("par" if n % 2 else "impar",), values=(
                i["id"], i["nome_item"], i["categoria"], i["descricao"] or "",
                f"R$ {float(i['preco']):.2f}".replace(".", ",")))
            n += 1
        self.lbl_total.config(text=f"{n} item(ns)")
        if n == 0:
            self.vazio.place(relx=0.5, rely=0.4, anchor="center")
        else:
            self.vazio.place_forget()

    def limpar(self):
        self.editando_id = None
        self.lbl_form.config(text="Novo item")
        self.b_salvar.config(text="＋  Cadastrar", style="Verde.TButton")
        self.b_cancelar.pack_forget()
        self.e_nome.delete(0, "end")
        self.t_desc.delete("1.0", "end")
        self.e_preco.delete(0, "end")
        self.c_cat.current(0)

    def salvar(self):
        payload = {
            "nome_item": self.e_nome.get(), "categoria": self.c_cat.get(),
            "descricao": self.t_desc.get("1.0", "end").strip(), "preco": self.e_preco.get()}
        if self.editando_id:
            dados, erro = chamar("POST", f"editar_item.php?id={self.editando_id}", data=payload)
        else:
            dados, erro = chamar("POST", "painel.php", data=payload)
        if erro or not dados.get("ok"):
            messagebox.showerror("Erro", erro or dados.get("erro"))
            return
        self.limpar()
        self.carregar()

    def _id_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Aviso", "Selecione um item na tabela.")
            return None
        return self.tree.item(sel[0])["values"][0]

    def editar(self):
        item_id = self._id_selecionado()
        if item_id is None:
            return
        dados, erro = chamar("GET", f"editar_item.php?id={item_id}")
        if erro or not dados.get("ok"):
            messagebox.showerror("Erro", erro or dados.get("erro"))
            return
        it = dados["item"]
        self.limpar()
        self.editando_id = it["id"]
        self.lbl_form.config(text=f"Editando item #{it['id']}")
        self.b_salvar.config(text="✔  Salvar alterações", style="Primario.TButton")
        self.b_cancelar.pack(fill="x", pady=(8, 0))
        self.e_nome.insert(0, it["nome_item"])
        self.t_desc.insert("1.0", it["descricao"] or "")
        self.e_preco.insert(0, it["preco"])
        if it["categoria"] not in CATEGORIAS:
            self.c_cat.config(values=CATEGORIAS + [it["categoria"]])
        self.c_cat.set(it["categoria"])

    def excluir(self):
        item_id = self._id_selecionado()
        if item_id is None:
            return
        if not messagebox.askyesno("Excluir", "Deseja realmente excluir este item?"):
            return
        dados, erro = chamar("GET", f"excluir_item.php?id={item_id}")
        if erro or not dados.get("ok"):
            messagebox.showerror("Erro", erro or dados.get("erro"))
            return
        if self.editando_id == item_id:
            self.limpar()
        self.carregar()

    def sair(self):
        chamar("GET", "logout.php")
        self.app.mostrar_login()


if __name__ == "__main__":
    App().mainloop()
