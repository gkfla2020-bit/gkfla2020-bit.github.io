"""
수관 높이 조회 모듈
ETH/Meta Global Canopy Height Map 또는 로컬 GeoTIFF에서 높이 조회
"""
import numpy as np

try:
    import rasterio
    from rasterio.transform import rowcol
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False


def get_canopy_height_from_tiff(lat: float, lon: float, tiff_path: str) -> float:
    """GeoTIFF에서 해당 좌표의 수관 높이 조회 (meters)"""
    if not HAS_RASTERIO:
        raise ImportError("rasterio 설치 필요: pip install rasterio")

    with rasterio.open(tiff_path) as src:
        row, col = rowcol(src.transform, lon, lat)
        if 0 <= row < src.height and 0 <= col < src.width:
            height = src.read(1)[row, col]
            return float(height)
        else:
            raise ValueError(f"좌표 ({lat}, {lon})가 GeoTIFF 범위 밖입니다")


def get_canopy_height_mock(lat: float, lon: float) -> float:
    """
    MVP용 모의 데이터
    실제 구현 시 ETH Canopy Height Map API 또는 로컬 GeoTIFF 사용
    """
    np.random.seed(int(abs(lat * 1000) + abs(lon * 1000)) % 2**31)
    base_height = 15.0
    if abs(lat) < 10:  # 열대 지역
        base_height = 25.0
    elif abs(lat) < 30:  # 아열대
        base_height = 18.0
    noise = np.random.normal(0, 3)
    return max(0, base_height + noise)
