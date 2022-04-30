import matplotlib.pyplot as plt
from unittest import TestCase
from unittest.mock import patch
from djangodir.articles.plots import *

class PlotsTest(TestCase):

    @patch('djangodir.articles.plots.plt')
    def test_gen_scatter_plot(self, mock_plt):
        """gen_scatter_plot()が座標、プロットテキスト、色指定、グラフタイトル
        を引数として受け取り、各種設定メソッドが呼ばれた上で、
        str型の画像を返すことを確認する。
        """
        x = [3.5, 2.05, 2.01]
        y = [0.02, 0.05, 0.32]
        text = ['test1', 'test2', 'test3', ]
        color_map = 'winter'
        title = 'test_title'
        image = gen_scatter_plot(x, y, text, color_map, title)
        
        mock_plt.xlabel.assert_called_once_with('IDF（逆文書頻度）')
        mock_plt.ylabel.assert_called_once_with('TF-IDF（単語出現頻度ー逆文書頻度）')
        mock_plt.colorbar.assert_called_once_with()
        mock_plt.title.assert_called_once_with(title)
        mock_plt.tight_layout.assert_called_once_with()
    
        #base64でエンコードされた画像(str型)が出力されていることを確認
        self.assertEqual(str, type(image))

    def test_output_png_with_plot_arg_returns_str_image(self):
        """output_png()がmatplotlib.pyplotを引数として受け取り
        str型の画像を返すことを確認する
        """
        plt.scatter([3.5, 2.05], [0.02, 0.05])
        image = output_png(plt)

        self.assertEqual(str, type(image))
