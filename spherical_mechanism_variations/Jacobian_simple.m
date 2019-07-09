clear all
clc
syms q_1 q_2 q_3 q_4 az n g real


x=[q_4*(-sin(q_1)*cos(q_2) + sin(q_2)*cos(az)*cos(q_1))*((-sin(q_1)*cos(q_2) + sin(q_2)*cos(az)*cos(q_1))^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2 + sin(az)^2*sin(q_2)^2*cos(q_1)^2)^(-0.5)]
y=[q_4*((-sin(q_1)*cos(q_2) + sin(q_2)*cos(az)*cos(q_1))^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2 + sin(az)^2*sin(q_2)^2*cos(q_1)^2)^(-0.5)*sin(az)*sin(q_2)*cos(q_1)]
z=[q_4*((-sin(q_1)*cos(q_2) + sin(q_2)*cos(az)*cos(q_1))^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2 + sin(az)^2*sin(q_2)^2*cos(q_1)^2)^(-0.5)*sin(az)*sin(q_1)*sin(q_2)]

% x_q1_dot = diff(x,q_1)
% x_q2_dot = diff(x,q_2)
% x_q3_dot = diff(x,q_3)
% x_q4_dot = diff(x,q_4)
% 
% y_q1_dot = diff(y,q_1)
% y_q2_dot = diff(y,q_2)
% y_q3_dot = diff(y,q_3)
% y_q4_dot = diff(y,q_4)
% 
% z_q1_dot = diff(z,q_1)
% z_q2_dot = diff(z,q_2)
% z_q3_dot = diff(z,q_3)
% z_q4_dot = diff(z,q_4)

x_q1_dot = (q_4*(cos(q_1)*cos(q_2) + cos(az)*sin(q_1)*sin(q_2))*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2)/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2) - (q_4*(cos(q_1)*cos(q_2) + cos(az)*sin(q_1)*sin(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2)
x_q1_dot_s = -(q_4*sin(az)^2*sin(q_2)^2*(cos(q_1)*cos(q_2) + cos(az)*sin(q_1)*sin(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2)

x_q2_dot = (q_4*(sin(q_1)*sin(q_2) + cos(az)*cos(q_1)*cos(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2) + (q_4*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))*(2*cos(q_1)^2*cos(q_2)*sin(az)^2*sin(q_2) - 2*(sin(q_1)*sin(q_2) + cos(az)*cos(q_1)*cos(q_2))*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2)) + 2*cos(q_2)*sin(az)^2*sin(q_1)^2*sin(q_2)))/(2*((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2))
x_q2_dot_s = (q_4*sin(az)^2*sin(q_1)*sin(q_2))/(- cos(az)^2*cos(q_1)^2*cos(q_2)^2 + cos(az)^2*cos(q_1)^2 + cos(az)^2*cos(q_2)^2 - cos(az)^2 - 2*sin(q_1)*sin(q_2)*cos(az)*cos(q_1)*cos(q_2) - cos(q_1)^2*cos(q_2)^2 + 1)^(3/2)
 
x_q3_dot_s = 0
x_q4_dot_s = -(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2)
 
y_q1_dot = - (q_4*sin(az)*sin(q_1)*sin(q_2))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2) - (q_4*cos(q_1)*sin(az)*sin(q_2)*(cos(q_1)*cos(q_2) + cos(az)*sin(q_1)*sin(q_2))*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2)
y_q1_dot_s = -(q_4*sin(az)*sin(q_2)*(cos(q_2)^2*sin(q_1) + sin(az)^2*sin(q_1)*sin(q_2)^2 - cos(az)*cos(q_1)*cos(q_2)*sin(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2)

y_q2_dot = (q_4*cos(q_1)*cos(q_2)*sin(az))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2) - (q_4*cos(q_1)*sin(az)*sin(q_2)*(2*cos(q_1)^2*cos(q_2)*sin(az)^2*sin(q_2) - 2*(sin(q_1)*sin(q_2) + cos(az)*cos(q_1)*cos(q_2))*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2)) + 2*cos(q_2)*sin(az)^2*sin(q_1)^2*sin(q_2)))/(2*((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2))
y_q2_dot_s = (q_4*cos(q_1)*sin(az)*sin(q_1)*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2)
 
y_q3_dot_s = 0
y_q4_dot_s = (cos(q_1)*sin(az)*sin(q_2))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2)
 
z_q1_dot = (q_4*cos(q_1)*sin(az)*sin(q_2))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2) - (q_4*sin(az)*sin(q_1)*sin(q_2)*(cos(q_1)*cos(q_2) + cos(az)*sin(q_1)*sin(q_2))*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2)
z_q1_dot_s = (q_4*sin(az)*sin(q_2)^2*(cos(q_1)*sin(q_2) - cos(az)*cos(q_2)*sin(q_1)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2)
 
z_q2_dot = (q_4*cos(q_2)*sin(az)*sin(q_1))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2) - (q_4*sin(az)*sin(q_1)*sin(q_2)*(2*cos(q_1)^2*cos(q_2)*sin(az)^2*sin(q_2) - 2*(sin(q_1)*sin(q_2) + cos(az)*cos(q_1)*cos(q_2))*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2)) + 2*cos(q_2)*sin(az)^2*sin(q_1)^2*sin(q_2)))/(2*((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2))
z_q2_dot_s = (q_4*sin(az)*sin(q_1)^2*(cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2)))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(3/2)
 
