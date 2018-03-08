# PyPOFacetsMonolithicYW - Monostatic version
# Inspired by the software POFacets noGUI v2.2 in MATLAB

import sys
import math
import numpy as np

from datetime import datetime
from timeit import default_timer as timer
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


# @begin PyPOFacetsMonolithicYW
# @in  name  @as Name
# @in  fname @as CoordinatesFile  @URI file:{name}/coordinates.m
# @in  fname2 @as FacetsFile  @URI file:{name}/facets.m
# @out plot @as Plot
# @out e0 @as E0
# @out T1 @as T1
# @out R @as R
start = timer()
now = datetime.now().strftime("%Y%m%d%H%M%S")
print now
print("PyPOFacets - v0.1")
print("=================")
print "\nScript:", sys.argv[0]
# Read and print 3D model package
input_model = sys.argv[1]
print "\n3D Model:", input_model
# Read and print input data file: pattern -> input_data_file_xxx.dat
input_data_file = sys.argv[2]
print "\nInput data file:", input_data_file
# Open input data file and gather parameters
params = open(input_data_file, 'r')
# 1: radar frequency
# @begin CalculateWaveLength
# :in:  freq :as: Frequency
# :out: waveL :as: WaveLength
params.readline()
freq = int(params.readline())
print "\nThe radar frequency in Hz:", freq, "Hz"
c = 3e8
wave = c / freq
print "\nWavelength in meters:", wave, "m"
# @end CalculateWaveLength

# 2: correlation distance in meters
params.readline()
corr = int(params.readline())
print "\nCorrelation distance in meters:", corr, "m"
corel = corr / wave
# 3: standard deviation in meters
params.readline()
delstd = int(params.readline())
print "\nStandard deviation in meters:", delstd, "m"
delsq = delstd ** 2
bk = 2 * math.pi / wave
cfact1 = math.exp(-4 * bk ** 2 * delsq)
cfact2 = 4 * math.pi * (bk * corel) ** delsq
rad = math.pi / 180
Lt = 0.05
Nt = 5

# 4: incident wave polarization
# @begin CalculateIncidentWavePolarization
# :in: ipol :as: InputPolarization
# @out Et
# @out Ep
params.readline()
ipol = int(params.readline())
print "\nIncident wave polarization:", ipol
if ipol == 0:
    Et = 1 + 0j
    Ep = 0 + 0j
elif ipol == 1:
    Et = 0 + 0j
    Ep = 1 + 0j
else:
    print("erro")
Co = 1
# @end CalculateIncidentWavePolarization

# Processing 3D model
# @begin ReadModelCoordinates
# @in  name @as Name
# @in  fname @as CoordinatesFile  @URI file:{name}/coordinates.m
# @out xpts @as XPoints
# @out ypts @as YPoints
# @out zpts @as ZPoints
print "\nProcessing 3D model..."
name = input_model
fname = name + "/coordinates.m"
print "\n...", fname
coordinates = np.loadtxt(fname)
print coordinates
xpts = coordinates[:, 0]
print xpts
ypts = coordinates[:, 1]
print ypts
zpts = coordinates[:, 2]
print zpts
nverts = len(xpts)
print nverts
# @end ReadModelCoordinates

# @begin ReadFacetsModel
# @in  name @as Name
# @in  fname2 @as FacetsFile  @URI file:{name}/facets.m
# @out facets @as Facets
fname2 = name + "/facets.m"
print "\n...", fname2
facets = np.loadtxt(fname2)
print facets
# @end ReadFacetsModel

# @begin GenerateTransposeMatrix
# @in  facets @as Facets
# @out node1 @as Node1
# @out node1 @as Node2
# @out node3 @as Node3
# @out ntria @as NTria
nfcv = facets[:, 0]
print nfcv
node1 = facets[:, 1]
print node1
node2 = facets[:, 2]
print node2
node3 = facets[:, 3]
print node3
iflag = 0
ilum = facets[:, 4]
Rs = facets[:, 5]
ntria = len(node3)
print ntria
vind = [[node1[i], node2[i], node3[i]]
        for i in range(ntria)]
