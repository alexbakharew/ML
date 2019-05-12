#! usr/bin/python3
import os
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio

separators = [",", ";", ".", ":", "\"", "\'", "`", "\\", "/", ">", "<", "=", "-", "_", "@", "#", "(", ")", "\t", "", " "]

def AddToDict(d, val):# function fror adding value in dictionary
    if val == None:
        return
    if val in d:
        d[val] += 1
    else:
        d[val] = 1

def ProcessFile(path, word_freq):# read file and collecting words

    file = open(path, "r", encoding = "latin-1")
    for line in file:
        words = line.split()
        for word in words:
            word = word.strip(str(separators))
            if word not in separators and not word.isnumeric():
                AddToDict(word_freq, word)
    file.close()

def DrawWordsDistribution(word_freq, name):# illustration of distribution
    words = []
    freq = []
    for w in word_freq.keys():
        if word_freq[w] < 5:# if word frequency less than 5, we don't use them
            continue        # this feature is optional, for more faster computation
        else:
            freq.append(word_freq[w])
            words.append(w)
    data = [go.Bar(x = words, y = freq)]
    layout = go.Layout(title = name + ' Words Distribution')
    fig = go.Figure(data = data, layout = layout)
    py.plot(fig, filename = name + ".html")

def MakeAnalysis(folder, analysis_name):# wrapper function for more convinient work
    word_freq = {}

    files = os.listdir(folder)
    for file in files: 
        ProcessFile(folder + file, word_freq)

    DrawWordsDistribution(word_freq, analysis_name)

def main():
    MakeAnalysis("./neg/", "Negative Reviwes")
    MakeAnalysis("./pos/", "Postive Reviwes")

if __name__ == "__main__":
    main()