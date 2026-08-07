import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import random
import shutil
from datetime import datetime, date, timedelta
import csv
from tkcalendar import Calendar, DateEntry  # Precisaremos instalar o tkcalendar: pip install tkcalendar

class EstudosConcursoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Estudos para Concurso")
        self.root.geometry("1024x768")
        
        # Flag para controlar se a interface já foi criada
        self.interface_criada = False
        
        # Configurar cores e estilos personalizados
        self.cores = {
            'primaria': '#2196F3',  # Azul material
            'secundaria': '#FFC107',  # Amarelo material
            'fundo': '#F5F5F5',  # Cinza claro
            'texto': '#212121',  # Cinza escuro
            'sucesso': '#4CAF50',  # Verde material
            'alerta': '#F44336'   # Vermelho material
        }
        
        # Configurar tema e estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usar tema clam que é mais moderno
        self.configurar_estilos()
        
        # Configurar a cor de fundo da janela principal
        self.root.configure(bg=self.cores['fundo'])
        
        # Diretório de dados
        self.diretorio_dados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_concursos")
        if not os.path.exists(self.diretorio_dados):
            os.makedirs(self.diretorio_dados)
            
        # Arquivo que armazena a lista de concursos
        self.arquivo_concursos = os.path.join(self.diretorio_dados, "concursos.json")
        
        # Lista de concursos e concurso atual
        self.concursos = []
        self.concurso_atual = None
        self.nome_concurso_atual = ""
        
        # Verificar se já existem concursos cadastrados
        self.carregar_lista_concursos()
        
        # Se não houver concursos, mostrar a tela de criação de concurso
        if not self.concursos:
            self.mostrar_tela_selecao_concurso()
        else:
            # Se houver concursos, carregar o último concurso selecionado
            ultimo_concurso = self.carregar_ultimo_concurso_selecionado()
            if ultimo_concurso and ultimo_concurso in self.concursos:
                self.carregar_concurso(ultimo_concurso)
            else:
                self.mostrar_tela_selecao_concurso()
    
    def carregar_lista_concursos(self):
        """Carrega a lista de concursos cadastrados"""
        if os.path.exists(self.arquivo_concursos):
            try:
                with open(self.arquivo_concursos, 'r', encoding='utf-8') as file:
                    dados = json.load(file)
                    self.concursos = dados.get("concursos", [])
                    # Verificar o formato correto
                    if not isinstance(self.concursos, list):
                        self.concursos = []
            except Exception as e:
                print(f"Erro ao carregar lista de concursos: {e}")
                self.concursos = []
    
    def salvar_lista_concursos(self):
        """Salva a lista de concursos cadastrados"""
        try:
            dados = {
                "concursos": self.concursos,
                "ultimo_selecionado": self.nome_concurso_atual
            }
            with open(self.arquivo_concursos, 'w', encoding='utf-8') as file:
                json.dump(dados, ensure_ascii=False, indent=4, fp=file)
        except Exception as e:
            print(f"Erro ao salvar lista de concursos: {e}")
    
    def carregar_ultimo_concurso_selecionado(self):
        """Carrega o nome do último concurso selecionado"""
        if os.path.exists(self.arquivo_concursos):
            try:
                with open(self.arquivo_concursos, 'r', encoding='utf-8') as file:
                    dados = json.load(file)
                    return dados.get("ultimo_selecionado", None)
            except Exception as e:
                print(f"Erro ao carregar último concurso: {e}")
                return None
        return None
    
    def carregar_concurso(self, nome_concurso):
        """Carrega os dados de um concurso específico"""
        self.nome_concurso_atual = nome_concurso
        
        # Atualizar o último concurso selecionado
        self.salvar_lista_concursos()
        
        # Carregar dados do concurso
        diretorio_concurso = os.path.join(self.diretorio_dados, self.nome_concurso_atual)
        arquivo_dados = os.path.join(diretorio_concurso, "dados_concurso.json")
        
        # Se o diretório do concurso não existir, criar
        if not os.path.exists(diretorio_concurso):
            os.makedirs(diretorio_concurso)
        
        # Carregar dados básicos do concurso
        if os.path.exists(arquivo_dados):
            try:
                with open(arquivo_dados, 'r', encoding='utf-8') as file:
                    self.concurso_atual = json.load(file)
            except Exception as e:
                print(f"Erro ao carregar dados do concurso: {e}")
                self.concurso_atual = self.criar_estrutura_concurso_padrao(nome_concurso)
        else:
            # Se o arquivo não existir, criar estrutura padrão
            self.concurso_atual = self.criar_estrutura_concurso_padrao(nome_concurso)
            self.salvar_dados_concurso()
        
        # Atualizar dados do concurso
        self.conteudo_programatico = self.concurso_atual.get("conteudo_programatico", {})
        self.meta_diaria = self.concurso_atual.get("meta_diaria", 140)
        self.disciplinas = list(self.conteudo_programatico.keys())
        
        # Carregar progresso do concurso
        self.arquivo_progresso = os.path.join(diretorio_concurso, "progresso.json")
        self.progresso = {}
        self.ciclos_completos = 0
        self.questoes_hoje = 0
        self.data_atual = date.today().isoformat()
        self.assuntos_do_dia = []
        self.assunto_atual = None
        self.disciplina_atual = None
        
        # Carregar dados se existirem
        self.carregar_progresso()
        
        # Verificar se é um novo dia
        self.verificar_novo_dia()
        
        # Inicializar progresso para novos assuntos se necessário
        self.inicializar_progresso()
        
        # Atualizar o título da janela
        self.root.title(f"Gerenciador de Estudos - {self.nome_concurso_atual}")
        
        # Atualizar o label do concurso atual, se existir
        if hasattr(self, 'lbl_concurso_atual'):
            self.lbl_concurso_atual.config(text=f"Concurso: {self.nome_concurso_atual}")
        
        # Se a interface já foi criada, atualizar
        if self.interface_criada:
            # Limpar a interface atual
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # Recriar a interface
            self.interface_criada = False
            self.criar_interface()
            self.gerar_assuntos_do_dia()
            self.atualizar_exibicao()
        else:
            # Criar interface
            self.criar_interface()
            
            # Gerar assuntos do dia e atualizar interface
            self.gerar_assuntos_do_dia()
            self.atualizar_exibicao()
    
    def criar_estrutura_concurso_padrao(self, nome_concurso):
        """Cria uma estrutura padrão para um novo concurso"""
        return {
            "nome": nome_concurso,
            "meta_diaria": 140,
            "conteudo_programatico": {
                "EXEMPLO - MATEMÁTICA": [
                    "Álgebra",
                    "Geometria",
                    "Trigonometria"
                ],
                "EXEMPLO - PORTUGUÊS": [
                    "Gramática",
                    "Interpretação de Texto",
                    "Redação"
                ]
            }
        }
    
    def salvar_dados_concurso(self):
        """Salva os dados do concurso atual"""
        if not self.concurso_atual or not self.nome_concurso_atual:
            return
            
        # Atualizar os dados do concurso atual
        self.concurso_atual["conteudo_programatico"] = self.conteudo_programatico
        self.concurso_atual["meta_diaria"] = self.meta_diaria
        
        # Salvar no arquivo
        diretorio_concurso = os.path.join(self.diretorio_dados, self.nome_concurso_atual)
        arquivo_dados = os.path.join(diretorio_concurso, "dados_concurso.json")
        
        # Garantir que o diretório existe
        if not os.path.exists(diretorio_concurso):
            os.makedirs(diretorio_concurso)
            
        try:
            with open(arquivo_dados, 'w', encoding='utf-8') as file:
                json.dump(self.concurso_atual, ensure_ascii=False, indent=4, fp=file)
        except Exception as e:
            print(f"Erro ao salvar dados do concurso: {e}")
    
    def mostrar_tela_selecao_concurso(self):
        """Mostra a tela de seleção de concurso"""
        # Limpar qualquer widget existente
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.interface_criada = False
        
        # Frame principal
        frame_principal = ttk.Frame(self.root, style='Card.TFrame', padding=20)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(frame_principal, text="Selecione um Concurso", 
               style='Titulo.TLabel').pack(pady=(0, 20))
        
        # Lista de concursos
        lista_frame = ttk.LabelFrame(frame_principal, text="Concursos Disponíveis", padding=10)
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Criar uma lista para mostrar os concursos
        if self.concursos:
            for concurso in self.concursos:
                # Frame para cada concurso
                concurso_frame = ttk.Frame(lista_frame)
                concurso_frame.pack(fill=tk.X, pady=5)
                
                # Nome do concurso
                ttk.Label(concurso_frame, text=concurso, 
                       style='Subtitulo.TLabel').pack(side=tk.LEFT, pady=5)
                
                # Botões de ação
                btn_selecionar = ttk.Button(concurso_frame, text="Selecionar", 
                                         command=lambda c=concurso: self.carregar_concurso(c),
                                         style='Primario.TButton')
                btn_selecionar.pack(side=tk.RIGHT, padx=(5, 0))
                
                btn_editar = ttk.Button(concurso_frame, text="Editar", 
                                     command=lambda c=concurso: self.editar_concurso(c))
                btn_editar.pack(side=tk.RIGHT, padx=(5, 0))
                
                btn_excluir = ttk.Button(concurso_frame, text="Excluir", 
                                      command=lambda c=concurso: self.excluir_concurso(c))
                btn_excluir.pack(side=tk.RIGHT, padx=(5, 0))
                
                # Separador
                ttk.Separator(lista_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        else:
            ttk.Label(lista_frame, text="Nenhum concurso cadastrado. Crie um novo concurso para começar.",
                   style='Subtitulo.TLabel').pack(pady=20)
        
        # Botão para criar novo concurso
        btn_novo = ttk.Button(frame_principal, text="Novo Concurso", 
                           command=self.criar_novo_concurso,
                           style='Sucesso.TButton')
        btn_novo.pack(side=tk.RIGHT, pady=(10, 0))
    
    def criar_novo_concurso(self):
        """Abre a janela para criar um novo concurso"""
        # Janela para criação de novo concurso
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Concurso")
        dialog.geometry("600x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal
        frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome do concurso
        ttk.Label(frame, text="Nome do Concurso:", style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        nome_entry = ttk.Entry(frame, width=50)
        nome_entry.pack(fill=tk.X, pady=(0, 20))
        nome_entry.focus_set()
        
        # Meta diária
        ttk.Label(frame, text="Meta Diária (questões):", style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        meta_entry = ttk.Entry(frame, width=10)
        meta_entry.insert(0, "140")
        meta_entry.pack(anchor=tk.W, pady=(0, 20))
        
        # Opções de criação
        ttk.Label(frame, text="Conteúdo Programático:", style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        # Variável para o tipo de criação
        tipo_var = tk.StringVar(value="padrao")
        
        # Opções
        ttk.Radiobutton(frame, text="Usar modelo padrão de exemplo", 
                      variable=tipo_var, value="padrao").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Criar a partir de outro concurso", 
                      variable=tipo_var, value="copiar").pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Importar de arquivo JSON", 
                      variable=tipo_var, value="importar").pack(anchor=tk.W)
        
        # Combobox para seleção de concurso a copiar
        ttk.Label(frame, text="Concurso base (se 'Criar a partir de outro'):", 
               style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        concurso_base_combo = ttk.Combobox(frame, values=self.concursos, state="readonly")
        if self.concursos:
            concurso_base_combo.current(0)
        concurso_base_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Botão para selecionar arquivo
        arquivo_var = tk.StringVar()
        ttk.Label(frame, text="Arquivo JSON (se 'Importar'):", 
               style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        arquivo_frame = ttk.Frame(frame)
        arquivo_frame.pack(fill=tk.X, pady=(0, 20))
        
        arquivo_entry = ttk.Entry(arquivo_frame, textvariable=arquivo_var, width=40)
        arquivo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_arquivo = ttk.Button(arquivo_frame, text="Selecionar", 
                              command=lambda: self.selecionar_arquivo_json(arquivo_var))
        btn_arquivo.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Botões de ação
        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(fill=tk.X, pady=(20, 0))
        
        btn_cancelar = ttk.Button(botoes_frame, text="Cancelar", 
                               command=dialog.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=(5, 0))
        
        btn_criar = ttk.Button(botoes_frame, text="Criar Concurso", 
                            command=lambda: self.finalizar_criacao_concurso(
                                nome_entry.get(), 
                                meta_entry.get(), 
                                tipo_var.get(),
                                concurso_base_combo.get() if tipo_var.get() == "copiar" else None,
                                arquivo_var.get() if tipo_var.get() == "importar" else None,
                                dialog
                            ),
                            style='Sucesso.TButton')
        btn_criar.pack(side=tk.RIGHT)
    
    def selecionar_arquivo_json(self, var):
        """Abre um diálogo para selecionar arquivo JSON"""
        filename = filedialog.askopenfilename(
            title="Selecionar Arquivo JSON",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if filename:
            var.set(filename)
    
    def finalizar_criacao_concurso(self, nome, meta, tipo, concurso_base=None, arquivo=None, dialog=None):
        """Finaliza a criação de um novo concurso"""
        # Validar nome
        if not nome:
            messagebox.showerror("Erro", "O nome do concurso é obrigatório.")
            return
            
        # Verificar se já existe um concurso com este nome
        if nome in self.concursos:
            messagebox.showerror("Erro", f"Já existe um concurso com o nome '{nome}'.")
            return
            
        # Validar meta
        try:
            meta = int(meta)
            if meta <= 0:
                raise ValueError("Meta deve ser um número positivo")
        except ValueError:
            messagebox.showerror("Erro", "A meta diária deve ser um número inteiro positivo.")
            return
        
        # Criar estrutura do concurso
        novo_concurso = {
            "nome": nome,
            "meta_diaria": meta,
            "conteudo_programatico": {}
        }
        
        # Determinar o conteúdo programático com base no tipo
        if tipo == "padrao":
            novo_concurso["conteudo_programatico"] = self.criar_estrutura_concurso_padrao(nome)["conteudo_programatico"]
        elif tipo == "copiar" and concurso_base:
            # Copiar conteúdo de outro concurso
            diretorio_base = os.path.join(self.diretorio_dados, concurso_base)
            arquivo_dados_base = os.path.join(diretorio_base, "dados_concurso.json")
            
            if os.path.exists(arquivo_dados_base):
                try:
                    with open(arquivo_dados_base, 'r', encoding='utf-8') as file:
                        dados_base = json.load(file)
                        novo_concurso["conteudo_programatico"] = dados_base.get("conteudo_programatico", {})
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao copiar conteúdo: {str(e)}")
                    return
            else:
                messagebox.showerror("Erro", f"Arquivo de dados do concurso base não encontrado.")
                return
        elif tipo == "importar" and arquivo:
            # Importar de arquivo JSON
            if not os.path.exists(arquivo):
                messagebox.showerror("Erro", f"Arquivo não encontrado: {arquivo}")
                return
                
            try:
                with open(arquivo, 'r', encoding='utf-8') as file:
                    dados_importados = json.load(file)
                    
                    # Verificar se o formato é correto
                    if not isinstance(dados_importados, dict):
                        messagebox.showerror("Erro", "Formato de arquivo inválido. Esperado um objeto JSON.")
                        return
                        
                    # Se for um arquivo de concurso completo
                    if "conteudo_programatico" in dados_importados:
                        novo_concurso["conteudo_programatico"] = dados_importados["conteudo_programatico"]
                    # Se for apenas o conteúdo programático
                    else:
                        novo_concurso["conteudo_programatico"] = dados_importados
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar arquivo: {str(e)}")
                return
        
        # Adicionar o concurso à lista
        self.concursos.append(nome)
        self.salvar_lista_concursos()
        
        # Atualizar o submenu de concursos
        if hasattr(self, 'submenu_concursos'):
            self.atualizar_submenu_concursos()
        
        # Salvar os dados do concurso
        self.nome_concurso_atual = nome
        self.concurso_atual = novo_concurso
        self.salvar_dados_concurso()
        
        # Fechar a janela de diálogo
        if dialog:
            dialog.destroy()
        
        # Carregar o novo concurso
        self.carregar_concurso(nome)
        
        # Mostrar mensagem de sucesso
        messagebox.showinfo("Sucesso", f"Concurso '{nome}' criado com sucesso!")
    
    def editar_concurso(self, nome_concurso):
        """Abre a janela para editar um concurso existente"""
        # Carregar dados do concurso
        diretorio_concurso = os.path.join(self.diretorio_dados, nome_concurso)
        arquivo_dados = os.path.join(diretorio_concurso, "dados_concurso.json")
        
        dados_concurso = None
        if os.path.exists(arquivo_dados):
            try:
                with open(arquivo_dados, 'r', encoding='utf-8') as file:
                    dados_concurso = json.load(file)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar dados do concurso: {str(e)}")
                return
        
        if not dados_concurso:
            messagebox.showerror("Erro", "Dados do concurso não encontrados.")
            return
        
        # Janela para edição do concurso
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar Concurso - {nome_concurso}")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal
        frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome do concurso
        ttk.Label(frame, text="Nome do Concurso:", style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        nome_entry = ttk.Entry(frame, width=50)
        nome_entry.insert(0, nome_concurso)
        nome_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Meta diária
        ttk.Label(frame, text="Meta Diária (questões):", style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        meta_entry = ttk.Entry(frame, width=10)
        meta_entry.insert(0, str(dados_concurso.get("meta_diaria", 140)))
        meta_entry.pack(anchor=tk.W, pady=(0, 20))
        
        # Conteúdo Programático
        ttk.Label(frame, text="Conteúdo Programático:", style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        # Frame para disciplinas e assuntos
        conteudo_frame = ttk.LabelFrame(frame, text="Disciplinas e Assuntos", padding=10)
        conteudo_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Notebook para disciplinas
        notebook = ttk.Notebook(conteudo_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dicionário para armazenar widgets de texto de cada disciplina
        disciplinas_widgets = {}
        
        # Função para adicionar uma disciplina
        def adicionar_disciplina():
            nome_disciplina = disciplina_entry.get().strip()
            if not nome_disciplina:
                messagebox.showerror("Erro", "O nome da disciplina é obrigatório.")
                return
                
            if nome_disciplina in disciplinas_widgets:
                messagebox.showerror("Erro", f"A disciplina '{nome_disciplina}' já existe.")
                return
            
            # Criar uma aba para a disciplina
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=nome_disciplina)
            
            # Área de texto para os assuntos
            texto = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=10)
            texto.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Adicionar ao dicionário
            disciplinas_widgets[nome_disciplina] = texto
            
            # Limpar o campo
            disciplina_entry.delete(0, tk.END)
        
        # Função para remover uma disciplina
        def remover_disciplina():
            # Obter a aba selecionada
            indice_selecionado = notebook.index("current")
            if indice_selecionado < 0:
                messagebox.showerror("Erro", "Nenhuma disciplina selecionada.")
                return
                
            # Obter o nome da disciplina
            nome_disciplina = notebook.tab(indice_selecionado, "text")
            
            # Confirmar a remoção
            resposta = messagebox.askyesno("Remover Disciplina", 
                                        f"Deseja realmente remover a disciplina '{nome_disciplina}'?\nTodos os assuntos serão perdidos.")
            
            if resposta:
                # Remover do dicionário
                if nome_disciplina in disciplinas_widgets:
                    del disciplinas_widgets[nome_disciplina]
                
                # Remover a aba
                notebook.forget(indice_selecionado)
        
        # Adicionar disciplinas existentes
        conteudo_programatico = dados_concurso.get("conteudo_programatico", {})
        for disciplina, assuntos in conteudo_programatico.items():
            # Criar uma aba para a disciplina
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=disciplina)
            
            # Área de texto para os assuntos
            texto = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=10)
            texto.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Adicionar os assuntos
            for assunto in assuntos:
                texto.insert(tk.END, assunto + "\n")
            
            # Adicionar ao dicionário
            disciplinas_widgets[disciplina] = texto
        
        # Frame para adicionar disciplinas
        add_disciplina_frame = ttk.Frame(conteudo_frame)
        add_disciplina_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(add_disciplina_frame, text="Nova Disciplina:").pack(side=tk.LEFT, padx=(0, 5))
        disciplina_entry = ttk.Entry(add_disciplina_frame, width=30)
        disciplina_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_add_disciplina = ttk.Button(add_disciplina_frame, text="Adicionar", 
                                      command=adicionar_disciplina,
                                      style='Primario.TButton')
        btn_add_disciplina.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_remover_disciplina = ttk.Button(add_disciplina_frame, text="Remover Selecionada", 
                                         command=remover_disciplina)
        btn_remover_disciplina.pack(side=tk.LEFT)
        
        # Botões de importação/exportação
        import_export_frame = ttk.Frame(frame)
        import_export_frame.pack(fill=tk.X, pady=(0, 20))
        
        btn_importar = ttk.Button(import_export_frame, text="Importar de JSON", 
                               command=lambda: self.importar_conteudo_json(disciplinas_widgets))
        btn_importar.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_exportar = ttk.Button(import_export_frame, text="Exportar para JSON", 
                               command=lambda: self.exportar_conteudo_json(disciplinas_widgets))
        btn_exportar.pack(side=tk.LEFT)
        
        # Botões de ação
        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(fill=tk.X, pady=(20, 0))
        
        btn_cancelar = ttk.Button(botoes_frame, text="Cancelar", 
                               command=dialog.destroy)
        btn_cancelar.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Função para salvar as alterações
        def salvar_alteracoes():
            # Obter o novo nome do concurso
            novo_nome = nome_entry.get().strip()
            if not novo_nome:
                messagebox.showerror("Erro", "O nome do concurso é obrigatório.")
                return
                
            # Verificar se o nome mudou e já existe outro concurso com este nome
            if novo_nome != nome_concurso and novo_nome in self.concursos:
                messagebox.showerror("Erro", f"Já existe um concurso com o nome '{novo_nome}'.")
                return
                
            # Validar meta
            try:
                nova_meta = int(meta_entry.get())
                if nova_meta <= 0:
                    raise ValueError("Meta deve ser um número positivo")
            except ValueError:
                messagebox.showerror("Erro", "A meta diária deve ser um número inteiro positivo.")
                return
            
            # Construir o novo conteúdo programático
            novo_conteudo = {}
            for disciplina, texto_widget in disciplinas_widgets.items():
                # Obter texto do widget
                texto = texto_widget.get("1.0", tk.END).strip()
                # Dividir em linhas e remover linhas vazias
                assuntos = [linha.strip() for linha in texto.split("\n") if linha.strip()]
                
                # Adicionar ao dicionário
                if assuntos:  # Só adicionar se houver assuntos
                    novo_conteudo[disciplina] = assuntos
            
            # Se o dicionário estiver vazio, mostrar erro
            if not novo_conteudo:
                messagebox.showerror("Erro", "O conteúdo programático não pode estar vazio.")
                return
            
            # Atualizar os dados do concurso
            dados_concurso["nome"] = novo_nome
            dados_concurso["meta_diaria"] = nova_meta
            dados_concurso["conteudo_programatico"] = novo_conteudo
            
            # Se o nome mudou, atualizar a lista de concursos e renomear o diretório
            if novo_nome != nome_concurso:
                # Atualizar na lista
                indice = self.concursos.index(nome_concurso)
                self.concursos[indice] = novo_nome
                
                # Atualizar o submenu de concursos
                if hasattr(self, 'submenu_concursos'):
                    self.atualizar_submenu_concursos()
                
                # Renomear o diretório
                antigo_diretorio = os.path.join(self.diretorio_dados, nome_concurso)
                novo_diretorio = os.path.join(self.diretorio_dados, novo_nome)
                
                try:
                    if os.path.exists(antigo_diretorio):
                        # Se já existir um diretório com o novo nome, fazer backup
                        if os.path.exists(novo_diretorio):
                            backup_dir = f"{novo_diretorio}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            shutil.move(novo_diretorio, backup_dir)
                        
                        # Renomear o diretório
                        shutil.move(antigo_diretorio, novo_diretorio)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao renomear diretório: {str(e)}")
                    return
                
                # Atualizar o último concurso selecionado se for o atual
                if self.nome_concurso_atual == nome_concurso:
                    self.nome_concurso_atual = novo_nome
            
            # Salvar a lista de concursos
            self.salvar_lista_concursos()
            
            # Salvar os dados do concurso
            arquivo_dados = os.path.join(os.path.join(self.diretorio_dados, novo_nome), "dados_concurso.json")
            diretorio = os.path.dirname(arquivo_dados)
            
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
                
            try:
                with open(arquivo_dados, 'w', encoding='utf-8') as file:
                    json.dump(dados_concurso, ensure_ascii=False, indent=4, fp=file)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar dados do concurso: {str(e)}")
                return
            
            # Fechar a janela
            dialog.destroy()
            
            # Se for o concurso atual, recarregar
            if self.nome_concurso_atual == nome_concurso:
                self.carregar_concurso(novo_nome)
            
            # Atualizar a tela de seleção
            self.mostrar_tela_selecao_concurso()
            
            # Mostrar mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Concurso '{novo_nome}' atualizado com sucesso!")
        
        # Botão para salvar
        btn_salvar = ttk.Button(botoes_frame, text="Salvar Alterações", 
                             command=salvar_alteracoes,
                             style='Sucesso.TButton')
        btn_salvar.pack(side=tk.RIGHT)
    
    def importar_conteudo_json(self, widgets_dict):
        """Importa conteúdo programático de um arquivo JSON"""
        filename = filedialog.askopenfilename(
            title="Importar Conteúdo",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                dados = json.load(file)
                
                # Verificar o formato
                conteudo = None
                if "conteudo_programatico" in dados and isinstance(dados["conteudo_programatico"], dict):
                    conteudo = dados["conteudo_programatico"]
                elif isinstance(dados, dict):
                    conteudo = dados
                
                if not conteudo:
                    messagebox.showerror("Erro", "Formato de arquivo inválido.")
                    return
                
                # Perguntar se deseja substituir ou adicionar
                resposta = messagebox.askyesno("Importar Conteúdo", 
                                          "Deseja substituir o conteúdo atual?\n\n"
                                          "Sim = Substituir tudo\n"
                                          "Não = Adicionar ao conteúdo atual")
                
                if resposta:
                    # Limpar widgets existentes
                    for widget in list(widgets_dict.values()):
                        notebook = widget.master.master
                        notebook.forget(0, notebook.index("end"))
                    
                    widgets_dict.clear()
                
                # Adicionar novo conteúdo
                notebook = None
                for disciplina, assuntos in conteudo.items():
                    if disciplina in widgets_dict:
                        # Disciplina já existe, adicionar ao final
                        widget = widgets_dict[disciplina]
                        texto_atual = widget.get("1.0", tk.END).strip()
                        if texto_atual:
                            widget.insert(tk.END, "\n")
                        
                        for assunto in assuntos:
                            widget.insert(tk.END, assunto + "\n")
                    else:
                        # Nova disciplina
                        if not notebook:
                            for widget in widgets_dict.values():
                                notebook = widget.master.master
                                break
                        
                        if not notebook:
                            messagebox.showerror("Erro", "Notebook não encontrado.")
                            return
                        
                        # Criar uma aba para a disciplina
                        tab = ttk.Frame(notebook)
                        notebook.add(tab, text=disciplina)
                        
                        # Área de texto para os assuntos
                        texto = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=10)
                        texto.pack(fill=tk.BOTH, expand=True, pady=10)
                        
                        # Adicionar os assuntos
                        for assunto in assuntos:
                            texto.insert(tk.END, assunto + "\n")
                        
                        # Adicionar ao dicionário
                        widgets_dict[disciplina] = texto
                
                messagebox.showinfo("Sucesso", "Conteúdo importado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar conteúdo: {str(e)}")
    
    def exportar_conteudo_json(self, widgets_dict):
        """Exporta conteúdo programático para um arquivo JSON"""
        # Construir o conteúdo programático
        conteudo = {}
        for disciplina, texto_widget in widgets_dict.items():
            # Obter texto do widget
            texto = texto_widget.get("1.0", tk.END).strip()
            # Dividir em linhas e remover linhas vazias
            assuntos = [linha.strip() for linha in texto.split("\n") if linha.strip()]
            
            # Adicionar ao dicionário
            if assuntos:  # Só adicionar se houver assuntos
                conteudo[disciplina] = assuntos
        
        # Se o dicionário estiver vazio, mostrar erro
        if not conteudo:
            messagebox.showerror("Erro", "O conteúdo programático não pode estar vazio.")
            return
        
        # Pedir nome do arquivo
        filename = filedialog.asksaveasfilename(
            title="Exportar Conteúdo",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump({"conteudo_programatico": conteudo}, ensure_ascii=False, indent=4, fp=file)
                
            messagebox.showinfo("Sucesso", f"Conteúdo exportado com sucesso para '{filename}'!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar conteúdo: {str(e)}")
    
    def excluir_concurso(self, nome_concurso):
        """Exclui um concurso da lista"""
        # Confirmar exclusão
        resposta = messagebox.askyesno("Excluir Concurso", 
                                   f"Deseja realmente excluir o concurso '{nome_concurso}'?\n\n"
                                   "Todos os dados serão perdidos!")
        
        if not resposta:
            return
            
        # Verificar se é o concurso atual
        if self.nome_concurso_atual == nome_concurso:
            messagebox.showerror("Erro", "Não é possível excluir o concurso atual. Selecione outro concurso primeiro.")
            return
            
        # Remover da lista
        if nome_concurso in self.concursos:
            self.concursos.remove(nome_concurso)
            
        # Salvar a lista
        self.salvar_lista_concursos()
        
        # Atualizar o submenu de concursos
        if hasattr(self, 'submenu_concursos'):
            self.atualizar_submenu_concursos()
        
        # Excluir diretório do concurso
        diretorio_concurso = os.path.join(self.diretorio_dados, nome_concurso)
        if os.path.exists(diretorio_concurso):
            try:
                shutil.rmtree(diretorio_concurso)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir diretório: {str(e)}")
        
        # Atualizar a tela de seleção
        self.mostrar_tela_selecao_concurso()
        
        # Mostrar mensagem de sucesso
        messagebox.showinfo("Sucesso", f"Concurso '{nome_concurso}' excluído com sucesso!")
    
    def configurar_estilos(self):
        """Configura estilos personalizados para widgets"""
        # Configurar cores de fundo
        self.style.configure('TFrame', background=self.cores['fundo'])
        self.style.configure('TLabelframe', background=self.cores['fundo'])
        self.style.configure('TLabelframe.Label', background=self.cores['fundo'])
        self.style.configure('TNotebook', background=self.cores['fundo'])
        self.style.configure('TNotebook.Tab', background=self.cores['fundo'],
                           padding=[10, 5])
        
        # Estilo para frames
        self.style.configure('Card.TFrame',
                           background=self.cores['fundo'])
        
        # Estilo para labels
        self.style.configure('Titulo.TLabel',
                           font=('Segoe UI', 16, 'bold'),
                           foreground=self.cores['texto'],
                           background=self.cores['fundo'])
        self.style.configure('Subtitulo.TLabel',
                           font=('Segoe UI', 12),
                           foreground=self.cores['texto'],
                           background=self.cores['fundo'])
        self.style.configure('TLabel',
                           background=self.cores['fundo'])
        
        # Estilo para botões
        self.style.configure('Primario.TButton',
                           font=('Segoe UI', 10),
                           padding=5)
        self.style.configure('Sucesso.TButton',
                           font=('Segoe UI', 10),
                           padding=5)
        
        # Estilo para progressbar
        self.style.configure('Horizontal.TProgressbar',
                           troughcolor=self.cores['fundo'],
                           background=self.cores['primaria'],
                           lightcolor=self.cores['primaria'],
                           darkcolor=self.cores['primaria'])
        
        # Estilo para Treeview
        self.style.configure('Treeview',
                           background='white',
                           fieldbackground='white',
                           foreground=self.cores['texto'])
        self.style.configure('Treeview.Heading',
                           font=('Segoe UI', 9, 'bold'))
        
        # Mapear estados dos widgets
        self.style.map('Treeview',
                      background=[('selected', self.cores['primaria'])],
                      foreground=[('selected', 'white')])
        
        self.style.map('TNotebook.Tab',
                      background=[('selected', 'white')],
                      foreground=[('selected', self.cores['texto'])])
        
        self.style.map('Primario.TButton',
                      background=[('active', self.cores['primaria'])],
                      foreground=[('active', 'white')])
        
        self.style.map('Sucesso.TButton',
                      background=[('active', self.cores['sucesso'])],
                      foreground=[('active', 'white')])
    
    def criar_interface(self):
        """Cria a interface principal do aplicativo"""
        # Área de notificação - Movida para o início
        self.criar_area_notificacao()
        
        # Criar notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Estudo
        self.tab_estudo = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_estudo, text='📚 Estudo do Dia')
        self.criar_aba_estudo()
        
        # Aba de Revisão
        self.tab_revisao = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_revisao, text='🔍 Revisão')
        self.criar_aba_revisao()
        
        # Aba de Estatísticas
        self.tab_stats = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_stats, text='📊 Estatísticas')
        self.criar_aba_estatisticas()
        
        # Aba de Histórico
        self.tab_historico = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_historico, text='📅 Histórico')
        self.criar_aba_historico()
        
        # Menu principal
        self.criar_menu()
        
        # Marcar que a interface foi criada
        self.interface_criada = True
    
    def criar_aba_estudo(self):
        """Cria o conteúdo da aba de estudo"""
        # Container principal com padding
        container = ttk.Frame(self.tab_estudo, style='Card.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header = ttk.Frame(container)
        header.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header, text="Disciplina Atual:", style='Titulo.TLabel').pack(anchor=tk.W)
        self.lbl_disciplina = ttk.Label(header, text="", style='Subtitulo.TLabel')
        self.lbl_disciplina.pack(anchor=tk.W, pady=(5, 0))
        
        # Área do assunto atual
        assunto_frame = ttk.LabelFrame(container, text="Assunto em Estudo", padding=10)
        assunto_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.lbl_assunto = ttk.Label(assunto_frame, text="", style='Subtitulo.TLabel', wraplength=800)
        self.lbl_assunto.pack(fill=tk.X, pady=(0, 10))
        
        # Progresso do assunto
        progresso_frame = ttk.Frame(assunto_frame)
        progresso_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_progresso_assunto = ttk.Label(progresso_frame, text="0/20 questões")
        self.lbl_progresso_assunto.pack(side=tk.LEFT)
        
        self.progresso_bar = ttk.Progressbar(progresso_frame, orient="horizontal",
                                           length=400, mode="determinate",
                                           style='Horizontal.TProgressbar')
        self.progresso_bar.pack(side=tk.LEFT, padx=(10, 0))
        
        # Área de notas
        notas_frame = ttk.LabelFrame(container, text="Suas Anotações", padding=10)
        notas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.txt_notas = scrolledtext.ScrolledText(notas_frame, wrap=tk.WORD, height=8,
                                                 font=('Segoe UI', 10))
        self.txt_notas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.btn_salvar_notas = ttk.Button(notas_frame, text="💾 Salvar Anotações",
                                         command=self.salvar_notas, style='Primario.TButton')
        self.btn_salvar_notas.pack(anchor=tk.E)
        
        # Botões de controle
        botoes_frame = ttk.Frame(container)
        botoes_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_meta = ttk.Button(botoes_frame, text="✅ Meta Cumprida!",
                                command=self.meta_cumprida, style='Sucesso.TButton')
        self.btn_meta.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_proximo = ttk.Button(botoes_frame, text="➡️ Próximo Assunto",
                                   command=self.proximo_assunto, style='Primario.TButton')
        self.btn_proximo.pack(side=tk.LEFT)
    
    def criar_aba_estatisticas(self):
        """Cria o conteúdo da aba de estatísticas"""
        # Container principal com padding
        container = ttk.Frame(self.tab_stats, style='Card.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Meta diária
        meta_frame = ttk.LabelFrame(container, text="Meta Diária", padding=10)
        meta_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(meta_frame, text=f"Meta: {self.meta_diaria} questões",
                style='Subtitulo.TLabel').pack(anchor=tk.W)
        
        self.lbl_questoes_hoje = ttk.Label(meta_frame,
                                        text=f"Questões hoje: {self.questoes_hoje}/{self.meta_diaria}")
        self.lbl_questoes_hoje.pack(anchor=tk.W, pady=(5, 5))
        
        self.progresso_diario_bar = ttk.Progressbar(meta_frame, orient="horizontal",
                                                  length=400, mode="determinate",
                                                  style='Horizontal.TProgressbar')
        self.progresso_diario_bar.pack(anchor=tk.W)
        
        # Progresso geral
        progresso_frame = ttk.LabelFrame(container, text="Progresso Geral", padding=10)
        progresso_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Grid de estatísticas
        grid = ttk.Frame(progresso_frame)
        grid.pack(fill=tk.BOTH, expand=True)
        
        # Primeira coluna
        col1 = ttk.Frame(grid)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.lbl_total_assuntos = ttk.Label(col1, text="Assuntos totais: 0")
        self.lbl_total_assuntos.pack(anchor=tk.W, pady=2)
        
        self.lbl_assuntos_concluidos = ttk.Label(col1, text="Assuntos concluídos: 0")
        self.lbl_assuntos_concluidos.pack(anchor=tk.W, pady=2)
        
        self.lbl_percentual_concluido = ttk.Label(col1, text="Percentual concluído: 0%")
        self.lbl_percentual_concluido.pack(anchor=tk.W, pady=2)
        
        # Segunda coluna
        col2 = ttk.Frame(grid)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.lbl_total_questoes = ttk.Label(col2, text="Total de questões: 0")
        self.lbl_total_questoes.pack(anchor=tk.W, pady=2)
        
        self.lbl_ciclos_completos = ttk.Label(col2, text="Ciclos completos: 0")
        self.lbl_ciclos_completos.pack(anchor=tk.W, pady=2)
        
        # Barra de progresso geral
        ttk.Label(progresso_frame, text="Progresso do ciclo atual:").pack(anchor=tk.W, pady=(20, 5))
        self.progresso_geral_bar = ttk.Progressbar(progresso_frame, orient="horizontal",
                                                length=400, mode="determinate",
                                                style='Horizontal.TProgressbar')
        self.progresso_geral_bar.pack(anchor=tk.W)
    
    def criar_aba_historico(self):
        """Cria o conteúdo da aba de histórico"""
        # Container principal com padding
        container = ttk.Frame(self.tab_historico, style='Card.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Treeview para histórico
        colunas = ('disciplina', 'assunto', 'status', 'data', 'questoes')
        self.tree = ttk.Treeview(container, columns=colunas, show='headings')
        
        # Definir cabeçalhos
        self.tree.heading('disciplina', text='Disciplina')
        self.tree.heading('assunto', text='Assunto')
        self.tree.heading('status', text='Status')
        self.tree.heading('data', text='Data de Conclusão')
        self.tree.heading('questoes', text='Questões')
        
        # Configurar colunas
        self.tree.column('disciplina', width=200)
        self.tree.column('assunto', width=300)
        self.tree.column('status', width=100)
        self.tree.column('data', width=150)
        self.tree.column('questoes', width=100)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Atualizar histórico
        self.atualizar_historico()
    
    def criar_menu(self):
        """Cria o menu principal"""
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="📊 Exportar Progresso (CSV)",
                              command=self.exportar_progresso)
        arquivo_menu.add_command(label="🔄 Reiniciar Ciclo",
                              command=self.reiniciar_ciclo)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="❌ Sair", command=self.root.quit)
        
        # Menu Concursos
        concursos_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Concursos", menu=concursos_menu)
        concursos_menu.add_command(label="🔄 Trocar de Concurso", 
                                command=self.mostrar_tela_selecao_concurso)
        concursos_menu.add_command(label="✏️ Editar Concurso Atual", 
                                command=lambda: self.editar_concurso(self.nome_concurso_atual))
        concursos_menu.add_command(label="➕ Novo Concurso", 
                                command=self.criar_novo_concurso)
        concursos_menu.add_separator()
        
        # Submenu para selecionar concurso diretamente
        self.submenu_concursos = tk.Menu(concursos_menu, tearoff=0)
        concursos_menu.add_cascade(label="Selecionar Concurso", menu=self.submenu_concursos)
        
        # Preencher submenu com concursos
        self.atualizar_submenu_concursos()
    
    def atualizar_submenu_concursos(self):
        """Atualiza o submenu de concursos com a lista atual"""
        # Limpar submenu
        self.submenu_concursos.delete(0, tk.END)
        
        # Adicionar concursos
        if self.concursos:
            for concurso in self.concursos:
                self.submenu_concursos.add_command(
                    label=concurso,
                    command=lambda c=concurso: self.carregar_concurso(c)
                )
        else:
            self.submenu_concursos.add_command(
                label="Nenhum concurso disponível",
                state="disabled"
            )
    
    def criar_area_notificacao(self):
        """Cria a área de notificação"""
        self.frame_notificacao = ttk.Frame(self.root)
        self.frame_notificacao.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame para informações
        info_frame = ttk.Frame(self.frame_notificacao)
        info_frame.pack(fill=tk.X)
        
        # Indicador do concurso atual
        concurso_frame = ttk.Frame(info_frame)
        concurso_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.lbl_concurso_atual = ttk.Label(concurso_frame, 
                                        text=f"Concurso: {self.nome_concurso_atual}",
                                        font=('Segoe UI', 9),
                                        foreground=self.cores['primaria'])
        self.lbl_concurso_atual.pack(side=tk.LEFT)
        
        # Botão para trocar de concurso rapidamente
        btn_trocar = ttk.Button(concurso_frame, text="Trocar", 
                             command=self.mostrar_tela_selecao_concurso,
                             width=8)
        btn_trocar.pack(side=tk.LEFT, padx=5)
        
        # Notificação
        self.lbl_notificacao = ttk.Label(self.frame_notificacao, text="",
                                      font=('Segoe UI', 10, 'bold'),
                                      foreground=self.cores['sucesso'])
        self.lbl_notificacao.pack(pady=5)
    
    def atualizar_historico(self):
        """Atualiza a visualização do histórico"""
        # Limpar itens existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar dados do progresso
        for disciplina, assuntos in self.progresso.items():
            if disciplina == "ultima_data":
                continue
                
            for assunto, dados in assuntos.items():
                status = "Concluído" if dados["concluido"] else "Em andamento"
                
                # Formatar a data para exibição no formato dd/mm/aaaa hh:mm
                data = "-"
                if dados["data_conclusao"]:
                    data_obj = datetime.strptime(dados["data_conclusao"], "%Y-%m-%d %H:%M:%S")
                    data = data_obj.strftime("%d/%m/%Y %H:%M")
                
                questoes = f"{dados['questoes_resolvidas']}/20"
                
                self.tree.insert('', tk.END, values=(
                    disciplina,
                    assunto,
                    status,
                    data,
                    questoes
                ))
    
    def verificar_novo_dia(self):
        """Verifica se é um novo dia e reinicia a contagem diária se necessário"""
        data_hoje = date.today().isoformat()
        
        if "ultima_data" in self.progresso:
            ultima_data = self.progresso["ultima_data"]
            
            if ultima_data != data_hoje:
                # É um novo dia, reiniciar contagem
                self.questoes_hoje = 0
                self.progresso["ultima_data"] = data_hoje
                self.data_atual = data_hoje
                self.salvar_progresso()
        else:
            # Primeira vez que o programa é executado
            self.progresso["ultima_data"] = data_hoje
            self.data_atual = data_hoje
            self.salvar_progresso()
    
    def reiniciar_ciclo(self):
        """Reinicia o ciclo atual mantendo a contagem de ciclos completos"""
        resposta = messagebox.askyesno("Reiniciar Ciclo", "Deseja realmente reiniciar o ciclo atual? Isso manterá a contagem de ciclos completos, mas reiniciará o progresso de todos os assuntos no ciclo atual.")
        
        if not resposta:
            return
            
        # Marcar todos os assuntos como não concluídos, preservando as notas
        for disciplina in self.progresso:
            if disciplina == "ultima_data":
                continue
                
            for assunto in self.progresso[disciplina]:
                # Preservar as notas existentes
                notas = self.progresso[disciplina][assunto].get("notas", "")
                
                self.progresso[disciplina][assunto]["questoes_resolvidas"] = 0
                self.progresso[disciplina][assunto]["concluido"] = False
                self.progresso[disciplina][assunto]["data_conclusao"] = None
                self.progresso[disciplina][assunto]["notas"] = notas  # Preservar as notas
                
        # Salvar progresso
        self.salvar_progresso()
        
        # Gerar novos assuntos do dia
        self.gerar_assuntos_do_dia()
        
        # Atualizar interface
        self.atualizar_exibicao()
        
        # Mostrar mensagem na interface sem popup
        self.mostrar_notificacao("Ciclo reiniciado com sucesso!")
    
    def criar_aba_revisao(self):
        """Cria o conteúdo da aba de revisão"""
        # Container principal com padding
        container = ttk.Frame(self.tab_revisao, style='Card.TFrame')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header = ttk.Frame(container)
        header.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header, text="Revisão de Estudos", style='Titulo.TLabel').pack(anchor=tk.W)
        ttk.Label(header, text="Selecione um período para revisar seus estudos", 
                  style='Subtitulo.TLabel').pack(anchor=tk.W, pady=(5, 0))
        
        # Frame para seleção de período
        periodo_frame = ttk.LabelFrame(container, text="Período de Revisão", padding=10)
        periodo_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Frame para botões de período predefinido
        botoes_periodo = ttk.Frame(periodo_frame)
        botoes_periodo.pack(fill=tk.X, pady=(0, 10))
        
        # Botões de período predefinido
        btn_hoje = ttk.Button(botoes_periodo, text="Hoje", 
                          command=lambda: self.selecionar_periodo_predefinido("hoje"),
                          style='Primario.TButton')
        btn_hoje.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_semana = ttk.Button(botoes_periodo, text="Última Semana", 
                            command=lambda: self.selecionar_periodo_predefinido("semana"),
                            style='Primario.TButton')
        btn_semana.pack(side=tk.LEFT, padx=5)
        
        btn_mes = ttk.Button(botoes_periodo, text="Último Mês", 
                         command=lambda: self.selecionar_periodo_predefinido("mes"),
                         style='Primario.TButton')
        btn_mes.pack(side=tk.LEFT, padx=5)
        
        btn_todos = ttk.Button(botoes_periodo, text="Todos", 
                           command=lambda: self.selecionar_periodo_predefinido("todos"),
                           style='Primario.TButton')
        btn_todos.pack(side=tk.LEFT, padx=5)
        
        # Frame para calendário personalizado
        calendario_frame = ttk.Frame(periodo_frame)
        calendario_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(calendario_frame, text="Data Inicial:").pack(side=tk.LEFT, padx=(0, 5))
        self.data_inicio = DateEntry(calendario_frame, width=12, background=self.cores['primaria'],
                                  foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.data_inicio.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(calendario_frame, text="Data Final:").pack(side=tk.LEFT, padx=(0, 5))
        self.data_fim = DateEntry(calendario_frame, width=12, background=self.cores['primaria'],
                               foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.data_fim.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_filtrar = ttk.Button(calendario_frame, text="Filtrar", 
                              command=self.filtrar_periodo_personalizado,
                              style='Primario.TButton')
        btn_filtrar.pack(side=tk.LEFT, padx=(0, 5))
        
        # Frame para exibir os assuntos do período
        self.assuntos_periodo_frame = ttk.LabelFrame(container, text="Assuntos Estudados no Período", padding=10)
        self.assuntos_periodo_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Label para exibir o período selecionado
        self.lbl_periodo_selecionado = ttk.Label(self.assuntos_periodo_frame, 
                                              text="Nenhum período selecionado",
                                              font=('Segoe UI', 10, 'italic'))
        self.lbl_periodo_selecionado.pack(anchor=tk.W, pady=(0, 10))
        
        # Área de rolagem para os assuntos
        self.canvas_assuntos = tk.Canvas(self.assuntos_periodo_frame, bg=self.cores['fundo'])
        scrollbar = ttk.Scrollbar(self.assuntos_periodo_frame, orient="vertical", command=self.canvas_assuntos.yview)
        self.canvas_assuntos.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_assuntos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para os assuntos dentro do canvas
        self.frame_assuntos_revisao = ttk.Frame(self.canvas_assuntos, style='Card.TFrame')
        self.canvas_window = self.canvas_assuntos.create_window((0, 0), window=self.frame_assuntos_revisao, anchor="nw")
        
        # Configurar redimensionamento do canvas
        self.frame_assuntos_revisao.bind("<Configure>", self._configurar_canvas_assuntos)
        self.canvas_assuntos.bind("<Configure>", self._configurar_canvas_window)
        
        # Configurar eventos de rolagem do mouse
        self.canvas_assuntos.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Texto informativo inicial
        self.lbl_sem_assuntos = ttk.Label(self.frame_assuntos_revisao, 
                                       text="Selecione um período para visualizar os assuntos estudados.",
                                       style='Subtitulo.TLabel')
        self.lbl_sem_assuntos.pack(pady=20)
        
    def _configurar_canvas_assuntos(self, event):
        """Ajusta o scroll region do canvas quando o frame interno muda de tamanho"""
        self.canvas_assuntos.configure(scrollregion=self.canvas_assuntos.bbox("all"))
    
    def _configurar_canvas_window(self, event):
        """Ajusta a largura do frame dentro do canvas quando o canvas muda de tamanho"""
        self.canvas_assuntos.itemconfig(self.canvas_window, width=event.width)
    
    def _on_mousewheel(self, event):
        """Trata o evento de rolagem do mouse no canvas"""
        # Diferentes sistemas operacionais têm diferentes comportamentos de rolagem
        if event.num == 5 or event.delta < 0:  # Rolagem para baixo
            self.canvas_assuntos.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:  # Rolagem para cima
            self.canvas_assuntos.yview_scroll(-1, "units")
    
    def selecionar_periodo_predefinido(self, periodo):
        """Seleciona um período predefinido para revisão"""
        data_hoje = date.today()
        nome_periodo = ""
        
        if periodo == "hoje":
            data_inicio = data_hoje
            data_fim = data_hoje
            nome_periodo = "Hoje"
        elif periodo == "semana":
            data_inicio = data_hoje - timedelta(days=7)
            data_fim = data_hoje
            nome_periodo = "Última Semana"
        elif periodo == "mes":
            data_inicio = data_hoje - timedelta(days=30)
            data_fim = data_hoje
            nome_periodo = "Último Mês"
        elif periodo == "todos":
            # Data mínima para incluir todos os assuntos
            data_inicio = date(2000, 1, 1)
            data_fim = data_hoje
            nome_periodo = "Todos os Períodos"
        
        # Atualizar os widgets de data
        self.data_inicio.set_date(data_inicio)
        self.data_fim.set_date(data_fim)
        
        # Filtrar e mostrar os assuntos
        self.filtrar_assuntos_por_periodo(data_inicio, data_fim, nome_periodo)
    
    def filtrar_periodo_personalizado(self):
        """Filtra os assuntos com base nas datas selecionadas no calendário"""
        data_inicio = self.data_inicio.get_date()
        data_fim = self.data_fim.get_date()
        
        # Verificar se a data final é posterior à data inicial
        if data_fim < data_inicio:
            messagebox.showerror("Erro", "A data final deve ser posterior ou igual à data inicial.")
            return
        
        # Criar descrição do período personalizado
        data_inicio_str = data_inicio.strftime("%d/%m/%Y")
        data_fim_str = data_fim.strftime("%d/%m/%Y")
        nome_periodo = f"Período Personalizado: {data_inicio_str} até {data_fim_str}"
        
        # Filtrar e mostrar os assuntos
        self.filtrar_assuntos_por_periodo(data_inicio, data_fim, nome_periodo)
    
    def filtrar_assuntos_por_periodo(self, data_inicio, data_fim, nome_periodo=None):
        """Filtra e exibe os assuntos estudados no período selecionado"""
        # Limpar os widgets existentes
        for widget in self.frame_assuntos_revisao.winfo_children():
            widget.destroy()
            
        # Atualizar o label de período selecionado
        if not nome_periodo:
            data_inicio_str = data_inicio.strftime("%d/%m/%Y")
            data_fim_str = data_fim.strftime("%d/%m/%Y")
            nome_periodo = f"Período: {data_inicio_str} até {data_fim_str}"
            
        self.lbl_periodo_selecionado.config(text=nome_periodo)
        
        # Converter datas para string formato ISO para comparação
        data_inicio_str = data_inicio.isoformat()
        data_fim_str = data_fim.isoformat()
        
        # Encontrar assuntos concluídos no período
        assuntos_no_periodo = []
        
        for disciplina, assuntos in self.progresso.items():
            if disciplina == "ultima_data":
                continue
                
            for assunto, dados in assuntos.items():
                # Verificar se tem data de conclusão
                if dados.get("data_conclusao"):
                    try:
                        # Converter a data de conclusão para objeto date
                        data_conclusao = datetime.strptime(dados["data_conclusao"], "%Y-%m-%d %H:%M:%S").date()
                        data_conclusao_str = data_conclusao.isoformat()
                        
                        # Verificar se está dentro do período
                        if data_inicio_str <= data_conclusao_str <= data_fim_str:
                            assuntos_no_periodo.append((disciplina, assunto, dados))
                    except ValueError:
                        # Ignorar o assunto se o formato da data estiver incorreto
                        continue
        
        # Ordenar por data de conclusão (mais recente primeiro)
        assuntos_no_periodo.sort(key=lambda x: x[2].get("data_conclusao", ""), reverse=True)
        
        if not assuntos_no_periodo:
            self.lbl_sem_assuntos = ttk.Label(self.frame_assuntos_revisao, 
                                          text="Nenhum assunto encontrado no período selecionado.",
                                          style='Subtitulo.TLabel')
            self.lbl_sem_assuntos.pack(pady=20)
            return
        
        # Exibir os assuntos filtrados
        for disciplina, assunto, dados in assuntos_no_periodo:
            self.criar_card_assunto_revisao(disciplina, assunto, dados)
        
        # Ajustar a região de rolagem
        self.canvas_assuntos.configure(scrollregion=self.canvas_assuntos.bbox("all"))
    
    def criar_card_assunto_revisao(self, disciplina, assunto, dados):
        """Cria um card para exibir informações de um assunto para revisão"""
        # Frame do card
        card = ttk.Frame(self.frame_assuntos_revisao, style='Card.TFrame')
        card.pack(fill=tk.X, pady=5, padx=5)
        
        # Bordas para o card
        card_interior = ttk.Frame(card, style='Card.TFrame')
        card_interior.pack(fill=tk.X, padx=2, pady=2)
        
        # Cabeçalho do card
        header = ttk.Frame(card_interior)
        header.pack(fill=tk.X, pady=(5, 0), padx=10)
        
        # Disciplina
        disciplina_label = ttk.Label(header, text=disciplina, 
                                   font=('Segoe UI', 10, 'bold'),
                                   foreground=self.cores['primaria'])
        disciplina_label.pack(anchor=tk.W)
        
        # Assunto
        assunto_label = ttk.Label(header, text=assunto, 
                                font=('Segoe UI', 12, 'bold'),
                                wraplength=800)
        assunto_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Informações
        info_frame = ttk.Frame(card_interior)
        info_frame.pack(fill=tk.X, padx=10)
        
        # Data de conclusão
        data_str = dados.get("data_conclusao", "")
        if data_str:
            try:
                data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                data_formatada = data_obj.strftime("%d/%m/%Y %H:%M")
                ttk.Label(info_frame, text=f"Concluído em: {data_formatada}").pack(anchor=tk.W)
            except ValueError:
                ttk.Label(info_frame, text="Concluído em: (data não disponível)").pack(anchor=tk.W)
        
        # Progresso
        progresso_str = f"{dados.get('questoes_resolvidas', 0)}/20 questões"
        ttk.Label(info_frame, text=f"Progresso: {progresso_str}").pack(anchor=tk.W)
        
        # Vezes concluído
        vezes = dados.get("vezes_concluido", 0)
        ttk.Label(info_frame, text=f"Vezes concluído: {vezes}").pack(anchor=tk.W)
        
        # Notas
        notas = dados.get("notas", "")
        if notas:
            notas_frame = ttk.LabelFrame(card_interior, text="Suas Anotações")
            notas_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)
            
            # Texto das notas
            txt_notas = scrolledtext.ScrolledText(notas_frame, wrap=tk.WORD, height=4,
                                               font=('Segoe UI', 10))
            txt_notas.pack(fill=tk.X, expand=True)
            txt_notas.insert("1.0", notas)
            txt_notas.configure(state="disabled")  # Somente leitura
            
        # Botão para revisar este assunto específico
        btn_frame = ttk.Frame(card_interior)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        btn_revisar = ttk.Button(btn_frame, text="Revisar este Assunto", 
                              command=lambda d=disciplina, a=assunto: self.revisar_assunto(d, a),
                              style='Primario.TButton')
        btn_revisar.pack(side=tk.RIGHT)
        
        # Separador
        ttk.Separator(self.frame_assuntos_revisao, orient="horizontal").pack(fill=tk.X, pady=5)
    
    def revisar_assunto(self, disciplina, assunto):
        """Abre o assunto selecionado na aba de estudo para revisão"""
        # Defina o assunto atual como o selecionado
        self.disciplina_atual = disciplina
        self.assunto_atual = assunto
        
        # Atualize a exibição para mostrar este assunto
        self.atualizar_exibicao()
        self.exibir_notas_do_assunto_atual()
        
        # Mude para a aba de estudo
        self.notebook.select(self.tab_estudo)
        
        # Mostrar notificação
        self.mostrar_notificacao(f"Revisando: {assunto}", cor=self.cores['secundaria'])
        
    def inicializar_progresso(self):
        """Inicializa o progresso para novos assuntos"""
        for disciplina, assuntos in self.conteudo_programatico.items():
            if disciplina not in self.progresso:
                self.progresso[disciplina] = {}
                
            for assunto in assuntos:
                if assunto not in self.progresso[disciplina]:
                    self.progresso[disciplina][assunto] = {
                        "questoes_resolvidas": 0,
                        "concluido": False,
                        "data_conclusao": None,
                        "vezes_concluido": 0,
                        "notas": ""  # Campo para armazenar notas
                    }
        
        # Inicializar questões do dia
        if "ultima_data" not in self.progresso:
            self.progresso["ultima_data"] = self.data_atual
            self.questoes_hoje = 0
        
        # Salvar o progresso atualizado
        self.salvar_progresso()
    
    def calcular_progresso_disciplina(self, disciplina):
        """Calcula o percentual de progresso em uma disciplina"""
        assuntos_total = len(self.conteudo_programatico[disciplina])
        assuntos_concluidos = 0
        
        for assunto in self.conteudo_programatico[disciplina]:
            if self.progresso[disciplina][assunto]["concluido"]:
                assuntos_concluidos += 1
                
        return (assuntos_concluidos / assuntos_total) * 100 if assuntos_total > 0 else 0
    
    def ordenar_disciplinas_por_progresso(self):
        """Ordena as disciplinas do menor para o maior progresso"""
        # Criar uma lista de tuplas (disciplina, progresso)
        disciplinas_com_progresso = [(d, self.calcular_progresso_disciplina(d)) for d in self.disciplinas]
        
        # Ordenar do menor para o maior progresso
        disciplinas_ordenadas = [d for d, p in sorted(disciplinas_com_progresso, key=lambda x: x[1])]
        
        return disciplinas_ordenadas
    
    def gerar_assuntos_do_dia(self):
        """Gera a lista de assuntos para estudar no dia priorizando disciplinas com menos progresso"""
        self.assuntos_do_dia = []
        
        # Obter disciplinas ordenadas por progresso (menor para maior)
        disciplinas_ordenadas = self.ordenar_disciplinas_por_progresso()
        
        # Selecionar assuntos não concluídos de cada disciplina
        for disciplina in disciplinas_ordenadas:
            # Filtrar assuntos não concluídos
            assuntos_nao_concluidos = [
                assunto for assunto in self.conteudo_programatico[disciplina]
                if not self.progresso[disciplina][assunto]["concluido"]
            ]
            
            if assuntos_nao_concluidos:
                # Escolher um assunto aleatório não concluído desta disciplina
                assunto_escolhido = random.choice(assuntos_nao_concluidos)
                self.assuntos_do_dia.append((disciplina, assunto_escolhido))
        
        # Embaralhar a ordem das disciplinas para a sessão de estudo
        random.shuffle(self.assuntos_do_dia)
        
        # Se todos os assuntos já foram concluídos, iniciar um novo ciclo
        if not self.assuntos_do_dia:
            self.incrementar_ciclo()
            return
            
        # Selecionar o primeiro assunto
        if self.assuntos_do_dia:
            self.disciplina_atual, self.assunto_atual = self.assuntos_do_dia[0]
            self.exibir_notas_do_assunto_atual()
    
    def incrementar_ciclo(self):
        """Incrementa o contador de ciclos completos e reinicia todos os assuntos"""
        self.ciclos_completos += 1
        
        # Marcar todos os assuntos como não concluídos para o novo ciclo, preservando as notas
        for disciplina in self.progresso:
            if disciplina == "ultima_data":
                continue
                
            for assunto in self.progresso[disciplina]:
                # Preservar as notas
                notas = self.progresso[disciplina][assunto].get("notas", "")
                
                # Incrementar o contador de vezes que o assunto foi concluído
                if self.progresso[disciplina][assunto]["concluido"]:
                    self.progresso[disciplina][assunto]["vezes_concluido"] += 1
                
                # Resetar os campos de conclusão
                self.progresso[disciplina][assunto]["questoes_resolvidas"] = 0
                self.progresso[disciplina][assunto]["concluido"] = False
                self.progresso[disciplina][assunto]["data_conclusao"] = None
                self.progresso[disciplina][assunto]["notas"] = notas  # Manter as notas
        
        # Salvar progresso
        self.salvar_progresso()
        
        # Gerar novos assuntos do dia
        self.gerar_assuntos_do_dia()
        
        # Mostrar mensagem na interface sem popup
        self.mostrar_notificacao(f"Parabéns! Você completou todos os assuntos do ciclo. Iniciando ciclo #{self.ciclos_completos + 1}.")
    
    def proximo_assunto(self):
        """Avança para o próximo assunto da lista do dia"""
        # Salvar notas do assunto atual antes de mudar
        self.salvar_notas()
        
        if not self.assuntos_do_dia:
            self.gerar_assuntos_do_dia()
            return
            
        # Embaralhar novamente a lista de assuntos para garantir variação
        random.shuffle(self.assuntos_do_dia)
        
        # Escolher o primeiro assunto da lista recém-embaralhada
        if self.assuntos_do_dia:
            self.disciplina_atual, self.assunto_atual = self.assuntos_do_dia[0]
        
        self.atualizar_exibicao()
        self.exibir_notas_do_assunto_atual()
    
    def salvar_notas(self):
        """Salva as notas do assunto atual"""
        if not self.assunto_atual or not self.disciplina_atual:
            return
            
        # Obter o texto das notas
        notas = self.txt_notas.get("1.0", tk.END).strip()
        
        # Salvar no dicionário de progresso
        self.progresso[self.disciplina_atual][self.assunto_atual]["notas"] = notas
        
        # Salvar progresso
        self.salvar_progresso()
        
        # Mostrar confirmação
        self.mostrar_notificacao("Notas salvas com sucesso!")
    
    def exibir_notas_do_assunto_atual(self):
        """Exibe as notas do assunto atual"""
        if not self.assunto_atual or not self.disciplina_atual:
            self.txt_notas.delete("1.0", tk.END)
            return
            
        # Limpar o campo de texto
        self.txt_notas.delete("1.0", tk.END)
        
        # Obter as notas do assunto atual
        notas = self.progresso[self.disciplina_atual][self.assunto_atual].get("notas", "")
        
        # Inserir no campo de texto
        if notas:
            self.txt_notas.insert("1.0", notas)
    
    def meta_cumprida(self):
        """Marca o assunto atual como concluído (20 questões resolvidas)"""
        if not self.assunto_atual:
            return
            
        # Salvar notas antes de marcar como concluído
        self.salvar_notas()
            
        # Marcar como concluído
        self.progresso[self.disciplina_atual][self.assunto_atual]["questoes_resolvidas"] = 20
        self.progresso[self.disciplina_atual][self.assunto_atual]["concluido"] = True
        self.progresso[self.disciplina_atual][self.assunto_atual]["data_conclusao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Atualizar questões do dia
        self.questoes_hoje += 20
        
        # Mostrar mensagem na interface sem popup
        self.mostrar_notificacao(f"Assunto concluído: {self.assunto_atual}")
        
        # Verificar se atingiu a meta diária
        if self.questoes_hoje >= self.meta_diaria and self.questoes_hoje - 20 < self.meta_diaria:
            self.mostrar_notificacao(f"PARABÉNS! Você atingiu a meta diária de {self.meta_diaria} questões!", cor="blue")
        
        # Remover este assunto da lista do dia
        self.assuntos_do_dia = [(d, a) for d, a in self.assuntos_do_dia if a != self.assunto_atual or d != self.disciplina_atual]
        
        # Salvar progresso
        self.salvar_progresso()
        
        # Verificar se completou todos os assuntos
        total_assuntos = 0
        assuntos_concluidos = 0
        
        for disciplina, assuntos_dict in self.progresso.items():
            if disciplina == "ultima_data":
                continue
                
            for assunto, dados in assuntos_dict.items():
                total_assuntos += 1
                if dados["concluido"]:
                    assuntos_concluidos += 1
        
        # Se completou todos os assuntos, iniciar novo ciclo
        if assuntos_concluidos == total_assuntos:
            self.incrementar_ciclo()
        
        # Passar para o próximo assunto
        self.proximo_assunto()
    
    def mostrar_notificacao(self, mensagem, cor="green", duracao=5000):
        """Exibe uma notificação na interface sem popup"""
        if not hasattr(self, 'lbl_notificacao') or not self.interface_criada:
            print(f"Notificação: {mensagem}")  # Fallback para console quando interface não está pronta
            return
            
        self.lbl_notificacao.config(text=mensagem, foreground=cor)
        # Apagar a notificação após alguns segundos
        self.root.after(duracao, lambda: self.lbl_notificacao.config(text=""))
    
    def atualizar_exibicao(self):
        """Atualiza a interface com os dados atuais"""
        # Atualizar informações do assunto atual
        if self.assunto_atual:
            self.lbl_disciplina.config(text=self.disciplina_atual)
            self.lbl_assunto.config(text=self.assunto_atual)
            
            questoes = self.progresso[self.disciplina_atual][self.assunto_atual]["questoes_resolvidas"]
            self.lbl_progresso_assunto.config(text=f"{questoes}/20 questões")
            
            # Atualizar barra de progresso do assunto
            progresso_percentual = (questoes / 20) * 100
            self.progresso_bar["value"] = progresso_percentual
        else:
            self.lbl_disciplina.config(text="Nenhum assunto disponível")
            self.lbl_assunto.config(text="")
            self.lbl_progresso_assunto.config(text="0/20 questões")
            self.progresso_bar["value"] = 0
        
        # Atualizar informações de meta diária
        self.lbl_questoes_hoje.config(text=f"Questões hoje: {self.questoes_hoje}/{self.meta_diaria}")
        progresso_diario = min(100, (self.questoes_hoje / self.meta_diaria) * 100)
        self.progresso_diario_bar["value"] = progresso_diario
        
        # Atualizar estatísticas gerais
        self.atualizar_estatisticas()
    
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas gerais na interface"""
        total_assuntos = 0
        assuntos_concluidos = 0
        total_questoes = 0
        
        for disciplina, assuntos_dict in self.progresso.items():
            if disciplina == "ultima_data":
                continue
                
            for assunto, dados in assuntos_dict.items():
                total_assuntos += 1
                
                if dados["concluido"]:
                    assuntos_concluidos += 1
                
                total_questoes += dados["questoes_resolvidas"]
                total_questoes += dados["vezes_concluido"] * 20  # Adicionar questões de ciclos anteriores
        
        # Atualizar labels de estatísticas
        self.lbl_total_assuntos.config(text=f"Assuntos totais: {total_assuntos}")
        self.lbl_assuntos_concluidos.config(text=f"Assuntos concluídos: {assuntos_concluidos}")
        
        percentual = 0
        if total_assuntos > 0:
            percentual = (assuntos_concluidos / total_assuntos) * 100
            
        self.lbl_percentual_concluido.config(text=f"Percentual concluído: {percentual:.1f}%")
        self.lbl_total_questoes.config(text=f"Total de questões: {total_questoes}")
        self.lbl_ciclos_completos.config(text=f"Ciclos completos: {self.ciclos_completos}")
        
        # Atualizar barra de progresso geral
        self.progresso_geral_bar["value"] = percentual
    
    def carregar_progresso(self):
        """Carrega o progresso salvo do arquivo JSON"""
        try:
            # Usar caminho absoluto e normalizar para o Windows
            caminho_arquivo = os.path.abspath(self.arquivo_progresso)
            caminho_arquivo = os.path.normpath(caminho_arquivo)
            
            if not os.path.exists(caminho_arquivo):
                self.mostrar_notificacao("Arquivo de progresso não encontrado. Criando novo progresso.", cor="orange")
                self.progresso = {}
                self.ciclos_completos = 0
                self.questoes_hoje = 0
                return
                
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                conteudo = file.read()
                if not conteudo.strip():
                    self.mostrar_notificacao("Arquivo de progresso vazio.", cor="orange")
                    self.progresso = {}
                    return
                    
                dados = json.loads(conteudo)
                if not dados:
                    self.mostrar_notificacao("Arquivo de progresso vazio.", cor="orange")
                    return
                    
                self.progresso = dados.get("progresso", {})
                if not self.progresso:
                    self.mostrar_notificacao("Nenhum dado de progresso encontrado no arquivo.", cor="orange")
                    return
                    
                self.ciclos_completos = dados.get("ciclos_completos", 0)
                self.questoes_hoje = dados.get("questoes_hoje", 0)
                
                # Verificar se é um novo dia
                ultima_data = self.progresso.get("ultima_data", "")
                data_hoje = date.today().isoformat()
                
                if ultima_data != data_hoje:
                    self.questoes_hoje = 0
                    self.progresso["ultima_data"] = data_hoje
                    
                self.mostrar_notificacao("Progresso carregado com sucesso!", cor="green")
                
        except json.JSONDecodeError as e:
            self.mostrar_notificacao(f"Erro ao decodificar o arquivo JSON: {str(e)}", cor="red")
            self.progresso = {}
            self.ciclos_completos = 0
            self.questoes_hoje = 0
        except Exception as e:
            self.mostrar_notificacao(f"Erro ao carregar o progresso: {str(e)}", cor="red")
            self.progresso = {}
            self.ciclos_completos = 0
            self.questoes_hoje = 0
    
    def salvar_progresso(self):
        """Salva o progresso atual em um arquivo JSON"""
        try:
            if not self.progresso:
                self.mostrar_notificacao("Nenhum progresso para salvar.", cor="orange")
                return
                
            dados = {
                "progresso": self.progresso,
                "ciclos_completos": self.ciclos_completos,
                "questoes_hoje": self.questoes_hoje
            }
            
            # Verificar se os dados são serializáveis
            try:
                json_str = json.dumps(dados, ensure_ascii=False, indent=4)
            except TypeError as e:
                self.mostrar_notificacao(f"Erro ao serializar dados: {str(e)}", cor="red")
                return
            
            # Usar caminho absoluto e normalizar para o Windows
            caminho_arquivo = os.path.abspath(self.arquivo_progresso)
            caminho_arquivo = os.path.normpath(caminho_arquivo)
            
            # Garantir que o diretório existe
            diretorio = os.path.dirname(caminho_arquivo)
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
            
            # Salvar o arquivo
            with open(caminho_arquivo, 'w', encoding='utf-8') as file:
                file.write(json_str)
                
            self.mostrar_notificacao("Progresso salvo com sucesso!", cor="green")
            
        except Exception as e:
            self.mostrar_notificacao(f"Erro ao salvar o progresso: {str(e)}", cor="red")
    
    def exportar_progresso(self):
        """Exporta o progresso para um arquivo CSV"""
        if not self.progresso:
            self.mostrar_notificacao("Não há dados de progresso para exportar.", cor="orange")
            return
            
        # Pedir ao usuário para escolher onde salvar o arquivo
        filename = filedialog.asksaveasfilename(
            title="Exportar Progresso",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if not filename:
            return
            
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escrever cabeçalho
                writer.writerow([
                    "Disciplina", 
                    "Assunto", 
                    "Questões Resolvidas", 
                    "Concluído", 
                    "Data de Conclusão",
                    "Vezes Concluído",
                    "Notas"  # Adicionado campo de notas à exportação
                ])
                
                # Escrever dados
                for disciplina, assuntos in self.progresso.items():
                    if disciplina == "ultima_data":
                        continue
                        
                    for assunto, dados in assuntos.items():
                        writer.writerow([
                            disciplina,
                            assunto,
                            dados["questoes_resolvidas"],
                            "Sim" if dados["concluido"] else "Não",
                            dados["data_conclusao"] if dados["data_conclusao"] else "",
                            dados["vezes_concluido"],
                            dados.get("notas", "")  # Exportar as notas
                        ])
                
            self.mostrar_notificacao(f"Dados exportados com sucesso para {filename}", cor="green")
            
        except Exception as e:
            self.mostrar_notificacao(f"Erro ao exportar dados: {str(e)}", cor="red")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#F5F5F5')  # Configurar cor de fundo da janela principal
    app = EstudosConcursoApp(root)
    root.mainloop()