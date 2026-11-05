import customtkinter as ctk
from pathlib import Path
from customtkinter import filedialog
from src.components.base_screen import BaseScreen
from src.components.tab import Tabview
from src.components.switch import Switch
from src.components.input import Input
from src.components.botao import Botao
from src.components.container import Container
from src.components.message import Message
from src.components.label import Label
from src.services.itens import ApuracaoItens
from src.services.servico import ApuracaoService

class LayoutSystem(BaseScreen):
    def __init__(self, titulo = "Apuração fiscal", min_width = 600, min_height = 420):
        super().__init__(titulo = titulo, min_width = min_width, min_height = min_height)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.swtich = Switch(master=self, text="Modo escuro", command=self.mudar_tema)
        self.swtich.grid(row=0, column=0, sticky="s", pady=(0,10))
        self.swtich.set(True)

        self.tabview = Tabview(master=self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 50))

        self.tab_item = self.tabview.add("Itens")
        self.tab_item.grid_columnconfigure(0, weight=1)
        self.tab_item.grid_rowconfigure(0, weight=1)
        self.tab_servico = self.tabview.add("Serviço")
        self.tab_servico.grid_columnconfigure(0, weight=1)
        self.tab_servico.grid_rowconfigure(0, weight=1)

        # Aba item
        self.container_item = Container(self.tab_item)
        self.container_item.grid_columnconfigure(0, weight=1)
        self.container_item.grid_columnconfigure(1, weight=0)
        self.container_item.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.arquivo_empresa = Input(self.container_item, placeholder_text="Insira o livro do ICMS/IPI da empresa")
        self.arquivo_empresa.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        self.btn_aquivo_empresa = Botao(self.container_item, text="Procurar...", command=lambda: self.selecionar_arquivo(self.arquivo_empresa))
        self.btn_aquivo_empresa.grid(row=0, column=1, padx=5, pady=10)

        self.arquivo_icms_contabilidade = Input(self.container_item, placeholder_text="Insira o livro do ICMS da contabilidade")
        self.arquivo_icms_contabilidade.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        self.btn_arquivo_icms_contabilidade = Botao(self.container_item, text="Prourar...", command=lambda: self.selecionar_arquivo(self.arquivo_icms_contabilidade))
        self.btn_arquivo_icms_contabilidade.grid(row=1, column=1, padx=5, pady=10)

        self.arquivo_ipi_contabilidade = Input(self.container_item, placeholder_text="Insira o livro do IPI da contabilidade")
        self.arquivo_ipi_contabilidade.grid(row=2, column=0, sticky='ew', padx=5, pady=10)
        self.btn_arquivo_ipi_contabilidade = Botao(self.container_item, text="Procurar...", command=lambda: self.selecionar_arquivo(self.arquivo_ipi_contabilidade))
        self.btn_arquivo_ipi_contabilidade.grid(row=2, column=1, padx=5, pady=10)

        self.btn_executar = Botao(self.tab_item, text="Realizar apuração", command=self.realizar_apuracao_itens)
        self.btn_executar.grid(row=1, column=0, padx=(5))

        # Aba servico
        self.container_service = Container(self.tab_servico)
        self.container_service.grid_columnconfigure(0, weight=1)
        self.container_service.grid_columnconfigure(1, weight=0)
        self.container_service.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.arquivo_servico_empresa = Input(self.container_service, placeholder_text="Insira o livro de serviço da empresa")
        self.arquivo_servico_empresa.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        self.btn_aquivo_empresa = Botao(self.container_service, text="Procurar...", command=lambda: self.selecionar_arquivo(self.arquivo_servico_empresa))
        self.btn_aquivo_empresa.grid(row=0, column=1, padx=5, pady=10)

        self.arquivo_servico_contabilidade = Input(self.container_service, placeholder_text="Insira o livro de serviço da contabilidade")
        self.arquivo_servico_contabilidade.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        self.btn_arquivo_servico_contabilidade = Botao(self.container_service, text="Prourar...", command=lambda: self.selecionar_arquivo(self.arquivo_servico_contabilidade))
        self.btn_arquivo_servico_contabilidade.grid(row=1, column=1, padx=5, pady=10)

        self.btn_executar = Botao(self.tab_servico, text="Realizar apuração", command=self.realizar_apuracao_servico)
        self.btn_executar.grid(row=1, column=0, padx=(5))

        self.by_creator = Label(master=self, text="by iz - 20/10/2026")
        self.by_creator.grid(row=0, column=0, sticky="se", pady=(0,10), padx=(0,10))


    def realizar_apuracao_itens(self):           
        self.caminho_empresa = self.arquivo_empresa.get()
        self.caminho_imcs_contabilidade = self.arquivo_icms_contabilidade.get()
        self.caminho_ipi_contabilidade = self.arquivo_ipi_contabilidade.get()

        # Validação
        if not self.caminho_empresa:
            Message(title="Erro!", message="Livro da empresa, não inserido!", icon="cancel", option_1="OK")
            return
        
        if not self.caminho_imcs_contabilidade:
            Message(title="Erro!", message="Livro do ICMS da contabilidade, não inserido!", icon="cancel", option_1="OK")
            return
        
        if not self.caminho_ipi_contabilidade:
            Message(title="Erro!", message="Livro do IPI da contabilidade, não inserido!", icon="cancel", option_1="OK")
            return

        ApuracaoItens.executar(self.caminho_empresa, self.caminho_imcs_contabilidade, self.caminho_ipi_contabilidade)
        Message(title="Sucesso", message="Apuração realizada com sucesso!", icon="check", option_1="OK")
        self.limpeza_campos_itens()

    def realizar_apuracao_servico(self):
        self.caminho_servico_empresa = self.arquivo_servico_empresa.get()
        self.caminho_servico_contabilidadde = self.arquivo_servico_contabilidade.get()

        ApuracaoService.executar(self.caminho_servico_empresa, self.caminho_servico_contabilidadde)
        Message(title="Sucesso", message="Apuração realizada com sucesso!", icon="check", option_1="OK")
        self.limpeza_campos_servico()

    def mudar_tema(self):
        self.tema_atual = ctk.get_appearance_mode()

        if self.tema_atual == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def limpeza_campos_itens(self):
        self.arquivo_empresa.delete(0, "end")
        self.arquivo_empresa.configure(placeholder_text="Insira o livro do ICMS/IPI da empresa")
        self.arquivo_icms_contabilidade.delete(0, "end")
        self.arquivo_icms_contabilidade.configure(placeholder_text="Insira o livro do ICMS da contabilidade")
        self.arquivo_ipi_contabilidade.delete(0, "end")
        self.arquivo_ipi_contabilidade.configure(placeholder_text="Insira o livro do IPI da contabilidade")

    def limpeza_campos_servico(self):
        self.arquivo_servico_empresa.delete(0, "end")
        self.arquivo_servico_empresa.configure(placeholder_text="Insira o livro de serviço da empresa")
        self.arquivo_servico_contabilidade.delete(0, "end")
        self.arquivo_servico_contabilidade.configure(placeholder_text="Insira o livro de serviço da contabilidade")

    def selecionar_arquivo(self, entry_widget):
        """Abre a janela para escolher o arquivo Excel correspondente"""
        arquivo = filedialog.askopenfilename(
            title="Selecione a planilha",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        if arquivo:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, arquivo)
