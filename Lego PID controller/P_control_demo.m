distance_away = 500.0;
required_gap = 200.0;
current_position = 0.0;
static_velocity = 10;
error = (distance_away - current_position) - required_gap;
dt = 0.1;
error_values = [error] ;
speeds = [0];
time = [0];

i = 1

figure;

Kp = 1;



while error > 0.1
    
    Speed = Kp*error - static_velocity;
    current_position = current_position + Speed*dt;
    error = (distance_away - current_position) - required_gap;
    error_values(end +1) = error;
    speeds(end +1) = Speed;
    time(end+1) = time(end) + dt;
    
    
%     plot(time,error_values);
%     xlim([0,10]);
%     ylim([0,300]);
%     xlabel('time');
%     ylabel('Error');
%     title('Error vs Time');
% 
%     drawnow;
    
    i = i +1;
    if i >1000
        break
    end
end


plot(time,error_values);
xlim([0,10]);
ylim([0,300]);
xlabel('time (m)');
ylabel('Error (m)');
title('Error vs Time');

steady_state_error = error(end)



