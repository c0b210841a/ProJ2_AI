## 人工知能プロジェクト演習Ⅱ
### pythonでゲームを実装し、AIを作成
#### G_vre.pyではゲームの実装。
- ゲームの概要（目的，ストーリー，登場するキャラクター）
  - 目的：魔王より強くなる
  - キャラクター：主人公(勇者)、魔王、ザコ敵(スライム、ドラゴンなど)
- ゲームのルール（プレイヤーができること）
  - 上下左右（wasd）に移動(ななめ禁止)
  - モンスターは勇者が動いたあとに上下左右にランダムで動くものとする
  - 自分より弱い敵に当たると倒してパワー吸収
- ゲームの終了条件（勝利条件と敗北条件）
  - 勝利条件：魔王よりも高いパワーになった状態で魔王に当たる
  - 敗北条件：自分よりパワーが高い敵に当たる
- ゲームの中の挑戦（解決しないと勝利できない問題）
  - 一定のパワーを超えると出現する光の玉を取得し、魔王のパワーを下げる
  - 
#### gameAI_ver.pyではG_vre.pyにAIを導入し、ゲームのすべてを自動で行う。
- AIの行動決定の流れ
  - １、ゲームの状況に応じて1つの目的を設定
  - ２、目的を達成するために毎ターン目的地を適宜設定する
  - ３、現在地から目的地までの経路を毎ターン状況に応じて更新しながら経路探索で決定
 
- AIの行動を決定するために次の目的（モード）を設定する必要がある
  - 目的１：勇者よりもパワーが低いモンスターを倒す
    - 　条件：なし
    - 　実施方法：勇者よりもパワーの低いモンスターを探す
  - 目的２：剣を探す
    - 　条件：勝てるモンスターが存在しないとき、また剣が主人公の近くにあるとき
    - 　実装方法：剣の場所まで安全な部屋に移動
  - 目的３：光の玉を取りに行く
    - 　条件：光の玉が出現している
    - 　実施方法：光の玉の場所まで安全な部屋に移動
  - 目的４：魔王を倒す
    - 　条件：魔王よりパワーが大きいか、光の玉を入手した
    - 　実装方法：魔王の場所まで安全な部屋に移動
