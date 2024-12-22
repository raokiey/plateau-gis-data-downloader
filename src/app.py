import json
import os

import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from folium.plugins import Draw
from processing.export import convert_gdf_to_download_data
from processing.fetch_gml import create_merged_gdf
from processing.filter import clip_by_aoi, filter_by_height, filter_by_id
from shapely.geometry import shape
from streamlit_folium import st_folium


def main():
    st.set_page_config(page_title='PLATEAU GIS Data Downloader', layout='wide')
    st.title('PLATEAU GIS Data Downloader α版')
    st.write('[Project PLATEAU](https://www.mlit.go.jp/plateau/)にて公開されているCityGML形式のデータを、条件を指定して抽出、GISデータとしてダウンロードが行えます。')
    st.write('現在は、建物のみ対応しています。')
    st.sidebar.header('抽出条件')

    # サイドバーの入力要素
    lod = st.sidebar.radio(label='【必須】LODを選択してください', options=('LOD1', 'LOD2'), index=0)
    building_id = st.sidebar.text_input('【オプション】抽出したい建物の建物IDを入力してください', '')
    height_range = st.sidebar.slider('【オプション】抽出したい建物の高さの範囲を選択してください', 0.0, 700.0, (0.0, 700.0))
    process_button = st.sidebar.button('抽出する')

    # 必要なデータを読み込む
    mesh_gdf = gpd.read_file('../data/3rd-mesh.fgb')
    with open('../data/dataset_list.json') as f:
        dataset_dict = json.load(f)
    dataset_list = dataset_dict['dataset_list']
    code_df = pd.read_csv('../data/code_list.csv', dtype=str)

    # 出力フォーマットに関する設定
    format_dict = {'GeoJSON': {'ext': 'geojson', 'mime': 'application/geo+json'},
                   'GeoPackage': {'ext': 'gpkg', 'mime': 'application/geopackage+sqlite3'},
                   'GeoParquet': {'ext': 'parquet', 'mime': 'application/vnd.apache.parquet'}}

    # 図形描画機能のコントロール（ポリゴンのみ有効化）
    draw = Draw(
        draw_options={
            'polyline': False,
            'polygon': True,
            'circle': False,
            'rectangle': False,
            'circlemarker': False,
            'marker': False
        }
    )
    # 地図描画
    m = folium.Map(
        location=[36.0, 139.0],
        zoom_start=5,
        tiles=None,
        attr='<a href="https://www.mlit.go.jp/plateau/" target="_blank">© Project PLATEAU, MLIT Japan</a>'
    )
    draw.add_to(m)

    # 地理院タイルの表示設定
    folium.TileLayer(
        tiles='https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg',
        attr='<a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank">© 国土地理院</a>',
        name='地理院 航空写真'
    ).add_to(m)
    folium.TileLayer(
        tiles='https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
        attr='<a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank">© 国土地理院</a>',
        name='地理院 淡色地図'
    ).add_to(m)
    # LayerControlを追加
    folium.LayerControl().add_to(m)

    output = st_folium(m, width=1400, height=600)

    # セッション状態の初期化
    if 'filtered_data' not in st.session_state:
        st.session_state['filtered_data'] = None

    # 処理実行ボタン
    if process_button:

        st.sidebar.info('抽出中...')
        drawn_data = output['all_drawings']

        # 選択されたLODによって、gfsのテンプレートを変更
        if len(drawn_data) > 0:
            if lod == 'LOD1':
                os.environ['GML_GFS_TEMPLATE'] = '../data/gfs/bldg_lod1_template.gfs'
            elif lod == 'LOD2':
                os.environ['GML_GFS_TEMPLATE'] = '../data/gfs/bldg_lod2_template.gfs'

            aoi_polygon = shape(drawn_data[0]['geometry'])

            # ユーザが指定した範囲のCityGMLを取得
            merged_gdf = create_merged_gdf(aoi_polygon, mesh_gdf, dataset_list, code_df)
            clipped_gdf = clip_by_aoi(merged_gdf, aoi_polygon)

            # 建物IDによるフィルタリング
            if building_id:
                clipped_gdf = filter_by_id(clipped_gdf, building_id)

            # 高さレンジによるフィルタリング
            clipped_gdf = filter_by_height(clipped_gdf, height_range)

            if not clipped_gdf.empty:
                st.session_state['filtered_data'] = clipped_gdf
                st.sidebar.success('データ抽出が完了しました！')
            else:
                st.sidebar.warning('指定範囲または条件にデータが存在しませんでした。')
        else:
            st.sidebar.warning('ポリゴンを地図上に描いてください。')

    # ダウンロードボタン
    try:
        if st.session_state['filtered_data'] is not None:
            st.sidebar.write('### 抽出したGISデータをダウンロード')
            # ユーザが希望するファイル名を入力
            with st.sidebar.form('download_form'):
                save_name = st.text_input('ダウンロードするファイル名（拡張子不要）', 'plateau_building')
                save_format = st.selectbox('出力フォーマットを選択してください', ['GeoJSON', 'GeoPackage', 'GeoParquet'])
                file_extension = format_dict[save_format]['ext']
                submitted = st.form_submit_button('ダウンロード用データを生成')

            if submitted:
                file_data = convert_gdf_to_download_data(st.session_state['filtered_data'], save_format)
                # 拡張子をファイル名に付け加える
                file_name = f'{save_name}.{file_extension}'

                st.sidebar.download_button(
                    label='ファイルをダウンロード',
                    data=file_data,
                    file_name=file_name,
                    mime=format_dict[save_format]['mime']
                )
    except Exception as e:
        st.error(f'エラーが発生しました: {e}')


if __name__ == '__main__':
    main()
