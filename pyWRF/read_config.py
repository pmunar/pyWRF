def get_config_parameters(config_file):
    import configparser
    Config = configparser.ConfigParser()
    Config.read(config_file)
    Config.sections()
    start_date = Config.get('Analysis', 'start_date')[1:-1]
    end_date = Config.get('Analysis', 'end_date')[1:-1]
    group_of_days = Config.get('Analysis', 'group_of_days')
    data_path = Config.get('Data', 'data_path')
    output_path = Config.get('Data', 'output_path')

    return data_path, output_path, start_date, end_date, int(group_of_days)

# start_date_datetime = conf_date_to_datetime(start_date)
# end_date_datetime = conf_date_to_datetime(end_date)
#
# length_of_analysis = end_date_datetime - start_date_datetime
# print('Length of the analysis: {:d} days'.format(length_of_analysis.days))
