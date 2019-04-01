% collect data to a new time series structure

OUT.T_Room_rel=house_data.explanatories.T_Room_rel.Data;
OUT.T_Room_lag1_rel=house_data.explanatories.T_Room_lag1_rel.Data;
OUT.T_Room_lag2_rel=house_data.explanatories.T_Room_lag2_rel.Data;
OUT.T_Room_lag3_rel=house_data.explanatories.T_Room_lag3_rel.Data;
OUT.T_Room_lag4_rel=house_data.explanatories.T_Room_lag4_rel.Data;
OUT.T_Outdoor_rel=house_data.explanatories.T_Outdoor_rel.Data;

OUT.Humidity=house_data.explanatories.Humidity.Data;

OUT.T_Set=house_data.T_Set.Data;
OUT.Thermostate_Switch=house_data.Thermostate_Switch.Data;
OUT.T_Room=house_data.T_Room.Data;

struct2csv(OUT,'.\data\hh_collected_data.csv')
% find times when thermostat was off


is_dT_set=[0;OUT.T_Set(2:end)-OUT.T_Set(1:end-1)];
locs_dT_set=find(is_dT_set~=0);

% find next max indoor temperature


[pks,locs] = findpeaks( OUT.T_Room );

is_Thermostate_Set_Period=zeros(length(is_dT_set),1);

for i=1:length(locs_dT_set)
    d_locs=locs-locs_dT_set(i);
     
    closest_next_peak_locs=find(d_locs==min(d_locs(d_locs>0)));
    closest_prev_peak_locs=find(d_locs==max(d_locs(d_locs<0)));

    if isempty(closest_next_peak_locs) 
        end_loc=length(locs_dT_set);
    else
        end_loc=locs(closest_next_peak_locs);
    end
    if isempty(closest_prev_peak_locs) 
        start_loc=1;
    else
        start_loc=locs(closest_prev_peak_locs);
    end
    is_Thermostate_Set_Period(start_loc:end_loc)=1;
end

last_locs=max(locs);

nextPeak=zeros(last_locs,1);
nextPeak(locs)=OUT.T_Room(locs);

i=1;
while sum(nextPeak==0)>0
    n_nextPeak=nextPeak(i+1:end);
    c_nextPeak=nextPeak(1:end-i);
    c_nextPeak(c_nextPeak==0)=n_nextPeak(c_nextPeak==0);
    nextPeak(1:end-i)=c_nextPeak;
    i=i+1;
end




%%

T_Room=OUT.T_Room(1:last_locs);
T_Set=OUT.T_Set(1:last_locs);
Thermostate_Switch=OUT.Thermostate_Switch(1:last_locs);
is_Thermostate_Set_Period=is_Thermostate_Set_Period(1:last_locs);
T_nextMax=nextPeak;

is_Thermostate_Switched_OFF=[OUT.Thermostate_Switch(2:end)-OUT.Thermostate_Switch(1:end-1);0]<0;
is_Thermostate_Switched_OFF=is_Thermostate_Switched_OFF(1:last_locs);
T_Room_rel=(OUT.T_Room_rel(1:last_locs));
T_Room_lag1_rel=(OUT.T_Room_lag1_rel(1:last_locs));
T_Room_lag2_rel=(OUT.T_Room_lag2_rel(1:last_locs));
T_Room_lag3_rel=(OUT.T_Room_lag3_rel(1:last_locs));
T_Room_lag4_rel=(OUT.T_Room_lag4_rel(1:last_locs));
T_Outdoor_rel=OUT.T_Outdoor_rel(1:last_locs);

Humidity=OUT.Humidity(1:last_locs);

%%
figure('Name','Measured Data','NumberTitle','off');
    plot(T_Room)
    hold on
    plot(T_Room.*is_Thermostate_Switched_OFF,'go')
    hold on
    plot(nextPeak,'r')
  

%%
%n_lag=3;

is_rising=T_Room(1+1:end)-T_Room(1:end-1)>0;
is_rising=[0;is_rising]; % heat is on

    
 %%
 select_event=find(is_Thermostate_Switched_OFF & ~is_Thermostate_Set_Period);
 
 %%
figure('Name','Measured Data','NumberTitle','off');
    plot(T_Room(~is_Thermostate_Set_Period))
    hold on
    plot(nextPeak(~is_Thermostate_Set_Period),'r')
 
 
figure('Name','Measured Data','NumberTitle','off');
    plot(T_Room(select_event))
    hold on
    plot(nextPeak(select_event),'r')

 
 %% 
 % explanatories for NN
 explanatories=[T_Room_rel,T_Room_lag1_rel,T_Room_lag2_rel,T_Room_lag3_rel,T_Room_lag4_rel,T_Outdoor_rel,Humidity];
 
 dependent=T_nextMax-T_Room;
 
 explanatories=explanatories(select_event,:);
 dependent=dependent(select_event,:);
 
 % nnstart
 % save to net
 % dt=10
 % gensim(net,dt)
 
 y=net(explanatories');
 
 figure('Name','Measured Data','NumberTitle','off');
     plot(dependent','bo')
     hold on
     plot(y,'r+')