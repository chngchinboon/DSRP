syms c_1 c_2 c_3 c_4 c_az s_1 s_2 s_3 s_4 s_az real


dt11 = (m_t*sin(az)^2*sin(q_2)^2*(l_t + q_4)^2*(cos(q_2)^2*sin(q_1) + sin(az)^2*sin(q_1)*sin(q_2)^2 - cos(az)*cos(q_1)*cos(q_2)*sin(q_2))^2)/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + sin(az)^2*sin(q_2)^2)^3 + (m_t*sin(az)^2*sin(q_2)^4*(l_t + q_4)^2*(cos(q_1)*sin(q_2) - cos(az)*cos(q_2)*sin(q_1))^2)/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + sin(az)^2*sin(q_2)^2)^3 + (m_t*sin(az)^4*sin(q_2)^4*(l_t + q_4)^2*(cos(q_1)*cos(q_2) + cos(az)*sin(q_1)*sin(q_2))^2)/((cos(q_2)*sin(q_1) - cos(az)*cos(q_1)*sin(q_2))^2 + sin(az)^2*sin(q_2)^2)^3
dt11_s = subs(dt11, old_s, new_s);

(m_t*s_2^2*s_az^2*(l_t + q_4)^2*(s_1*c_2^2 - c_1*c_az*c_2*s_2 + s_1*s_2^2*s_az^2)^2)/(s_2^2*s_az^2 + (c_2*s_1 - c_1*c_az*s_2)^2)^3 + (m_t*s_2^4*s_az^2*(c_1*s_2 - c_2*c_az*s_1)^2*(l_t + q_4)^2)/(s_2^2*s_az^2 + (c_2*s_1 - c_1*c_az*s_2)^2)^3 + (m_t*s_2^4*s_az^4*(c_1*c_2 + c_az*s_1*s_2)^2*(l_t + q_4)^2)/(s_2^2*s_az^2 + (c_2*s_1 - c_1*c_az*s_2)^2)^3
 