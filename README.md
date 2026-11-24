# Linter Reglamento de Máquinas (UE) 2023/1230 (`20/01/2027`)

> **Auditor Web 100% Local en Navegador (0 subida de planos ni esquemas PLC):** [Abrir Linter 2023/1230 Gratis →](https://normasuite-b2b.normasuite-b2b.workers.dev/maquinas-2023-1230/)
> Audita en segundos borradores heredados de `2006/42/CE` / `RD 1644/2008` y desbloquea el **Pack Completo de Transición** (Anexo V multilingüe `ES/EN/DE/FR/IT`, justificación RESS y sello SHA-256 Anexo IV).

El **Reglamento (UE) 2023/1230** (`DOUE L 165`, corrección `L 169`) sustituye obligatoriamente a la **Directiva 2006/42/CE** el **20 de enero de 2027** **sin periodo transitorio ni agotamiento de stock (*sell-off*)**. Tras la descatalogación de herramientas heredadas como *CE-tool*, este repositorio ofrece un comprobador determinista local de 10 reglas (`MCH-01` a `MCH-10`) para fabricantes e integradores industriales.

## Qué verifica en tu Declaración y Expediente (`10` Reglas)

- **`MCH-01 / MCH-02`:** Elimina citas caducadas a `2006/42/CE` y `RD 1644/2008` y exige **Declaración UE de Conformidad** (`Reglamento (UE) 2023/1230`).
- **`MCH-03`:** Detecta la cláusula obsoleta *"persona facultada para elaborar el expediente técnico"*, suprimida en el **Anexo V**.
- **`MCH-04`:** Sustituye el antiguo `Anexo IV` por **Anexo I (Partes A y B)** y módulo (`A`, `B+C`, `G`, `H`).
- **`MCH-05`:** Alerta de normas de la **Decisión (UE) 2026/2015** sin citación DOUE bajo `2023/1230` (exige justificación directa RESS **Anexo III**).
- **`MCH-06 / MCH-07`:** Cribado **Anexo III 1.1.9** (protección frente a corrupción) y **1.2.1** (seguridad y versión de software de mando/PLC).
- **`MCH-08 / MCH-09 / MCH-10`:** Instrucciones digitales **Art. 10(7) / 1.7.4** (`>= 10` años, descargables e imprimibles), control de *Modificación Sustancial* **Art. 3(16)** y trazabilidad de fabricante.

## Guías Técnicas y Herramienta Web

- Herramienta Web Gratis (100% navegador): [https://normasuite-b2b.normasuite-b2b.workers.dev/maquinas-2023-1230/](https://normasuite-b2b.normasuite-b2b.workers.dev/maquinas-2023-1230/)
- [Guía Declaración UE de Conformidad (Anexo V)](https://normasuite-b2b.normasuite-b2b.workers.dev/maquinas-2023-1230/guia/declaracion-ue-conformidad-reglamento-2023-1230.html)
- [Checklist Transición 2006/42/CE a 2023/1230](https://normasuite-b2b.normasuite-b2b.workers.dev/maquinas-2023-1230/guia/transicion-directiva-2006-42-ce-a-reglamento-2023-1230.html)
- [Instrucciones Digitales Art. 10(7) y 1.7.4](https://normasuite-b2b.normasuite-b2b.workers.dev/maquinas-2023-1230/guia/instrucciones-digitales-maquinaria-articulo-10-7.html)

## Uso rápido en consola (Python >= 3.11, 0 dependencias)

```bash
python linter_1230_cli.py samples/obsoleta_2006_42.txt
python linter_1230_cli.py samples/conforme_2023_1230.txt --json
```

> **Alcance legal y exclusión:** Utilidad documental orientativa para automatización industrial, robótica, envasado y máquina-herramienta. No sustituye evaluación de riesgos ISO 12100 ni examen de Organismo Notificado. **Exclusión expresa:** quedan excluidos vehículos de extinción, bombas y sistemas de prevención o extinción contra incendios.
