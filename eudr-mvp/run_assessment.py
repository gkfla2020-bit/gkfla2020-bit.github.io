"""
EUDR 산림 파괴 판정 실행
========================
대상 회사: Example Palm Oil Trading Co.
공급지: 인도네시아 (칼리만탄, 리아우, 수마트라)

실행: python3 run_assessment.py
"""
import json
from datetime import datetime
from company_assessment import (
    SUPPLY_CHAIN_PLOTS,
    assess_single_plot,
    generate_report,
    PlotAssessment,
)


def main():
    print("=" * 70)
    print("  EUDR 산림 파괴 판정 시스템 v1.0")
    print("  EU Deforestation Regulation (2023/1115) Compliance Check")
    print("=" * 70)
    print(f"  실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  대상 회사: Example Palm Oil Trading Co.")
    print(f"  품목: Palm Oil (팜유)")
    print(f"  공급지: {len(SUPPLY_CHAIN_PLOTS)}개 플롯 (인도네시아)")
    print(f"  기준일: 2020-12-31 (EUDR Cutoff)")
    print(f"  기준: FAO 산림 정의 (피복도≥10%, 높이≥5m, 면적≥0.5ha)")
    print("=" * 70)

    # 각 플롯 판정
    assessments = []
    for plot in SUPPLY_CHAIN_PLOTS:
        result = assess_single_plot(plot)
        assessments.append(result)

    # 보고서 생성
    report = generate_report(assessments)

    # 보고서 출력
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + "  EUDR COMPLIANCE REPORT".center(68) + "║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  회사: {report['company']:<58}║")
    print(f"║  품목: {report['commodity']:<58}║")
    print(f"║  기준: {report['standard']:<58}║")
    print(f"║  보고일: {report['report_date']:<56}║")
    print("╠" + "═" * 68 + "╣")
    print("║" + "  요약".center(66) + "║")
    print("╠" + "═" * 68 + "╣")

    s = report["summary"]
    print(f"║  총 플롯 수:     {s['total_plots']:<50}║")
    print(f"║  준수:           {s['compliant']:<50}║")
    print(f"║  비준수:         {s['non_compliant']:<50}║")
    print(f"║  준수율:         {s['compliance_rate']:<50}║")
    print(f"║  총 면적:        {s['total_area_ha']:.0f} ha{'':<44}║")
    print(f"║  파괴 면적:      {s['deforested_area_ha']:.0f} ha{'':<44}║")

    print("╠" + "═" * 68 + "╣")
    print("║" + "  위험도 분포".center(64) + "║")
    print("╠" + "═" * 68 + "╣")
    r = report["risk_distribution"]
    print(f"║  LOW:      {r['LOW']:<57}║")
    print(f"║  MEDIUM:   {r['MEDIUM']:<57}║")
    print(f"║  HIGH:     {r['HIGH']:<57}║")
    print(f"║  CRITICAL: {r['CRITICAL']:<57}║")

    print("╠" + "═" * 68 + "╣")
    print("║" + "  플롯별 상세".center(64) + "║")
    print("╠" + "═" * 68 + "╣")

    for p in report["plots"]:
        status = "✅" if p["eudr_compliant"] else "❌"
        print(f"║  {status} {p['id']} | {p['name'][:30]:<30} | {p['risk_level']:<8} ║")
        print(f"║    좌표: {p['coordinates']:<20} 면적: {p['area_ha']:.0f}ha{'':<18}║")
        print(f"║    피복도: {p['baseline_cover']} → {p['current_cover']} ({p['cover_change']}){'':<20}║")
        print(f"║    사유: {p['reason'][:55]:<55}║")
        print("║" + " " * 68 + "║")

    print("╚" + "═" * 68 + "╝")

    # JSON 보고서 저장
    output_path = "eudr_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  JSON 보고서 저장: {output_path}")

    # 비준수 플롯 경고
    non_compliant = [p for p in report["plots"] if not p["eudr_compliant"]]
    if non_compliant:
        print("\n  ⚠️  경고: 다음 플롯에서 산림 파괴가 감지되었습니다:")
        for p in non_compliant:
            print(f"     - {p['id']} ({p['name']}): {p['reason']}")
        print("\n  → 해당 공급지의 제품은 EU 시장 반입 불가")
        print("  → Due Diligence Statement 제출 시 비준수로 보고 필요")

    return report


if __name__ == "__main__":
    main()
