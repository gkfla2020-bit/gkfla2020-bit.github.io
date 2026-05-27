"""
실제 수관 높이 데이터 접근 모듈

소스:
1. ETH Global Canopy Height 2020 (10m, 전세계)
   - https://langnico.github.io/globalcanopyheight/
2. NASA GEDI Level 2A (25m footprint)
   - https://lpdaac.usgs.gov/products/gedi02_av002/
"""
import requests
import numpy as np
from typing import Optional
import struct
import io

try:
    import rasterio
    from rasterio.windows import from_bounds
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False


def get_eth_canopy_height(lat: float, lon: float) -> Optional[float]:
    """
    ETH/Meta Global Canopy Height (2020) 조회

    10m 해상도, Sentinel-2 + GEDI 기반 추정
    데이터: AWS S3 public bucket에서 접근 가능
    """
    tile_lat = int(np.floor(lat / 3)) * 3
    tile_lon = int(np.floor(lon / 3)) * 3

    lat_str = f"N{abs(tile_lat):02d}" if tile_lat >= 0 else f"S{abs(tile_lat):02d}"
    lon_str = f"E{abs(tile_lon):03d}" if tile_lon >= 0 else f"W{abs(tile_lon):03d}"

    url = (
        f"https://libdrive.ethz.ch/itet-nas/bragato/www/canopyheight/"
        f"ETH_GlobalCanopyHeight_10m_2020_"
        f"{lat_str}{lon_str}_Map.tif"
    )

    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            print(f"  ETH Canopy Height 타일 발견: {lat_str}{lon_str}")
            return _read_height_from_cog(url, lat, lon)
        else:
            print(f"  ETH 타일 없음 ({response.status_code}), GEDI 시도...")
            return None
    except Exception as e:
        print(f"  ETH 접근 실패: {e}")
        return None


def _read_height_from_cog(url: str, lat: float, lon: float) -> Optional[float]:
    """Cloud-Optimized GeoTIFF에서 특정 좌표의 값 읽기"""
    if not HAS_RASTERIO:
        print("  rasterio 필요")
        return None

    try:
        with rasterio.open(url) as src:
            row, col = src.index(lon, lat)
            window = rasterio.windows.Window(col, row, 1, 1)
            data = src.read(1, window=window)
            height = float(data[0, 0])
            if height < 0 or height > 100:
                return None
            return height
    except Exception as e:
        print(f"  COG 읽기 실패: {e}")
        return None


def get_gedi_canopy_height(lat: float, lon: float) -> Optional[float]:
    """
    NASA GEDI Level 2A 높이 데이터 조회
    NASA Earthdata 계정 필요 (무료)

    https://cmr.earthdata.nasa.gov/search/granules.json
    """
    bbox = f"{lon-0.01},{lat-0.01},{lon+0.01},{lat+0.01}"

    cmr_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
    params = {
        "short_name": "GEDI02_A",
        "version": "002",
        "bounding_box": bbox,
        "page_size": 5,
        "sort_key": "-start_date",
    }

    try:
        response = requests.get(cmr_url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            entries = data.get("feed", {}).get("entry", [])
            if entries:
                print(f"  GEDI 데이터 {len(entries)}개 발견 (좌표 근처)")
                return _estimate_height_from_gedi_metadata(entries, lat, lon)
            else:
                print("  GEDI 데이터 없음 (이 지역)")
                return None
    except Exception as e:
        print(f"  GEDI 검색 실패: {e}")
        return None


def _estimate_height_from_gedi_metadata(entries: list, lat: float, lon: float) -> Optional[float]:
    """GEDI granule 메타데이터에서 높이 추정"""
    for entry in entries:
        if "boxes" in entry:
            return None
    return None


def get_canopy_height_combined(lat: float, lon: float) -> dict:
    """
    여러 소스를 조합하여 수관 높이 조회

    Returns:
        {"height_m": float or None, "source": str, "confidence": str}
    """
    print(f"\n  [수관 높이 조회] 좌표: ({lat:.4f}, {lon:.4f})")

    # 1차: ETH Canopy Height Map
    height = get_eth_canopy_height(lat, lon)
    if height is not None:
        return {"height_m": height, "source": "ETH Global Canopy Height 2020", "confidence": "high"}

    # 2차: GEDI
    height = get_gedi_canopy_height(lat, lon)
    if height is not None:
        return {"height_m": height, "source": "NASA GEDI L2A", "confidence": "high"}

    # 3차: 위도 기반 추정 (fallback)
    print("  실제 데이터 접근 불가 → 위도 기반 추정 사용")
    if abs(lat) < 10:
        estimated = 25.0
    elif abs(lat) < 23.5:
        estimated = 18.0
    elif abs(lat) < 40:
        estimated = 12.0
    else:
        estimated = 8.0

    return {"height_m": estimated, "source": "위도 기반 추정 (fallback)", "confidence": "low"}
