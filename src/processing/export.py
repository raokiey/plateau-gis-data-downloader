import os
import tempfile

import geopandas as gpd


def convert_gdf_to_download_data(gdf: gpd.GeoDataFrame, file_format: str) -> bytes:
    """GeoDataFrameをStreamlitからダウンロードできる形式に変換

    Args:
        gdf (gpd.GeoDataFrame): ダウンロード対象のGeoDataFrame
        file_format (str): ダウンロードするファイルのフォーマット

    Returns:
        bytes: ダウンロードするデータ
    """
    if file_format == 'GeoJSON':
        # 文字列としてGeoJSONを取得し、UTF-8バイト列に変換
        return gdf.to_json().encode('utf-8')

    elif file_format == 'GeoPackage':
        # 一時ファイルにGeoPackageとして書き込んで、バイナリで読み取り
        with tempfile.NamedTemporaryFile(suffix='.gpkg', delete=False) as tmp:
            tmp_path = tmp.name
        gdf.to_file(tmp_path, driver='GPKG', layer='bldg')

        with open(tmp_path, 'rb') as f:
            gpkg_bytes = f.read()

        os.remove(tmp_path)
        return gpkg_bytes

    elif file_format == 'GeoParquet':
        # 一時ファイルにGeoParquetとして書き込んで、バイナリで読み取り
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
            tmp_path = tmp.name
        gdf.to_parquet(tmp_path)

        with open(tmp_path, 'rb') as f:
            parquet_bytes = f.read()

        os.remove(tmp_path)
        return parquet_bytes
