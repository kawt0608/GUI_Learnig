クラス仕様
Stopwatchクラス
継承: QMainWindow

属性:

timer: ストップウォッチ計測用 QTimer。
current_time_timer: 現在時刻表示用 QTimer。
elapsed_time: 計測された経過時間をミリ秒で保持。
lap_times: 記録されたラップタイムリスト。
is_mini_mode: ミニモードの状態フラグ。
メソッド:

__init__: UIの初期化とタイマーセットアップ。
initMainUI: UIウィジェットの作成および配置。
start_timer: ストップウォッチ開始。
stop_timer: ストップウォッチ停止。
reset_timer: ストップウォッチリセット。
record_lap: ラップタイムの記録およびリストに追加。
toggle_mini_mode: ミニモードとフルモードの切り替え。
update_timer: 経過時間を100msごとに更新。
update_current_time: 1秒ごとに現在時刻を更新。
elapsed_time_format: ミリ秒時間を MM:SS.C形式にフォーマット。
save_lap_times: ラップタイムをファイルとして保存。
resizeEvent: ウィンドウのリサイズに応じてフォントサイズを動的に調整。
