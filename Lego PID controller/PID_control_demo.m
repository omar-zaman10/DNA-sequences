distance_away = 501.0;
required_gap =  200.0;
current_position = 0.0;
static_velocity = 10;
error = (distance_away - current_position) - required_gap;
dt = 0.1;
error_values = [error] ;
speeds = [0];
time = [0];

figure;
Kp = 1;
Ki = 0.02;
Kd = 0.1;


while error ~= 0
    
    P = Kp*error;
    
    if error > 300 
        I = 0;
        D = 0;
    else
        I = Ki * trapz(time,error_values);
        D = Kd * (error_values(end) - error_values(end-1)) / dt;

    end
    

        
    Speed = P + I + D - static_velocity;
    
    if Speed > 100.0 
        Speed = 100.0;
    end
    
   
    
    current_position = current_position + Speed*dt;
    error = (distance_away - current_position) - required_gap;
    error_values(end +1) = error;
    speeds(end +1) = Speed;
    time(end+1) = time(end) + dt;
    
    
%     plot(time,error_values);
%     xlim([0,30]);
%     ylim([-150,300]);
%     xlabel('time (s)');
%     ylabel('Error (m)');
%     title('Error vs Time');
% 
%     drawnow;
    

    if time(end) >30.0
        break
    end
end

plot(time,error_values);
xlim([0,30]);
ylim([-150,300]);
xlabel('time (s)');
ylabel('Error (m)');
title('Error vs Time');


steady_state_error = error_values(end)