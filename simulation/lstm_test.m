pred_net = importKerasNetwork('D:\Projects\ThermoNN\prediction\saved_models\04052019-134221-e100.h5');
% C is a N-by-1 cell array where N is the number of observations
%  Each entry of C is a time series represented by a matrix with rows corresponding to data points, and columns corresponding to time steps.
%x = rand(1,25,1); %(samples, time steps, features)

T = readtable('d:\Projects\ThermoNN\prediction\data\hh_processed_data.csv');
x=table2array(T(1:end,2:end-1));
y=table2array(T(1:end,end));
C = num2cell(x,2);

y_pred=predict(pred_net,C);

figure('Name','prediction','NumberTitle','off');
     plot(y','b')
     hold on
     plot(y_pred,'r')