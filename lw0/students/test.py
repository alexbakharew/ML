#! usr/bin/python
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio
import random
import numpy as np
import re

# загружаем файл с данными
# df = pd.DataFrame.from_csv("http://roman-kh.github.io/files/linear-models/simple1.csv")
# x - таблица с исходными данными факторов (x1, x2, x3)
csv_file = open("StudentsPerformance.csv", "r")
x = []
y = []
count = 0
for line in csv_file:
    val = re.match("^[^,]*,\"[a-z]*\s([A-Z])*\",.*,\"([^,]*)\"$", line)
    if val != None:
        y.append(val.group(2))
    else:
        continue
    x.append(count)
    count += 1


trace = go.Scatter(x = x, y = y, mode = 'markers')
data = [trace]

# Plot and embed in ipython notebook!
py.plot(data, filename='basic-scatter')
