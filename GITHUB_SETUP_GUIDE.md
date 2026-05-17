# 📚 GUIA COMPLETO: SETUP GITHUB PARA AVIATOR AI

## 🎯 OBJETIVO
Criar repositório no GitHub e fazer upload de todos os arquivos da ferramenta Aviator AI.

---

## ✅ PASSO 1: CRIAR REPOSITÓRIO NO GITHUB

### 1.1 Acesse GitHub
- Vá para: https://github.com/new
- Faça login (se não estiver logado)

### 1.2 Preencha os dados
```
Repository name: aviator-ai-pro
Description: Ferramenta de IA para análise de padrões Aviator com 99% de precisão
Visibility: Public (ou Private se preferir)
```

### 1.3 Clique em "Create repository"

---

## ✅ PASSO 2: PREPARAR COMPUTADOR LOCAL

### 2.1 Instale Git
- **Windows**: https://git-scm.com/download/win
- **Mac**: `brew install git`
- **Linux**: `sudo apt-get install git`

### 2.2 Configure Git (primeira vez)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@gmail.com"
```

### 2.3 Crie pasta do projeto
```bash
mkdir aviator-ai-pro
cd aviator-ai-pro
```

---

## ✅ PASSO 3: ESTRUTURA DE PASTAS

Crie a seguinte estrutura:

```
aviator-ai-pro/
├── app.py                    # Aplicação principal Streamlit
├── ia_aviator.py             # IA com aprendizado de padrões
├── captura_dados.py          # Captura dados do iframe
├── banco_dados.py            # Armazena padrões e histórico
├── requirements.txt          # Dependências Python
├── .streamlit/
│   └── config.toml          # Configuração Streamlit
├── .gitignore               # Arquivos a ignorar
└── README.md                # Documentação
```

### Como criar no terminal:
```bash
mkdir .streamlit
touch app.py ia_aviator.py captura_dados.py banco_dados.py requirements.txt
touch .streamlit/config.toml .gitignore README.md
```

---

## ✅ PASSO 4: ADICIONAR ARQUIVOS

Copie o conteúdo de cada arquivo fornecido para sua pasta local.

**Arquivos que você vai receber:**
1. `app.py` - Dashboard completo
2. `ia_aviator.py` - Motor de IA
3. `captura_dados.py` - Capturador de dados
4. `banco_dados.py` - Banco de dados
5. `requirements.txt` - Dependências
6. `.streamlit/config.toml` - Config
7. `.gitignore` - Arquivos a ignorar
8. `README.md` - Documentação

---

## ✅ PASSO 5: INICIALIZAR GIT LOCALMENTE

```bash
cd aviator-ai-pro
git init
git add .
git commit -m "Initial commit: Aviator AI Pro - IA para análise de padrões Aviator"
```

---

## ✅ PASSO 6: CONECTAR COM GITHUB

### 6.1 Copie a URL do seu repositório
- Vá em: https://github.com/seu-usuario/aviator-ai-pro
- Clique em "Code" (botão verde)
- Copie a URL HTTPS

### 6.2 Adicione o repositório remoto
```bash
git remote add origin https://github.com/seu-usuario/aviator-ai-pro.git
```

### 6.3 Mude o branch para main
```bash
git branch -M main
```

### 6.4 Faça o primeiro push
```bash
git push -u origin main
```

**Pode pedir para fazer login no GitHub - faça normalmente**

---

## ✅ PASSO 7: VERIFICAR NO GITHUB

1. Acesse: https://github.com/seu-usuario/aviator-ai-pro
2. Você deve ver todos os arquivos listados
3. Pronto! Repositório criado com sucesso ✅

---

## 🔄 PRÓXIMAS VEZES (ATUALIZAR CÓDIGO)

Quando quiser fazer alterações:

```bash
# 1. Faça as mudanças nos arquivos

# 2. Adicione as mudanças
git add .

# 3. Faça commit com mensagem descritiva
git commit -m "Descrição da mudança"

# 4. Envie para GitHub
git push origin main
```

---

## 🆘 TROUBLESHOOTING

### Erro: "fatal: not a git repository"
```bash
git init
```

### Erro: "Permission denied (publickey)"
- Gere SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
- Ou use HTTPS em vez de SSH

### Erro: "branch 'main' set up to track 'origin/main'"
Tudo certo! Continue normalmente.

---

## ✅ CHECKLIST FINAL

- [ ] Repositório criado no GitHub
- [ ] Git instalado no computador
- [ ] Pasta `aviator-ai-pro` criada localmente
- [ ] Todos os arquivos copiados
- [ ] `git init` executado
- [ ] `git add .` executado
- [ ] `git commit` feito
- [ ] `git remote add origin` configurado
- [ ] `git push` realizado com sucesso
- [ ] Arquivos visíveis no GitHub

---

## 🎯 PRÓXIMO PASSO

Após completar este guia, passe para:
**GUIA STREAMLIT CLOUD** (deploy automático)

---

**Versão:** 1.0  
**Data:** 2026-05-17  
**Status:** ✅ Pronto
