"""
실제 Sentinel-2 데이터 접근
Copernicus Data Space Ecosystem (CDSE) API 사용

무료 계정 필요: https://dataspace.copernicus.eu/
API 키 없이도 STAC 카탈로그 검색 + 일부 다운로드 가능
"""
import requests
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any


CDSE_STAC_URL = "https://catalogue.dataspace.copernicus.eu/stac"
CDSE_OData_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1"


def search_sentinel2_scenes(lat: float, lon: float, date_start: str,
                            date_end: str, cloud_cover_max: int = 20) -> list:
    """
    Sentinel-2 장면 검색 (STAC API)

    Args:
        lat, lon: 중심 좌표
        date_start: 시작일 (YYYY-MM-DD)
        date_end: 종료일 (YYYY-MM-DD)
        cloud_cover_max: 최대 구름 비율 (%)
    """
    bbox = [lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05]

    params = {
        "collections": ["SENTINEL-2"],
        "bbox": bbox,
        "datetime": f"{date_start}T00:00:00Z/{date_end}T23:59:59Z",
        "limit": 10,
        "filter": f"eo:cloud_cover<{cloud_cover_max}",
    }

    search_url = f"{CDSE_STAC_URL}/search"
    response = requests.post(search_url, json=params, timeout=30)

    if response.status_code == 200:
        data = response.json()
        return data.get("features", [])
    else:
        print(f"  STAC 검색 실패: {response.status_code}")
        return []


def get_ndvi_from_copernicus_wms(lat: float, lon: float,
                                  date: str, buffer_deg: float = 0.005) -> Optional[np.ndarray]:
    """
    Copernicus WMS를 통해 NDVI 데이터 조회
    인증 없이 접근 가능한 방법
    """
    bbox = f"{lon-buffer_deg},{lat-buffer_deg},{lon+buffer_deg},{lat+buffer_deg}"
    width = 100
    height = 100

    wms_url = (
        "https://sh.dataspace.copernicus.eu/ogc/wms/"
        "?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap"
        f"&BBOX={bbox}"
        f"&CRS=EPSG:4326"
        f"&WIDTH={width}&HEIGHT={height}"
        f"&LAYERS=NDVI"
        f"&FORMAT=image/tiff"
        f"&TIME={date}"
    )
    try:
        response = requests.get(wms_url, timeout=30)
        if response.status_code == 200 and len(response.content) > 1000:
            return np.frombuffer(response.content, dtype=np.float32).reshape(height, width)
    except Exception as e:
        print(f"  WMS 접근 실패: {e}")
    return None


def get_sentinel2_ndvi_openeo(lat: float, lon: float, date_start: str,
                               date_end: str) -> Optional[float]:
    """
    OpenEO 기반 NDVI 평균값 조회 (무료 티어)
    https://openeo.dataspace.copernicus.eu/
    """
    bbox = {
        "west": lon - 0.005,
        "south": lat - 0.005,
        "east": lon + 0.005,
        "north": lat + 0.005,
    }

    process_graph = {
        "loadcollection1": {
            "process_id": "load_collection",
            "arguments": {
                "id": "SENTINEL2_L2A",
                "spatial_extent": bbox,
                "temporal_extent": [date_start, date_end],
                "bands": ["B04", "B08"]
            }
        },
        "ndvi1": {
            "process_id": "ndvi",
            "arguments": {
                "data": {"from_node": "loadcollection1"},
                "nir": "B08",
                "red": "B04"
            }
        },
        "reduce1": {
            "process_id": "reduce_dimension",
            "arguments": {
                "data": {"from_node": "ndvi1"},
                "dimension": "t",
                "reducer": {"process_graph": {"mean1": {"process_id": "mean", "arguments": {"data": {"from_parameter": "data"}}, "result": True}}}
            },
            "result": True
        }
    }

    try:
        url = "https://openeo.dataspace.copernicus.eu/openeo/1.2/result"
        response = requests.post(url, json={"process": {"process_graph": process_graph}}, timeout=60)
        if response.status_code == 200:
            return float(np.frombuffer(response.content, dtype=np.float32).mean())
    except Exception as e:
        print(f"  OpenEO 접근 실패: {e}")
    return None
