# Gerenciador de Estudos para Concurso

Um aplicativo desktop desenvolvido em Python/Tkinter para gerenciar estudos para concursos públicos, com foco em organização e acompanhamento do progresso.

## Funcionalidades

- 📚 Organização de estudos por disciplinas e assuntos
- ✅ Acompanhamento de metas diárias
- 📊 Estatísticas detalhadas de progresso
- 📝 Sistema de anotações por assunto
- 📅 Histórico de estudos
- 💾 Salvamento automático do progresso
- 📈 Exportação de dados para CSV

## Requisitos

- Python 3.x
- Tkinter (geralmente já vem com Python)
- ttkthemes (opcional, para temas modernos)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/gerenciador_estudos.git
cd gerenciador_estudos
```

2. Instale as dependências (opcional):
```bash
pip install ttkthemes
```

3. Execute o programa:
```bash
python gerenciador2.py
```

## Como Usar

1. Ao iniciar o programa, você verá três abas principais:
   - **Estudo do Dia**: Mostra o assunto atual e permite fazer anotações
   - **Estatísticas**: Exibe seu progresso geral e metas diárias
   - **Histórico**: Lista todos os assuntos estudados

2. O programa automaticamente:
   - Gera uma lista de assuntos para estudar no dia
   - Acompanha seu progresso por disciplina
   - Salva suas anotações e progresso automaticamente

3. Para cada assunto você pode:
   - Marcar como concluído (✅ Meta Cumprida!)
   - Fazer anotações
   - Passar para o próximo assunto (➡️ Próximo Assunto)

4. O programa mantém um ciclo de estudos e quando todos os assuntos são concluídos, um novo ciclo é iniciado automaticamente.

## Estrutura do Projeto

- `gerenciador2.py`: Arquivo principal do programa
- `progresso_estudos.json`: Arquivo onde o progresso é salvo
- `README.md`: Este arquivo de documentação

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 