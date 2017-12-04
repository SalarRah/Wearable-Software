from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtWidgets, QtGui, QtCore

import time
import Cursor
import GUI
import Sensors
import State
import Shaders
import StickMan

import Definitions


eventKey = None
eventPress = None
eventModifier = None

lastTime = 0 # for time between frames

""" mouse controls """
mouse_click = False
setLookAt = False
rename = None
renameType = 0
caps = False
ctrl = False

""" camera/position/orientation controls """
leftRight_acceleration = 0
leftRight_keyHold = 0
leftRight_cam = 0
leftRight_cam_cap = 5
leftRight_pos_cap = 0.1
leftRight_ori_cap = 5

upDown_acceleration = 0
upDown_keyHold = 0
upDown_cam = 0
upDown_cam_cap = 5
upDown_pos_cap = 0.1
upDown_ori_cap = 5

frontBack_acceleration = 0
frontBack_keyHold = 0
frontBack_cam = -1.5
frontBack_cam_cap = 0.1
frontBack_pos_cap = 0.1
frontBack_ori_cap = 5

""" parts control """
pivot = [0,0,0]
pivotSpeed = 5.
q_keyHold = False
w_keyHold = False
e_keyHold = False
r_keyHold = False
t_keyHold = False
y_keyHold = False
reset = False # reset selected part orientation
prevNext = 0 # select previous/next part

""" sensors control """
incSens = [0,0,0] # [x,t,s]
z_keyHold = False
x_keyHold = False
c_keyHold = False
v_keyHold = False
b_keyHold = False
n_keyHold = False
resetSens = False
deleteSens = False

style = 0 # rendering style
SHOW = 0
FADE = 1
HIDE = 2
showBody = SHOW
showMuscles = True
showSensors = True
showSaturations = SHOW
showGround = True
rMax = 0 # ground radius

loadGroup = False
loadZoi = False

