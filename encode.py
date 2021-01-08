import matplotlib.pyplot as plt
import numpy as np
import os


def get_GPS_from_logfile(file_name):
    with open(file_name, mode='rb') as file:
        flight_data = file.readlines()
        file.close()
        flight_data = [x.decode('UTF-8') for x in flight_data]
        flight_data = [x.split(',') for x in flight_data]
        flight_data = list(filter(lambda x: x[0] == 'GPS', flight_data))
        # get the timestamp and (x, y, z) = (Lat, Lng, Alt)
        GPSs = [[x[0], int(x[1]), float(x[8]), float(x[9]), float(x[10])] for x in flight_data]
        # v_x = np.array([x[2] for x in GPSs])
        # v_y = np.array([x[3] for x in GPSs])
        # v_z = np.array([x[4] for x in GPSs])

        file_name = file_name.strip('logs/')
        output_file = open("data/" + file_name+"txt", "w")
        output_file.write('TimeStamp' + '\t' + 'POS_X' + '\t' + 'POS_Y' + '\t' + 'POS_Z' + '\n')
        for value in GPSs:
            output_file.write(str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]) + '\t' + str(value[4]) + '\n')
        output_file.close()

        # plot coordinates
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # ax.plot_trisurf(v_x, v_y, v_z, linewidth=0, antialiased=False)
        # plt.show()


if __name__ == '__main__':
    directory = r'D:\University\Coding\DroneProject_1\logs'
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            get_GPS_from_logfile("logs/"+filename)
        else:
            continue

    # get_GPS_from_logfile("logs/2021-01-07 15-59-47.log")
