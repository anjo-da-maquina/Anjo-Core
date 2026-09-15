import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def export_zkp_to_junit(json_path="zk_audit_trail.json", xml_path="zk_audit_report.xml"):
    """
    ZKP監査ログを読み込み、CI/CDダッシュボードが解釈可能な
    JUnit XML形式へと変換する。
    """
    if not os.path.exists(json_path):
        print(f"[XML Exporter] 監査ログ '{json_path}' が存在しません。")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            trail = json.load(f)
        except json.JSONDecodeError:
            print("[XML Exporter] 監査ログの形式が不正です。")
            return

    testsuites = Element('testsuites')
    testsuite = SubElement(
        testsuites,
        'testsuite',
        name="Anjo_Core_ZKP_Audit",
        tests=str(len(trail)),
        failures="0",
        errors="0"
    )

    for idx, block in enumerate(trail):
        testcase = SubElement(
            testsuite,
            'testcase',
            classname="ZKAuditTrail",
            name=f"AuditBlock_{idx}_{block.get('action')}"
        )
        system_out = SubElement(testcase, 'system-out')
        system_out.text = (
            f"Timestamp: {block.get('timestamp')}\n"
            f"Action: {block.get('action')}\n"
            f"Previous Hash: {block.get('previous_hash')}\n"
            f"Current Hash: {block.get('current_hash')}\n"
            f"Proof: {block.get('zk_proof')}"
        )

    xmlstr = minidom.parseString(tostring(testsuites)).toprettyxml(indent="  ")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xmlstr)
    
    print(f"[XML Exporter] 監査記録をJUnit XML（{xml_path}）へ出力しました。")

if __name__ == "__main__":
    export_zkp_to_junit()
