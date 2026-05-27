"""
Sentinel-2 데이터 접근 모듈
실제 구현 시 Copernicus Data Space API 사용
MVP에서는 모의 데이터 생성
"""
import numpy as np
from typing import Tuple


def download_sentinel2(lat: float, lon: float, date: str,
                       buffer_m: int = 500) -> Tuple[np.ndarray, np.ndarray]:
    """
    Sentinel-2 RED, NIR 밴드 다운로드

    실제 구현 시:
    - Copernicus Data Space Ecosystem API
    - 또는 sentinelhub 라이브러리
    - 또는 Google Earth Engine

    Returns:
        (red_band, nir_band): 각각 numpy array
    """
    raise NotImplementedError(
        "실제 Sentinel-2 데이터 다운로드는 API 키 필요. "
        "generate_mock_sentinel2()를 사용하세요."
    )


def generate_mock_sentinel2(lat: float, lon: float,
                            forest_ratio: float = 0.7,
                            size: int = 50) -> Tuple[np.ndarray, np.ndarray]:
    """
    MVP용 모의 Sentinel-2 데이터 생성

    Args:
        lat, lon: 좌표
        forest_ratio: 숲 비율 (0~1)
        size: 이미지 크기 (size x size 픽셀)

    Returns:
        (red_band, nir_band)
    """
    seed = int(abs(lat * 100) + abs(lon * 100)) % 2**31
    np.random.seed(seed)

    red = np.zeros((size, size), dtype=np.float32)
    nir = np.zeros((size, size), dtype=np.float32)

    n_forest_pixels = int(size * size * forest_ratio)
    forest_mask = np.zeros(size * size, dtype=bool)
    forest_mask[:n_forest_pixels] = True
    np.random.shuffle(forest_mask)
    forest_mask = forest_mask.reshape(size, size)

    # 숲: 높은 NIR, 낮은 RED (NDVI > 0.4)
    red[forest_mask] = np.random.uniform(200, 600, n_forest_pixels)
    nir[forest_mask] = np.random.uniform(2000, 4000, n_forest_pixels)

    # 비숲: 비슷한 NIR/RED (NDVI < 0.2)
    n_non_forest = size * size - n_forest_pixels
    red[~forest_mask] = np.random.uniform(800, 1500, n_non_forest)
    nir[~forest_mask] = np.random.uniform(900, 1600, n_non_forest)

    return red, nir


def generate_deforested_sentinel2(lat: float, lon: float,
                                  original_forest_ratio: float = 0.7,
                                  deforestation_ratio: float = 0.3,
                                  size: int = 50) -> Tuple[np.ndarray, np.ndarray]:
    """
    산림 파괴 후 상태의 모의 데이터 생성
    """
    new_forest_ratio = original_forest_ratio * (1 - deforestation_ratio)
    return generate_mock_sentinel2(lat + 0.001, lon + 0.001,
                                   forest_ratio=new_forest_ratio, size=size)
