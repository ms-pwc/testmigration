#!/usr/bin/env python3
"""Convert JMeter JTL (XML or CSV) into a JUnit XML report."""

import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_jtl(input_path: Path):
    text = input_path.read_text(encoding="utf-8", errors="ignore").lstrip()
    if not text:
        return []

    if text.startswith("<"):
        root = ET.fromstring(text)
        rows = []
        for sample in root.iter():
            if sample.tag not in {"sample", "httpSample"}:
                continue
            rows.append(
                {
                    "label": sample.attrib.get("lb", "unnamed"),
                    "success": sample.attrib.get("s", "true") == "true",
                    "message": sample.attrib.get("rm", ""),
                    "code": sample.attrib.get("rc", ""),
                    "time_ms": sample.attrib.get("t", "0"),
                }
            )
        return rows

    rows = []
    with input_path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            success_raw = (row.get("success") or row.get("s") or "true").strip().lower()
            rows.append(
                {
                    "label": row.get("label") or row.get("lb") or "unnamed",
                    "success": success_raw == "true",
                    "message": row.get("responseMessage") or row.get("rm") or "",
                    "code": row.get("responseCode") or row.get("rc") or "",
                    "time_ms": row.get("elapsed") or row.get("t") or "0",
                }
            )
    return rows


def build_junit(samples, output_path: Path):
    tests = len(samples)
    failures = sum(1 for s in samples if not s["success"])

    testsuite = ET.Element(
        "testsuite",
        {
            "name": "JMeter",
            "tests": str(tests),
            "failures": str(failures),
            "errors": "0",
            "skipped": "0",
        },
    )

    for idx, sample in enumerate(samples, start=1):
        testcase = ET.SubElement(
            testsuite,
            "testcase",
            {
                "classname": "jmeter",
                "name": f"{idx}. {sample['label']}",
                "time": str(float(sample["time_ms"]) / 1000.0 if str(sample["time_ms"]).strip() else 0),
            },
        )
        if not sample["success"]:
            ET.SubElement(
                testcase,
                "failure",
                {
                    "message": f"{sample['code']} {sample['message']}".strip(),
                    "type": "AssertionError",
                },
            ).text = f"JMeter sample failed: {sample['label']}"

    testsuites = ET.Element("testsuites")
    testsuites.append(testsuite)

    tree = ET.ElementTree(testsuites)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def main(argv):
    if len(argv) != 3:
        print("Usage: python scripts/jtl_junit_converter.py <input.jtl> <output.xml>")
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    if not input_path.exists():
        print(f"Input JTL file not found: {input_path}")
        return 2

    samples = parse_jtl(input_path)
    if not samples:
        # Emit a valid but empty test suite to keep reporter step stable.
        build_junit([], output_path)
        return 0

    build_junit(samples, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
