import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import random
from datetime import datetime, date
import csv

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
        
        # Definir meta diária
        self.meta_diaria = 140  # 7 disciplinas x 20 questões
        self.questoes_hoje = 0
        self.data_atual = date.today().isoformat()
        
        # Conteúdo programático embutido
        self.conteudo_programatico = {
            "NOÇÕES DE SUSTENTABILIDADE": [
                "Do Meio Ambiente (Constituição Federal de 1988, Art. 225).",
                "Conceito de Desenvolvimento Sustentável (Relatório Brundtland).",
                "Agenda Ambiental da Administração Pública (A3P), do Ministério do Meio Ambiente e Mudança do Clima (antigo Ministério do Meio Ambiente).",
                "Política Nacional sobre Mudanças do Clima (Lei nº 12.187/2009).",
                "Política Nacional de Resíduos Sólidos (Lei nº 12.305/2010 e suas alterações e Decreto nº 10.936/2022).",
                "Lei de Crimes Ambientais (Lei nº 9.605/1998 e suas alterações).",
                "Sistema Nacional de Unidades de Conservação da Natureza (Lei nº 9.985/2000 e suas alterações).",
                "Lei da cooperação federativa em matéria ambiental (Lei Complementar nº 140/2011)."
            ],
            "NOÇÕES DE DIREITOS HUMANOS E FUNDAMENTAIS E DE ACESSIBILIDADE": [
                "Teoria geral dos direitos fundamentais.",
                "Direitos Humanos e Direitos Fundamentais.",
                "Declaração Universal dos Direitos Humanos.",
                "Agenda 2030 da ONU.",
                "Política Nacional de Direitos Humanos.",
                "A constituição brasileira e os tratados internacionais de direitos humanos.",
                "Pacto de São José da Costa Rica e Decreto nº 678/1992 (Convenção Americana sobre Direitos Humanos).",
                "Noções gerais de gênero e equidade. Estatuto de igualdade racial (Lei nº 12.288/2010 e suas alterações).",
                "Lei Brasileira de Inclusão da Pessoa com Deficiência – Estatuto da Pessoa com Deficiência (Lei nº 13.146/2015 e suas alterações).",
                "Normas gerais e critérios básicos para a promoção da acessibilidade das pessoas com deficiência ou com mobilidade reduzida (Lei nº 10.098/2000 e suas alterações).",
                "Prioridade de atendimento às pessoas com deficiência (Lei nº 10.048/2000 e suas alterações)."
            ],
            "NOÇÕES DE ADMINISTRAÇÃO PÚBLICA": [
                "Conceitos básicos em administração: eficiência, eficácia, efetividade, qualidade; papéis do administrador.",
                "Organização: princípios de organização; tipos de estrutura organizacional; departamentalização; centralização e descentralização.",
                "Funções da administração: planejamento, organização, direção e controle.",
                "Planejamento: princípios e conceitos básicos, níveis estratégico, tático e operacional.",
                "Gestão de processos: conceitos, fundamentos, técnicas de mapeamento, análise e melhoria de processos.",
                "Gestão por competências: competências organizacionais, coletivas e individuais; desenvolvimento de competências.",
                "Comportamento organizacional: liderança; motivação; atitudes e satisfação no trabalho; trabalho em equipe; comunicação; cultura organizacional.",
                "Administração Pública: definição; evolução dos modelos da administração pública (patrimonialista, burocrática e gerencial); reformas administrativas.",
                "Transformação Digital na Administração Pública.",
                "Tecnologia no contexto jurídico.",
                "Automação do processo.",
                "Inteligência Artificial.",
                "Blockchain e Algoritmos.",
                "Resolução CNMP nº 276/2023 – Dispõe sobre a Política Nacional do Ministério Público Digital – MP Digital."
            ],
            "LEGISLAÇÃO INSTITUCIONAL": [
                "Lei Complementar nº 75/1993.",
                "Lei nº 13.316/2016  e suas alterações.",
                "Portaria PGR/MPU nº 98/2017 (Código de Ética e de Conduta do MPU e da ESMPU).",
                "Portaria PGR/MPU nº 247/2023 (Programa de Integridade do Ministério Público da União)."
            ],
            "NOÇÕES DE DIREITO ADMINISTRATIVO": [
                "Princípios de Direito Administrativo.",
                "Atos Administrativos.",
                "Poderes administrativos.",
                "Uso e abuso do poder.",
                "Organização Administrativa.",
                "Administração Direta e Indireta.",
                "Contratos Administrativos. Licitações e Contratos. Lei nº 14.133/2021 e suas alterações.",
                "Processo administrativo. Lei nº 9.784/1999 e suas alterações.",
                "Segurança jurídica e eficiência na criação e na aplicação do Direito Público. LINDB. Lei nº 13.655/2018.",
                "Agentes Públicos e Servidores Públicos. Lei nº 8.112/1990 e suas alterações. Regime Jurídico dos servidores públicos civis da União, das autarquias e das fundações públicas federais. Serviços Públicos.",
                "Responsabilidade Civil do Estado.",
                "Controle da Administração Pública.",
                "Conselho Nacional do Ministério Público.",
                "Tribunais de Contas.",
                "Improbidade Administrativa.",
                "Lei nº 12.527/2011 e suas alterações (Lei de Acesso à Informação).",
                "Lei nº 13.709/2018 e suas alterações (Lei Geral de Proteção de Dados Pessoais – LGPD).",
                "Súmulas e Jurisprudência dos tribunais superiores."
            ],
            "NOÇÕES DE PERÍCIA EM PROCESSO CIVIL": [
                "Perícia no processo civil – CPC, Art. 156 a 158 e Art. 464 a 480.",
                "Definição de prova e finalidade da prova.",
                "Relações entre verdade e prova.",
                "Condicionamentos legais de nomeação do perito judicial (CPC, Art. 156 a 158 e Art. 465 a 468).",
                "Princípios fundamentais do processo civil aplicado à prova.",
                "Perito nomeado pelo juízo e assistentes técnicos periciais: funções distintas na produção probatória.",
                "Prazos processuais para a produção da prova pericial.",
                "Possibilidades de substituição do perito judicial.",
                "Possibilidades de impugnação e suspeição do perito judicial. Conteúdo mínimo do laudo de perícia judicial – CPC, Art. 473.",
                "Perícia complexa – CPC, Art. 475.",
                "Quesitos impertinentes, quesitos suplementares e complementação de perícia.",
                "Contraditório na análise do laudo de perícia judicial e possíveis divergências – CPC, Art. 477.",
                "Audiência de instrução e julgamento para esclarecimentos – CPC, Art. 477.",
                "Característica e função da segunda perícia judicial.",
                "Previsão de eventuais sanções ao perito judicial."
            ],
            "NOÇÕES DE DIREITO PROCESSUAL PENAL": [
                "Princípios. Inquérito policial: histórico; natureza; conceito; finalidade; características; fundamento; titularidade; grau de cognição; valor probatório; formas de instauração; notitia criminis; delatio criminis; procedimentos investigativos; indiciamento; garantias do investigado; conclusão; prazos.",
                "Provas. Teoria Geral da Prova. Procedimento probatório. Sistemas probatórios. Ônus da prova. Valoração da prova. Standards probatórios. Distinção entre atos de investigação e atos de prova. Limites à atividade probatória. Provas ilícitas. Cadeia de custódia. Princípio da Serendipidade. Prova emprestada.",
                "Provas em espécie. Exame do corpo de delito e perícias em geral. Prova oral. Valor probatório da confissão. Reconhecimento de pessoas e coisas. Acareação. Prova documental. Presunções. Indícios. Busca e apreensão. Interceptação de comunicações telefônicas e do fluxo de comunicações em sistemas de informática e telemática. Captação ambiental de sinais eletromagnéticos, ópticos ou acústicos. Reprodução simulada de fatos ou reconstituição do crime. Quebra de sigilo fiscal, bancário e de dados. Coleta de perfil genético como forma de identificação criminal. Emprego de tecnologias na produção de provas. Provas digitais. Reconhecimento facial. Exame do corpo de delito e perícias em geral. Interrogatório do investigado. Confissão. Qualificação e oitiva do ofendido. Testemunhas. Reconhecimento de pessoas e coisas. Acareação. Documentos de prova. Indícios. Busca e apreensão.",
                "Sujeitos do processo: do juiz, do Ministério Público, do acusado e defensor, dos assistentes e auxiliares da Justiça. Impedimentos e suspeições.",
                "Atos processuais: comunicações, citações, intimações e notificações.",
                "Tópicos contemporâneos em Perícia de TIC. Perícias em Sítios de Internet e em Redes Sociais (OSINT). Perícias em Imagens Digitais – IA e DeepFake. Internet das coisas. Aspectos relacionados a criptomoedas, blockchain, transações e ferramentas modernas de análise, carteiras digitais, conceitos de Darkweb. Denúncia."
            ]
        }
        
        # Conteúdo programático e variáveis de estado
        self.disciplinas = list(self.conteudo_programatico.keys())
        self.progresso = {}
        self.assuntos_do_dia = []
        self.assunto_atual = None
        self.disciplina_atual = None
        
        # Configurar arquivo de progresso
        self.arquivo_progresso = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progresso_estudos.json")
        self.ciclos_completos = 0
        
        # Carregar dados se existirem
        self.carregar_progresso()
        
        # Verificar se é um novo dia
        self.verificar_novo_dia()
        
        # Inicializar progresso para novos assuntos se necessário
        self.inicializar_progresso()
        
        # Criar interface - Movido para depois da inicialização dos dados
        self.criar_interface()
        
        # Gerar assuntos do dia e atualizar interface
        self.gerar_assuntos_do_dia()
        self.atualizar_exibicao()
    
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
    
    def criar_area_notificacao(self):
        """Cria a área de notificação"""
        self.frame_notificacao = ttk.Frame(self.root)
        self.frame_notificacao.pack(fill=tk.X, padx=10, pady=5)
        
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
                data = dados["data_conclusao"] if dados["data_conclusao"] else "-"
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