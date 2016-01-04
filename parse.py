import re,sys,csv
import matplotlib.pyplot as plt
import numpy as np
def smooth(x,window_len=11,window='hanning'):
    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    if window == 'flat': #moving average
      w=np.ones(window_len,'d')
    else:
      w=eval('np.'+window+'(window_len)')
    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

ch1=[]
ch2=[]
ch3=[]
ch4=[]
ch5=[]

ch7=[]
ch8=[]
ch9=[]
ch10=[]
ch11=[]
ch12=[]
with open('sample_pressure_wave','r') as f:
    reader = csv.reader(f, delimiter=',')
    i = 1
    for line in reader:
        if i<17:
            print('#')
        else:
            ch1.append(float(line[1]))
            ch2.append(float(line[2]))
            ch3.append(float(line[3]))
            ch4.append(float(line[4]))
            ch5.append(float(line[5]))
            ch7.append(float(line[6]))
            ch8.append(float(line[7]))
            ch9.append(float(line[8]))
            ch10.append(float(line[9]))
            ch11.append(float(line[10]))
            ch12.append(float(line[11]))
        i+=1
length=len(ch1)


ch1=(np.array(ch1)-1)*5/4
ch2=(np.array(ch2)-1)*5/4
ch3=(np.array(ch3)-1)*5/4
ch4=(np.array(ch4)-1)*5/4
ch5=(np.array(ch5)-1)*5/4
ch7=np.array(ch7)
ch8=np.array(ch8)
ch9=np.array(ch9)
ch10=np.array(ch10)
ch11=np.array(ch11)
ch12=np.array(ch12)

xs = 1./5000 * np.arange(length)

#plot the pressure wave in expansion room and compression room
plt.figure(num=1, figsize=(5, 8), dpi=120, facecolor='w', edgecolor='k')

plt.subplot(411)
pos = 0.02*np.sin(1.33*xs*6.28-1.6*3.14)
plt.axis([0,2,-.02,.02])
plt.title('Displacer position')
plt.plot(xs,pos,'g-')

plt.subplot(412)
vel = -0.02*6.28*1.33*np.cos(1.33*xs*6.28-1.6*3.14)
plt.axis([0,2,-.2,.2])
plt.title('Displaser velocity')
plt.plot(xs,vel,'g-')
  
plt.subplot(413)
plt.axis([0,2,0.5,2.5])
plt.plot(xs,ch1,'g-')
plt.plot(xs,ch2,'b-')
plt.xlabel('Time (sec)')
plt.ylabel('Pressure (Mpa)')
plt.title('Upside Pressure')

plt.subplot(414)
plt.axis([0,2,0.5,2.5])
plt.plot(xs,ch3,'g-')
plt.plot(xs,ch4,'b-')
plt.title('Downside pressure')

#plot pressure loss
plt.figure(num=3, figsize=(5, 8), dpi=120, facecolor='w', edgecolor='k')
plt.subplot(411)
plt.axis([0,2,-3000,3000])
up_loss_force = (ch1 - ch2) * 1000000 * 0.25 *3.14 * 0.12**2
plt.plot(xs,up_loss_force,'g-')
plt.title('Upside Loss force')

plt.subplot(412)
plt.axis([0,2,-3000,3000])
down_loss_force = (ch4 - ch3) * 1000000 * 0.25 *3.14 * 0.12**2
plt.plot(xs,down_loss_force,'g-')
plt.title('Downside Loss force')

plt.subplot(413)
plt.axis([0,2,-3000,3000])
total_loss_force = up_loss_force + down_loss_force
plt.plot(xs,total_loss_force,'g-')
plt.title('Total Loss force')

plt.subplot(414)
plt.axis([0,2,-3000,3000])
assist = (ch2 - ch3) * 1000000 * 0.25 *3.14 * 0.033**2
plt.plot(xs,assist,'g-')
plt.title('Assist force')

#plot motor load 
plt.figure(num=2, figsize=(5, 6), dpi=120, facecolor='w', edgecolor='k')
plt.subplot(211)
plt.axis([0,2,0,1000])
motor_load = np.multiply(np.subtract(ch7,ch8),ch10) + np.multiply(np.subtract(ch8,ch9),ch11)
motor_load_smooth = smooth(motor_load,80)

plt.plot(xs,motor_load,'g-')
plt.title('Motor load')

plt.subplot(212)
plt.axis([0,2,0,600])
xs_smooth = 2. / motor_load_smooth.size * np.arange(motor_load_smooth.size)
plt.plot(xs_smooth,motor_load_smooth,'g-')
plt.title('Motor load smoothed')

#plot total force
plt.figure(num=4, figsize=(5,8), dpi=120)
plt.subplot(311)
plt.axis([0,2,-3000,3000])
plt.plot(xs,assist+total_loss_force,'b-')
plt.title('Total force')

plt.subplot(312)
plt.axis([0,2,-500,500])
torque = (assist+total_loss_force) * vel
plt.plot(xs,torque,'b-')
plt.title('Total torque')

plt.subplot(313)
plt.axis([0,2,0,600])
xs_smooth = 2. / motor_load_smooth.size * np.arange(motor_load_smooth.size)
plt.plot(xs_smooth,motor_load_smooth,'r-')
plt.title('Motor load smoothed')

plt.show()

