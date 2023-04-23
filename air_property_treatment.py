from os import getcwd
from numpy import float_power
from pandas import DataFrame
def read_air_prop(path : str) -> list:
    filename : str = getcwd() + "/" + path
    print(filename)
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        file.close()
    return lines

def generate_table(input : list):
    params = {'T':[],'Ro':[],'Cp':[],'mu':[],'v':[],'k':[],'alpha':[],'Pr':[]}
    raw_size = len(input)
    previous_i = 0
    for i in [aux*(raw_size/5) for aux in range(1,5+1)]:
        raw_slice = input[previous_i:int(i)]
        previous_i = int(i)
        previous_j = 0
        for j, key  in zip([aux*5 for aux in range(1,8+1)], params.keys()):
            params[key] += raw_slice[previous_j:int(j)]
            previous_j = int(j)
    for key in params.keys():
        params[key] = [float(x.replace(',','.')) for x in params[key]]
        if key in ('alpha','v'):
            params[key] = [j*float_power(10,-6) for j in params[key]]
        elif key == "mu":
            params[key] = [j*float_power(10,-7) for j in params[key]]
        elif key == "k":
            params[key] = [j*float_power(10,-3) for j in params[key]]
    DataFrame(params).to_parquet("air_params_treated.parquet")
    exit(-1)
generate_table(read_air_prop('air_params.txt'))