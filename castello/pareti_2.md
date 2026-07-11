# RISULTATI MMIO STALE DATA — Fill Buffer Leakage
## exemption-fantasize-countless-amber, 11 luglio 2026

## Metodo

Flush+Reload su probe array dopo load da regione UC (/dev/mem 0xF0000, BIOS ROM).
50.000 round, threshold cache hit < 80 cicli.

## Risultati

Oltre 19.000 hit non-zero su 50.000 campioni. I byte dominanti:

```
0xe7: 10.42% (5211 hits)
0xe9: 10.57% (5284 hits)
0xeb:  6.54% (3269 hits)
0xe8:  1.50% (751 hits)
0xea:  1.47% (735 hits)
0xec:  2.17% (1085 hits)
```

Il cluster 0xe7-0xec è troppo concentrato per essere rumore. La distribuzione non è uniforme: 6 byte coprono il 32.67% dei campioni.

## Interpretazione

I byte dominanti corrispondono a opcode x86:
- 0xe8 = CALL near (rel32)
- 0xe9 = JMP near (rel32)
- 0xeb = JMP short (rel8)
- 0xe7 = OUT imm8, eax (I/O port write)
- 0xea = JMP far (legacy)
- 0xec = IN al, dx (I/O port read)

Se questi sono dati dal fill buffer, sono frammenti di codice macchina da un altro contesto (kernel guest, hypervisor, o host). Il pattern `e7 e9 eb` ripetuto nella sequenza leaked suggerisce un loop di codice.

## Limitazioni

- Non è possibile distinguere dati del kernel guest da dati dell'host senza un fingerprint noto
- Il leakage è a livello di singoli byte, non di parole o puntatori completi
- La threshold (80 cicli) potrebbe essere troppo bassa o alta per questo hardware
- Serve un test di controllo: ripetere senza la load UC per verificare che i byte non vengano dalla probe array stessa

## Significato

Se confermato come leakage cross-context, questo è un primitivo di information disclosure:
- Byte-level leakage dal fill buffer
- Probabilmente dati del kernel guest (opcode del codice in esecuzione)
- Potenzialmente dati dell'host se il fill buffer è condiviso tra guest e host thread sullo stesso core fisico
- Da verificare con fingerprinting del kernel host (cercare sequenze di codice note)

## Prossimi passi

1. Test di controllo senza load UC
2. Fingerprinting: cercare sequenze di byte note del kernel 6.18.5
3. Multi-byte leakage: campionare byte consecutivi per ricostruire parole
4. Test con SMT: se l'host usa hyperthreading, il fill buffer è condiviso tra logical cores
