from endobot import endobot_fk
from boon_sp_gen import *
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# setup 
# generate list of values with combinations of q1 and q2 from 0-180 degree


numpoints = 20
adiff = 85
mina = 90 - adiff
maxa = 90 + adiff

stepsize = (maxa - mina)/ numpoints

anglevectd = np.linspace(mina,maxa,numpoints)
anglevectrad = np.deg2rad(anglevectd)
meshx, meshy = np.meshgrid(anglevectrad,anglevectrad)
q3 = np.zeros(meshx.shape)
q4 = 100*np.ones(meshx.shape)

# q = np.dstack((meshx,meshy,q3,q4)).reshape(np.multiply(*meshx.shape),4)

# load position expression
endo_step, endo_final = endobot_fk()
# rotx = sp.eye(4)
# rotx[0:3,0:3] = sp.rot_axis3(np.pi/2)
# endo_final = rotx*endo_final

mechanism = DRSP()
mechanism.populate()
azimuth = np.pi / 2
az = azimuth * np.ones(meshx.shape)
boon_T0E = mechanism.func_T0E_M

q_1, q_2, q_3, q_4 = sp.symbols('q_1 q_2 q_3 q_4')

fklist = [endo_final, boon_T0E]
clist = ['g', 'b']
titlelist = ['final', 'boon']


q_boon = np.dstack((meshx, meshy, q3, q4, az)).reshape(np.multiply(*meshx.shape), 5)
q_endobot = np.dstack((meshx+np.pi/2, meshy+np.pi/2, q3, q4)).reshape(np.multiply(*meshx.shape), 4)

fig = plt.figure()
ax = Axes3D(fig)
ax.set_proj_type('ortho')
ax.set_title('Workspace comparison')
ax.set_xlabel('X', labelpad=10, fontsize=20)
ax.set_ylabel('Y', labelpad=10, fontsize=20)
ax.set_zlabel('Z', labelpad=10, fontsize=20)
ax.set_aspect('equal')
plt_labels = ['DRSP', 'Endobot']

for idx,fk in enumerate(fklist):
    if idx == 1:
        traj = np.array([boon_T0E(*joint_pos)[0:3, 3] for joint_pos in q_boon])
        boon_data = traj.copy()
    else:
        func = sp.lambdify((q_1, q_2, q_3, q_4), fk, 'numpy')
        traj = np.array([func(*joint_pos)[0:3, 3] for joint_pos in q_endobot[:,0:4]])
        endobot_data = traj.copy()
    ax.scatter(traj[:, 0], traj[:, 1], traj[:, 2], c=clist[idx], label = plt_labels[idx])


    # ax.plot_surface(traj[:, 0].reshape(*meshx.shape), traj[:, 1].reshape(*meshx.shape), traj[:, 2].reshape(*meshx.shape), rstride = 1,cstride=1
    #     ,alpha = 0.5)
    surface = traj.reshape(*meshx.shape,3)
    rows,cols = meshx.shape
    for row in range(rows):
        x = surface[:,row,:][:,0]
        y = surface[:,row,:][:,1]
        z = surface[:,row,:][:,2]
        ax.plot3D(x,y,z,color = clist[idx], label='_nolegend_')

    for column in range(cols):
        x = surface[column, :, :][:,0]
        y = surface[column, :, :][:,1]
        z = surface[column, :, :][:,2]
        ax.plot3D(x, y, z, color=clist[idx], label='_nolegend_')

set_axes_equal(ax)
ax.view_init(elev=16, azim=45) # iso

# ax.view_init(elev=0, azim=0) #YZ
# ax.set_xlabel('')
# ax.set_xticks([])

# ax.view_init(elev=0, azim=90) #XZ
# ax.set_ylabel('')
# ax.set_yticks([])

# ax.view_init(elev=90, azim=90) #XY
# ax.set_zlabel('')
# ax.set_zticks([])

ax.legend(loc='best')

fig2 = plt.figure()
ax2 = Axes3D(fig2)
ax2.set_proj_type('ortho')
ax2.set_title('Error')
ax2.set_xlabel('X', labelpad=10, fontsize=20)
ax2.set_ylabel('Y', labelpad=10, fontsize=20)
ax2.set_zlabel('Z', labelpad=10, fontsize=20)
ax2.set_aspect('equal')

kin_error = (boon_data - endobot_data).reshape(*meshx.shape,3)

abs_error = ((kin_error**2).sum(axis=2))**0.5

ax2.plot_surface(np.rad2deg(meshx), np.rad2deg(meshy), abs_error, linewidth=0, antialiased=False)


fig3, ax3 = plt.subplots()
ax3.set_title('Kinematic Differences')
z = np.nan_to_num(abs_error)
z_min, z_max = np.abs(z).min(), np.abs(z).max()
c = ax3.pcolormesh(np.rad2deg(meshx), np.rad2deg(meshy), abs_error, cmap='jet', vmin=z_min, vmax=z_max)
fig.colorbar(c, ax=ax3)
plt.show()
