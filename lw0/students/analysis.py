#! usr/bin/python
import re
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio
import os
def AddToDict(d, val):# function fror adding value in dictionary
    if val == None:
        return
    if val in d:
        d[val] += 1
    else:
        d[val] = 1

def AddToMarkList(mark_list, match):# this function will add marks into list.
    group = match.group(1)
    mark = match.group(2)
    mark_list[ord(group) - ord("A")].append(int(mark))
    
def DrawDistribution(dist, name):# Visualisation of simple Distribution. See html file in work dirrectory
    labels = list(dist.keys())
    values = list(dist.values())
    trace = go.Pie(labels = labels, values = values)
    py.plot([trace], filename = name + ".html")

def ReadFile(csv_file):# read whole file for getting information
    count = 0
    GroupDist = {}
    EduLevelDist = {}
    MathMarksList = [[], [], [], [], []]
    WritingMarkList = [[], [], [], [], []]
    for line in csv_file:
        if count == 0:
            count += 1
            continue

        AddToDict(GroupDist, re.match("^[^,]*,([^,]*)", line).group(1))
    
        AddToDict(EduLevelDist, re.match("^[^,]*,[^,]*,([^,]*)", line).group(1))
    
        AddToMarkList(MathMarksList, re.match("^[^,]*,\"[a-z]*\s([A-Z])*\",.*,\"([^,]*)\",[^,]*,[^,]*$", line))
    
        AddToMarkList(WritingMarkList, re.match("^[^,]*,\"[a-z]*\s([A-Z])*\",.*,\"([^,]*)\"$", line))
    
    return GroupDist, EduLevelDist, MathMarksList, WritingMarkList

def GetMarkStatistics(mark_list):# mark_list is a list with marks
    
    def GetExpectation(mark_list):#0
        sum = 0
        for n in mark_list:
            sum += int(n)
        return sum / len(mark_list)
    
    def GetDispersion(mark_list, E):#1
        square_vals = []
        for n in mark_list:
            square_vals.append((n - int(E)) ** 2)
        return GetExpectation(square_vals)

    def GetMedian(mark_list):#2
        return mark_list[int(len(mark_list) / 2)]
    
    def GetMode(mark_list):#3
        mark_freq = {}

        max_freq = 0
        max_mark = 0
        for n in mark_list:
            AddToDict(mark_freq, n)
            if mark_freq[n] > max_freq:
                max_freq = mark_freq[n]
                max_mark = n
        return max_mark

    def GetMin(mark_list):
        return mark_list[0]
    
    def GetMax(mark_list):
        return mark_list[len(mark_list) - 1]
    
    def GetRange(mark_list):
        return GetMax(mark_list) - GetMin(mark_list)
    
    mark_list.sort()
    Stats = []

    E = GetExpectation(mark_list)
    Stats.append(E) #0
    Stats.append(GetDispersion(mark_list, E)) #1
    Stats.append(GetMedian(mark_list)) #2
    Stats.append(GetMode(mark_list)) #3
    Stats.append(GetMax(mark_list)) #4
    Stats.append(GetMin(mark_list)) #5
    Stats.append(GetRange(mark_list)) #6
    return Stats    

def DrawMarkStatistics(groups_mark_list, name): # groups_mark_list is a list, which contains list with marks
    groups = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E']
    if not os.path.isdir("./" + name):
        os.mkdir("./" + name)
    os.chdir("./" + name)

    def DrawExpectation(res_list):
        val = []
        for gr in res_list: # each group in result list
            val.append(gr[0]) # 0 - position of expectation in list

        data = [go.Bar(x = groups, y = val)]
        layout = go.Layout(title = name + ' expectation among all groups')
        fig = go.Figure(data = data, layout = layout)
        py.plot(fig, filename = name + "Expectation.html")

    def DrawMode(res_list):
        val = []
        for gr in res_list: # each group in result list
            val.append(gr[3]) # 3 - position of mode in list

        data = [go.Bar(x = groups, y = val)]
        layout = go.Layout(title = name + ' mode among all groups')
        fig = go.Figure(data = data, layout = layout)
        py.plot(fig, filename = name + "Mode.html")
    
    def DrawMinMaxRange(res_list):
        min_val = []
        max_val = []
        range_val = []
        median_val = []
        for gr in res_list:
            min_val.append(gr[5])
            max_val.append(gr[4])
            range_val.append(gr[6])
            median_val.append(gr[2])

        trace1 = go.Bar(x = groups, y = min_val, name='Min')
        trace2 = go.Bar(x = groups, y = max_val, name = 'Max')
        trace3 = go.Bar(x = groups, y = range_val, name = 'Range')
        trace4 = go.Bar(x = groups, y = median_val, name = 'Median')
        data = [trace1, trace2, trace3, trace4]
        layout = go.Layout(barmode='group')

        fig = go.Figure(data = data, layout = layout)
        py.plot(fig, filename = name + 'MinMaxRangeMedian.html')

    res_list = []
    for m in groups_mark_list:
        res_list.append(GetMarkStatistics(m))
    
    DrawExpectation(res_list)
    DrawMode(res_list)
    DrawMinMaxRange(res_list)
    os.chdir("./..")
    

def main():
    csv_file = open("StudentsPerformance.csv", "r")
    GroupDist, EducationDist, MathMarks, WritingMarks = ReadFile(csv_file)

    DrawDistribution(GroupDist, "Groups")
    DrawDistribution(EducationDist, "Education")
    DrawMarkStatistics(MathMarks, "MathMarks")
    DrawMarkStatistics(WritingMarks, "WritingMarks")

if __name__ == "__main__":
    main() 