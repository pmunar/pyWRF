def get_config_parameters(config_file):
    """
    Function that parses the config file and retrieves the parameters needed for the analysis
    :param config_file:
    :return: data_path, output_path, start_date, end_date, group_of_days
    """
    import configparser
    Config = configparser.ConfigParser()
    Config.read(config_file)
    Config.sections()
    start_date = Config.get('Analysis', 'start_date')[1:-1]
    end_date = Config.get('Analysis', 'end_date')[1:-1]
    group_of_days = Config.get('Analysis', 'group_of_days')
    data_path = Config.get('Data', 'data_path')
    output_path = Config.get('Data', 'output_path')
    data_format = Config.get('Data', 'data_format')

    return data_path, output_path, data_format, start_date, end_date, int(group_of_days)