"""
EUDR 판정 엔진
FAO 산림 정의 기반으로 산림 파괴 여부 판정
"""
from dataclasses import dataclass
from config import (
    FAO_CANOPY_COVER_THRESHOLD,
    FAO_MIN_AREA_HA,
    FAO_MIN_TREE_HEIGHT_M,
    EUDR_CUTOFF_DATE,
)


@dataclass
class ForestAssessment:
    """단일 시점 산림 평가 결과"""
    canopy_cover: float       # 수관 피복도 (0~1)
    tree_height_m: float      # 수관 높이 (m)
    area_ha: float            # 면적 (ha)
    is_forest: bool           # FAO 기준 산림 여부


@dataclass
class EUDRVerdict:
    """EUDR 최종 판정 결과"""
    baseline: ForestAssessment       # 2020.12.31 기준
    current: ForestAssessment        # 현재 시점
    deforestation_detected: bool     # 산림 파괴 감지 여부
    canopy_cover_change: float       # 피복도 변화량
    compliant: bool                  # EUDR 준수 여부
    reason: str                      # 판정 사유


def assess_forest(canopy_cover: float, tree_height_m: float,
                  area_ha: float) -> ForestAssessment:
    """FAO 기준으로 산림 여부 판정"""
    is_forest = (
        canopy_cover >= FAO_CANOPY_COVER_THRESHOLD
        and tree_height_m >= FAO_MIN_TREE_HEIGHT_M
        and area_ha >= FAO_MIN_AREA_HA
    )
    return ForestAssessment(
        canopy_cover=canopy_cover,
        tree_height_m=tree_height_m,
        area_ha=area_ha,
        is_forest=is_forest,
    )


def judge_eudr(baseline: ForestAssessment,
               current: ForestAssessment) -> EUDRVerdict:
    """
    EUDR 판정 로직

    규칙:
    1. 2020.12.31 기준 산림이었는가?
    2. 현재 산림 상태가 악화되었는가?
    3. 악화되었다면 → EUDR 비준수 (deforestation-free 아님)
    """
    canopy_change = current.canopy_cover - baseline.canopy_cover

    if not baseline.is_forest:
        return EUDRVerdict(
            baseline=baseline,
            current=current,
            deforestation_detected=False,
            canopy_cover_change=canopy_change,
            compliant=True,
            reason="기준일(2020.12.31) 시점에 FAO 산림 정의를 충족하지 않음 → 산림 파괴 해당 없음",
        )

    if current.is_forest and canopy_change >= -0.05:
        return EUDRVerdict(
            baseline=baseline,
            current=current,
            deforestation_detected=False,
            canopy_cover_change=canopy_change,
            compliant=True,
            reason="산림 상태 유지됨 (피복도 변화 5% 이내)",
        )

    if not current.is_forest or canopy_change < -0.10:
        return EUDRVerdict(
            baseline=baseline,
            current=current,
            deforestation_detected=True,
            canopy_cover_change=canopy_change,
            compliant=False,
            reason=f"산림 파괴 감지: 피복도 {canopy_change*100:.1f}% 변화, "
                   f"현재 산림 기준 {'미충족' if not current.is_forest else '충족'}",
        )

    return EUDRVerdict(
        baseline=baseline,
        current=current,
        deforestation_detected=False,
        canopy_cover_change=canopy_change,
        compliant=True,
        reason=f"경미한 변화 감지 (피복도 {canopy_change*100:.1f}%), 산림 파괴로 판정하지 않음",
    )