# @end GenerateTransposeMatrix

# @begin GenerateCoordinatesPoints
# @in  xpts @as XPoints
# @in  ypts @as YPoints
# @in  zpts @as ZPoints
# @out r @as Points
x = xpts
y = ypts
z = zpts
r = [[x[i], y[i], z[i]]
     for i in range(nverts)]
# @end GenerateCoordinatesPoints

# Start plot
# # @begin Plot3dGraphModel
# # @in  node1 @as Node1
# # @in  node1 @as Node2
# # @in  node3 @as Node3
# # @in  r @as Points
# # @out plot @as Plot
# start plot
# print "\n... start plot..."
# fig1 = plt.figure()
# ax = Axes3D(fig1)
# for i in range(ntria):
#     Xa = [int(r[int(vind[i][0])-1][0]), int(r[int(vind[i][1])-1][0]), int(r[int(vind[i][2])-1][0]), int(r[int(vind[i][0])-1][0])]
#     Ya = [int(r[int(vind[i][0])-1][1]), int(r[int(vind[i][1])-1][1]), int(r[int(vind[i][2])-1][1]), int(r[int(vind[i][0])-1][1])]
#     Za = [int(r[int(vind[i][0])-1][2]), int(r[int(vind[i][1])-1][2]), int(r[int(vind[i][2])-1][2]), int(r[int(vind[i][0])-1][2])]
#     ax.plot3D(Xa, Ya, Za)
#     # ax.plot(Xa, Ya, Za) # same above
#     # ax.plot_wireframe(Xa, Ya, Za) # one color
#     # ax.plot_surface(Xa, Ya, Za) # does not work
#     ax.set_xlabel("X Axis")
# ax.set_title("3D Model: " + input_model)
# plt.show()
# plt.close()
# # @end Plot3dGraphModel

# Oct 138 - Pattern Loop
# 5: start phi angle in degrees
params.readline()
pstart = int(params.readline())
print "\nStart phi angle in degrees:", pstart

# 6: stop phi angle in degrees
params.readline()
pstop = int(params.readline())
print "\nStop phi angle in degrees:", pstop

# 7: phi increment (step) in degrees
params.readline()
delp = int(params.readline())
print "\nPhi increment (step) in degrees:", delp

# 8: start theta angle in degrees
params.readline()
tstart = int(params.readline())
print "\nStart theta angle in degrees:", tstart

# 9: stop theta angle in degrees
params.readline()
tstop = int(params.readline())
print "\nStop theta angle in degrees:", tstop

# 10: theta increment (step) in degrees
params.readline()
delt = int(params.readline())
print "\nTheta increment (step) in degrees:", delt

# @begin CalculateRefsGeometryModel
# :in:  pstart :as: PStart
# :in:  pstop :as: PStop
# :in:  delp :as: InputDelP
# :in:  tstart :as: TStart
# :in:  tstop :as: TStop
# :in:  delt :as: InputDelT
# :in:  rad :as: Rad
# @out it @as IT
# @out ip @as IP
# @out delp @as DelP
# @out delt @as DelT
if delp == 0:
    delp = 1
if pstart == pstop:
    phr0 = pstart*rad

if delt == 0:
    delt = 1
if tstart == tstop:
    thr0 = tstart*rad

it = math.floor((tstop-tstart)/delt)+1
print(it)
ip = math.floor((pstop-pstart)/delp)+1
print(ip)
# @end CalculateRefsGeometryModel
params.close()

