# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error

comends = "LOGIN", "LOGOUT", "LOGGED", "GET_QUESTION", "LOGIN_OK"
def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	if cmd in comends:
		l_c = (16 - len(cmd))*" "
		full_msg = f"{cmd}{l_c}|{str(len(data)).zfill(4)}|{data}"
		return full_msg
	else:
		return ERROR_RETURN


def parse_message(data = ""):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	sp_da = data.split("|")
	if len(sp_da) != 3:
		return ERROR_RETURN ,ERROR_RETURN
	elif sp_da[1].strip().zfill(4) == str(len(sp_da[2])).zfill(4) and sp_da[0].strip() in comends:
		msg = sp_da[2]
		cmd = sp_da[0].strip()
		return cmd, msg
	else:
		return ERROR_RETURN ,ERROR_RETURN


	
def split_data(msg="", expected_fields=0):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	splited_msg = msg.split("|")[2]
	if len(splited_msg("#")) == expected_fields:
		return splited_msg("#")
	else:
		return ERROR_RETURN


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	return "#".join(msg_fields)