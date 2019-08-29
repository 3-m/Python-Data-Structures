# Based on practical script from COMP1002
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np

# Generate csv of random data from ASX files
def generateData(numRuns):
    path = "testData/"
    size = 0

    if not os.path.exists("outputData"):
        os.mkdir("outputData")

    with open("outputData/randShares.txt", "w") as output:
        for data in sorted(os.listdir(path)):
            if data.endswith(".txt"):
                numLines = random.randint(100, 1500)
                size += numLines
                chosenLines = sorted(random.sample(range(1500), numLines))

                currLine = 0
                with open(path+data, "r") as f:
                    for line in f:
                        if len(chosenLines) != 0 and chosenLines[0] == currLine:
                            output.write(line)
                            chosenLines.pop(0)

                        currLine += 1


        runTreeProfiler(size, numRuns)


def runTreeProfiler(maxSize, numRuns):
    # generate a profile
    sizes = sorted(random.sample(range(maxSize), numRuns))

    # BST runs
    for i in range(numRuns):
        command = "python3 TreeProfiler.py -p bs "+str(sizes[i])+" outputData/randShares.txt csv >/dev/null"
        os.system(command)
    print("Binary search tree runs complete.")

    # btree runs
    numKeys = np.arange(5, 27, 2, dtype=int)

    for n in range(len(numKeys)):
        for j in range(numRuns):
            command = "python3 TreeProfiler.py -p bt"+str(numKeys[n])+" "+str(sizes[j])+" outputData/randShares.txt csv >/dev/null"
            os.system(command)
    print("B-Tree runs complete.")

    # 234 tree runs
    for k in range(numRuns):
        command = "python3 TreeProfiler.py -p 234t "+str(sizes[k])+" outputData/randShares.txt csv >/dev/null"
        os.system(command)
    print("2,3,4-Tree runs complete.")

#https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
def generatePlots():
    data = pd.read_csv("outputData/TreeProfilerOutput.log",
                       sep = ",",
                       usecols=[0,3,4,5,6,7,8,9],
                       #names=["type", "size", "file", "Number of elements inserted", "height", "balance", "insert", "delete", "find", "sort"])
                       names=["type", "Number of elements inserted", "height", "balance", "insert", "delete", "find", "sort"])


    ax = data[data['type'] == "bs"].plot(x='Number of elements inserted', logy=True, title="Binary Search Tree", ylim=(1e-5,3500))
    ax.set_xlabel(xlabel="Number of elements inserted")
    ax.set_ylabel("Time (seconds)")
    plt.savefig("outputData/Binary Search Tree.jpg")

    ax = data[data['type'] == "234t"].plot(x='Number of elements inserted', logy=True, title="2,3,4-Tree", ylim=(1e-5,3500))
    ax.set_xlabel(xlabel="Number of elements inserted")
    ax.set_ylabel("Time (seconds)")
    plt.savefig("outputData/2,3,4-Tree.jpg")

    fig, axes = plt.subplots(nrows=3, ncols=2, sharex = True, figsize=(8,10))
    fig.suptitle("B-Tree Statistics")
    axes[0,0] = data[data['type'].str.startswith("bt")].sort_values(by="Number of elements inserted").groupby('type').plot(x='Number of elements inserted', y='height', title="Height", ax=axes[0,0], legend=False)
    axes[0,1] = data[data['type'].str.startswith("bt")].sort_values(by="Number of elements inserted").groupby('type').plot(x='Number of elements inserted', y='balance', title="Balance", ax=axes[0,1], legend=False)
    axes[1,0] = data[data['type'].str.startswith("bt")].sort_values(by="Number of elements inserted").groupby('type').plot(x='Number of elements inserted', y='insert', title="Insertion Time", ax=axes[1,0], legend=False)
    axes[1,1] = data[data['type'].str.startswith("bt")].sort_values(by="Number of elements inserted").groupby('type').plot(x='Number of elements inserted', y='delete', title="Deletion Time", ax=axes[1,1], legend=False)
    axes[2,0] = data[data['type'].str.startswith("bt")].sort_values(by="Number of elements inserted").groupby('type').plot(x='Number of elements inserted', y='find', title="Find Time", ax=axes[2,0], legend=False)
    axes[2,1] = data[data['type'].str.startswith("bt")].sort_values(by="Number of elements inserted").groupby('type').plot(x='Number of elements inserted', y='sort', title="Sort Time", legend=False, ax=axes[2,1])
    fig.axes[5].legend(loc='lower center', bbox_to_anchor=(0, -0.5), ncol=6, labels=('5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25'), title="Number of keys per node")
    fig.tight_layout()
    plt.savefig("outputData/B-Tree stats.jpg")

try:
    print("Starting...")
    numRuns = int(sys.argv[1])
except:
    numRuns = 20

generateData(numRuns)
generatePlots()
print("Success!")
