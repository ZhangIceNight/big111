# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyecharts import Bar
filename = "/home/student/workspace/58/rent.csv"
def spark_analyse(filename):
    print("开始spark分析")
    # 程序主入口
    spark = SparkSession.builder.master("local").appName("rent_analyse").getOrCreate()
    df = spark.read.csv(filename, header=True)

    # max_list存储各个区的最大值，0为南岗，1为道里，2为江北，3为香坊，4为道外，5为松北,6为平房;同理的mean_list, 以及min_list,approxQuantile中位数
    max_list = [0 for i in range(7)]
    mean_list = [1.2 for i in range(7)]
    min_list = [0 for i in range(7)]
    mid_list = [0 for i in range(7)]
    # 类型转换，十分重要，保证了price列作为int用来比较，否则会用str比较, 同时排除掉一些奇怪的价格，比如写字楼的出租超级贵
    # 或者有人故意标签1元，其实要面议, 还有排除价格标记为面议的
    df = df.filter(df.price != '面议').withColumn("price", df.price.cast(IntegerType()))
    df = df.filter(df.price >= 50).filter(df.price <= 40000)

    mean_list[0] = df.filter(df.area == "南岗").agg({"price": "mean"}).first()['avg(price)']
    mean_list[1] = df.filter(df.area == "道里").agg({"price": "mean"}).first()['avg(price)']
    mean_list[2] = df.filter(df.area == "江北").agg({"price": "mean"}).first()['avg(price)']
    mean_list[3] = df.filter(df.area == "香坊").agg({"price": "mean"}).first()['avg(price)']
    mean_list[4] = df.filter(df.area == "道外").agg({"price": "mean"}).first()['avg(price)']
    mean_list[5] = df.filter(df.area == "松北").agg({"price": "mean"}).first()['avg(price)']
    mean_list[6] = df.filter(df.area == "平房").agg({"price": "mean"}).first()['avg(price)']

    min_list[0] = df.filter(df.area == "南岗").agg({"price": "min"}).first()['min(price)']
    min_list[1] = df.filter(df.area == "道里").agg({"price": "min"}).first()['min(price)']
    min_list[2] = df.filter(df.area == "江北").agg({"price": "min"}).first()['min(price)']
    min_list[3] = df.filter(df.area == "香坊").agg({"price": "min"}).first()['min(price)']
    min_list[4] = df.filter(df.area == "道外").agg({"price": "min"}).first()['min(price)']
    min_list[5] = df.filter(df.area == "松北").agg({"price": "min"}).first()['min(price)']
    min_list[6] = df.filter(df.area == "平房").agg({"price": "min"}).first()['min(price)']

    max_list[0] = df.filter(df.area == "南岗").agg({"price": "max"}).first()['max(price)']
    max_list[1] = df.filter(df.area == "道里").agg({"price": "max"}).first()['max(price)']
    max_list[2] = df.filter(df.area == "江北").agg({"price": "max"}).first()['max(price)']
    max_list[3] = df.filter(df.area == "香坊").agg({"price": "max"}).first()['max(price)']
    max_list[4] = df.filter(df.area == "道外").agg({"price": "max"}).first()['max(price)']
    max_list[5] = df.filter(df.area == "松北").agg({"price": "max"}).first()['max(price)']
    max_list[6] = df.filter(df.area == "平房").agg({"price": "max"}).first()['max(price)']

    # 返回值是一个list，所以在最后加一个[0]
    mid_list[0] = df.filter(df.area == "南岗").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[1] = df.filter(df.area == "道里").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[2] = df.filter(df.area == "江北").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[3] = df.filter(df.area == "香坊").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[4] = df.filter(df.area == "道外").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[5] = df.filter(df.area == "松北").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[6] = df.filter(df.area == "平房").approxQuantile("price", [0.5], 0.01)[0]

    all_list = []
    all_list.append(min_list)
    all_list.append(max_list)
    all_list.append(mean_list)
    all_list.append(mid_list)

    print("结束spark分析")
    print(all_list)
    print("1111")
    return all_list
def draw_bar(all_list):
    print("开始绘图")
    attr = ["南岗", "道里", "江北", "香坊", "道外", "松北", "平房"]
    v0 = all_list[0]
    v1 = all_list[1]
    v2 = all_list[2]
    v3 = all_list[3]

    bar = Bar("harbin市租房租金概况")
    bar.add("最小值", attr, v0, is_stack=True)
    bar.add("最大值", attr, v1, is_stack=True)
    bar.add("平均值", attr, v2, is_stack=True)
    bar.add("中位数", attr, v3, is_stack=True)
    bar.render()
    print("结束绘图")
if __name__=='__main__':
    all_list = spark_analyse(filename)
    draw_bar(all_list)