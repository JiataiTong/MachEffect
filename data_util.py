
# This function is modified from RealtimeGraphingV5_with_logging.py by Hank Bethel
def get_voltage(board):
	channel_0 = board.a_in_read(0)
	channel_1 = board.a_in_read(1)
	channel_2 = board.a_in_read(2)
	channel_3 = board.a_in_read(3)
	channel_4 = board.a_in_read(4)
	channel_5 = board.a_in_read(5)
	channel_6 = board.a_in_read(6)
	channel_7 = board.a_in_read(7)
	# Change channel names below
	v1 = round(channel_6 - channel_4, 4)
	v2 = round(channel_4 - channel_2, 4)
	v3 = round(channel_2 - channel_0, 4)
	v4 = round(channel_1 - channel_0, 4)
	v5 = round(channel_1 - channel_7, 4)
	v6 = round(channel_7 - channel_3, 4)
	sr = round(channel_3 - channel_5, 4)
	return v1, v2, v3, v4, v5, v6, sr
