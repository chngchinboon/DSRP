clear all
clc
syms q_1 q_2 q_3 q_4 az n g real

% equation from norm of intersection 
% (-sin(q_1)*cos(q_2) + sin(q_2)*cos(az)*cos(q_1))**2 + sin(az)**2*sin(q_1)**2*sin(q_2)**2 + sin(az)**2*sin(q_2)**2*cos(q_1)**2

% eq = sin(q_1)^2*cos(q_2)^2 - 2*sin(q_1)*sin(q_2)*cos(az)*cos(q_1)*cos(q_2) + sin(q_2)^2*cos(az)^2*cos(q_1)^2
%%
% eq = (-sin(q_1)*cos(q_2) + sin(q_2)*cos(az)*cos(q_1))^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2 + sin(az)^2*sin(q_2)^2*cos(q_1)^2
% 
% eq_s = simplify(eq)
% 
% eq_squared = simplify(eq^0.5)
% 
% eq_semi = sin(az)^2*sin(q_1)^2*sin(q_2)^2 + sin(az)^2*sin(q_2)^2*cos(q_1)^2
% 
% eq_semi_s = simplify(eq_semi)
% 
% eq_first_part = (-sin(q_1)*cos(q_2) + sin(q_2)*cos(az)*cos(q_1))^2
% 
% eq_first_part_s = simplify(eq_first_part)
% 
% ty = [0; sin(q_1)*cos(q_2); -cos(q_1)*cos(q_2)]
% syms n
% tz = [-sin(q_1)*cos(q_2)+sin(q_2)*cos(az)*cos(q_1); sin(az)*sin(q_2)*cos(q_1); sin(az)*sin(q_1)*sin(q_2)]
% 
% tx = cross(ty,1/n*tz)
% 
% tx_s = simplify(tx)
% 
% 
% tx_norm = sqrt(tx_s'*tx_s)
% tx_s/tx_norm
% 
% tx_hat_s = 1/n*[sin(az)*sin(q_2)*cos(q_2); cos(q_1)*cos(q_2)*g; sin(q_1)*cos(q_2)*g]/cos(q_2)
% ty = [-sin(az)*sin(q_2);sin(q_2)*cos(az);-cos(q_2)]
% tz_hat_s = 1/n*[-sin(q_1)*cos(q_2)+sin(q_2)*cos(az)*cos(q_1);  sin(az)*sin(q_1)*sin(q_2); sin(az)*sin(q_2)*cos(q_1)]

%% 

tx_hat =  1/n*[sin(az)*sin(q_2)*cos(q_2); cos(q_1)*cos(q_2)*g; sin(q_1)*cos(q_2)*g]/cos(q_2)
ty = [-sin(az)*sin(q_2);sin(q_2)*cos(az);-cos(q_2)]
tz_hat = 1/n*[g;  sin(az)*cos(q_1)*sin(q_2); sin(az)*sin(q_2)*sin(q_1)]

TSE = [cos(q_3) -sin(q_3) 0 0; sin(q_3) cos(q_3) 0 0; 0 0 1 q_4; 0 0 0 1]

TOS = [tx_hat ty tz_hat zeros(3,1); zeros(1,3) 1]

TOE = TOS*TSE

pretty(TOE)

