"""
EUDR / FAO 산림 기준 설정
"""

# FAO 산림 정의
FAO_CANOPY_COVER_THRESHOLD = 0.10  # 10%
FAO_MIN_AREA_HA = 0.5              # 0.5 hectares
FAO_MIN_TREE_HEIGHT_M = 5.0        # 5 meters

# EUDR 기준일
EUDR_CUTOFF_DATE = "2020-12-31"

# NDVI 임계값
NDVI_FOREST_THRESHOLD = 0.4        # 이상이면 숲
NDVI_NON_FOREST_THRESHOLD = 0.2    # 이하면 비숲

# Sentinel-2 밴드 인덱스 (Level-2A)
BAND_RED = "B04"   # 665nm
BAND_NIR = "B08"   # 842nm

# ETH Global Canopy Height Map URL (Copernicus에서 접근)
CANOPY_HEIGHT_DATASET = "eth_global_canopy_height_2020"

# Sentinel-2 버퍼 (GPS 포인트 주변 탐색 영역)
BUFFER_METERS = 500  # 500m 반경
