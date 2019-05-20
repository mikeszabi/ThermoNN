BlockPaths = find_system('house_thermal_model','Type','Block');

ei=get_param('house_thermal_model','ExternalInput')

set_param('house_thermal_model','ExternalInput',get_param('house_thermal_model','ExternalInput'))