z_q3_dot_s = 0
z_q4_dot_s = (sin(az)*sin(q_1)*sin(q_2))/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + cos(q_1)^2*sin(az)^2*sin(q_2)^2 + sin(az)^2*sin(q_1)^2*sin(q_2)^2)^(1/2)

syms c_1 c_2 c_3 c_4 c_az s_1 s_2 s_3 s_4 s_az real

old_s = [cos(q_1), cos(q_2), cos(q_3), cos(q_4), cos(az), sin(q_1), sin(q_2), sin(q_3), sin(q_4), sin(az)];
new_s = [c_1, c_2, c_3, c_4, c_az, s_1, s_2, s_3, s_4, s_az];
x_q1_dot_sb = subs(x_q1_dot_s, old_s, new_s);
x_q2_dot_sb = subs(x_q2_dot_s, old_s, new_s);
x_q3_dot_sb = subs(x_q3_dot_s, old_s, new_s);
x_q4_dot_sb = subs(x_q4_dot_s, old_s, new_s);

y_q1_dot_sb = subs(y_q1_dot_s, old_s, new_s);
y_q2_dot_sb = subs(y_q2_dot_s, old_s, new_s);
y_q3_dot_sb = subs(y_q3_dot_s, old_s, new_s);
y_q4_dot_sb = subs(y_q4_dot_s, old_s, new_s);

z_q1_dot_sb = subs(z_q1_dot_s, old_s, new_s);
z_q2_dot_sb = subs(z_q2_dot_s, old_s, new_s);
z_q3_dot_sb = subs(z_q3_dot_s, old_s, new_s);
z_q4_dot_sb = subs(z_q4_dot_s, old_s, new_s);

J = [x_q1_dot_sb x_q2_dot_sb x_q3_dot_sb x_q4_dot_sb;
    y_q1_dot_sb y_q2_dot_sb y_q3_dot_sb y_q4_dot_sb;
    z_q1_dot_sb z_q2_dot_sb z_q3_dot_sb z_q4_dot_sb];

lambda = sin(q_2)*cos(az)*cos(q_1)-sin(q_1)*cos(q_2)
lambda_q1 = diff(lambda,q_1)
lambda_q2 = diff(lambda,q_2)
lambda_q3 = diff(lambda,q_3)
lambda_q4 = diff(lambda,q_4)

n = (lambda^2+(sin(az)*sin(q_2))^2)^0.5
n_q1 = diff(n,q_1)
n_q2 = diff(n,q_2)
n_q3 = diff(n,q_3)
n_q4 = diff(n,q_4)

n_q1_sb = subs(n_q1, old_s, new_s)
n_q2_sb = subs(n_q2, old_s, new_s)


test1=-sin(q_1)*lambda^2-sin(az)^2*sin(q_1)*sin(q_2)^2+lambda*cos(q_1)^2*cos(q_2)+lambda*sin(q_1)* sin(q_2)* cos(az)* cos(q_1)
test2=sin(q_1)* cos(q_2)^2- sin(q_2)* cos(az)* cos(q_1)* cos(q_2)+ sin(az)^2 *sin(q_1)* sin(q_2)^2

t1=symfun(test1,[q_1,q_2,az])
t2=symfun(test2,[q_1,q_2,az])

eval(t1(30,30,45))
eval(t2(30,30,45))