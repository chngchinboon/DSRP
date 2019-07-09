clc
clear all
syms q_4 az q_1 q_2 q_3 n lambda real
syms l_r l_t real
syms I_rx I_ry I_rz real
syms I_tx I_ty I_tz real
syms m_r m_t real
syms g real

p = [sin(q_2)*q_4; -sin(q_1)*cos(q_2)*q_4; cos(q_1)*cos(q_2)*q_4]

J = [0 sin(q_1)^2*cos(q_2)*q_4 0 sin(q_2);
    -cos(q_1)*cos(q_2)*q_4 sin(q_1)*sin(q_2)*q_4 0 -sin(q_1)*cos(q_2);
    -sin(q_1)*cos(q_2)*q_4 -cos(q_1)*sin(q_2)*q_4 0 cos(q_1)*cos(q_2);
    1 0 sin(q_2) 0;
    0 cos(q_1) -sin(q_1)*cos(q_2) 0;
    0 sin(q_2) cos(q_1)*cos(q_2) 0]

J_R = subs(J,[q_4],[l_r])
I_R = eye(3).*[I_rx I_ry I_rz]'
M_R = eye(6)*m_r
M_R(4:6,4:6) = I_R

J_T = subs(J,[q_4],[l_t])
I_T = eye(3).*[I_tx I_ty I_tz]'
M_T = eye(6)*m_t
M_T(4:6,4:6) = I_T

T_t = J_T'*M_T*J_T

T_r = J_R'*M_R*J_R

p_r = subs(p,[q_4],[l_r])
p_t = subs(p,[q_4],[l_t])

P_t = m_t*p*g

P_r = m_r*p*g