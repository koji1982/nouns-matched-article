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
    if len(x) == 0:
        return
    plot_count = DISPLAY_COUNT
    if len(x) < DISPLAY_COUNT:
        plot_count = len(x)
    plt.switch_backend("AGG")
    plt.figure(figsize=(7.5, 4))
    plt.scatter(x=x[:plot_count], y=y[:plot_count], s=30,
                c=y[:plot_count], norm=colors.Normalize(0.0,y[0]), cmap=color_map)
    plt.xlabel('IDF（逆文書頻度）')
    plt.ylabel('TF-IDF（単語出現頻度ー逆文書頻度）')
    plt.colorbar()
    plt.title(title)
    plt.tight_layout()
    plt.grid()
    #各単語とプロットをx,y座標で紐付ける
    #各リストは同じ順番に並べられた状態で引数として渡されていることを前提とする
    plot_texts = [plt.text(x[i], y[i], word)
                         for i, word in enumerate(word_list[:plot_count])]
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