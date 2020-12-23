% Set up EV3 brick connection and Assign Motors/Sensors
myev3 = legoev3('usb');

motor_l = motor(myev3,'D');
motor_r = motor(myev3,'A');
ir_sensor = irSensor(myev3);


desired_gap = 40;
time_now = clock;

proximity = readProximity(ir_sensor);
error = proximity - desired_gap;

error_values = [double(error)];
time_values = [0];
speed_values = [0];

motor_r.Speed = 0;
motor_l.Speed = 0;
start(motor_r);
start(motor_l);

Kp = 2.0;
Ki = 0.0;
Kd = 0.5;


while error ~= 0
    
    P = Kp*error;
   
    if size(error_values,2) < 2 || error > 60
        I = 0;
        D = 0;
    else
        I = Ki * trapz(time_values,error_values);
        D = Kd * (error_values(end) - error_values(end-1)) /(time_values(end) - time_values(end-1)) ;
        
    end
    
  
        
    Speed = P + I + D;
    
    if Speed > 100.0 
        Speed = 100.0;
    elseif Speed < -100.0
        Speed = -100.0;
    end
    
    motor_r.Speed = -Speed;
    motor_l.Speed = -Speed;
    
    
    new_time = clock;
    proximity = readProximity(ir_sensor);
    error = proximity - desired_gap;
    time = (new_time - time_now);
    time_diff = 60*time(5) + time(6);
    

    time_values(end+1) = time_diff;
    error_values(end+1) = double(error);
    speed_values(end+1) = Speed;
    
    
    plot(time_values,error_values);
    xlim([0,time_values(end)]);
    ylim([-100,100]);
    xlabel('time (s)');
    ylabel('Error');
    title('Error vs Time');
    
    drawnow;
    
    
    if time_diff > 10
        break
    end
    
    
end



stop(motor_r);
stop(motor_l);



figure;

plot(time_values,speed_values);
xlim([0,time_values(end)]);
ylim([-100,100]);
xlabel('time (s)');
ylabel('Speed');
title('Speed vs Time');


steady_state_error = error_values(end);
steady_state_error    