print("last step")
# @begin CalculateEdgesAndNormalTriangles
# @in  node1 @as Node1
# @in  node1 @as Node2
# @in  node3 @as Node3
# @in  r @as Points
# :out: areai :as: AreaI
# @out beta @as Beta
# @out alpha @as Alpha
areai = []
beta = []
alpha = []
# OctT 168 - Get edge vectors and normal from edge cross products
for i in range(ntria):
    A0 = ((r[int(vind[i][1])-1][0]) - (r[int(vind[i][0])-1][0]))
    A1 = ((r[int(vind[i][1])-1][1]) - (r[int(vind[i][0])-1][1]))
    A2 = ((r[int(vind[i][1])-1][2]) - (r[int(vind[i][0])-1][2]))
    A = [int(A0), int(A1), int(A2)]
    B0 = ((r[int(vind[i][2]) - 1][0]) - (r[int(vind[i][1]) - 1][0]))
    B1 = ((r[int(vind[i][2]) - 1][1]) - (r[int(vind[i][1]) - 1][1]))
    B2 = ((r[int(vind[i][2]) - 1][2]) - (r[int(vind[i][1]) - 1][2]))
    B = [int(B0), int(B1), int(B2)]
    C0 = ((r[int(vind[i][0]) - 1][0]) - (r[int(vind[i][2]) - 1][0]))
    C1 = ((r[int(vind[i][0]) - 1][1]) - (r[int(vind[i][2]) - 1][1]))
    C2 = ((r[int(vind[i][0]) - 1][2]) - (r[int(vind[i][2]) - 1][2]))
    C = [int(C0), int(C1), int(C2)]
    N = -(np.cross(B,A))
    print(N)

    # OctT 184 - Edge lengths for triangle "i"
    d = [np.linalg.norm(A), np.linalg.norm(B), np.linalg.norm(C)]
    ss = 0.5*sum(d)
    areai.append(math.sqrt(ss*(ss-np.linalg.norm(A))*(ss-np.linalg.norm(B))*(ss-np.linalg.norm(C))))
    Nn = np.linalg.norm(N)
    # unit normals
    N = N/Nn
    # 0 < beta < 180
    beta.append(math.acos(N[2]))
    # -180 < phi < 180
    alpha.append(math.atan2(N[1],N[0]))
# @end CalculateEdgesAndNormalTriangles

