def get_config_parameters(config_file):
    """
    Function that parses the config file and retrieves the parameters needed for the analysis
    :param config_file:
    :return: data_path, output_path, start_date, end_date, group_of_days
    """
    import configparser
    Config = configparser.ConfigParser()
    Config.read(config_file)
    config_params = []
    for s in Config.sections():
        config_params.append(dict(Config.items(s)))
    return config_params


#OLD WAY TO PARSE THE CONFIG FILE
    # Config.sections()
    # data_path = Config.get('Data', 'data_path')
    # output_path = Config.get('Data', 'output_path')
    # data_format = Config.get('Data', 'data_format')
    # hours_step = Config.get('Data', 'hours_step')
    # input_data_server = Config.get('Data', 'input_data_server')
    # start_date = Config.get('Analysis', 'start_date')[1:-1]
    # end_date = Config.get('Analysis', 'end_date')[1:-1]
    # group_of_days = Config.get('Analysis', 'group_of_days')
    # num_domains = Config.get('Analysis', 'num_domains')
    # parallel = Config.get('Analysis', 'parallel')
    # ncores = Config.get('Analysis', 'ncores')
    #
    # return data_path, output_path, data_format, start_date, end_date, int(num_domains), int(group_of_days), \
    #            int(hours_step), input_data_server, parallel, ncores
