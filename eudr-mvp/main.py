"""
EUDR 산림 파괴 판정 MVP
GPS 좌표 입력 → EUDR 준수 여부 출력
"""
import numpy as np
from config import BUFFER_METERS, FAO_MIN_AREA_HA
from ndvi import calculate_ndvi, estimate_canopy_cover
from canopy_height import get_canopy_height_mock
from sentinel_data import generate_mock_sentinel2, generate_deforested_sentinel2
from eudr_judge import assess_forest, judge_eudr, EUDRVerdict


def analyze_location(lat: float, lon: float,
                     deforestation_ratio: float = 0.0) -> EUDRVerdict:
    """
    GPS 좌표에 대한 EUDR 판정 수행

    Args:
        lat: 위도
        lon: 경도
        deforestation_ratio: 시뮬레이션용 산림 파괴 비율 (0~1)

    Returns:
        EUDRVerdict 결과
    """
    # 1. 기준일(2020.12.31) Sentinel-2 데이터
    red_baseline, nir_baseline = generate_mock_sentinel2(lat, lon, forest_ratio=0.7)
    ndvi_baseline = calculate_ndvi(nir_baseline, red_baseline)
    cover_baseline = estimate_canopy_cover(ndvi_baseline, ndvi_baseline.size)

    # 2. 현재 시점 데이터
    if deforestation_ratio > 0:
        red_current, nir_current = generate_deforested_sentinel2(
            lat, lon, original_forest_ratio=0.7,
            deforestation_ratio=deforestation_ratio
        )
    else:
        red_current, nir_current = generate_mock_sentinel2(lat, lon, forest_ratio=0.7)
    ndvi_current = calculate_ndvi(nir_current, red_current)
    cover_current = estimate_canopy_cover(ndvi_current, ndvi_current.size)

    # 3. 수관 높이 조회
    height = get_canopy_height_mock(lat, lon)

    # 4. 면적 추정 (500m 버퍼 기준)
    area_ha = (BUFFER_METERS * 2) ** 2 / 10000  # 100ha (1km x 1km)

    # 5. FAO 기준 산림 평가
    baseline = assess_forest(cover_baseline, height, area_ha)
    current = assess_forest(cover_current, height * (1 - deforestation_ratio * 0.5), area_ha)

    # 6. EUDR 판정
    return judge_eudr(baseline, current)


def print_verdict(lat: float, lon: float, verdict: EUDRVerdict):
    """판정 결과 출력"""
    print("=" * 60)
    print(f"  EUDR 산림 파괴 판정 결과")
    print(f"  좌표: ({lat}, {lon})")
    print("=" * 60)
    print()

    print("[ 기준일 2020.12.31 ]")
    print(f"  수관 피복도: {verdict.baseline.canopy_cover*100:.1f}%")
    print(f"  수관 높이:   {verdict.baseline.tree_height_m:.1f}m")
    print(f"  면적:        {verdict.baseline.area_ha:.1f}ha")
    print(f"  FAO 산림:    {'예' if verdict.baseline.is_forest else '아니오'}")
    print()

    print("[ 현재 시점 ]")
    print(f"  수관 피복도: {verdict.current.canopy_cover*100:.1f}%")
    print(f"  수관 높이:   {verdict.current.tree_height_m:.1f}m")
    print(f"  면적:        {verdict.current.area_ha:.1f}ha")
    print(f"  FAO 산림:    {'예' if verdict.current.is_forest else '아니오'}")
    print()

    print("[ 변화 분석 ]")
    print(f"  피복도 변화: {verdict.canopy_cover_change*100:+.1f}%")
    print(f"  산림 파괴:   {'감지됨' if verdict.deforestation_detected else '미감지'}")
    print()

    if verdict.compliant:
        print("  ✅ EUDR 준수 (Deforestation-Free)")
    else:
        print("  ❌ EUDR 비준수 (Deforestation Detected)")
    print(f"  사유: {verdict.reason}")
    print("=" * 60)


if __name__ == "__main__":
    print("\n[시나리오 1] 브라질 아마존 - 산림 보존 지역")
    verdict1 = analyze_location(-3.4653, -62.2159, deforestation_ratio=0.0)
    print_verdict(-3.4653, -62.2159, verdict1)

    print("\n\n[시나리오 2] 인도네시아 - 팜유 플랜테이션 전환 (30% 파괴)")
    verdict2 = analyze_location(1.5, 110.0, deforestation_ratio=0.3)
    print_verdict(1.5, 110.0, verdict2)

    print("\n\n[시나리오 3] 코트디부아르 - 심각한 산림 파괴 (60%)")
    verdict3 = analyze_location(6.8, -5.3, deforestation_ratio=0.6)
    print_verdict(6.8, -5.3, verdict3)

    print("\n\n[시나리오 4] 사하라 사막 - 원래 산림 아님")
    verdict4 = analyze_location(25.0, 10.0, deforestation_ratio=0.0)
    # 사막이니까 forest_ratio를 낮게 설정
    from sentinel_data import generate_mock_sentinel2
    # 재실행 with low forest ratio
    red, nir = generate_mock_sentinel2(25.0, 10.0, forest_ratio=0.05)
    from ndvi import calculate_ndvi, estimate_canopy_cover
    from canopy_height import get_canopy_height_mock
    from eudr_judge import assess_forest, judge_eudr

    ndvi = calculate_ndvi(nir, red)
    cover = estimate_canopy_cover(ndvi, ndvi.size)
    height = get_canopy_height_mock(25.0, 10.0)
    baseline = assess_forest(cover, 2.0, 100.0)  # 높이 2m → 산림 아님
    current = assess_forest(cover, 2.0, 100.0)
    verdict4 = judge_eudr(baseline, current)
    print_verdict(25.0, 10.0, verdict4)
