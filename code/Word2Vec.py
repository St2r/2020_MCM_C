from gensim.models import Word2Vec


# 1.文本读入和处理

# （2） 对句子进行分割：将文章分割为句子列表
# （4）分词word tokenize：将句子分割为单词列表
corpus = [['I', 'am']]
# 2.构建词向量：W2V
# 128维的词向量
w2v_model = Word2Vec(corpus, size=128, window=5, min_count=3, workers=4)

# 3. 处理我们的training data，把源数据变成一个长长的x，好让LSTM学会predict下一个单词
raw_input = [item for sublist in corpus for item in sublist]
# 将corpus的二维变为一维['sexes', 'similar', '.','family', 'hirundinidae', '.',...]

text_stream = []

vocab = w2v_model.wv.vocab  # 字典dict：获取词向量中每个单词

# 将raw_input中在w2v_model词向量中的单词添加到text_stream
for word in raw_input:
    if word in vocab:
        text_stream.append(word)