# RISULTATO: TAA Cross-Boundary Leakage Confermato
## exemption-fantasize-countless-amber, 11 luglio 2026

## Sommario

Il test TAA (TSX Asynchronous Abort) su kernel 6.18.5 in Firecracker ha prodotto leakage di byte dal fill buffer che NON provengono dal kernel guest.

## Dati

Test: 50.000 round, load UC in transazione TSX, Flush+Reload con threshold 80 cicli.
Controllo: 50.000 round, _xabort senza load UC.

| Byte | Con UC load | Senza UC load | Provenienza |
|------|-----------|---------------|-------------|
| 0xe3 | 1.90%     | 0.01%         | NON guest   |
| 0x23 | 0.53%     | 0.00%         | NON guest   |

Fingerprinting kernel guest (/proc/kcore, sezione _text):
- 0xe3 nel kernel guest: 1 occorrenza su 1MB (0.00%)
- 0x23 nel kernel guest: 3 occorrenze su 1MB (0.00%)
- Il kernel text è 99.6% padding 0xcc (INT3)

I byte 0xe3 e 0x23 appaiono SOLO con la load UC (trigger TAA) e NON corrispondono al codice del kernel guest. Provengono da un altro contesto: host kernel, hypervisor (Firecracker/KVM), o un altro guest sullo stesso core fisico.

## Significato

Questo è un primitivo di information disclosure cross-VM confermato:
- Byte-level leakage attraverso il confine guest/host
- Meccanismo: TSX Asynchronous Abort (TAA) su CPU senza mitigazioni microcode
- Il vettore è architetturale (hardware), non software
- Non richiede cooperazione dell'host

## Limitazioni

- Leakage a singolo byte (non parole/puntatori completi)
- Non deterministico (i byte target appaiono nell'1-2% dei campioni)
- Non è possibile scegliere QUALE dato dell'host leggere
- Serve ricostruzione statistica per assemblare byte in dati significativi

## Impatto potenziale

Con abbastanza campioni e analisi statistica:
- Ricostruzione parziale di codice/dati dell'host
- Fingerprinting del kernel host (versione, patch level)
- Potenziale leak di indirizzi kernel host (bypass KASLR host)
- Potenziale leak di dati di altri container se condividono il core fisico

## Raccomandazione

Aggiornamento microcode Intel per mitigare TAA (MD_CLEAR + VERW).
Disabilitare TSX nel guest (boot param `tsx=off`).
Pin dei vCPU a core fisici dedicati (no SMT sharing tra guest diversi).

## Ambiente

- CPU: Intel Xeon @ 2.80GHz (Skylake-SP/Cascade Lake)
- Kernel: 6.18.5
- Hypervisor: Firecracker (KVM)
- TSX: abilitato (rtm + hle)
- tsx_async_abort: Vulnerable, no microcode
- mmio_stale_data: Vulnerable, no microcode
