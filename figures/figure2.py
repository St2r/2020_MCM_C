import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math


def get_data(category: str):
    data_path = '../data/{0}.tsv'.format(category)
    return pd.read_csv(data_path, sep='\t')


def get_product_parent(src: pd.DataFrame) -> tuple:
    src = src['product_parent'].value_counts()
    _product_parent = list()
    _review_count = list()
    for p, r in src.iteritems():
        _product_parent.append(p)
        _review_count.append(r)
    return _product_parent, _review_count


def get_star_mean(src: pd.DataFrame, product_parents: list) -> list:
    src = src[['star_rating', 'product_parent']]
    out = list()
    for p in product_parents:
        temp = src[src['product_parent'] == p]
        out.append(temp['star_rating'].mean())
    return out


def get_weight(vine: str, helpful_votes: int, total_votes: int) -> float:
    out = 1.
    if vine == 'Y' or vine == 'y':
        out *= 3
    out *= math.log2(2 + total_votes)
    b = 1 + (2 * helpful_votes - total_votes) / 5
    if b < 0.5:
        b = 0.5
    if b > 2:
        b = 2
    return out * b


def get_star_weight(src: pd.DataFrame, product_parents: list) -> list:
    src = src[['star_rating', 'product_parent', 'vine', 'helpful_votes', 'total_votes']]
    out = list()
    for p in product_parents:
        temp = src[src['product_parent'] == p]
        total = 0
        total_weight = 0
        for _, i in temp.iterrows():
            weight = get_weight(i['vine'], i['helpful_votes'], i['total_votes'])
            total += i['star_rating'] * weight
            total_weight += weight
        out.append(total / total_weight)
    return out


category = 'microwave'
data = get_data(category)

product_parent, review_count = get_product_parent(data)
star_rating = get_star_weight(data, product_parent)

product_parent = product_parent[:10]
review_count = review_count[:10]
star_rating = star_rating[:10]

ind = np.arange(len(product_parent))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
rects1 = ax1.bar(ind - width / 2, review_count, width,
                 color='SkyBlue', label='Count')
rects2 = ax2.bar(ind + width / 2, star_rating, width,
                 color='IndianRed', label='Star')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Count')
ax1.set_title('Stars vs Reviews: microwave - weighted')
ax1.set_xticks(ind)
# ax.set_xticklabels(('G1', 'G2', 'G3', '...', 'G5'))
fig.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                 '{}'.format(height), ha=ha[xpos], va='bottom')


# autolabel(rects1, "left")
# autolabel(rects2, "right")

plt.show()
