# 🎯 AVIATOR AI PRO - Ferramenta de Análise Inteligente

Ferramenta premium para análise de padrões do Aviator (playnabets.com) com IA que aprende até 99% de precisão.

## 🎯 O QUE É?

Aviator AI Pro é uma aplicação Streamlit que:

1. **Captura dados** do Aviator em tempo real
2. **Aprende padrões** de velas (azul, roxa, rosa)
3. **Fornece sinais** com alta precisão
4. **Permite feedback** manual para calibração
5. **Monitora 24/7** e melhora continuamente

## 📊 CATEGORIAS DE VELAS

| Cor | Range | Significado | Ação |
|-----|-------|-------------|------|
| 🔵 Azul | 1.00x - 1.99x | Recolhimento/Perda | ❌ Não Entrar |
| 🟣 Roxa | 2.00x - 9.99x | Fase Média/Pagamento | ⚠️ Entrar 5x |
| 🔴 Rosa | 10.00x - 5000x | Objetivo/Raro | ✅ Entrar Rosa |

## 🚀 COMO COMEÇAR

### Passo 1: Clonar do GitHub

```bash
git clone https://github.com/seu-usuario/aviator-ai-pro.git
cd aviator-ai-pro
```

### Passo 2: Instalar Dependências

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Passo 3: Rodar Localmente

```bash
streamlit run app.py
```

Acesse: http://localhost:8501

## 📋 ESTRUTURA DO PROJETO

```
aviator-ai-pro/
├── app.py                    # Dashboard Streamlit
├── ia_aviator.py             # Motor de IA
├── captura_dados.py          # Capturador de dados
├── banco_dados.py            # Banco de dados SQLite
├── requirements.txt          # Dependências
├── .streamlit/
│   └── config.toml          # Configuração Streamlit
├── .gitignore               # Arquivos a ignorar
└── README.md                # Este arquivo
```

## 🧠 COMO FUNCIONA A IA

### 5 Mecanismos de Aprendizado

1. **Synaptic Plasticity** - Ajusta pesos dos padrões
2. **Neurogenesis** - Cria novos padrões
3. **Memory Consolidation** - Consolida aprendizados
4. **Lateral Inhibition** - Inibe padrões fracos
5. **Reconsolidation** - Reforça sucessos

### Fluxo de Dados

```
Aviator (playnabets.com)
        ↓
Capturador de Dados
        ↓
IA Aviator (aprende padrões)
        ↓
Banco de Dados (armazena histórico)
        ↓
Dashboard (exibe sinais)
        ↓
Feedback Manual (calibra IA)
```

## 💡 COMO USAR

### 1. Adicionar Dados

Cole os dados capturados no campo de entrada:
```
Exemplo: 2.45x 14:32:15
```

Ou clique em "🧪 Teste" para adicionar dados aleatórios.

### 2. Analisar Sinais

O dashboard mostra:
- ✅ **ENTRAR ROSA** - Vela rosa detectada
- ✅ **ENTRAR AGORA 5x** - Fase de pagamento
- ❌ **NÃO ENTRAR** - Fase de recolhimento
- ⏳ **AGUARDE FIM DE CICLO** - Analisando padrões

### 3. Fornecer Feedback

Após cada resultado:
- 👍 **ACERTOU** - IA acertou a previsão
- 👎 **ERROU** - IA errou a previsão

Isso calibra a IA para melhorar.

### 4. Monitorar Progresso

No dashboard veja:
- 📊 **Aprendizado** - Progresso de aprendizado (0-100%)
- 🎪 **Rodadas** - Total de rodadas processadas
- 🎯 **Precisão** - Percentual de acertos

## 📈 ABAS DO DASHBOARD

### 📊 Dashboard
- Estatísticas gerais
- Distribuição de cores
- Padrões aprendidos

### 📈 Gráficos
- Evolução dos multiplicadores
- Distribuição de cores
- Análise de tendências

### 🎪 Histórico
- Últimas 50 velas
- Dados detalhados
- Exportação

### ⚙️ Controles
- Resetar banco de dados
- Resetar IA
- Resetar capturador
- Visualizar estatísticas

## 🌐 DEPLOY NO STREAMLIT CLOUD

### Passo 1: Fazer Push para GitHub

```bash
git add .
git commit -m "Initial commit: Aviator AI Pro"
git push origin main
```

### Passo 2: Conectar ao Streamlit Cloud

1. Acesse: https://streamlit.io/cloud
2. Clique em "New app"
3. Selecione seu repositório GitHub
4. Configure:
   - Repository: seu-usuario/aviator-ai-pro
   - Branch: main
   - Main file path: app.py
5. Clique "Deploy"

### Passo 3: Usar em Produção

Sua app estará disponível em:
```
https://seu-app-name.streamlit.app
```

## 🔐 SEGURANÇA

- ✅ Sem armazenamento de dados sensíveis
- ✅ Sem chamadas de API não autorizadas
- ✅ Validação de entrada
- ✅ Isolamento de estado

## 📊 DADOS ARMAZENADOS

### SQLite Database (aviator_ia.db)

- **velas** - Histórico de velas capturadas
- **padroes** - Padrões aprendidos pela IA
- **feedback** - Feedback manual do usuário
- **estatisticas** - Histórico de estatísticas

## 🎯 OBJETIVOS DE APRENDIZADO

- [ ] 10% de precisão (primeiras 100 rodadas)
- [ ] 30% de precisão (500 rodadas)
- [ ] 50% de precisão (1000 rodadas)
- [ ] 70% de precisão (5000 rodadas)
- [ ] 90% de precisão (10000 rodadas)
- [ ] 99% de precisão (50000+ rodadas)

## 🆘 TROUBLESHOOTING

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "Port 8501 already in use"
```bash
streamlit run app.py --server.port 8502
```

### Erro: "Connection refused"
Verifique se Streamlit está rodando:
```bash
streamlit run app.py
```

### Banco de dados corrompido
```bash
rm aviator_ia.db
# Reinicie a aplicação
```

## 📞 SUPORTE

Para dúvidas ou sugestões, abra uma issue no GitHub.

## 📝 LICENÇA

Propriedade do usuário - Uso exclusivo

## 🎯 ROADMAP

- [ ] Integração com Betou API
- [ ] Alertas em tempo real
- [ ] Análise avançada com ML
- [ ] Exportação de relatórios
- [ ] Dashboard mobile
- [ ] Histórico persistente
- [ ] Múltiplos usuários
- [ ] API REST

## 📊 ESTATÍSTICAS

- **Versão:** 1.0.0
- **Linguagem:** Python 3.8+
- **Framework:** Streamlit 1.28+
- **Banco de Dados:** SQLite
- **Status:** ✅ Produção

---

**Desenvolvido com ❤️ para Aviator AI Pro**

**Última atualização:** 2026-05-17
