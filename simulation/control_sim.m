%% Read config file
config_file=[pwd,'\ThermoNN_config_20190425.json'];

fid = fopen(config_file);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
simdata = jsondecode(str);

%%
% Solver parameters
% SIMULATION step size
dt=simdata.Simulation.dt.value;
% simulation length
n_simulation_steps=1*7*24*3600;

%% 
% Load prediction net
pred_net = importKerasNetwork('D:\Projects\ThermoNN\prediction\saved_models\04052019-134221-e100.h5');

%%
T_pred=single(0);

% open simulation
open_system('house_thermal_model')
% open model workspace
mdlWks = get_param('house_thermal_model', 'ModelWorkspace');
% set Solver parameters
set_param('house_thermal_model','FixedStep','10')
set_param('house_thermal_model','StopTime',num2str(n_simulation_steps))

% start and pause
set_param('house_thermal_model','SimulationCommand','start','SimulationCommand','pause')
%%

for i = 1:n_simulation_steps/10

    x=T_ROOM_lags.Data(end,:);
    x=x-x(end);
    C = num2cell(x,2);
    y_pred=predict(pred_net,C);

    t_sim=get_param('house_thermal_model','SimulationTime');

    T_pred=y_pred;
    % make one step
    set_param('house_thermal_model','SimulationCommand','step')
end
%mdlWks.reload
%%
set_param('house_thermal_model','SimulationCommand','stop')

close_system('house_thermal_model')

