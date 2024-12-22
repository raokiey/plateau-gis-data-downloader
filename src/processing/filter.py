from typing import Tuple

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon


def clip_by_aoi(gdf: gpd.GeoDataFrame, aoi_geometry: Polygon) -> gpd.GeoDataFrame:
    """範囲内のポリゴンのみを抽出

    Args:
        gdf (gpd.GeoDataFrame): 3次メッシュ単位のCityGMLをマージしたGeoDataFrame
        aoi_geometry (Polygon): 欲しい範囲のポリゴン

    Returns:
        gpd.GeoDataFrame: 欲しい範囲内のみ抽出したGeoDataFrame
    """
    clipped_gdf = gdf[gdf.within(aoi_geometry)].reset_index(drop=True)
    return clipped_gdf


def filter_by_height(gdf: gpd.GeoDataFrame, height_range: Tuple) -> gpd.GeoDataFrame:
    """高さフィルター

    Args:
        gdf (gpd.GeoDataFrame): 抽出元となるGeoDataFrame
        height_range (tuple): 欲しい高さのレンジ

    Returns:
        gpd.GeoDataFrame: 指定した高さのレンジで抽出したGeoDataFrame
    """
    filtered_height_gdf = gdf.query(f'{height_range[0]} <= measuredHeight <= {height_range[1]}').reset_index(drop=True)

    return filtered_height_gdf


def filter_by_id(gdf: gpd.GeoDataFrame, bldg_id: str) -> gpd.GeoDataFrame:
    """建物IDにて欲しい地物を指定して抽出

    Args:
        gdf (gpd.GeoDataFrame): 抽出元となるGeoDataFrame
        gml_id_list (List): 抽出した地物の建物ID

    Returns:
        gpd.GeoDataFrame: 指定した`gml_id`で抽出したGeoDataFrame
    """
    filtered_id_gdf = gdf.query(f'buildingID == "{bldg_id}"').reset_index(drop=True)

    return filtered_id_gdf
