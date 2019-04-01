%   house_heat_model_init
%   This script runs in conjunction with the "house_heat_model"
%   house thermodynamics example. Note that time is given in units of
%   seconds

%%
% Main user parameters

% SIMULATION step size
dt=10;

% Heater temperature
THeater = 40;

% Water flow rate (kg/sec )
Mdot = 0.5;  % second is the time unit

% TinIC = initial outdoor temperature = 20 deg C
ToutIC=0;

% TinIC = initial indoor temperature = 20 deg C
TinIC = 20;
dT_histerezis=0.5;

% -------------------------------
% Enter the cost of electricity and initial internal temperature
% -------------------------------
% Assume the cost of electricity is $0.09 per kilowatt/hour
% Assume all electric energy is transformed to heat energy
% 1 kW-hr = 3.6e6 J
% cost = $0.09 per 3.6e6 J
cost = 0.09/3.6e6;

%%
% Material constants

% Heat capacities
%J/kg-K - http://www2.ucdsb.on.ca/tiss/stretton/database/specific_heat_capacity_table.html; http://www.engineeringtoolbox.com/specific-heat-solids-d_154.html
% c = cp of air (273 K) = 1005.4 J/kg-K
c_s = 1650; % max
c_a = 1005.4; % min
c_floor=650; 
c_water=4184;
% Densities
densConcrete = 2000; %http://mek.oszk.hu/00000/00056/html/083.htm
densAir = 1.2250; % assumed to be constant

%%
% -------------------------------
% Problem constant
% -------------------------------
% converst radians to degrees
r2d = 180/pi;

%%
% -------------------------------
% Define the house geometry
% -------------------------------
% House length = 30 m
lenHouse = 10;
% House width = 10 m
widHouse = 10;
% House height = 4 m
htHouse = 3;
% Roof pitch = 40 deg
pitRoof = 40/r2d;
% Number of windows = 6
numWindows = 4;
% Height of windows = 1 m
htWindows = 1;
% Width of windows = 1 m
widWindows = 1;
windowArea = numWindows*htWindows*widWindows;
wallArea = 2*lenHouse*htHouse + 2*widHouse*htHouse + ...
           2*(1/cos(pitRoof/2))*widHouse*lenHouse + ...
           tan(pitRoof)*widHouse - windowArea;
heatedPct=0.01;
floorArea = lenHouse*widHouse;

% -------------------------------
% Define the type of insulation used
% -------------------------------
% Glass wool in the walls, 0.2 m thick
% k is in units of J/sec/m/C 
k_wall = 0.038;   % second is the time unit
L_wall = .2;
%  http://www.engineeringtoolbox.com/thermal-conductivity-d_429.html
k_window = 0.3;  % second is the time unit - thermal resistivity
L_window = .02;
k_floor = 0.4; % no insulation - concrete
L_floor = 0.2;

R_window = L_window/(k_window*windowArea);
R_wall = L_wall/(k_wall*wallArea);
% -------------------------------
% Determine the equivalent thermal resistance for the whole building
% -------------------------------
R_house = R_wall*R_window/(R_wall + R_window);

R_floor = L_floor/(k_floor*floorArea);
M_floor=floorArea*L_floor*densConcrete*heatedPct; % 0.2m floor width

M_air = (lenHouse*widHouse*htHouse+tan(pitRoof)*widHouse*lenHouse)*densAir;


