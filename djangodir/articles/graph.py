import copy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import japanize_matplotlib
import numpy as np
import base64
from io import BytesIO

COLOR_BLUE = 'winter_r'
COLOR_RED = 'autumn_r'

DISPLAY_COUNT = 30

def gen_scatter_plot(x, y, word_list, color_map, title):
    """各プロットにテキストを付加した散布図を作成する。"""
    plt.switch_backend("AGG")
    plt.figure(figsize=(7.5, 4))
    plt.scatter(x=x[:DISPLAY_COUNT], y=y[:DISPLAY_COUNT], s=30,
                c=y[:DISPLAY_COUNT], norm=colors.Normalize(0.0,y[0]), cmap=color_map)
    plt.xlabel('IDF（逆文書頻度）')
    plt.ylabel('TF-IDF（単語出現頻度ー逆文書頻度）')
    plt.colorbar()
    plt.title(title)
    plt.tight_layout()
    #各単語とプロットをx,y座標で紐付ける
    #プロットが重なるときはyの値を修正する
    # corrected_y = correct_overlapped_coods(x, y)
    # for i, word in enumerate(word_list[:DISPLAY_COUNT]):
    #     plt.text(x[i], corrected_y[i], word)
    plot_texts = [plt.text(x[i], y[i], word) for i, word in enumerate(word_list[:DISPLAY_COUNT])]
    
    graph = output_png(plt)
    return graph

def output_png(plot):
    """引数として受け取ったmatplotlib.pyplotを画像として出力する"""
    buffer = BytesIO()
    #作成したグラフをbufferに保存
    plot.savefig(buffer, format="png")
    #bufferの先頭に移動
    buffer.seek(0)
    #byteとしてグラフのデータを取得
    byte_image   = buffer.getvalue()
    #base64でエンコード
    base64_image = base64.b64encode(byte_image)
    image = base64_image.decode("utf-8")
    buffer.close()
    return image

def correct_overlapped_coods(x_list, y_list):
    """グラフ内の文字が重なっている場合に見やすい位置に文字の座標を修正する"""
    limit = 0.05
    correct_step = 0.01
    overlapped_indices = []
    corrected_y_list = copy.copy(y_list)
    for i in range(len(x_list)-1):
        if abs(x_list[i] - x_list[i+1]) < limit:
            if x_list[i] <= x_list[i+1]:
                corrected_y_list[i] = corrected_y_list[i] + correct_step
            if x_list[i+1] <= x_list[i]:
                corrected_y_list[i+1] = corrected_y_list[i+1] + correct_step
    return corrected_y_list