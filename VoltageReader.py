import time

from daqhats import hat_list, HatIDs, mcc118
import daqhats


class VoltageReader:
    def __init__(self, board_index):
        self.index = board_index
        if not hat_list(filter_by_id=board_index):
            self.board = None
        else:
            self.board = mcc118(board_index)


    def get_voltage(self):
        # modified from RealtimeGraphingV5_with_logging.py by Hank Bethel
        channel_0 = self.board.a_in_read(0)
        channel_1 = self.board.a_in_read(1)
        channel_2 = self.board.a_in_read(2)
        channel_3 = self.board.a_in_read(3)
        channel_4 = self.board.a_in_read(4)
        channel_5 = self.board.a_in_read(5)
        channel_6 = self.board.a_in_read(6)
        channel_7 = self.board.a_in_read(7)
        # Change  channel names below
        v1 = round(channel_6 - channel_4, 4)
        v2 = round(channel_4 - channel_2, 4)
        v3 = round(channel_2 - channel_0, 4)
        v4 = round(channel_1 - channel_0, 4)
        v5 = round(channel_1 - channel_7, 4)
        v6 = round(channel_7 - channel_3, 4)
        sr = round(channel_3 - channel_5, 4)
        ret_list = [v1, v2, v3, v4, v5, v6, sr]
        return ret_list