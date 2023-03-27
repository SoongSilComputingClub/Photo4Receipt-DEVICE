from escpos.connections import getUSBPrinter


printer = getUSBPrinter()(idVendor=0x1fc9,
                          idProduct=0x2016,
                          inputEndPoint=0x81,
                          outputEndPoint=0x01) # Create the printer object with the connection params

# Print a image
printer.image('255.jpg')
printer.cutPaper()
printer.drawerKickPulse()