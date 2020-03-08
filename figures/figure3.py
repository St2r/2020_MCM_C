import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


def get_data(category: str):
    data_path = '../data/{0}.tsv'.format(category)
    return pd.read_csv(data_path, sep='\t')


def get_date(date_str: str):
    date_list = date_str.split(sep='/')
    return datetime.datetime(int(date_list[2]), int(date_list[0]), int(date_list[1]))


def get_label(review_time: datetime) -> str:
    seasons = {1: '1', 2: '1', 3: '1', 4: '2', 5: '2', 6: '2', 7: '3', 8: '3', 9: '3', 10: '4', 11: '4', 12: '4'}
    return str(review_time.year) + '_' + seasons[review_time.month]


def select_by_date(src: pd.DataFrame) -> (dict, dict):
    src = pd.DataFrame(src[['star_rating', 'review_date']])
    sum = dict()
    count = dict()
    for _, v in src.iterrows():
        label = get_label(get_date(v['review_date']))
        if not label in sum.keys():
            sum[label] = 0
            count[label] = 0
        sum[label] += v['star_rating']
        count[label] += 1
    for k, v in sum.items():
        sum[k] = v / count[k]
    return sum, count


def sort_dict(d: dict) -> (list, list):
    keys = list(d.keys())
    keys.sort()
    return [d[key] for key in keys], keys


def get_values(category: str) -> (list, list, list):
    data = get_data(category)
    average_star, count_per_month = select_by_date(data)
    average_star, _ = sort_dict(average_star)
    count_per_month, labels = sort_dict(count_per_month)
    return average_star, count_per_month, labels


def plot_sub_figure(ax, values, category):
    x = np.arange(len(values[2]))
    xticks = np.arange(0, len(values[2]), 5)
    ax_right = ax.twinx()
    ax.plot(x, values[0], label='average_star', color='SkyBlue')
    ax_right.plot(x, values[1], label='count', color='IndianRed')
    ax.legend(loc='upper left')
    ax_right.legend(loc='lower right')
    ax.set_title('average star and num of review:' + category)
    ax.set_xticks(xticks)
    ax.set_xticklabels(values[2][::5])
    ax.set_ylabel('average star')
    ax2.set_ylabel('count per month')


# date
values_microwave = get_values('microwave')
values_pacifier = get_values('pacifier')
values_hair_dryer = get_values('hair_dryer')

# plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.set_size_inches(12, 8)

plot_sub_figure(ax1, values_microwave, 'microwave')
plot_sub_figure(ax2, values_hair_dryer, 'hair_dryer')
plot_sub_figure(ax3, values_pacifier, 'pacifier')
fig.show()
