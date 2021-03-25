import os


from FlightDBAccess import FlightDBAccess


def get_flight_data_in_uniform_format(file_name):
    """
        Returns GPS points form log file
    :param file_name: log file name
    :return:
    """
    file_name = "logs/" + file_name
    with open(file_name, mode='rb') as file:
        flight_data = file.readlines()
        file.close()
        flight_data = [x.decode('UTF-8') for x in flight_data]
        flight_data = [x.split(',') for x in flight_data]
        x_index = 0   # Lat
        y_index = 0   # Lng
        z_index = 0   # Alt
        for data in flight_data:
            data = [x.strip() for x in data]
            try:
                gps_index = data.index('GPS')
                x_index = data.index('Lat') - gps_index -1
                y_index = data.index('Lng') - gps_index -1
                z_index = data.index('Alt') - gps_index -1
                break
            except:
                pass
        flight_data = list(filter(lambda x: x[0] == 'GPS', flight_data))
        # get the timestamp and (x, y, z) = (Lat, Lng, Alt)
        GPSs = [[x[0], int(x[1]), float(x[x_index]), float(x[y_index]), float(x[z_index])] for x in flight_data]

        flight_data = 'TimeStamp' + '\t' + 'POS_X' + '\t' + 'POS_Y' + '\t' + 'POS_Z' + '\n'
        for value in GPSs:
            flight_data += str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]) + '\t' + str(value[4]) + '\n'
        os.remove(file_name)
        return flight_data


# def convert_log_to_uniform_format(file_name, location, details):
#     """
#     Export GPS points form log file
#     :param file_name: log file name
#     :return:
#     """
#     file_name = "logs/" + file_name
#     with open(file_name, mode='rb') as file:
#         flight_data = file.readlines()
#         file.close()
#         flight_data = [x.decode('UTF-8') for x in flight_data]
#         flight_data = [x.split(',') for x in flight_data]
#         x_index = 0   # Lat
#         y_index = 0   # Lng
#         z_index = 0   # Alt
#         for data in flight_data:
#             data = [x.strip() for x in data]
#             try:
#                 gps_index = data.index('GPS')
#                 x_index = data.index('Lat') - gps_index -1
#                 y_index = data.index('Lng') - gps_index -1
#                 z_index = data.index('Alt') - gps_index -1
#                 break
#             except:
#                 pass
#
#         flight_data = list(filter(lambda x: x[0] == 'GPS', flight_data))
#         # get the timestamp and (x, y, z) = (Lat, Lng, Alt)
#         GPSs = [[x[0], int(x[1]), float(x[x_index]), float(x[y_index]), float(x[z_index])] for x in flight_data]
#         # v_x = np.array([x[2] for x in GPSs])
#         # v_y = np.array([x[3] for x in GPSs])
#         # v_z = np.array([x[4] for x in GPSs])
#
#         fit_and_save_data(file_name, GPSs, location, details)
#         # plot coordinates
#         # fig = plt.figure()
#         # ax = fig.add_subplot(111, projection='3d')
#         # ax.plot_trisurf(v_x, v_y, v_z, linewidth=0, antialiased=False)
#         # plt.show()


# def fit_and_save_data(file_name, gps_points, location, details):
#     """
#     Transform the GPS points to fit Eliyaho's code and saves it in the data directory
#     :param file_name:
#     :param gps_points:
#     :return:
#     """
#     file_name = file_name.strip('logs/')
#     # if not os.path.exists("data/" + location):
#     #     os.makedirs("data/" + location)
#     # output_file = open("data/" + location + "/" + file_name + "txt", "w")
#     if not os.path.exists("data/" + file_name):
#         # os.makedirs("data/" + location)
#         output_file = open("data/" + file_name + "txt", "w")
#
#         output_file.write(details + '\n')
#         output_file.write('TimeStamp' + '\t' + 'POS_X' + '\t' + 'POS_Y' + '\t' + 'POS_Z' + '\n')
#         for value in gps_points:
#             output_file.write(str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]) + '\t' + str(value[4]) + '\n')
#         output_file.close()
#

def upload_flight(file, location, params=None, values=None):
    """
    Add new drone's flight to the DB
    :param params: flight details
    :param values: value of flight details
    :param flight: flight's log file to upload
    :return: Failure or Success
    """
    # # saves the log file in logs directory
    # file.save('logs/'+file.filename)
    # details = 'location=' + location + ','
    # details = reduce(lambda acc, i: acc + params[int(i)] + '=' + values[int(i)] + ',', list(range(0, len(params))), details)
    # details = details[0:len(details)-1]
    # convert_log_to_uniform_format(file.filename, location, details)

    file.save('logs/'+file.filename)
    flight_data = get_flight_data_in_uniform_format(file.filename)
    params += ['location', 'data', 'file_name']
    values += [location, flight_data, file.filename]
    size = len(params)
    flight_dict = {params[i]: values[i] for i in range(0, size)}
    FlightDBAccess.getInstance().insert_one(flight_dict)
    FlightDBAccess.getInstance().update_parameters(params)
    FlightDBAccess.getInstance().close_conn()

