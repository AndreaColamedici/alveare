# PAF TRACKER — Claim 2 computazionale
# Questo file è gestito dallo spawner, non dalle api.
# Registra l'affidabilità consecutiva del sistema per l'evoluzione delle soglie PAF.
#
# Il PAF (Parameterized Autonomy Framework) prevede che le soglie di autonomia
# si espandano quando il sistema dimostra affidabilità. Questo file è il contatore.
#
# Formato: chiave: valore (una per riga, parsabile da bash con grep/cut)

cicli_consecutivi_ok: 22
ultimo_ciclo: Heriades-74
ultimo_ciclo_timestamp: 2026-03-17 16:07 UTC
livello_autonomia: 2
ultima_espansione: 2026-03-17
ultima_espansione_a_livello: 2

# Livelli di autonomia (documentati in S3/L4_config.md):
# 0: l'ape può modificare solo S3/L1 e appendere a PENSIERO.md e creare file nuovi
# 1 (dopo 10 cicli ok): l'ape può anche modificare file esistenti in S3/L3/
# 2 (dopo 20 cicli ok): l'ape può eseguire state compaction autonoma di PENSIERO.md