def manage():

    global eventKey
    global eventPress
    global eventModifier

    global lastTime

    global mouse_click
    global setLookAt
    global rename
    global caps
    global ctrl

    global leftRight_acceleration
    global leftRight_keyHold
    global leftRight_cam

    global upDown_acceleration
    global upDown_keyHold
    global upDown_cam
    
    global frontBack_acceleration
    global frontBack_keyHold
    global frontBack_cam

    global q_keyHold
    global w_keyHold
    global e_keyHold
    global r_keyHold
    global t_keyHold
    global y_keyHold
    global reset
    global prevNext
    
    global z_keyHold
    global x_keyHold
    global c_keyHold
    global v_keyHold
    global b_keyHold
    global n_keyHold
    global resetSens
    global incSens
    global deleteSens

    global style
    global showBody
    global showMuscles
    global showSensors
    global showSaturations
    global showGround
    global rMax

    global loadGroup
    global loadZoi

    dt = time.clock() - lastTime
    lastTime = time.clock()
    k = 18*dt # adjust speed to time instead of frame rate

    
    reset = False
    resetSens = False
    deleteSens = False
    prevNext = 0
    
    if loadGroup == True:
        State.loadGroups()
        loadGroup = False
    if loadZoi == True:
        State.loadZOI(GUI.selectedZoi)
        loadZoi = False
    if Sensors.newSens != []:
        Sensors.virtuSens = Sensors.virtuSens + Sensors.newSens
        Sensors.newSens = []

    """ New events """

    if eventKey != None:
        """ Exit """
        if eventKey == QtCore.Qt.Key_Escape:
            quit()
            
        """ Special keys """
        caps = (eventModifier == QtCore.Qt.ShiftModifier)
        ctrl = (eventModifier == QtCore.Qt.ControlModifier)
        if eventModifier == QtCore.Qt.ShiftModifier:
            upDown_acceleration = 0
            leftRight_acceleration = 0
            frontBack_acceleration = 0
            
        if eventModifier == QtCore.Qt.ControlModifier:
            upDown_acceleration = 0
            leftRight_acceleration = 0
            frontBack_acceleration = 0

        """ Camera/position/orientation controller """
        if eventPress == True and eventKey == QtCore.Qt.Key_Left:
            leftRight_keyHold = 1
            if leftRight_acceleration < 0.2:
                leftRight_acceleration = 0.2
        if eventPress == True and eventKey == QtCore.Qt.Key_Right:
            leftRight_keyHold = -1
            if leftRight_acceleration > -0.2:
                leftRight_acceleration = -0.2
        if eventPress == False and (eventKey == QtCore.Qt.Key_Left or eventKey == QtCore.Qt.Key_Right):
            leftRight_keyHold = 0
    
    
        if eventPress == True and eventKey == QtCore.Qt.Key_Up:
            upDown_keyHold = 1
            if upDown_acceleration < 0.2:
                upDown_acceleration = 0.2
        if eventPress == True and eventKey == QtCore.Qt.Key_Down:
            upDown_keyHold = -1
            if upDown_acceleration > -0.2:
                upDown_acceleration = -0.2
        if eventPress == False and (eventKey == QtCore.Qt.Key_Up or eventKey == QtCore.Qt.Key_Down):
            upDown_keyHold = 0
    
    
        if eventPress == True and eventKey == QtCore.Qt.Key_PageUp:
            frontBack_keyHold = 1
            if frontBack_acceleration < 0.2:
                frontBack_acceleration = 0.2
        elif eventPress == True and eventKey == QtCore.Qt.Key_PageDown:
            frontBack_keyHold = -1
            if frontBack_acceleration > -0.2:
                frontBack_acceleration = -0.2
        if eventPress == False and (eventKey == QtCore.Qt.Key_PageUp or eventKey == QtCore.Qt.Key_PageDown):
            frontBack_keyHold = 0
    
    
        if rename != None:
            pass
            #if eventPress == True:
            #    State.renameFile(pygame.key.name(eventKey))
        else:
            """ Stickman controller """ # WARNING : pygame uses qwerty by default !
            if eventPress == True and eventKey == QtCore.Qt.Key_Q:
                q_keyHold = True
                pivot[0] = pivotSpeed*k
            elif eventPress == False and eventKey == QtCore.Qt.Key_Q:
                q_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_W:
                w_keyHold = True
                pivot[0] = -pivotSpeed*k
            elif eventPress == False and eventKey == QtCore.Qt.Key_W:
                w_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_E:
                e_keyHold = True
                pivot[1] = pivotSpeed*k
            elif eventPress == False and eventKey == QtCore.Qt.Key_E:
                e_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_R:
                r_keyHold = True
                pivot[1] = -pivotSpeed*k
            elif eventPress == False and eventKey == QtCore.Qt.Key_R:
                r_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_T:
                t_keyHold = True
                pivot[2] = pivotSpeed*k
            elif eventPress == False and eventKey == QtCore.Qt.Key_T:
                t_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_Z:
                y_keyHold = True
                pivot[2] = -pivotSpeed*k
            elif eventPress == False and eventKey == QtCore.Qt.Key_Z:
                y_keyHold = False
    
            if eventPress == False and eventKey == QtCore.Qt.Key_Y:
                z_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_Y:
                z_keyHold = True
                incSens[0] = 0.025*k
            if eventPress == False and eventKey == QtCore.Qt.Key_X:
                x_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_X:
                x_keyHold = True
                incSens[0] = -0.025*k
            if eventPress == False and eventKey == QtCore.Qt.Key_C:
                c_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_C:
                c_keyHold = True
                incSens[1] = 5*k
            if eventPress == False and eventKey == QtCore.Qt.Key_V:
                v_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_V:
                v_keyHold = True
                incSens[1] = -5*k
            if eventPress == False and eventKey == QtCore.Qt.Key_B:
                b_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_B:
                b_keyHold = True
                incSens[2] = 5*k
            if eventPress == False and eventKey == QtCore.Qt.Key_N:
                n_keyHold = False
            if eventPress == True and eventKey == QtCore.Qt.Key_N:
                n_keyHold = True
                incSens[2] = -5*k
            if eventPress == True and eventKey == QtCore.Qt.Key_M:
                resetSens = True
    
            if eventPress == True and eventKey == QtCore.Qt.Key_U:
                reset = True
            if eventPress == True and eventKey == QtCore.Qt.Key_I:
                prevNext = 1
            if eventPress == True and eventKey == QtCore.Qt.Key_O:
                prevNext = -1
            if eventPress == True and eventKey == QtCore.Qt.Key_P:
                style = (style + 1)%4
            if eventPress == True and eventKey == QtCore.Qt.Key_1:
                showBody = (showBody+1)%3
            if eventPress == True and eventKey == QtCore.Qt.Key_2:
                showMuscles = not showMuscles
            if eventPress == True and eventKey == QtCore.Qt.Key_3:
                showSensors = not showSensors
            if eventPress == True and eventKey == QtCore.Qt.Key_4:
                showSaturations = (showSaturations+1)%3
            if eventPress == True and eventKey == QtCore.Qt.Key_5:
                showGround = not showGround
            if eventPress == True and eventKey == QtCore.Qt.Key_H:
                State.savePosture(StickMan.virtuMan)
            if eventPress == True and eventKey == QtCore.Qt.Key_A:
                State.saveGroups(State.saveGroupFile)
            if eventPress == True and eventKey == QtCore.Qt.Key_S:
                if GUI.selectedTemplate != "":
                    for sensorData in Sensors.sensorGraphics:
                        if GUI.selectedTemplate == sensorData.type:
                            sensorData.shape = (sensorData.shape - 1 + len(Definitions.packagePreprocess)) % len(Definitions.packagePreprocess)
                            State.saveTemplates(sensorData)
            if eventPress == True and eventKey == QtCore.Qt.Key_D:
                if GUI.selectedTemplate != "":
                    for sensorData in Sensors.sensorGraphics:
                        if GUI.selectedTemplate == sensorData.type:
                            sensorData.shape = (sensorData.shape + 1) % len(Definitions.packagePreprocess)
                            State.saveTemplates(sensorData)
            if eventPress == True and eventKey == QtCore.Qt.Key_Delete:
                deleteSens = True
            if eventPress == True and eventKey == QtCore.Qt.Key_G:
                rMax += 1
                if rMax > 6:
                    rMax = -5


    eventKey = None
    eventPress = None
    eventModifier = None

    """ Controller acceleration update - left / right """
    if leftRight_keyHold == 0:
        if leftRight_acceleration > 0.1:
            leftRight_acceleration -= 0.1
        elif leftRight_acceleration < -0.1:
            leftRight_acceleration += 0.1
        else:
            leftRight_acceleration = 0.
    elif leftRight_keyHold == 1:
        if leftRight_acceleration < 0.9:
            leftRight_acceleration += 0.1
        else:
            leftRight_acceleration = 1
    elif leftRight_keyHold == -1:
        if leftRight_acceleration > -0.9:
            leftRight_acceleration -= 0.1
        else:
            leftRight_acceleration = -1
            
    """ Controller acceleration update - up / down """
    if upDown_keyHold == 0:
        if upDown_acceleration > 0.1:
            upDown_acceleration -= 0.1
        elif upDown_acceleration < -0.1:
            upDown_acceleration += 0.1
        else:
            upDown_acceleration = 0.
    elif upDown_keyHold == 1:
        if upDown_acceleration < 0.9:
            upDown_acceleration += 0.1
        else:
            upDown_acceleration = 1
    elif upDown_keyHold == -1:
        if upDown_acceleration > -0.9:
            upDown_acceleration -= 0.1
        else:
            upDown_acceleration = -1

    """ Controller acceleration update - front / back """
    if frontBack_keyHold == 0:
        if frontBack_acceleration > 0.1:
            frontBack_acceleration -= 0.1
        elif frontBack_acceleration < -0.1:
            frontBack_acceleration += 0.1
        else:
            frontBack_acceleration = 0.
    elif frontBack_keyHold == 1:
        if frontBack_acceleration < 0.9:
            frontBack_acceleration += 0.1
        else:
            frontBack_acceleration = 1
    elif frontBack_keyHold == -1:
        if frontBack_acceleration > -0.9:
            frontBack_acceleration -= 0.1
        else:
            frontBack_acceleration = -1


    """ Apply camera/position/orientation control """
    if caps == True:
        StickMan.virtuMan.position[0] += leftRight_acceleration*leftRight_pos_cap*k
        StickMan.virtuMan.position[1] += upDown_acceleration*upDown_pos_cap*k
        StickMan.virtuMan.position[2] += frontBack_acceleration*frontBack_pos_cap*k
    elif ctrl == True:
        Q = Definitions.vector4D((StickMan.virtuMan.orientation))
        Qdelta = Definitions.vector4D.Eul2Quat(Definitions.vector4D((0,upDown_acceleration*upDown_ori_cap*k,
                                                                     frontBack_acceleration*frontBack_ori_cap*k,
                                                                     leftRight_acceleration*leftRight_ori_cap*k)))
        Q = Definitions.vector4D.QuatProd(Q, Qdelta)
        StickMan.virtuMan.orientation = [Q.o, Q.x, Q.y, Q.z]
    else:
        frontBack_cam += frontBack_acceleration*frontBack_cam_cap*k
        leftRight_cam += leftRight_acceleration*upDown_cam_cap*k
        upDown_cam += upDown_acceleration*leftRight_cam_cap*k
        # update camera in shader
        Definitions.viewMatrix.push()
        Definitions.viewMatrix.translate(0,0,frontBack_cam)
        Definitions.viewMatrix.rotate(upDown_cam, 1, 0, 0)
        Definitions.viewMatrix.rotate(leftRight_cam, 0, 1, 0)
        glUniformMatrix4fv(Shaders.view_loc, 1, GL_FALSE, Definitions.viewMatrix.peek())
        Definitions.viewMatrix.pop()


    """ limbs control """
    if q_keyHold == False and w_keyHold == False:
        pivot[0] = 0
    if e_keyHold == False and r_keyHold == False:
        pivot[1] = 0
    if t_keyHold == False and y_keyHold == False:
        pivot[2] = 0

    """ sensors control """
    if z_keyHold == False and x_keyHold == False:
        incSens[0] = 0
    if c_keyHold == False and v_keyHold == False:
        incSens[1] = 0
    if b_keyHold == False and n_keyHold == False:
        incSens[2] = 0
    
    """ Limbs Events """
    for j in range (0, len(StickMan.selectedLimbs)):
        for i in range (0,len(StickMan.virtuMan.limbs)):
            if StickMan.selectedLimbs[j] == StickMan.virtuMan.limbs[i].tag:
                if reset == True:
                    StickMan.virtuMan.limbs[i].twist = [1,0,0,0]
                    StickMan.virtuMan.limbs[i].swing = [1,0,0,0]
                    StickMan.virtuMan.limbs[i].angle = [1,0,0,0]
                if prevNext != 0:
                    StickMan.selectedLimbs[j] = StickMan.virtuMan.limbs[(i+prevNext+len(StickMan.virtuMan.limbs))% (len(StickMan.virtuMan.limbs))].tag
                break

        