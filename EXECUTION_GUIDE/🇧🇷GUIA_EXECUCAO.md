# 📖 GUIA COMPLETO DE EXECUÇÃO
## MCP Smart Incident Analyzer

---

## 🎯 ÍNDICE

1. [Preparação do Ambiente](#1-preparação-do-ambiente)
2. [Instalação Passo a Passo](#2-instalação-passo-a-passo)
3. [Executando o Projeto](#3-executando-o-projeto)
4. [Testes e Validação](#4-testes-e-validação)
5. [Exemplos de Uso](#5-exemplos-de-uso)
6. [Solução de Problemas](#6-solução-de-problemas)

---

## 1. PREPARAÇÃO DO AMBIENTE

### 1.1 Verificar Python Instalado

Abra o terminal (CMD no Windows, Terminal no Linux/Mac) e execute:

```bash
python --version
```

**Resultado esperado:**
```
Python 3.10.x ou superior
```

Se não tiver Python instalado:
- **Windows**: Baixe em https://www.python.org/downloads/
- **Linux**: `sudo apt install python3.10` (Ubuntu/Debian)
- **macOS**: `brew install python@3.10`

### 1.2 Verificar pip Instalado

```bash
pip --version
```

**Resultado esperado:**
```
pip 23.x.x (python 3.10)
```

---

## 2. INSTALAÇÃO PASSO A PASSO

### 2.1 Baixar o Projeto

**Opção A: Clone do repositório (se estiver no Git)**
```bash
git clone <URL_DO_REPOSITORIO>
cd mcp-smart-incident-analyzer
```

**Opção B: Se você tem os arquivos localmente**
```bash
cd caminho/para/mcp-smart-incident-analyzer
```

### 2.2 Criar Ambiente Virtual

**No Windows:**
```bash
python -m venv .venv
```

**No Linux/macOS:**
```bash
python3 -m venv .venv
```

**Por que criar ambiente virtual?**
- Isola as dependências do projeto
- Evita conflitos com outros projetos
- Facilita o gerenciamento de pacotes

### 2.3 Ativar Ambiente Virtual

**No Windows:**
```bash
.venv\Scripts\activate
```

**No Linux/macOS:**
```bash
source .venv/bin/activate
```

**Você saberá que funcionou quando ver:**
```
(.venv) C:\caminho\do\projeto>
```

### 2.4 Instalar Dependências

```bash
pip install -r requirements.txt
```

**Resultado esperado:**
```
Successfully installed pytest-7.4.0 pytest-asyncio-0.21.0 ...
```

---

## 3. EXECUTANDO O PROJETO

### 3.1 Abrir Dois Terminais

Você precisará de **2 terminais abertos simultaneamente**:
- **Terminal 1**: Para o servidor
- **Terminal 2**: Para o cliente

### 3.2 Terminal 1 - Executar o Servidor

```bash
# Ative o ambiente virtual (se ainda não estiver ativo)
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Execute o servidor
python server/server.py
```

**Saída esperada:**
```
============================================================
MCP Smart Incident Analyzer - Servidor
============================================================

2025-04-30 10:00:00 - MCP-Server - INFO - Servidor MCP iniciado em localhost:8000
2025-04-30 10:00:00 - MCP-Server - INFO - Aguardando conexões...
```

✅ **O servidor está pronto!** Deixe este terminal aberto.

### 3.3 Terminal 2 - Executar o Cliente

```bash
# Ative o ambiente virtual (se ainda não estiver ativo)
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Execute o cliente
python client/client.py
```

**Saída esperada:**
```
============================================================
MCP Smart Incident Analyzer - Cliente
============================================================

Conectando ao servidor MCP...
✓ Conectado com sucesso

Testando conectividade...
✓ Servidor respondendo corretamente

============================================================
MENU PRINCIPAL
============================================================
1. Executar exemplos de uso
2. Modo interativo
3. Obter estatísticas
4. Teste de ping
5. Sair

Escolha uma opção:
```

✅ **O cliente está pronto!**

---

## 4. TESTES E VALIDAÇÃO

### 4.1 Teste Rápido de Conectividade

No **Terminal 2 (cliente)**, escolha opção **4**:

```
Escolha uma opção: 4
```

**Resultado esperado:**
```
✓ Ping bem-sucedido
```

### 4.2 Executar Exemplos Pré-Configurados

No **Terminal 2 (cliente)**, escolha opção **1**:

```
Escolha uma opção: 1
```

Você verá 3 incidentes sendo analisados:
1. Incidente de segurança
2. Incidente de performance
3. Erro de aplicação

### 4.3 Executar Testes Automatizados

Com o **servidor rodando** no Terminal 1, abra um **terceiro terminal**:

```bash
# Ative o ambiente virtual
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Execute os testes
python tests/test_connectivity.py
```

**Resultado esperado:**
```
[1/6] Testando conexão com o servidor...
✓ Teste 1 PASSOU: Servidor aceitou a conexão

[2/6] Testando método ping...
✓ Teste 2 PASSOU: Método ping funciona corretamente

...

============================================================
TODOS OS TESTES PASSARAM COM SUCESSO!
============================================================
```

---

## 5. EXEMPLOS DE USO

### 5.1 Exemplo 1: Modo Interativo

No **Terminal 2 (cliente)**, escolha opção **2**:

```
Escolha uma opção: 2

============================================================
MODO INTERATIVO
============================================================
Digite 'sair' para encerrar

Descreva o incidente:
> Sistema de pagamento apresentando timeout nas transações

Severidade (low/medium/high/critical) [medium]:
> high

Fonte do incidente [user-input]:
> payment-gateway
```

**Resultado:**
```
============================================================
RESULTADO DA ANÁLISE
============================================================
ID do Incidente: INC-0001
Classificação: performance_incident
Prioridade: high
Status: processed
Analisado em: 2025-04-30T10:15:30.123456

Recomendação:
  Verificar métricas de sistema e aplicação.

Ambiente: interactive
Região: local
============================================================
```

### 5.2 Exemplo 2: Incidente de Segurança

```
Descreva o incidente:
> Detectadas 50 tentativas de login com credenciais inválidas

Severidade (low/medium/high/critical) [medium]:
> critical

Fonte do incidente [user-input]:
> auth-service
```

**Classificação esperada:** `security_incident`
**Recomendação esperada:** `Isolamento imediato do sistema e acionamento da equipe de segurança.`

### 5.3 Exemplo 3: Erro de Aplicação

```
Descreva o incidente:
> NullPointerException no módulo de checkout

Severidade (low/medium/high/critical) [medium]:
> high

Fonte do incidente [user-input]:
> e-commerce-app
```

**Classificação esperada:** `error_incident`
**Recomendação esperada:** `Investigar logs de erro e corrigir bug.`

---

## 6. SOLUÇÃO DE PROBLEMAS

### ❌ Problema: "Servidor não disponível"

**Causa:** O servidor não está rodando.

**Solução:**
1. Abra o Terminal 1
2. Execute: `python server/server.py`
3. Aguarde a mensagem "Servidor MCP iniciado"
4. Tente conectar o cliente novamente

### ❌ Problema: "Endereço já em uso" (Address already in use)

**Causa:** Já existe outro processo usando a porta 8000.

**Solução no Windows:**
```bash
# Encontrar o processo
netstat -ano | findstr :8000

# Encerrar o processo (substitua PID pelo número encontrado)
taskkill /PID <PID> /F
```

**Solução no Linux/macOS:**
```bash
# Encontrar o processo
lsof -i :8000

# Encerrar o processo (substitua PID pelo número encontrado)
kill -9 <PID>
```

### ❌ Problema: "ModuleNotFoundError"

**Causa:** Dependências não instaladas.

**Solução:**
```bash
# Certifique-se de que o ambiente virtual está ativado
pip install -r requirements.txt
```

### ❌ Problema: "Ambiente virtual não ativa"

**Sintoma:** Não aparece `(.venv)` antes do prompt.

**Solução Windows:**
```bash
.venv\Scripts\activate
```

**Solução Linux/macOS:**
```bash
source .venv/bin/activate
```

### ❌ Problema: "python: command not found" (Linux/macOS)

**Solução:** Use `python3` em vez de `python`:
```bash
python3 -m venv .venv
python3 server/server.py
```

---

## 7. FLUXO COMPLETO RECOMENDADO

### Passo 1: Prepare o ambiente (uma vez)
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### Passo 2: Inicie o servidor (Terminal 1)
```bash
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
python server/server.py
```

### Passo 3: Execute o cliente (Terminal 2)
```bash
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
python client/client.py
```

### Passo 4: Explore as funcionalidades
- Opção 1: Veja exemplos prontos
- Opção 2: Teste seus próprios incidentes
- Opção 3: Verifique estatísticas
- Opção 4: Teste a conectividade

### Passo 5: Execute testes (Terminal 3 - opcional)
```bash
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
python tests/test_connectivity.py
```

---

## 8. ENCERRANDO O SISTEMA

### Encerrar o Cliente (Terminal 2)
- Escolha opção **5** no menu
- Ou pressione `Ctrl+C`

### Encerrar o Servidor (Terminal 1)
- Pressione `Ctrl+C`

**Saída esperada:**
```
^C
Servidor encerrado pelo usuário
```

### Desativar Ambiente Virtual
```bash
deactivate
```

---

## 9. DICAS IMPORTANTES

✅ **Sempre ative o ambiente virtual** antes de executar qualquer comando
✅ **Mantenha o servidor rodando** enquanto usa o cliente
✅ **Use dois terminais separados** - um para servidor, outro para cliente
✅ **Leia as mensagens de erro** - elas geralmente indicam o problema
✅ **Teste a conectividade** com ping antes de enviar incidentes

---

## 10. PRÓXIMOS PASSOS

Depois de dominar o básico, você pode:

1. **Modificar o código** para adicionar novos tipos de incidentes
2. **Criar novos métodos** no servidor
3. **Integrar com APIs externas**
4. **Adicionar persistência** (banco de dados)
5. **Criar um dashboard web**

---

**📞 Precisa de ajuda?**

Consulte:
- README.md principal
- Código-fonte comentado em `server/server.py` e `client/client.py`
- Testes em `tests/test_connectivity.py`

---

**✨ Bom trabalho! Você está pronto para usar o MCP Smart Incident Analyzer!**
