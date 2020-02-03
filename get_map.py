from pyecharts import options as opts
from pyecharts.charts import Map
import pandas as pd


df = pd.read_csv('2020-02-03 17.34.csv')
df = df.iloc[1:] # 去掉第一行

provinces = list(df.地区)
confirmedCount = list(df.确诊)


def map_base() -> Map:
    c = (
        Map()
        .add("确诊数", [list(z) for z in zip(provinces,confirmedCount)], "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="疫情确诊数地图"),
            visualmap_opts=opts.VisualMapOpts(max_=500))
    )
    return c


def create_map():
    c = map_base()
    c.render('疫情确诊数地图.html')