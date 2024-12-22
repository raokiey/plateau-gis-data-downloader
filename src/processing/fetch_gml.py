from typing import List

import fiona
import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import Polygon

API_URL = 'https://www.geospatial.jp/ckan/api/3'


def get_gml_url(resource_id: str, mesh_code: int) -> str:
    """リソースIDと3次メッシュコードをもとに対象のCityGMLのURLを取得

    Args:
        resource_id (str): 対象のCityGMLのリソースID
        mesh_code (int): 対象のCityGMLが整備されているメッシュコード

    Returns:
        str: 取得したCityGMLのURL
    """
    # G空間情報センターのAPIを用いて、CityGMLのダウンロードURLを取得
    response = requests.get(f'{API_URL}/action/resource_show', params={'id': resource_id})
    data = response.json()

    if not data['success']:
        raise Exception('Failed to download CityGML.')

    zipped_dataset_url = data['result']['url']

    gml_url = f'/vsizip//vsicurl/{zipped_dataset_url}/udx/bldg/{mesh_code}_bldg_6697_op.gml'

    return gml_url


def create_merged_gdf(aoi_geometry: Polygon,
                      mesh_gdf: gpd.GeoDataFrame,
                      dataset_list: List,
                      code_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """ユーザが欲しい範囲のCityGMLを3次メッシュ単位で取得し、マージしたGeoDataFrameを作成

    Args:
        aoi_geometry (Polygon): ユーザが欲しい範囲 (aoi)
        mesh_gdf (gpd.GeoDataFrame): 3次メッシュのGeoDataFrame
        dataset_list (List): G空間情報にあるCityGMLのデータセットリスト
        code_df (pd.Dataframe): 市区町村コードと3次メッシュコードの対応表

    Returns:
        gpd.GeoDataFrame: _description_
    """
    # ユーザが描いたポリゴンと交差する3次メッシュコードを求める
    intersect_index = mesh_gdf.sindex.query(aoi_geometry, predicate='intersects', sort=True)
    mesh_code_list = mesh_gdf.loc[intersect_index]['code'].to_list()

    # メッシュコードから対象の市区町村コードを求める
    filtered_df = code_df[code_df['mesh_code'].isin(mesh_code_list)].reset_index(drop=True)

    # 対象のCityGMLが含まれているG空間情報センターのデータセットのリソースIDを求める
    resource_id_list = []
    for lgcode in filtered_df['lg_code']:
        for item in dataset_list:
            if (str(lgcode) in item['dataset_id']) and ('latest' in item):
                resource_id_list.append(item['citygml'])

    # リソースIDと3次メッシュコードから対象のCityGMLのURLを生成、CityGMLを読み込みマージ
    merged_citygml_gdf = gpd.GeoDataFrame([])
    for resource_id, mesh_code in zip(resource_id_list, mesh_code_list):
        citygml_url = get_gml_url(resource_id, mesh_code)
        try:
            citygml_gdf = gpd.read_file(citygml_url, driver='GML', engine='fiona')
        except fiona.errors.DriverError as e: # 自治体の範囲ではあるが、その3次メッシュが整備されていない場合はスキップ
            continue
        merged_citygml_gdf = pd.concat([merged_citygml_gdf, citygml_gdf])

    return merged_citygml_gdf
