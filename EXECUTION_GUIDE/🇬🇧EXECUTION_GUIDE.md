

# MCP Smart Incident Analyzer - COMPLETE EXECUTION GUIDE

<br><br>

## 🎯 TABLE OF CONTENTS

1. [Environment Setup](#1-environment-setup)
2. [Step-by-Step Installation](#2-step-by-step-installation)
3. [Running the Project](#3-running-the-project)
4. [Testing and Validation](#4-testing-and-validation)
5. [Usage Examples](#5-usage-examples)
6. [Troubleshooting](#6-troubleshooting)



## 1. ENVIRONMENT SETUP

### 1.1 Check Python Installation

Open the terminal (CMD on Windows, Terminal on Linux/Mac) and run:

```bash
python --version
```

**Expected result:**

```text
Python 3.10.x or higher
```

If Python is not installed:

* **Windows**: Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **Linux**: `sudo apt install python3.10` (Ubuntu/Debian)
* **macOS**: `brew install python@3.10`

### 1.2 Check pip Installation

```bash
pip --version
```

**Expected result:**

```text
pip 23.x.x (python 3.10)
```

---

## 2. STEP-BY-STEP INSTALLATION

### 2.1 Download the Project

**Option A: Clone the repository (if hosted on Git)**

```bash
git clone <REPOSITORY_URL>
cd mcp-smart-incident-analyzer
```

**Option B: If you already have the files locally**

```bash
cd path/to/mcp-smart-incident-analyzer
```

### 2.2 Create a Virtual Environment

**On Windows:**

```bash
python -m venv .venv
```

**On Linux/macOS:**

```bash
python3 -m venv .venv
```

**Why create a virtual environment?**

* Isolates project dependencies
* Prevents conflicts with other projects
* Simplifies package management

### 2.3 Activate the Virtual Environment

**On Windows:**

```bash
.venv\Scripts\activate
```

**On Linux/macOS:**

```bash
source .venv/bin/activate
```

**You’ll know it worked when you see:**

```text
(.venv) C:\path\to\project>
```

### 2.4 Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected result:**

```text
Successfully installed pytest-7.4.0 pytest-asyncio-0.21.0 ...
```

---

## 3. RUNNING THE PROJECT

### 3.1 Open Two Terminals

You will need **2 terminals open simultaneously**:

* **Terminal 1**: Server
* **Terminal 2**: Client

### 3.2 Terminal 1 – Run the Server

```bash
# Activate the virtual environment (if not already active)
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Run the server
python server/server.py
```

**Expected output:**

```text
============================================================
MCP Smart Incident Analyzer - Server
============================================================

2025-04-30 10:00:00 - MCP-Server - INFO - MCP server started at localhost:8000
2025-04-30 10:00:00 - MCP-Server - INFO - Waiting for connections...
```

✅ **The server is ready!** Leave this terminal open.

### 3.3 Terminal 2 – Run the Client

```bash
# Activate the virtual environment (if not already active)
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Run the client
python client/client.py
```

**Expected output:**

```text
============================================================
MCP Smart Incident Analyzer - Client
============================================================

Connecting to MCP server...
✓ Successfully connected

Testing connectivity...
✓ Server responding correctly

============================================================
MAIN MENU
============================================================
1. Run usage examples
2. Interactive mode
3. Get statistics
4. Ping test
5. Exit

Choose an option:
```

✅ **The client is ready!**

---

## 4. TESTING AND VALIDATION

### 4.1 Quick Connectivity Test

In **Terminal 2 (client)**, choose option **4**:

```text
Choose an option: 4
```

**Expected result:**

```text
✓ Ping successful
```

### 4.2 Run Preconfigured Examples

In **Terminal 2 (client)**, choose option **1**:

```text
Choose an option: 1
```

You will see **3 incidents being analyzed**:

1. Security incident
2. Performance incident
3. Application error

### 4.3 Run Automated Tests

With the **server running** in Terminal 1, open a **third terminal**:

```bash
# Activate the virtual environment
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Run the tests
python tests/test_connectivity.py
```

**Expected result:**

```text
[1/6] Testing server connection...
✓ Test 1 PASSED: Server accepted the connection

[2/6] Testing ping method...
✓ Test 2 PASSED: Ping method works correctly

...

============================================================
ALL TESTS PASSED SUCCESSFULLY!
============================================================
```

---

## 5. USAGE EXAMPLES

### 5.1 Example 1: Interactive Mode

In **Terminal 2 (client)**, choose option **2**:

```text
Choose an option: 2

============================================================
INTERACTIVE MODE
============================================================
Type 'exit' to quit

Describe the incident:
> Payment system experiencing transaction timeouts

Severity (low/medium/high/critical) [medium]:
> high

Incident source [user-input]:
> payment-gateway
```

**Result:**

```text
============================================================
ANALYSIS RESULT
============================================================
Incident ID: INC-0001
Classification: performance_incident
Priority: high
Status: processed
Analyzed at: 2025-04-30T10:15:30.123456

Recommendation:
  Check system and application performance metrics.

Environment: interactive
Region: local
============================================================
```

### 5.2 Example 2: Security Incident

```text
Describe the incident:
> Detected 50 login attempts with invalid credentials

Severity (low/medium/high/critical) [medium]:
> critical

Incident source [user-input]:
> auth-service
```

**Expected classification:** `security_incident`
**Expected recommendation:** `Immediate system isolation and security team escalation.`

### 5.3 Example 3: Application Error

```text
Describe the incident:
> NullPointerException in the checkout module

Severity (low/medium/high/critical) [medium]:
> high

Incident source [user-input]:
> e-commerce-app
```

**Expected classification:** `error_incident`
**Expected recommendation:** `Investigate error logs and fix the bug.`

---

## 6. TROUBLESHOOTING

### ❌ Problem: "Server unavailable"

**Cause:** The server is not running.

**Solution:**

1. Open Terminal 1
2. Run: `python server/server.py`
3. Wait for the message `"MCP server started"`
4. Try connecting the client again

### ❌ Problem: "Address already in use"

**Cause:** Another process is already using port 8000.

**Windows solution:**

```bash
# Find the process
netstat -ano | findstr :8000

# Kill the process (replace PID with the number found)
taskkill /PID <PID> /F
```

**Linux/macOS solution:**

```bash
# Find the process
lsof -i :8000

# Kill the process (replace PID with the number found)
kill -9 <PID>
```

### ❌ Problem: "ModuleNotFoundError"

**Cause:** Dependencies are not installed.

**Solution:**

```bash
# Ensure the virtual environment is activated
pip install -r requirements.txt
```

### ❌ Problem: "Virtual environment not activating"

**Symptom:** `(.venv)` does not appear before the prompt.

**Windows solution:**

```bash
.venv\Scripts\activate
```

**Linux/macOS solution:**

```bash
source .venv/bin/activate
```

### ❌ Problem: "python: command not found" (Linux/macOS)

**Solution:** Use `python3` instead of `python`:

```bash
python3 -m venv .venv
python3 server/server.py
```

---

## 7. RECOMMENDED COMPLETE WORKFLOW

### Step 1: Prepare the environment (one-time setup)

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Step 2: Start the server (Terminal 1)

```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python server/server.py
```

### Step 3: Run the client (Terminal 2)

```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python client/client.py
```

### Step 4: Explore the features

* Option 1: View ready-made examples
* Option 2: Test your own incidents
* Option 3: Check statistics
* Option 4: Test connectivity

### Step 5: Run tests (Terminal 3 – optional)

```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python tests/test_connectivity.py
```

---

## 8. SHUTTING DOWN THE SYSTEM

### Stop the Client (Terminal 2)

* Choose option **5** in the menu
* Or press `Ctrl+C`

### Stop the Server (Terminal 1)

* Press `Ctrl+C`

**Expected output:**

```text
^C
Server stopped by user
```

### Deactivate the Virtual Environment

```bash
deactivate
```

---

## 9. IMPORTANT TIPS

✅ **Always activate the virtual environment** before running commands
✅ **Keep the server running** while using the client
✅ **Use two separate terminals** — one for the server, one for the client
✅ **Read error messages carefully** — they usually indicate the issue
✅ **Test connectivity first** with ping before submitting incidents

---

## 10. NEXT STEPS

Once you master the basics, you can:

1. **Modify the code** to add new incident types
2. **Create new server methods**
3. **Integrate external APIs**
4. **Add persistence** (database support)
5. **Build a web dashboard**

---

**📞 Need help?**

Check:

* `README.md`
* Commented source code in `server/server.py` and `client/client.py`
* Tests in `tests/test_connectivity.py`

---

**✨ Great job! You are now ready to use the MCP Smart Incident Analyzer!**
