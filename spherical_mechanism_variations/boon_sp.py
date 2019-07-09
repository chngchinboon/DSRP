import sympy as sp

def boon_sp():
    '''
    New formulation
    :return: H
    where H is the homogenous transformation matrix for the spherical system
    '''

    q_1, q_2, q_3, q_4 = sp.symbols('q_1 q_2 q_3 q_4')

    xhat = sp.Matrix([1,0,0]) # unit vector of x-axis
    yhat = sp.Matrix([0,1,0]) # unit vector of y-axis

    jyz =  sp.Matrix([0,sp.cos(q_1),sp.sin(q_1)]) # vector projection of joystick onto YZ plane. starts from positive y-axis and goes anti clockwise
    # jxz = [sin(q2),0,cos(q2)] # vector projection of joystick onto XZ plane.
    jxz =  sp.Matrix([-sp.cos(q_2),0,sp.sin(q_2)]) # vector projection of joystick onto XZ plane. starts from negative x-axis and goes anticlockwise
    # jxz = [cos(q2),0,sin(q2)] # vector projection of joystick onto XZ plane. starts from positive x-axis and goes clockwise

    XOE = xhat.cross(jyz) # normal vector used to define plane XOE
    YOE = yhat.cross(jxz) # normal vector used to define plane YOE
    jz = XOE.cross(YOE) # intersection of both planes, i.e. z-axis of joystick
    # normjz = simple((sum(jz.^2))^0.5) #(s1^2*s2^2 - s1^2 + 1)^(1/2)= (1-c1^2*s2^2)^(1/2)
    # normjz = (1-cos(q1)^2*sin(q2)^2)^0.5 # even more simplifed form #sala? should be (1 - cos(q1)^2*cos(q2)^2)^(1/2)
    normjz = jz.norm()
    normjz_simplified = sp.sqrt(1 - sp.cos(q_1)**2*sp.cos(q_2)**2)
    jzhat = jz/normjz_simplified # unit vector z-axis of joystick

    jyhat = -XOE # make x-axis of joystick to be on XOE plane. Since x & z-axis used to make xoe plane and y-axis has to perpendicular to both,
    # y-axis is thus perpendicular to XOE, i.e. the norm of XOE.
    # make x-axis to be on xoe plane, and hence to find y axis, cross(jyz,xhat) or y=z X x. therefore jyhat=-(XOE), !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    jxhat = jyhat.cross(jzhat) # already unit vector, since jzhat and jyhat are perpendicular and are unit vectors.

    R0S = sp.BlockMatrix([[jxhat, jyhat, jzhat]]).as_explicit()
    T0S = sp.BlockMatrix([[R0S, sp.zeros(3,1)], [sp.zeros(1,3), sp.eye(1)]]).as_explicit() # Transformation function for parallel system.

    TSE = sp.Matrix([[sp.cos(q_3), -sp.sin(q_3), 0, 0], [sp.sin(q_3), sp.cos(q_3), 0, 0], [0, 0, 1, q_4], [0, 0, 0, 1]]) # knob/yaw angle with height of joystick

    T0E = T0S*TSE # Forward kinematics

    return T0S,T0E
