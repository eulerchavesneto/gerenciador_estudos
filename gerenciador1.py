import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import random
from datetime import datetime, date
import csv

class EstudosConcursoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Estudos para Concurso")
        self.root.geometry("800x600")
        self.root.config(padx=20, pady=20)
        
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
        
        # Variáveis de estado
        self.disciplinas = list(self.conteudo_programatico.keys())
        self.progresso = {}
        self.assuntos_do_dia = []
        self.assunto_atual = None
        self.disciplina_atual = None
        self.arquivo_progresso = "progresso_estudos.json"
        self.ciclos_completos = 0
        
        # Carregar dados se existirem
        self.carregar_progresso()
        
        # Inicializar progresso para novos assuntos se necessário
        self.inicializar_progresso()
        
        # Verificar se é um novo dia
        self.verificar_novo_dia()
        
        # Criar interface
        self.criar_interface()
        
        # Gerar assuntos do dia e atualizar interface
        self.gerar_assuntos_do_dia()
        self.atualizar_exibicao()
    
    def criar_interface(self):
        # Frame principal dividido em duas partes
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Parte esquerda - Assunto atual e controles
        frame_esquerdo = ttk.LabelFrame(frame_principal, text="Estudo do Dia")
        frame_esquerdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Parte direita - Estatísticas
        frame_direito = ttk.LabelFrame(frame_principal, text="Estatísticas")
        frame_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Conteúdo do frame esquerdo
        # Área para exibir a disciplina e assunto atual
        ttk.Label(frame_esquerdo, text="Disciplina:").pack(anchor=tk.W, pady=(10, 0))
        self.lbl_disciplina = ttk.Label(frame_esquerdo, text="", font=("Arial", 12, "bold"))
        self.lbl_disciplina.pack(anchor=tk.W, pady=(0, 10), fill=tk.X)
        
        ttk.Label(frame_esquerdo, text="Assunto:").pack(anchor=tk.W)
        self.lbl_assunto = ttk.Label(frame_esquerdo, text="", font=("Arial", 12), wraplength=350)
        self.lbl_assunto.pack(anchor=tk.W, pady=(0, 20), fill=tk.X)
        
        ttk.Label(frame_esquerdo, text="Progresso neste assunto:").pack(anchor=tk.W)
        self.lbl_progresso_assunto = ttk.Label(frame_esquerdo, text="0/20 questões", font=("Arial", 10))
        self.lbl_progresso_assunto.pack(anchor=tk.W, pady=(0, 10))
        
        self.progresso_bar = ttk.Progressbar(frame_esquerdo, orient="horizontal", length=350, mode="determinate")
        self.progresso_bar.pack(anchor=tk.W, pady=(0, 20), fill=tk.X)
        
        # Botões de controle
        frame_botoes = ttk.Frame(frame_esquerdo)
        frame_botoes.pack(pady=20, fill=tk.X)
        
        self.btn_meta = ttk.Button(frame_botoes, text="Meta Cumprida!", command=self.meta_cumprida)
        self.btn_meta.pack(side=tk.LEFT, padx=5)
        
        self.btn_proximo = ttk.Button(frame_botoes, text="Próximo Assunto", command=self.proximo_assunto)
        self.btn_proximo.pack(side=tk.LEFT, padx=5)
        
        # Conteúdo do frame direito
        # Resumo geral de progresso
        ttk.Label(frame_direito, text="Progresso Geral:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 10))
        
        self.frame_stats = ttk.Frame(frame_direito)
        self.frame_stats.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Meta diária
        ttk.Label(self.frame_stats, text=f"Meta diária: {self.meta_diaria} questões", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        self.lbl_questoes_hoje = ttk.Label(self.frame_stats, text=f"Questões hoje: {self.questoes_hoje}/{self.meta_diaria}")
        self.lbl_questoes_hoje.pack(anchor=tk.W, pady=2)
        
        # Barra de progresso da meta diária
        ttk.Label(self.frame_stats, text="Progresso da meta diária:").pack(anchor=tk.W, pady=(5, 0))
        self.progresso_diario_bar = ttk.Progressbar(self.frame_stats, orient="horizontal", length=350, mode="determinate")
        self.progresso_diario_bar.pack(anchor=tk.W, pady=(0, 10), fill=tk.X)
        
        # Informações de progresso geral
        self.lbl_total_assuntos = ttk.Label(self.frame_stats, text="Assuntos totais: 0")
        self.lbl_total_assuntos.pack(anchor=tk.W, pady=2)
        
        self.lbl_assuntos_concluidos = ttk.Label(self.frame_stats, text="Assuntos concluídos neste ciclo: 0")
        self.lbl_assuntos_concluidos.pack(anchor=tk.W, pady=2)
        
        self.lbl_percentual_concluido = ttk.Label(self.frame_stats, text="Percentual concluído do ciclo atual: 0%")
        self.lbl_percentual_concluido.pack(anchor=tk.W, pady=2)
        
        self.lbl_total_questoes = ttk.Label(self.frame_stats, text="Total de questões resolvidas: 0")
        self.lbl_total_questoes.pack(anchor=tk.W, pady=2)
        
        self.lbl_ciclos_completos = ttk.Label(self.frame_stats, text="Ciclos completos: 0")
        self.lbl_ciclos_completos.pack(anchor=tk.W, pady=2)
        
        # Barra de progresso geral
        ttk.Label(frame_direito, text="Progresso do ciclo atual:").pack(anchor=tk.W, pady=(10, 5))
        self.progresso_geral_bar = ttk.Progressbar(frame_direito, orient="horizontal", length=350, mode="determinate")
        self.progresso_geral_bar.pack(anchor=tk.W, pady=(0, 20), fill=tk.X)
        
        # Área de notificação
        self.frame_notificacao = ttk.Frame(frame_principal)
        self.frame_notificacao.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        
        self.lbl_notificacao = ttk.Label(self.frame_notificacao, text="", font=("Arial", 12, "bold"), foreground="green")
        self.lbl_notificacao.pack(pady=5)
        
        # Menu principal
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Exportar Progresso (CSV)", command=self.exportar_progresso)
        arquivo_menu.add_command(label="Reiniciar Ciclo", command=self.reiniciar_ciclo)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.quit)
    
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
            
        # Marcar todos os assuntos como não concluídos
        for disciplina in self.progresso:
            if disciplina == "ultima_data":
                continue
                
            for assunto in self.progresso[disciplina]:
                self.progresso[disciplina][assunto]["questoes_resolvidas"] = 0
                self.progresso[disciplina][assunto]["concluido"] = False
                self.progresso[disciplina][assunto]["data_conclusao"] = None
                
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
                        "vezes_concluido": 0
                    }
        
        # Inicializar questões do dia
        if "ultima_data" not in self.progresso:
            self.progresso["ultima_data"] = self.data_atual
            self.questoes_hoje = 0
        
        # Salvar o progresso atualizado
        self.salvar_progresso()
    
    def gerar_assuntos_do_dia(self):
        """Gera a lista de assuntos para estudar no dia (um de cada disciplina)"""
        self.assuntos_do_dia = []
        
        for disciplina in self.disciplinas:
            # Filtrar assuntos não concluídos
            assuntos_nao_concluidos = [
                assunto for assunto in self.conteudo_programatico[disciplina]
                if not self.progresso[disciplina][assunto]["concluido"]
            ]
            
            if assuntos_nao_concluidos:
                # Escolher um assunto aleatório não concluído desta disciplina
                assunto_escolhido = random.choice(assuntos_nao_concluidos)
                self.assuntos_do_dia.append((disciplina, assunto_escolhido))
        
        # Se todos os assuntos já foram concluídos, iniciar um novo ciclo
        if not self.assuntos_do_dia:
            self.incrementar_ciclo()
            return
            
        # Selecionar o primeiro assunto
        if self.assuntos_do_dia:
            self.disciplina_atual, self.assunto_atual = self.assuntos_do_dia[0]
    
    def incrementar_ciclo(self):
        """Incrementa o contador de ciclos completos e reinicia todos os assuntos"""
        self.ciclos_completos += 1
        
        # Marcar todos os assuntos como não concluídos para o novo ciclo
        for disciplina in self.progresso:
            if disciplina == "ultima_data":
                continue
                
            for assunto in self.progresso[disciplina]:
                # Incrementar o contador de vezes que o assunto foi concluído
                if self.progresso[disciplina][assunto]["concluido"]:
                    self.progresso[disciplina][assunto]["vezes_concluido"] += 1
                
                # Resetar os campos de conclusão
                self.progresso[disciplina][assunto]["questoes_resolvidas"] = 0
                self.progresso[disciplina][assunto]["concluido"] = False
                self.progresso[disciplina][assunto]["data_conclusao"] = None
        
        # Salvar progresso
        self.salvar_progresso()
        
        # Gerar novos assuntos do dia
        self.gerar_assuntos_do_dia()
        
        # Mostrar mensagem na interface sem popup
        self.mostrar_notificacao(f"Parabéns! Você completou todos os assuntos do ciclo. Iniciando ciclo #{self.ciclos_completos + 1}.")
    
    def proximo_assunto(self):
        """Avança para o próximo assunto da lista do dia"""
        if not self.assuntos_do_dia:
            self.gerar_assuntos_do_dia()
            return
            
        # Encontrar o índice do assunto atual
        try:
            indice_atual = self.assuntos_do_dia.index((self.disciplina_atual, self.assunto_atual))
            proximo_indice = (indice_atual + 1) % len(self.assuntos_do_dia)
            self.disciplina_atual, self.assunto_atual = self.assuntos_do_dia[proximo_indice]
        except ValueError:
            # Se o assunto atual não estiver na lista, pegar o primeiro
            if self.assuntos_do_dia:
                self.disciplina_atual, self.assunto_atual = self.assuntos_do_dia[0]
        
        self.atualizar_exibicao()
    
    def meta_cumprida(self):
        """Marca o assunto atual como concluído (20 questões resolvidas)"""
        if not self.assunto_atual:
            return
            
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
        self.lbl_assuntos_concluidos.config(text=f"Assuntos concluídos neste ciclo: {assuntos_concluidos}")
        
        percentual = 0
        if total_assuntos > 0:
            percentual = (assuntos_concluidos / total_assuntos) * 100
            
        self.lbl_percentual_concluido.config(text=f"Percentual concluído do ciclo atual: {percentual:.1f}%")
        self.lbl_total_questoes.config(text=f"Total de questões resolvidas: {total_questoes}")
        self.lbl_ciclos_completos.config(text=f"Ciclos completos: {self.ciclos_completos}")
        
        # Atualizar barra de progresso geral
        self.progresso_geral_bar["value"] = percentual
    
    def carregar_progresso(self):
        """Carrega o progresso salvo do arquivo JSON"""
        if os.path.exists(self.arquivo_progresso):
            try:
                with open(self.arquivo_progresso, 'r', encoding='utf-8') as file:
                    dados = json.load(file)
                    self.progresso = dados.get("progresso", {})
                    self.ciclos_completos = dados.get("ciclos_completos", 0)
                    self.questoes_hoje = dados.get("questoes_hoje", 0)
                    
                    # Verificar se é um novo dia
                    ultima_data = self.progresso.get("ultima_data", "")
                    data_hoje = date.today().isoformat()
                    
                    if ultima_data != data_hoje:
                        self.questoes_hoje = 0
                        self.progresso["ultima_data"] = data_hoje
            except Exception as e:
                # Mostrar mensagem na interface sem popup
                self.mostrar_notificacao(f"Não foi possível carregar o progresso: {str(e)}", cor="red")
                self.progresso = {}
                self.ciclos_completos = 0
                self.questoes_hoje = 0
        else:
            self.progresso = {}
            self.ciclos_completos = 0
            self.questoes_hoje = 0
    
    def salvar_progresso(self):
        """Salva o progresso atual em um arquivo JSON"""
        try:
            dados = {
                "progresso": self.progresso,
                "ciclos_completos": self.ciclos_completos,
                "questoes_hoje": self.questoes_hoje
            }
            
            with open(self.arquivo_progresso, 'w', encoding='utf-8') as file:
                json.dump(dados, file, ensure_ascii=False, indent=4)
        except Exception as e:
            # Mostrar mensagem na interface sem popup
            self.mostrar_notificacao(f"Não foi possível salvar o progresso: {str(e)}", cor="red")
    
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
                    "Vezes Concluído"
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
                            dados["vezes_concluido"]
                        ])
                
            self.mostrar_notificacao(f"Dados exportados com sucesso para {filename}", cor="green")
            
        except Exception as e:
            self.mostrar_notificacao(f"Erro ao exportar dados: {str(e)}", cor="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = EstudosConcursoApp(root)
    root.mainloop()