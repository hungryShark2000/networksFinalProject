# importing pandas as pd
import pandas as pd

def covert_to_csv(pathToOld, pathToNew):
    read_file = pd.read_excel(pathToOld)
    read_file.to_csv(pathToNew,
                 index=None,
                 header=True)
    df = pd.DataFrame(pd.read_csv(pathToNew))
    df

#covert_to_csv("../processed/all/2016.xlsx", "../edges/2016.csv")
covert_to_csv("../processed/all/2018.xlsx", "../edges/2018.csv")
