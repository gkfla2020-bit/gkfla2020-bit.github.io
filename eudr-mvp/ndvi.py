"""
NDVI 계산 모듈
Sentinel-2 밴드 데이터로 식생지수 계산
"""
import numpy as np
from config import NDVI_FOREST_THRESHOLD, NDVI_NON_FOREST_THRESHOLD


def calculate_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """NDVI = (NIR - RED) / (NIR + RED)"""
    nir = nir.astype(np.float64)
    red = red.astype(np.float64)
    denominator = nir + red
    ndvi = np.where(denominator == 0, 0, (nir - red) / denominator)
    return ndvi


def classify_forest(ndvi: np.ndarray) -> np.ndarray:
    """NDVI 값으로 숲/비숲 분류 (0=비숲, 1=숲, 2=모호)"""
    result = np.full_like(ndvi, 2, dtype=np.int8)
    result[ndvi >= NDVI_FOREST_THRESHOLD] = 1
    result[ndvi <= NDVI_NON_FOREST_THRESHOLD] = 0
    return result


def estimate_canopy_cover(ndvi: np.ndarray, area_pixels: int) -> float:
    """수관 피복도 추정 (숲 픽셀 비율)"""
    forest_pixels = np.sum(ndvi >= NDVI_FOREST_THRESHOLD)
    return float(forest_pixels / area_pixels) if area_pixels > 0 else 0.0
