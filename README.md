# ssh-handshake-grupi11
Përshkrimi i Projektit
------------------------------------------------------------------------------------------------------
Ky projekt përfshin implementimin e një versioni të thjeshtuar të Secure Shell Protocol Handshake në një model Client-Server duke përdorur gjuhën programuese Python.

Qëllimi i këtij projekti është të ofrojë një përshkrim teorik dhe praktik të mënyrës se si funksionon procesi i SSH Handshake, duke përfshirë fazat kryesore si negocimi i algoritmeve, shkëmbimi i çelësave kriptografikë, autentikimi i serverit dhe krijimi i një kanali të sigurt komunikimi.
Implementimi realizohet përmes dy aplikacioneve console:

 - SSH Client që fillon lidhjen dhe verifikon identitetin e serverit,
 - SSH Server që simulon sjelljen e një serveri SSH gjatë procesit të handshake.

Programi i lejon përdoruesit të iniciojë një lidhje të sigurt ndërmjet klientit dhe serverit, duke demonstruar në praktikë të gjitha fazat kryesore të krijimit të një sesioni të sigurt SSH. Gjatë ekzekutimit, aplikacioni shfaq mesazhe informative dhe logje të detajuara për secilin hap të handshake process, duke ndihmuar përdoruesin të kuptojë mënyrën e funksionimit të protokolleve të sigurta të komunikimit në rrjete kompjuterike.

---

## Struktura e Projektit

```
projekti3Arbena/
│
├── server.py          # Serveri SSH — menaxhon handshake-in dhe kanalin e sigurt
├── client.py          # Klienti SSH — inicializon lidhjen dhe handshake-in
├── crypto_utils.py    # Funksionet kriptografike (RSA, DH, AES, HMAC)
├── known_hosts.txt    # Krijohet automatikisht: ruan çelësin publik të serverit
├── .gitignore         # Skedarët që nuk ngarkohen në Git
└── README.md          # Ky skedar
```

---

## Përshkrimi i Pjesëve të Implementuara

### `server.py` — Serveri SSH
Simulon sjelljen e një serveri SSH gjatë fazës së handshake-ut. Detyrat kryesore:
- Gjeneron çift çelësash **RSA-2048** (simulon databazën e host keys të serverit)
- Pret lidhje nga klienti në portën `2222`
- Kryen të 4 hapat e handshake-ut: negocim algoritmesh, shkëmbim DH, nënshkrim dixhital, aktivizim kanali të enkriptuar
- Verifikon integritetin e mesazhit me **HMAC-SHA256** dhe e dekipton me **AES-256-CFB**

### `client.py` — Klienti SSH
Inicializon lidhjen dhe kryen handshake-in me serverin. Detyrat kryesore:
- Propozon algoritmet e mbështetura (x25519, AES256, SHA256)
- Gjeneron çelësat **X25519** dhe llogarit sekretin e përbashkët
- Verifikon identitetin e serverit duke kontrolluar **nënshkrimin RSA** dhe **known_hosts.txt**
- Zbaton mbrojtjen **MITM** — ndërpret lidhjen nëse çelësi i serverit ka ndryshuar
- Enkipton dhe dërgon mesazhin me AES-256-CFB + HMAC-SHA256

### `crypto_utils.py` — Funksionet Kriptografike
Moduli qendror që ofron të gjitha operacionet kriptografike:

| Funksioni           | Përshkrimi                                                        |
|---------------------|-------------------------------------------------------------------|
| `generate_rsa_keys()` | Gjeneron çift çelësash RSA-2048 për autentifikim serveri       |
| `sign_data()`       | Nënshkruan të dhëna me RSA-PSS + SHA-256                         |
| `verify_signature()`| Verifikon nënshkrimin RSA duke përdorur çelësin publik           |
| `generate_dh_keypair()` | Gjeneron çift çelësash X25519 për shkëmbim Diffie-Hellman    |
| `derive_shared_key()` | Llogarit sekretin e përbashkët nga çelësi publik i palës tjetër |
| `aes_encrypt()`     | Enkipton tekst me AES-256-CFB                                    |
| `aes_decrypt()`     | Dekipton tekst me AES-256-CFB                                    |
| `create_hmac()`     | Krijon HMAC-SHA256 për verifikim integriteti                     |
| `verify_hmac()`     | Verifikon HMAC me krahasim në kohë konstante (anti-timing attack) |

