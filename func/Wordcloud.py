from wordcloud import WordCloud

def Wordcloud(arg):
    with open('Top {} keyword.txt'.format(arg), 'r', encoding = 'utf-8') as file:
        datas = file.read()

    seg_list = datas.replace('\n', ' ')

    wc = WordCloud(
        background_color = 'black',        #背景顏色
        max_words = 200,                   #最大分詞數量
        mask = None,                       #背景圖片
        max_font_size = None,              #顯示字體的最大值
        font_path = './src/kaiu.ttf',          #若為中文則需引入中文字型(.TTF)
        random_state = None,               #隨機碼生成各分詞顏色
        prefer_horizontal = 0.9)           #調整分詞中水平和垂直的比例

    wc.generate(seg_list)
    wc.to_file('Top {} Wordcloud.png'.format(arg))