# ssh-handshake-grupi11
Përshkrimi i Projektit
------------------------------------------------------------------------------------------------------
Ky projekt përfshin implementimin e një versioni të thjeshtuar të Secure Shell Protocol Handshake në një model Client-Server duke përdorur gjuhën programuese Python.

Qëllimi i këtij projekti është të ofrojë një përshkrim teorik dhe praktik të mënyrës se si funksionon procesi i SSH Handshake, duke përfshirë fazat kryesore si negocimi i algoritmeve, shkëmbimi i çelësave kriptografikë, autentikimi i serverit dhe krijimi i një kanali të sigurt komunikimi.
Programi i lejon përdoruesit të iniciojë një lidhje të sigurt ndërmjet klientit dhe serverit, duke demonstruar në praktikë të gjitha fazat kryesore të krijimit të një sesioni të sigurt SSH.


Përshkrimi i Algoritmit  SSH Handshake 
------------------------------------------------------------------------------------------------------
SSH Handshake është procesi përmes të cilit klienti dhe serveri krijojnë një kanal të sigurt komunikimi para shkëmbimit të të dhënave. Gjatë këtij procesi realizohen negocimi i algoritmeve, shkëmbimi i çelësave, autentifikimi i serverit dhe aktivizimi i komunikimit të enkriptuar.

### Hapi 1: Negocimi i Algoritmeve
Klienti fillimisht dërgon një listë me algoritmet që mbështet për:
- key exchange,
- encryption,
- HMAC.

Serveri zgjedh algoritmet e përbashkëta dhe i konfirmon klientit.  
Ky hap siguron kompatibilitet dhe dakordësi për mekanizmat kriptografikë që do të përdoren gjatë sesionit.

### Hapi 2: Shkëmbimi i Çelësave — X25519 Diffie-Hellman
Klienti dhe serveri gjenerojnë çift çelësash X25519:
- private key,
- public key.

Pastaj shkëmbejnë çelësat publikë dhe secila palë llogarit një shared secret duke përdorur:
- çelësin privat të vet,
- dhe public key të palës tjetër.

Sekreti i përbashkët nuk transmetohet kurrë në rrjet, gjë që e bën komunikimin më të sigurt dhe ofron Perfect Forward Secrecy.

### Hapi 3: Derivimi i Session Key
Nga shared secret krijohet session key duke përdorur HKDF me SHA-256.

Ky session key përdoret për:
- enkriptimin simetrik,
- gjenerimin e HMAC,
- mbrojtjen e komunikimit gjatë sesionit.

### Hapi 4: Autentifikimi i Serverit
Serveri nënshkruan session key me RSA-2048 Digital Signature dhe ia dërgon klientit së bashku me public key.

Klienti:
- verifikon nënshkrimin,
- kontrollon public key në `known_hosts.txt`,
- dhe sigurohet që serveri është autentik.

Ky mekanizëm mbron kundër sulmeve MITM (Man-in-the-Middle).

### Hapi 5: Aktivizimi i Kanalit të Enkriptuar
Pas përfundimit të handshake-ut krijohet kanali i sigurt i komunikimit.

Klienti:
- enkripton mesazhin me AES-256-CFB,
- krijon HMAC-SHA256 për integritetin e të dhënave,
- dhe e dërgon mesazhin te serveri.

Serveri:
- verifikon HMAC-un,
- dekripton mesazhin,
- dhe pranon komunikimin e sigurt.

Ky proces garanton:
- konfidencialitetin,
- integritetin,
- dhe autentifikimin gjatë komunikimit SSH.

Komponentët Kryesor
------------------------------------------------------------------------------------------------------

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


### `known_hosts.tx` — Verifikimi i Identitetit të Serverit
Ruhet automatikisht nga klienti gjatë lidhjes së parë dhe përmban çelësin publik të serverit SSH.

- Ruan public key të serverit për lidhje të ardhshme
- Verifikon identitetin e serverit gjatë handshake-ut
- Zbulon ndryshimet e dyshimta të host key
- Mbron kundër sulmeve Man-in-the-middle attack (MITM)
- Nëse public key i serverit ndryshon papritur, klienti shfaq paralajmërim sigurie dhe ndërpret lidhjen për të parandaluar komunikimin me një server potencialisht të rrezikshem


## Masat e Sigurisë

| Kërcënimi | Mbrojtja |
|-----------|---------|
| Man-in-the-Middle (MITM) | Krahasimi i `known_hosts.txt` + verifikimi i nënshkrimit RSA |
| Përgjimi i të dhënave | Enkriptimi AES-256-CFB pas handshake-it |
| Manipulimi i mesazheve | HMAC-SHA256 me `hmac.compare_digest` (kohë konstante) |
| Çelësa të dobët / Replay | X25519 — çift i ri çelësash për çdo sesion |
| Autentifikim i dobët i serverit | RSA-2048 me mbushje PSS |


## Trajtimi i Gabimeve

| Skenari | Sjellja |
|---------|---------|
| Serveri nuk është duke punuar | Klienti logon `Connection refused` dhe mbyllet |
| MITM i zbuluar | Paralajmërim i qartë + ndërprerje e lidhjes |
| Nënshkrim invalid | Klienti logon gabimin dhe mbyll lidhjen |
| Dështim HMAC | Serveri refuzon mesazhin |
| Gabim i papritur | `finally` mbyll socket-in pastër në të dyja palët |


Shembull i Plotë i Ekzekutimit
------------------------------------------------------------------------------------------------------
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


Struktura e Projektit
------------------------------------------------------------------------------------------------------

```
SiguriTeDhenave_Projekti2_Grupi11/
│
├── server.py          
├── client.py          
├── crypto_utils.py   
├── known_hosts.txt    
├── .gitignore        
└── README.md          
```

Si të Ekzekutohet Projekti
------------------------------------------------------------------------------------------------------
1.	Klono repository-n:
 	git clone  https://github.com/ferideuka-git/ssh-handshake-grupi11.git
2.	Hape folderin e projektit ne PyCharm (Cfarëdo editori që përkrah gjuhën programuese Python)
3.	Instalo librarin cryptography: pip install cryptography
4.	Ekzekuto serverin : python server.py
5.	Ekzekuto klientin: python client.py













