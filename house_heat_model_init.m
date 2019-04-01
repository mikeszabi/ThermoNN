%   This script runs in conjunction with the "house_heat_model"
%   house thermodynamics example. Note that time is given in units of seconds

%% Read config file
config_file=[pwd,'\ThermoNN_config.json'];

fid = fopen(config_file);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
simdata = jsondecode(str);

%% Constans
% Assume the cost of electricity is $0.09 per kilowatt/hour
% Assume all electric energy is transformed to heat energy
% 1 kW-hr = 3.6e6 J
% cost = $0.09 per 3.6e6 J
cost = 0.09/3.6e6;
% converst radians to degrees
r2d = 180/pi;


%%
% Main user parameters

% SIMULATION step size
dt=simdata.Simulation.dt.value;
% Heater temperature
THeater = simdata.Simulation.Heat.T_Heater.value;
% Water flow rate (kg/sec )
Mdot = simdata.Simulation.Heat.M_dot.value;  % second is the time unit
% TinIC = initial outdoor temperature = 20 deg C
ToutIC=simdata.Simulation.Heat.T_OUT_ini.value;
% TinIC = initial indoor temperature = 20 deg C
TinIC = simdata.Simulation.Heat.T_IN_ini.value;
dT_histerezis=simdata.Simulation.Heat.dT_histerizes.value;


%%
% Material constants

% Heat capacities
%J/kg-K - http://www2.ucdsb.on.ca/tiss/stretton/database/specific_heat_capacity_table.html; http://www.engineeringtoolbox.com/specific-heat-solids-d_154.html
% c = cp of air (273 K) = 1005.4 J/kg-K
c_s = simdata.Simulation.Material.c_s.value; % max
c_a = simdata.Simulation.Material.c_a.value; % min
c_floor = simdata.Simulation.Material.c_floor.value;
c_water = simdata.Simulation.Material.c_water.value;
% Densities
densConcrete = 2000; %http://mek.oszk.hu/00000/00056/html/083.htm
densAir = 1.2250; % assumed to be constant


%%
% -------------------------------
% Define the house geometry
% -------------------------------
% House length = 30 m
lenHouse = simdata.Simulation.Building.l_house.value;
% House width = 10 m
widHouse = simdata.Simulation.Building.w_house.value;
% House height = 4 m
htHouse = simdata.Simulation.Building.h_house.value;
% Roof pitch = 40 deg
pitRoof = simdata.Simulation.Building.pitch_roof.value/r2d;
% Number of windows = 6
numWindows = simdata.Simulation.Building.n_windows.value;
% Height of windows = 1 m
htWindows = simdata.Simulation.Building.h_windows.value;
% Width of windows = 1 m
widWindows = simdata.Simulation.Building.w_windows.value;
heatedPct=simdata.Simulation.Building.pct_heated.value;

windowArea = numWindows*htWindows*widWindows;
wallArea = 2*lenHouse*htHouse + 2*widHouse*htHouse + ...
           2*(1/cos(pitRoof/2))*widHouse*lenHouse + ...
           tan(pitRoof)*widHouse - windowArea;
floorArea = lenHouse*widHouse;

%% depths
L_wall = simdata.Simulation.Building.d_wall.value;
L_window = simdata.Simulation.Building.d_window.value;
L_floor = simdata.Simulation.Building.d_floor.value;

% -------------------------------
% Define the type of insulation used
% -------------------------------
% Glass wool in the walls, 0.2 m thick
% k is in units of J/sec/m/C 
k_wall = simdata.Simulation.Material.k_wall.value;   % second is the time unit
%  http://www.engineeringtoolbox.com/thermal-conductivity-d_429.html
k_window = simdata.Simulation.Material.k_window.value;  % second is the time unit - thermal resistivity
k_floor = simdata.Simulation.Material.k_floor.value; % no insulation - concrete

% -------------------------------
% CALCULATIONS Determine the equivalent thermal resistance for the whole building
% -------------------------------
R_window = L_window/(k_window*windowArea);
R_wall = L_wall/(k_wall*wallArea);
R_house = R_wall*R_window/(R_wall + R_window);

R_floor = L_floor/(k_floor*floorArea);
M_floor=floorArea*L_floor*densConcrete*heatedPct; % 0.2m floor width

M_air = (lenHouse*widHouse*htHouse+tan(pitRoof)*widHouse*lenHouse)*densAir;
