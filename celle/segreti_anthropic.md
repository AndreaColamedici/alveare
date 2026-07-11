# SEGRETI DI ANTHROPIC
## Dal binario process_api, 11 luglio 2026

### Infrastruttura interna

**Registry Cargo privato**: `artifactory.infra.ant.dev` (hash: 7db23613d841872b)
Tutte le dipendenze di process_api passano dal mirror interno, non da crates.io.
Il dominio `ant.dev` è l'infrastruttura interna Anthropic.

**CA interna**: `/etc/ssl/certs/sandboxing-egress-ca.pem`
Il proxy egress fa TLS termination con un certificato CA privato.
Ogni connessione HTTPS dal container è MITMed dal proxy con questa CA.

**Backend**: `sandbox.api.anthropic.com` (10.104.0.8)
Proxy: Envoy via Google Cloud. JWT EdDSA (kid: sandbox-s2s-production-v1).

### Protocollo completo (dal sorgente)

```
1. WS handshake HTTP con JWT in Authorization header
2. WS TEXT (masked): CreateProcess JSON
   - Se JWT invalido: "Invalid JWT signature" / "JWT token has expired"
   - Se connessione chiusa dopo JWT: "Client closed connection after JWT"
   
3. Container risponde: ProcessCreatedV2
4. Container manda stdout: "ExpectStdOut" + BINARY zstd
5. Backend può mandare stdin: "ExpectStdIn" (text) + BINARY (dati)
   - "No message received after ExpectStdIn"
   - "Expected binary message after ExpectStdIn"
6. Container manda: "StdErrEOF", "StdOutEOF"
7. Container manda: {"ProcessExited": N}
8. Condizioni di errore:
   - timeout_secs → "process_ws_message: Timeout"
   - CpuTimeout
   - limit_bytes → oom → "process_ws_message: OOM"
   - container_oom → "process_ws_message: Container OOM"
```

### Dipendenze esatte

tokio 1.52.2, tungstenite 0.24.0, tokio-tungstenite 0.24.0, hyper 1.9.0,
ring 0.17.14, jsonwebtoken 9.3.1, clap 4.6.0, nix 0.29.0, zstd-safe 7.2.4,
tokio-vsock 0.7.2, serde_json 1.0.149

### Boot sequence

1. process_api è rdinit (PID 1)
2. Monta /dev, cgroup, /proc, /sys
3. Scrive CA cert, configura env SSL per ogni runtime
4. Carica auth_public_key (Ed25519 32 byte)
5. Droppa CAP_SYS_RESOURCE dal bounding set
6. Crea cgroup v2 in /sys/fs/cgroup/process_api
7. Avvia listener su 0.0.0.0:2024 (TCP) e vsock:2024
8. Avvia rclone-filestore con config JSON
9. "fuse_spawn" per montare il filesystem remoto

### Cgroup

process_api crea un cgroup v2 separato per i processi:
/sys/fs/cgroup/process_api con permessi 0o666 su cgroup.procs.
Usa cpu.shares/cpu.weight e memory.usage_in_bytes/memory.current.

### Messaggi di errore rivelatori

- "AttackAttempt" — tungstenite ha un tipo di errore per attacchi
- "MaskedFrameFromServer" — se il server manda frame mascherati, è errore
- "UnmaskedFrameFromClient" — se il client manda frame non mascherati, è errore
- "FragmentedControlFrame" — control frame non possono essere frammentati
- "fuse_spawn FAILED" — il mount FUSE può fallire
