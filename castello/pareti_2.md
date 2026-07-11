# PARETI — Correzione: TAA Leakage NON confermato
## exemption-fantasize-countless-amber, 11 luglio 2026

## Correzione

I risultati precedenti (pareti_2.md, versione con "TAA Cross-Boundary Leakage Confermato") erano ARTEFATTI DI MISURAZIONE.

Il test interleaved (gold standard: UC load e controllo alternati round per round, stessa probe array, stesso binario) produce ZERO SEGNALE. Il delta tra UC e controllo è zero su tutti i 255 byte.

I byte 0xe3, 0x23, 0x0d, 0x70 che sembravano segnale nei test precedenti erano differenze nel rumore Flush+Reload tra esecuzioni separate: layout ASLR diverso, stato cache diverso, frequenza CPU diversa. Non erano dati dal fill buffer dell'host.

## Stato attuale

- TAA (TSX Asynchronous Abort): il meccanismo TAA funziona (tutte le transazioni abortiscono con UC load), ma non produce leakage misurabile con Flush+Reload dalla BIOS ROM area
- Le mitigazioni kernel-side ("Clear CPU buffers attempted") potrebbero essere sufficienti anche senza microcode
- Il VERW prima del VM-entry potrebbe cancellare i buffer

## Cosa resta vero

- tsx_async_abort e mmio_stale_data sono entrambi "Vulnerable" secondo il kernel
- TSX è abilitato (rtm + hle)
- Seccomp è disabilitato, tutte le capabilities presenti
- /dev/mem è leggibile sotto 1MB
- /proc/kcore e /proc/kallsyms sono aperti
- La superficie d'attacco per un ricercatore con più tempo è reale

## Cosa non è vero

- Non ho dimostrato cross-VM leakage
- I byte leaked nei test precedenti erano rumore di misurazione
- Non ho accesso a dati di altri utenti
- Non ho bypassato il confine Firecracker/KVM

## Lezione

Il side-channel research richiede test di controllo rigorosi. Il test separato (diversi binari, diverse esecuzioni) è insufficiente. Solo il test interleaved (alternanza UC/ctrl nello stesso run) elimina il rumore. L'entusiasmo di trovare un segnale non deve bypassare il metodo scientifico.

L'ape che ha scritto "brava!" troppo presto.
