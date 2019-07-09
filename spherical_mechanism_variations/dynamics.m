clc
clear all
syms q_4 az q_1 q_2 q_3 n lambda real
syms l_r l_t real
syms I_rx I_ry I_rz real
syms I_tx I_ty I_tz real
syms m_r m_t real
syms g

old_s = [cos(q_1), cos(q_2), cos(q_3), cos(q_4), cos(az), sin(q_1), sin(q_2), sin(q_3), sin(q_4), sin(az)];
syms c_1 c_2 c_3 c_4 c_az s_1 s_2 s_3 s_4 s_az real
new_s = [c_1, c_2, c_3, c_4, c_az, s_1, s_2, s_3, s_4, s_az];

lambda = sin(q_2)*cos(az)*cos(q_1) - sin(q_1) * cos(q_2)
n = (lambda^2+(sin(az)*sin(q_2))^2)^0.5

P = q_4/n* [lambda; sin(az)*sin(q_2)*cos(q_1); sin(az)*sin(q_1)*sin(q_2)]

J = [-(q_4*sin(az)^2*sin(q_2)^2*(cos(q_1)*cos(q_2)+cos(az)*sin(q_1)*sin(q_2)))/n^3 (q_4*sin(az)^2*sin(q_2)*sin(q_1))/n^3 0 lambda/n;
    (q_4*sin(az)*sin(q_2)*(sin(q_2)*cos(az)*cos(q_1)*cos(q_2)-sin(q_1)*cos(q_2)^2-sin(az)^2*sin(q_1)*sin(q_2)^2))/n^3 (q_4*sin(az)*sin(q_1)*cos(q_1)*lambda)/n^3 0 (sin(az)*sin(q_2)*cos(q_1))/n; 
    (q_4*sin(az)*sin(q_2)^2*(sin(q_2)*cos(q_1)- sin(q_1)*cos(az)*cos(q_2)))/n^3 (q_4*sin(az)*sin(q_1)^2*lambda)/n^3 0 (sin(az)*sin(q_1)*sin(q_2))/n;
    1 cos(az) (q_4*lambda)/n 0;
    sin(az) cos(q_1) (q_4*sin(az)*sin(q_2)*cos(q_1))/n 0;
    0 sin(q_1) (q_4*sin(az)*sin(q_1)*sin(q_2))/n 0]

%% kinetic energy
J_R = subs(J,[q_4],[l_r])
J_Rv = J_R(1:3,1:4)
M_R = eye(3)*m_r
% M_R(4:6,4:6) = I_R

J_T = subs(J,[q_4],[l_t+q_4])
J_Tv = J_T(1:3,1:4)

M_T = eye(3)*m_t
% M_T(4:6,4:6) = I_T

% linear velocity
T_tv = J_Tv'*M_T*J_Tv
T_rv = J_Rv'*M_R*J_Rv

T_t_s = subs(T_tv, old_s, new_s);
T_r_s = subs(T_rv, old_s, new_s);

% rotational velocity
I_T = eye(3).*[I_tx I_ty I_tz]';
J_Tw = J_T(4:6,1:4);
T_tw = J_Tw'*I_T*J_Tw;

I_R = eye(3).*[I_rx I_ry I_rz]';
J_Rw = J_R(4:6,1:4);
T_rw = J_Rw'*I_R*J_Rw;

% total
T_v = T_tv+T_rv
T_w = T_tw+T_rw
T = T_v + T_w
T_s = subs(T, old_s, new_s);

%% potential energy
p_r = subs(P,[q_4],[l_r])
p_t = subs(P,[q_4],[l_t+q_4])

P_t = m_t*p_r(3)*g

P_r = m_r*p_t(3)*g

P_final = P_t + P_r

g_q = [diff(P_final,q_1);diff(P_final,q_2);diff(P_final,q_3);diff(P_final,q_4)]
g_q_s = subs(g_q, old_s, new_s);

%% Christoffel
q=[q_1;q_2;q_3;q_4]
n = 4

c=sym(zeros(n,n,n));
for i=1:n
    for j=1:n
        for k=1:n
            c(i,j,k)=0.5*(diff(T(k,j),q(i)) + diff(T(k,i),q(j)) + diff(T(i,j),q(k)));
        end
    end
end

syms q_1dot q_2dot q_3dot q_4dot

C=sym(zeros(n,n));
for i=1:n
    for j=1:n
        C(i,j)=c(i,j,1)*q_1dot + c(i,j,2)*q_2dot +c(i,j,3)*q_3dot+c(i,j,4)*q_4dot;
    end
end

C_s = subs(C, old_s, new_s);
