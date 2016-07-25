import  pifacerelayplus
pfr = pifacerelayplus.PiFaceRelayPlus(pifacerelayplus.RELAY)
pfr.init_board({ 'value':      0, 'direction':  0x00, 'pullup':     0}, {   'value':      0, 'direction':  0x10, 'pullup':     0})
# Initialize the board. The first block controls the 4 relays. The second block controls the X_Port pins.
# In the Piface Relay Plus X Port, GPIOs can only be configured as OUTPUTs, so the direction is set to "00".
# Values are provided in hex. 
# The first nibble controls the direction of the four GPIOs in X_PORT. 
# I guess that the second nibble controls the other four GPIOs in the expansion port.


pfr.x_pins[2].toggle()  # Toggle the value for X1
pfr.x_pins[2].value		# Show the current value for X1

pfr.x_pins[3].toggle()	# Toggle the value for X0
pfr.x_pins[3].value     # Show the current value for X0

pfr.x_port.value		# Show the current state of the pins in the X Port header in hex
bin(pfr.x_port.value)   # Show the current state of the pins in the X Port header in binary


pfr.x_port.value = 0xB  # Set the X Port GPIOs to 1011 (OFF, ON, OFF, OFF)
pfr.x_port.value = 0x7  # Set the X Port GPIOs to 0111 (ON, OFF, OFF, OFF)
bin(pfr.x_port.value)   # Show the current state of the pins in the X Port header '0b111'
						# They are "0" (ommitted but it is there!) for X3, "1" for X2, etc.