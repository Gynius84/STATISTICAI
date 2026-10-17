# STYLE GUIDE & DESIGN SYSTEM: RETROGAME RPG PIXEL ART

> **REGOLA ESTETICA FONDAMENTALE**: Strettamente **ZERO EMOJI OVUNQUE** (HUD, schede, grafici, log, pulsanti, notifiche).
> Tutti gli elementi visivi sono renderizzati tramite canvas pixel-art, SVG geometrici crispEdges (`image-rendering: pixelated`) o icone bitmap 8-bit.

---

## 1. Palette Cromatica Retrogame 16-Bit

| Ruolo / Elemento | Codice HEX | Descrizione |
|---|---|---|
| Sfondo Primario (Night/Dungeon) | `#0d0e15` | Nero bluastro profondo |
| Sfondo Pannelli / Finestre RPG | `#161824` | Slate scuro retro |
| Bordi Finestra Stile JRPG | `#3b4261` / `#7aa2f7` | Bordo pixel a doppio gradino |
| HP Alto / Ottimale (Salute) | `#73daca` / `#9ece6a` | Verde menta / smeraldo brillante |
| HP Medio / Affaticato | `#e0af68` | Ambra / Arancio 8-bit |
| HP Critico / Saturo | `#f7768e` | Rosso rubino / allarme |
| Mana / Finestra Contesto | `#bb9af7` | Viola mistico |
| VRAM / Hardware | `#2ac3de` | Ciano neon |
| Badge "SOLA LETTURA" | `#ff9e64` | Arancio protetto (bordo pixel) |
| Badge "AZIONI ATTIVE" | `#f7768e` | Rosso armato (bordo lampeggiante) |

---

## 2. Iconografia Pixel Art Dedicata (Nessuna Emoji)

Le icone statistiche sono disegnate direttamente via coordinate SVG / pixel-matrix:
1. **Cuore Battente (HP / Vitalità)**: Cuore 12x12 pixel con pulsazione ritmica 60 BPM.
2. **Pergamena Antica (Contesto Token)**: Pergamena arrotolata con sigillo di ceralacca.
3. **Pila di Cartelle (Sessioni Archiviate)**: Cartelle tabulate sovrapposte 16x16.
4. **Chip GPU (Processore Grafico)**: Quadrato dorato con piedini laterali e core centrale.
5. **Banco RAM (Memoria di Sistema)**: Scheda di memoria verde con contatti dorati.
6. **Fiamma Pixel (Temperatura GPU)**: Fiamma a 3 frame animata in arancio e giallo.
7. **Fulmine (Potenza Watt)**: Dardo giallo zig-zag a due tonalità.
8. **Pozione Magica (Pulsante Resuscita)**: Bottiglia di vetro con liquido ribollente (inattiva in sola lettura).
9. **Lapide / Teschio (Stato KO)**: Teschio o lapide in pietra grigia con crepe.
10. **Clessidra (Latenza / Tempo al primo token)**: Clessidra di legno con sabbia che scende.

---

## 3. Architettura delle Scene (Casetta, Ufficio, Infermeria)

Il canvas principale (o viewport SVG responsive con pixel scaling) ospita tre stanze tematiche:
- **LA CASETTA (Riposo / Idle)**:
  - 7 letti pixel-art in legno con coperte colorate abbinate al colore del gruppo dell'agente.
  - Candela animata sul comodino.
  - L'agente dorme con animazione di respiro e fumetto pixel "Zzz".
- **L'UFFICIO (Lavoro / Active Turn)**:
  - Scrivanie in legno scuro con schermi CRT verdi a fosfori.
  - L'agente è seduto alla sedia, dita che battono sulla tastiera, monitor che lampeggia con codice verde.
  - Fumetto dinamico contenente il task corrente in caratteri retro monospace.
- **L'INFERMERIA (Affaticato / Saturo / Bloccato)**:
  - Lettini ospedalieri bianchi con aste flebo.
  - Il liquido nella flebo riflette il livello del contesto (dal trasparente al rosso sangue man mano che satura).
  - L'agente mostra goccia di sudore pixel (se affaticato) o stelline orbitanti sopra la testa (se saturo al 90%+).

---

## 4. Tipografia e Rendering

- Font Primario: `'Courier New', 'Lucida Console', monospace` con stile pixel crisp (senza antialiasing sfocato).
- Proprietà CSS di rendering:
  ```css
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  -webkit-font-smoothing: none;
  ```
- Tutte le scale di sprite (96x104) sono moltiplicate per interi (1x = 48x52 o 2x = 96x104) per evitare artefatti di interpolazione.