phi = []
theta = []
D0 = []
R = []
e0 = []
filename_R = "R_PyPOFacetsMonolithicYW_"+sys.argv[1]+"_"+sys.argv[2]+"_"+now+".dat"
print filename_R
filename_E0 = "E0_PyPOFacetsMonolithicYW_"+sys.argv[1]+"_"+sys.argv[2]+"_"+now+".dat"
print filename_E0
fileR = open(filename_R, 'w')
fileE0 = open(filename_E0, 'w')
fileR.write(now)
fileR.write("\n")
fileR.write(sys.argv[0])
fileR.write("\n")
fileR.write(sys.argv[1])
fileR.write("\n")
fileR.write(sys.argv[2])
fileR.write("\n")
fileR.write(str(freq))
fileR.write("\n")
fileR.write(str(corr))
fileR.write("\n")
fileR.write(str(delstd))
fileR.write("\n")
fileR.write(str(ipol))
fileR.write("\n")
fileR.write(str(pstart))
fileR.write("\n")
fileR.write(str(pstop))
fileR.write("\n")
fileR.write(str(delp))
fileR.write("\n")
fileR.write(str(tstart))
fileR.write("\n")
fileR.write(str(tstop))
fileR.write("\n")
fileR.write(str(delt))
fileR.write("\n")
fileE0.write(now)
fileE0.write("\n")
fileE0.write(sys.argv[0])
fileE0.write("\n")
fileE0.write(sys.argv[1])
fileE0.write("\n")
fileE0.write(sys.argv[2])
fileE0.write("\n")
fileE0.write(str(freq))
fileE0.write("\n")
fileE0.write(str(corr))
fileE0.write("\n")
fileE0.write(str(delstd))
fileE0.write("\n")
fileE0.write(str(ipol))
fileE0.write("\n")
fileE0.write(str(pstart))
fileE0.write("\n")
fileE0.write(str(pstop))
fileE0.write("\n")
fileE0.write(str(delp))
fileE0.write("\n")
fileE0.write(str(tstart))
fileE0.write("\n")
fileE0.write(str(tstop))
fileE0.write("\n")
fileE0.write(str(delt))
fileE0.write("\n")
for i1 in range(0, int(ip)):
    for i2 in range(0, int(it)):
        # Global angles and direction cosines
        # @begin CalculateGlobalAnglesAndDirections
        # @in  ip @as IP
        # @in  it @as IT
        # :in:  pstart :as: PStart
        # @in  delp @as DelP
        # :in:  rad :as: Rad
        # :in:  tstart :as: TStart
        # @in  delt @as DelT
        # :in:  phi :as: Phi
        # :in:  theta :as: Theta
        # @out u @as U
        # @out v @as V
        # @out w @as W
        # @out uu @as UU
        # @out vv @as VV
        # @out ww @as WW
        # @out sp @as SP
        # @out cp @as CP
        # @out D0 @as D0
        phi.append(pstart+i1*delp)
        phr = phi[i2]*rad
        theta.append(tstart+i2*delt)
        thr = theta[i2]*rad
        st = math.sin(thr)
        ct = math.cos(thr)
        cp = math.cos(phr)
        sp = math.sin(phr)
        u = st*cp
        v = st*sp
        w = ct
        D0.append([u, v, w])
        U = u
        V = v
        W = w
        uu = ct*cp
        vv = ct*sp
        ww = -st
        # @end CalculateGlobalAnglesAndDirections

        # Spherical coordinate system radial unit vector
        # @begin CalculateSphericalCoordinateSystemRadialUnitVector
        # @in  u @as U
        # @in  v @as V
        # @in  w @as W
        # @out R @as R
        fileR.write(str(i2))
        fileR.write(" ")
        fileR.write(str([u, v, w]))
        fileR.write("\n")
        R.append([u, v, w])
        # @end CalculateSphericalCoordinateSystemRadialUnitVector

        # Incident field in global Cartesian coordinates
        # @begin CalculateIncidentFieldInGlobalCartesianCoordinates
        # @in  uu @as UU
        # @in  vv @as VV
        # @in  ww @as WW
        # @in  Et @as Et
        # @in  Ep @as Ep
        # @in  sp @as SP
        # @in  cp @as CP
        # @out e0 @as E0
        fileE0.write(str(i2))
        fileE0.write(" ")
        fileE0.write(str([(uu * Et - sp * Ep), (vv * Et + cp * Ep), (ww * Et)]))
        fileE0.write("\n")
        e0.append([(uu*Et-sp*Ep), (vv*Et+cp*Ep), (ww*Et)])
        # print(e0)
        # e0.append(vv*Et+cp*Ep)
        # e0.append(ww*Et)
        # @end CalculateIncidentFieldInGlobalCartesianCoordinates

        # Begin loop over triangles
        sumt = 0
        sump = 0
        sumdt = 0
        sumdp = 0
        for m in range(ntria):
            # OctT 236
            # Test to see if front face is illuminated: FUT
            # Local direction cosines
            # @begin CalculateIlumFaces
            # @in  ntria @as NTria
            # @in D0 @as D0
            # @in ip @as IP
            # @in alpha @as Alpha
            # @in beta @as Beta
            # @out T1 @as T1
            ca = math.cos(alpha[m])
            sa = math.sin(alpha[m])
            cb = math.cos(beta[m])
            sb = math.sin(beta[m])
            T1 = []
            T1 = [[ca, sa, 0], [-sa, ca, 0], [0, 0, 1]]
            T2 = []
            T2 = [[cb, 0, -sb], [0, 1, 0], [sb, 0, cb]]
            Dzero = np.array(D0[i1])
            D1 = T1*Dzero.transpose()
            D2 = T2*D1
            # @end CalculateIlumFaces
fileR.close()
fileE0.close()
end = timer()
print end - start, "seg"

# @end PyPOFacetsMonolithicYW