---

## Kërkesat dhe Instalimi

### Parakushtet
- **Python 3.8** ose më i ri
- **pip** (menaxheri i paketave të Python)

### Hapi 1 — Klono ose shkarko projektin

```bash
git clone https://github.com/username/projekti3Arbena.git
cd projekti3Arbena
```

ose shkarko dhe shpaketoje si ZIP, pastaj navigo në dosjen e projektit:

```bash
cd C:\Users\Lenovo\Desktop\projekti3Arbena
```

### Hapi 2 — Instalo varësitë

```bash
pip install cryptography
```

Verifiko instalimin:

```bash
python -c "import cryptography; print(cryptography.__version__)"
```

Duhet të shfaqet numri i versionit, p.sh. `48.0.0`.

---

## Udhëzime të Hollësishme për Ekzekutim

> ⚠️ **Kujdes:** Serveri duhet të jetë **i startuar dhe duke pritur** para se të ekzekutohet klienti.

---

### Hapi 1 — Hap dy dritare terminali

**Windows (PowerShell ose CMD):**
- Shtyp `Windows + R`, shkruaj `cmd`, shtyp Enter — bëje dy herë

**macOS / Linux:**
- Hap dy tab të reja në terminalin tënd

---

### Hapi 2 — Navigo në dosjen e projektit (në të dyja terminalet)

```bash
cd C:\Users\Lenovo\Desktop\projekti3Arbena
```

---

### Hapi 3 — Ekzekuto serverin (Terminali 1)

```bash
python server.py
```

**Output-i i pritur:**
```
==================================================
Server starting up...
==================================================
[SERVER] 2026-05-17 13:24:15,212 - INFO - RSA Host Keys generated successfully.
Awaiting client connections...
```

✅ Prit derisa të shfaqet `Awaiting client connections...` — serveri është gati.

---

### Hapi 4 — Ekzekuto klientin (Terminali 2)

```bash
python client.py
```

**Output-i i pritur:**
```
==================================================
Welcome to Simplified SSH Client.
==================================================
Attempting to connect to the SSH server...
Starting handshake protocol...
```

---

### Hapi 5 — Vëzhgo ekzekutimin e plotë

Pas ekzekutimit të klientit, handshake-i kryhet automatikisht. Shiko të dyja terminalet njëkohësisht.

---

## Shembull i Plotë i Ekzekutimit

### Terminali 1 — Serveri

```
==================================================
Server starting up...
==================================================
[SERVER] 2026-05-17 13:24:15,212 - INFO - RSA Host Keys generated successfully.
Awaiting client connections...
Client connected! Initiating handshake with ('127.0.0.1', 57197)...
[SERVER] 2026-05-17 13:24:16,329 - INFO - Step 1: Negotiating algorithms...
[SERVER] 2026-05-17 13:24:16,330 - INFO - Received client proposal: {'kex': ['x25519'], 'encryption': ['AES256'], 'hmac': ['SHA256']}
[SERVER] 2026-05-17 13:24:16,330 - INFO - Sent negotiated algorithms: {'kex': 'x25519', 'encryption': 'AES256', 'hmac': 'SHA256'}
[SERVER] 2026-05-17 13:24:16,330 - INFO - Step 2: Performing Diffie-Hellman Key Exchange...
[SERVER] 2026-05-17 13:24:16,341 - INFO - Shared master secret derived successfully.
[SERVER] 2026-05-17 13:24:16,342 - INFO - Step 3: Authenticating server identity...
[SERVER] 2026-05-17 13:24:16,344 - INFO - Sent Host Public Key and Digital Signature to client.
[SERVER] 2026-05-17 13:24:16,344 - INFO - Step 4: Activating Encrypted Channel...
[SERVER] 2026-05-17 13:24:16,357 - INFO - HMAC Verification: SUCCESS. Data integrity verified.

==================================================
Handshake successful. Proceeding to establish secure channel...
Received secure message: Hello secure server! This is a confidential SSH session.
==================================================

Session closed.
```

---

### Terminali 2 — Klienti

