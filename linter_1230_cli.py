"""Zero-dependency CLI linter for Transition 2006/42/CE -> Regulation (EU) 2023/1230."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys


@dataclass(frozen=True)
class RuleDef:
    rule_id: str
    severity: str
    weight: int
    legal_ref: str
    title: str
    remediation: str


RULES: tuple[RuleDef, ...] = (
    RuleDef(
        "MCH-01",
        "crítica",
        12,
        "Arts. 51 y 54 Reg. (UE) 2023/1230",
        "Ausencia de referencia vigente a Directiva 2006/42/CE / RD 1644/2008",
        "Sustituye 2006/42/CE (y RD 1644/2008) por el Reglamento (UE) 2023/1230 (sin sell-off tras 19/01/2027).",
    ),
    RuleDef(
        "MCH-02",
        "crítica",
        12,
        "Anexo V Parte A / B Reg. (UE) 2023/1230",
        "Cita expresa al Reglamento (UE) 2023/1230 y Declaración UE",
        "Incluye 'Declaración UE de Conformidad' (no 'CE') citando Reglamento (UE) 2023/1230.",
    ),
    RuleDef(
        "MCH-03",
        "crítica",
        10,
        "Anexo V Reg. (UE) 2023/1230",
        "Supresión de 'persona facultada para elaborar el expediente técnico'",
        "Elimina esa figura suprimida en 2023/1230; usa fabricante y representante autorizado/importador si aplica.",
    ),
    RuleDef(
        "MCH-04",
        "crítica",
        10,
        "Anexo I (Partes A y B) & Art. 25",
        "Clasificación Anexo I Parte A/B y Módulo de Conformidad",
        "Reemplaza 'Anexo IV' por 'Anexo I Parte A / Parte B' e indica el módulo (A, B+C, G o H).",
    ),
    RuleDef(
        "MCH-05",
        "mayor",
        10,
        "Decisión (UE) 2026/2015 & Anexo III RESS",
        "Justificación directa RESS ante vacío de normas armonizadas en DOUE",
        "Documenta justificación directa frente a RESS Anexo III si citas normas heredadas sin citación DOUE bajo 2023/1230.",
    ),
    RuleDef(
        "MCH-06",
        "crítica",
        10,
        "Anexo III punto 1.1.9",
        "Protección frente a corrupción de datos y conexiones (1.1.9)",
        "Acredita protección de hardware/software frente a corrupción accidental o intencionada (Anexo III 1.1.9).",
    ),
    RuleDef(
        "MCH-07",
        "crítica",
        10,
        "Anexo III punto 1.2.1",
        "Resiliencia de sistemas de mando y trazabilidad de software (1.2.1)",
        "Documenta versión de firmware/PLC, historial de seguridad y cumplimiento del punto 1.2.1.",
    ),
    RuleDef(
        "MCH-08",
        "mayor",
        10,
        "Art. 10(7) y Anexo III punto 1.7.4",
        "Instrucciones digitales accesibles 10 años, descargables e imprimibles",
        "Indica URL accesible >= 10 años, formato imprimible/descargable y copia gratuita en papel bajo demanda.",
    ),
    RuleDef(
        "MCH-09",
        "mayor",
        8,
        "Art. 3(16) y Art. 18",
        "Control de Modificación Sustancial en retrofits e integraciones",
        "Documenta valoración de modificación sustancial (Art. 3(16)).",
    ),
    RuleDef(
        "MCH-10",
        "estructural",
        8,
        "Anexo V Parte A puntos 1-3 y 9",
        "Trazabilidad fabricante (modelo/serie, dirección postal + digital, firma/fecha)",
        "Incluye serie/lote, contacto digital (email/URL) y fecha de emisión.",
    ),
)


def evaluate_rule(rule_id: str, text: str) -> tuple[bool, str]:
    if rule_id == "MCH-01":
        if re.search(r"(2006/42/CE|2006/42/EC|RD\s*1644/2008)", text, re.I) and not re.search(
            r"no aplica|sustituye|derogad|de\s+2006/42/CE\s+a\s+2023/1230", text, re.I
        ):
            return False, "Cita vigente a Directiva 2006/42/CE o RD 1644/2008, derogada el 20/01/2027."
        return True, "Sin dependencia activa de Directiva 2006/42/CE."
    if rule_id == "MCH-02":
        ok = bool(re.search(r"2023/1230", text) and re.search(r"Declaración\s+(UE|EU)\s+de\s+conformidad|EU\s+Declaration\s+of\s+Conformity", text, re.I))
        return (True, "Declaración UE citando 2023/1230.") if ok else (False, "Falta 'Declaración UE de Conformidad' o cita 2023/1230.")
    if rule_id == "MCH-03":
        obs = re.search(r"persona\s+facultada\s+para\s+(elaborar|reunir|compilar)\s+el\s+expediente\s+t[eé]cnico|person\s+authorised\s+to\s+compile\s+the\s+technical\s+file", text, re.I)
        return (False, "Incluye la figura suprimida 'persona facultada para elaborar el expediente técnico'.") if obs else (True, "Sin figura obsoleta de compilador.")
    if rule_id == "MCH-04":
        if re.search(r"Anexo\s+IV\s+(de\s+la\s+Directiva|2006/42)", text, re.I):
            return False, "Cita el antiguo Anexo IV de 2006/42/CE (ahora Anexo I Partes A y B)."
        ok = bool(re.search(r"Anexo\s+I", text, re.I) and re.search(r"M[oó]dulo\s+[ABCGH]|Control\s+interno|Organismo\s+Notificado", text, re.I))
        return (True, "Clasificación Anexo I y módulo presentes.") if ok else (False, "Falta Anexo I y módulo de conformidad.")
    if rule_id == "MCH-05":
        cites_norms = bool(re.search(r"EN\s*(ISO)?\s*\d{4,5}", text, re.I))
        cites_ress = bool(re.search(r"justificaci[oó]n\s+directa|RESS|Anexo\s+III|DOUE|2026/2015", text, re.I))
        if not cites_norms:
            return False, "No declara normas técnicas ni justificación directa Anexo III."
        return (True, "Justificación RESS Anexo III presente.") if cites_ress else (False, "Falta justificación directa RESS ante vacío DOUE.")
    if rule_id == "MCH-06":
        return (True, "Cobertura Anexo III 1.1.9 presente.") if re.search(r"1\.1\.9|corrupci[oó]n", text, re.I) else (False, "Falta evidencia Anexo III 1.1.9.")
    if rule_id == "MCH-07":
        return (True, "Cobertura Anexo III 1.2.1 presente.") if re.search(r"1\.2\.1|firmware|versi[oó]n.*(software|PLC)|mando", text, re.I) else (False, "Falta evidencia Anexo III 1.2.1.")
    if rule_id == "MCH-08":
        ok = bool(re.search(r"(10\(7\)|1\.7\.4|instrucciones\s+digitales)", text, re.I) and re.search(r"10\s*a[ñn]os", text, re.I))
        return (True, "Instrucciones digitales Art. 10(7) (>=10 años) presentes.") if ok else (False, "Falta Art. 10(7) / 1.7.4 (>=10 años).")
    if rule_id == "MCH-09":
        return (True, "Valoración Art. 3(16) presente.") if re.search(r"modificaci[oó]n\s+sustancial|3\(16\)", text, re.I) else (False, "Falta cribado Modificación Sustancial Art. 3(16).")
    if rule_id == "MCH-10":
        ok = bool(re.search(r"serie|lote|serial|n\.º", text, re.I) and re.search(r"@|https?://", text, re.I) and re.search(r"202\d", text))
        return (True, "Trazabilidad completa de fabricante.") if ok else (False, "Falta n.º de serie, contacto digital o fecha.")
    raise KeyError(rule_id)


def audit_text(text: str) -> dict[str, object]:
    earned = 0
    total = sum(r.weight for r in RULES)
    findings = []
    for r in RULES:
        passed, msg = evaluate_rule(r.rule_id, text)
        if passed:
            earned += r.weight
        findings.append({"id": r.rule_id, "passed": passed, "severity": r.severity, "legal_ref": r.legal_ref, "message": msg})
    score = round(100 * earned / total) if total else 0
    return {"score": score, "compliant": all(f["passed"] for f in findings), "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita declaraciones de conformidad 2006/42/CE -> Reg. (UE) 2023/1230.")
    parser.add_argument("file", type=Path, help="Archivo .txt o .md con el borrador de declaración.")
    parser.add_argument("--json", action="store_true", help="Salida estructurada en JSON.")
    args = parser.parse_args()
    if not args.file.exists():
        print(f"Error: no existe {args.file}", file=sys.stderr)
        return 2
    report = audit_text(args.file.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Preparación 2023/1230: {report['score']}% | Conforme: {report['compliant']}")
        for f in report["findings"]:
            tag = "OK" if f["passed"] else f"FALLO ({f['severity']})"
            print(f"  [{tag}] {f['id']} ({f['legal_ref']}): {f['message']}")
    return 0 if report["compliant"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
