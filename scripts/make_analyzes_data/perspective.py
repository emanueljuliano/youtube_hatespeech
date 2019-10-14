import pickle
import numpy as np
import itertools
import argparse
from sqlitedict import SqliteDict
from time import time

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on perspective scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../sentiment/empath/sqlite/empath_value.sqlite",
                    help="Where to save the output files.")

parser.add_argument("--name", dest="name", type=str, default="IDW",
                    help="Name of the community to create perspective files")

args = parser.parse_args()


def sqlite_to_array(num):

    p2 = SqliteDict(f"./perspective/perspective_value{num}.sqlite", tablename="value", flag="r")

    c = 0
    t_ini = time()
    ids = []
    perspective = []
    to_request = [(k, v) for k, v in itertools.islice(p2.items(), 15000001, 20000001)]

    for key, value in to_request:
        if c % 100000 == 0:
            print("iteration number ", c, "at", round((time()-t_ini)/60, 2), "minutes")
        c += 1

        if c % 5000000 == 0:
            save_arrays(num, perspective, ids, c)
            ids = []
            perspective = []

        ids.append(key)
        perspective.append(tuple(value.values()))
    c += 1
    save_arrays(num, perspective, ids, c)


def save_arrays(num, perspective, ids, c):
    print(":D")
    with open(f"./perspective/perspective_{num}_{c}_val", "wb") as f:
        pickle.dump(np.array(perspective), f, protocol=4)
    print("Val")
    with open(f"./perspective/perspective_{num}_{c}_id", "wb") as f:
        pickle.dump(tuple(np.array(ids)), f, protocol=4)
    print("ID")


def make_values_by_year(name):
    with open(f"{name}.pickle", "rb") as fp:
        ks = pickle.load(fp)

    d_persp = {}
    for year in range(2006, 2020):
        d_persp[year] = []

    filenames = ["0_5000000", "0_10000000_", "0_15000000", "0_20000000", "0_20369999", "1_3626600", "2_2390000",
                 "2.1_640000", "2.2_285042", "2.3_887730", "2.4_6000000", "3_7900000", "3.1_2180000", "4.1_4581097",
                 "4.2_320000", "4.3_1050000", "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999",
                 "7.1_3859623"]

    for fname in filenames:
        with open(f"./perspective/perspective_{fname}_val", "rb") as fp:
            perspective = pickle.load(fp)
        print("perspective")
        with open(f"./perspective/perspective_{fname}_id", "rb") as fp:
            ide = pickle.load(fp)
        print("id")

        for i in range(len(perspective)):
            if i % 1000000 == 0:
                print(i)
            key = ide[i]
            if key in ks:
                d_persp[ks[key]].append(perspective[i])

        print(fname, len(d_persp[2018]))

    for i in range(2007, 2020):
        print(i)
        with open(f"./perspective/{name}1_perspective_{i} ", "wb") as f:
            pickle.dump(tuple(np.array(d_persp[i])), f, protocol=4)


if __name__ == "__main__":
    pers_files = [0, 1, 2, 2.0, 2.1, 2.2, 2.3, 2.4, 3.1, 3, 4, 4.1, 4.2, 4.3, 5.1, 5.2, 6.1, 6.2, 7.1]
    for number_file in pers_files:
        sqlite_to_array(number_file)

    make_values_by_year(args.name)
