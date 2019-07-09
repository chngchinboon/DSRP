import sympy as sp

q1, q2, q3, q4, q4a, q4b = sp.symbols('q1 q2 q3 q4 q4a q4b')
c1, c2, s1, s2 = sp.symbols('c1 c2 s1 s2')


J = sp.Matrix([[0, s1**2*c2*q4a+c1**2*c2*q4a, 0, s2],
               [-c1*c2*q4, s1*s2*q4, 0, -s1*c2],
               [-s1*c2*q4, -c1*s2*q4, 0, c1*c2],
               [0, 0, 1, 0]])

J1=J.subs(q4,q4a)
J2=J.subs(q4,q4b)
