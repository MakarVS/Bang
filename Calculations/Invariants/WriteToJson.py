import json


def write_to_file(result, number):

    name_file = 'D:\RobotActualVers\PowderRobotMultiproc\Results\Result' + str(number) + ".json"
    with open(name_file, 'w') as outfile:
        json.dump(result, outfile)