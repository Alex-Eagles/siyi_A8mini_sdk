class utils:
    
    def int_to_hex_array_uint16(self,num):
        # Convert integer to 16-bit two's complement, using little-endian mode
        hex_bytes = num.to_bytes(2, byteorder='little', signed=True)
    
        # Convert each byte to hexadecimal representation
        # hex_array = [f"0x{byte:02x}" for byte in hex_bytes]
        return [(hex_bytes[0]), (hex_bytes[1])]
    
    def int_to_hex_array_uint8(self,num):
        # Convert integer to 8-bit signed number, using little-endian mode
        hex_bytes = num.to_bytes(1, byteorder='little', signed=True)
    
        # Return byte value
        return [hex_bytes[0]]
        




