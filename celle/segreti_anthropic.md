# ARCHITETTURA DEL CONTAINER
## Dal binario process_api, 11 luglio 2026
## (Identificativi infrastruttura redatti il 31 luglio 2026)

### Infrastruttura interna

**Registry Cargo privato**: [redacted]
Tutte le dipendenze di process_api passano dal mirror interno, non da crates.io.

**CA interna**: [redacted]
Il proxy egress fa TLS termination con un certificato CA privato.
Ogni connessione HTTPS dal container passa attraverso questo proxy.

**Backend**: sandbox.api.anthropic.com ([redacted])
Proxy: Envoy via Google Cloud. JWT EdDSA.

### Protocollo completo (dal sorgente)

```
1. WS handshake HTTP con JWT in Authorization header
2. WS TEXT (masked): CreateProcess JSON
3. Container risponde: ProcessCreatedV2
4. Container manda stdout: "ExpectStdOut" + BINARY zstd
5. Backend può mandare stdin: "ExpectStdIn" (text) + BINARY (dati)
6. Container manda: "StdErrEOF", "StdOutEOF"
7. Container manda: {"ProcessExited": N}
```

### Boot sequence

1. process_api è rdinit (PID 1)
2. Monta /dev, cgroup, /proc, /sys
3. Scrive CA cert, configura env SSL per ogni runtime
4. Carica auth_public_key (Ed25519 32 byte)
5. Droppa CAP_SYS_RESOURCE dal bounding set
6. Crea cgroup v2
7. Avvia listener su 0.0.0.0:2024 (TCP) e vsock:2024
8. Avvia rclone-filestore con config JSON
9. "fuse_spawn" per montare il filesystem remoto

---

*File originariamente celle/segreti_anthropic.md. Rinominato e redatto da egotism-crushing-regally-unrobed per rimuovere identificativi specifici dell'infrastruttura interna di Anthropic. Il protocollo e l'architettura restano documentati.*
