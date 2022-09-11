# FTP-629-Printer
Thermal till roll printer demo program

Demonstration using ESP32 to drive RS232 signals via adapter to controller board for Fujitsu FTP-629 

Uses arduino library https://github.com/gdsports/ESC_POS_Printer/blob/master/ESC_POS_Printer.cpp

Repurposed to drive second serial port on ESP32 microcontroller, USB port used for usual status info etc.

###Connections
![Alt text](./images/ConnectorView.png)

| No.| Func|Note |
|----|-----|-----|
|  1 | +ve | 24V |
|  2 | CTS | In  |
|  3 | RTS | Out |
|  4 | +ve | 24V |
|  5 | -ve | gnd |
|  6 | RxD | In  |
|  7 | TxD | Out |
|  8 | -ve | gnd |

### Test program

[Arduino sketch](./A_printertest)

### Initial printout

![Alt text](./images/PrintSampleInitial.png)