```
==================================================
Welcome to Simplified SSH Client.
==================================================
Attempting to connect to the SSH server...
Starting handshake protocol...
[CLIENT] 2026-05-17 13:24:16,100 - INFO - Step 1: Sending algorithm preferences...
[CLIENT] 2026-05-17 13:24:16,110 - INFO - Negotiated algorithms: {'kex': 'x25519', 'encryption': 'AES256', 'hmac': 'SHA256'}
[CLIENT] 2026-05-17 13:24:16,111 - INFO - Step 2: Exchanging Diffie-Hellman keys...
[CLIENT] 2026-05-17 13:24:16,125 - INFO - Shared master secret derived successfully.
[CLIENT] 2026-05-17 13:24:16,126 - INFO - Step 3: Verifying server identity...
[CLIENT] 2026-05-17 13:24:16,127 - INFO - New host. Saving server public key to known_hosts.txt
Server identity verified. Handshake successful.
[CLIENT] 2026-05-17 13:24:16,130 - INFO - Step 4: Setting up secure symmetric channel...

==================================================
Secure channel established. You can now begin your session.
Secure message sent to server.
==================================================
```

---

### Shembull: Detektimi i Sulmit MITM

Nëse serveri riniset (gjeneron çelësa të rinj RSA) ndërkohë që `known_hosts.txt` ruan çelësin e vjetër, klienti do të shfaqë:

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: POSSIBLE MAN-IN-THE-MIDDLE ATTACK!
Server host key has changed!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

Lidhja ndërpritet automatikisht.

---

## Shpjegimi i SSH Handshake — Hap pas Hapi

### Hapi 1: Negocimi i Algoritmeve
Klienti dërgon një propozim JSON me algoritmet që mbështet. Serveri zgjedh dhe konfirmon. Kjo siguron dakordësi para çdo operacioni kriptografik.

### Hapi 2: Shkëmbimi i Çelësave — Diffie-Hellman (X25519)
Të dyja palët gjenerojnë çift çelësash X25519 dhe shkëmbejnë çelësat publikë. Secila palë llogarit sekretin e përbashkët duke përdorur çelësin e vet privat + çelësin publik të tjetrit. Sekreti **nuk transmetohet** kurrë nëpër rrjet — ofron **Perfect Forward Secrecy**.

### Hapi 3: Autentifikimi i Serverit (Nënshkrimi Dixhital + MITM)
Serveri nënshkruan çelësin e përbashkët me RSA-2048 (PSS + SHA-256) dhe dërgon çelësin publik + nënshkrimin. Klienti verifikon nënshkrimin dhe kontrollon `known_hosts.txt` kundër sulmeve MITM.

### Hapi 4: Komunikimi i Enkriptuar (AES-256-CFB + HMAC-SHA256)
Klienti enkipton mesazhin me AES-256-CFB dhe llogarit HMAC-SHA256. Serveri verifikon HMAC-un (integritetin) pastaj dekipton mesazhin.

---

## Masat e Sigurisë

| Kërcënimi | Mbrojtja |
|-----------|---------|
| Man-in-the-Middle (MITM) | Krahasimi i `known_hosts.txt` + verifikimi i nënshkrimit RSA |
| Përgjimi i të dhënave | Enkriptimi AES-256-CFB pas handshake-it |
| Manipulimi i mesazheve | HMAC-SHA256 me `hmac.compare_digest` (kohë konstante) |
| Çelësa të dobët / Replay | X25519 — çift i ri çelësash për çdo sesion |
| Autentifikim i dobët i serverit | RSA-2048 me mbushje PSS |

---

## Trajtimi i Gabimeve

| Skenari | Sjellja |
|---------|---------|
| Serveri nuk është duke punuar | Klienti logon `Connection refused` dhe mbyllet |
| MITM i zbuluar | Paralajmërim i qartë + ndërprerje e lidhjes |
| Nënshkrim invalid | Klienti logon gabimin dhe mbyll lidhjen |
| Dështim HMAC | Serveri refuzon mesazhin |
| Gabim i papritur | `finally` mbyll socket-in pastër në të dyja palët |

---

## Skedarët e Gjeneruar Automatikisht

| Skedari | Përshkrimi |
|---------|-----------|
| `known_hosts.txt` | Ruan çelësin publik RSA të serverit pas lidhjes së parë. Parandalon MITM. |
| `__pycache__/` | Bytecode i kompajluar nga Python. Nuk ngarkohet në Git (shih `.gitignore`). |
