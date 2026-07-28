# AGENTS.md

## Cursor Cloud specific instructions

### O que é
Aplicação Flask única (server-rendered), o "Portal de Exercícios". Não há banco de
dados, cache, fila ou serviços externos — todo o conteúdo é derivado dos arquivos
`.html` em `exercicios_flask/templates/` e `exercicios_formularios/templates/`
e registrado explicitamente pelos controllers. Detalhes gerais de setup estão no
`README`.

### Como rodar
- Serviço único: `python3 app.py` → serve em `http://127.0.0.1:5000` (Flask, `debug=True`).
- Login (credenciais fixas em `app.py`): usuário `Miguel`, senha `12345`.

### Dependências
- Única dependência é `Flask` (`requirements.txt`), instalada via `pip install --user`.
- Observação: `python3 -m venv` NÃO funciona neste ambiente (falta `ensurepip` e o
  pacote `python3.12-venv` não está disponível via apt). Por isso o setup usa
  `pip install --user` em vez de virtualenv.

### Testes / Lint / Build
- Não há suíte de testes (o `README` cita `pytest`, mas não existe pasta `tests/`
  nem `pytest` em `requirements.txt`).
- Não há etapa de build nem lint configurados; o front-end é HTML/CSS servido direto.

### Notas úteis (não óbvias)
- Templates Jinja e `static/styles.css` são recarregados a cada request; mudanças em
  `.py` disparam o reloader do Flask (debug). Não é preciso reiniciar para editar
  templates/CSS.
- A sidebar retrátil guarda o estado (recolhida/expandida) em `localStorage`
  (`sidebar-collapsed`). Após recolher uma vez, ela permanece recolhida em logins
  seguintes até ser expandida novamente — isso é intencional.
- O pacote `controllers/` registra as rotas de cada exercício no `app.py`.
