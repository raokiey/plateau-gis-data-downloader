# このフォルダに格納されているデータについて  
データ取得に必要なデータが格納されています。  
**個人が公開されている情報を加工して作成したものです。間違いがある可能性もあります。**  

---

それぞれのデータの出典は、以下の通りです。

- **3次メッシュ（3rd-mesh.fgb）**
    日本全国の3次メッシュポリゴンです。  
    [環境省自然環境局生物多様性センター「全国標準地域メッシュ２次メッシュ（約10㎞四方）」](https://www.geospatial.jp/ckan/dataset/biodic-mesh/resource/8cc999b5-82d9-46e0-8eb8-f4fc7ab2612e)を加工して作成。  
<br/>

- **3次メッシュコードと市区町村コードの対応表（code_list.csv）**  
    日本産業規格「JIS X 0410 地域メッシュコード」にて定められている基準地域メッシュコードと[市区町村コード](https://www.soumu.go.jp/denshijiti/code.html)の対応表です。  
    [総務省統計局「市区町村別メッシュ・コード一覧」](https://www.stat.go.jp/data/mesh/m_itiran.html)を加工して作成。
<br/>

- **G空間情報センターにて公開されているPLATEAUのデータセット情報（dataset_list.json）**
    G空間情報センターにて公開されているPLATEAUのデータセットのデータセットIDやリソースIDなどの情報が格納されているJSONファイルです。  
    [Project PLATEAUオープンデータ-ファイル命名規則及びフォルダ構成規則 / 6.G空間情報センターAPIを利用したダウンロードリストの取得](https://github.com/Project-PLATEAU/plateau-naming-docs?tab=readme-ov-file#6-g%E7%A9%BA%E9%96%93%E6%83%85%E5%A0%B1%E3%82%BB%E3%83%B3%E3%82%BF%E3%83%BCapi%E3%82%92%E5%88%A9%E7%94%A8%E3%81%97%E3%81%9F%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AE%E5%8F%96%E5%BE%97)や[PlateauKit + PlateauLabのlist.py](https://github.com/ozekik/plateaukit/blob/master/plateaukit/download/list.py)をもとに、独自作成。
<br/>

- **gfs（gfs/）**  
    建物データを読み込む時に、LOD要素を指定するためのテンプレート。  
    現在は、LOD1とLOD2のみ対応しています。  
    [この記事](https://qiita.com/tkhrmeme/items/bdacd335494c125f3496)を参考に、独自作成。
