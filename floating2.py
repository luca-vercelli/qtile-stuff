# Copyright (c) 2010 matt
# Copyright (c) 2010-2011 Paul Colomiets
# Copyright (c) 2011 Mounier Florian
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2012, 2014-2015 Tycho Andersen
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2013 Julien Iguchi-Cartigny
# Copyright (c) 2014 ramnes
# Copyright (c) 2014 Sean Vig
# Copyright (c) 2014 dequis
# Copyright (c) 2018 Nazar Mokrynskyi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import warnings

from libqtile.config import Match
from libqtile.layout.base import Layout
from libqtile.layout.floating import Floating
from libqtile.log_utils import logger


class Floating2(Floating):
    """
    Floating layout
    Differently from Floating, there is no special handlng of Qtile for this layout
    """

    defaults = [
        ("border_focus", "#0000ff", "Border colour for the focused window."),
        ("border_normal", "#000000", "Border colour for un-focused windows."),
        ("border_width", 1, "Border width."),
        ("max_border_width", 0, "Border width for maximize."),
        ("fullscreen_border_width", 0, "Border width for fullscreen."),
    ]

    def __init__(self, float_rules=None, **config):
        Layout.__init__(self, **config)
        self.clients = []
        self.focused = None
        self.group = None
        self.no_reposition_rules = []   #useless

        self.add_defaults(Floating2.defaults)

    def cmd_next(self):
        # LV
        from libqtile import qtile
        #logger.info("Qtile groups: {}".format([g.windows for g in qtile.groups]))
        logger.info("Info: {}".format(self.info()))
        if self.group is not None:
            clients = self.find_clients(self.group)
            #logger.info("Clients: {}".format([c.window.wid for c in clients]))
            if len(clients) > 1:
                win = self.group.current_window
                logger.info("Top window was: {}".format(self.group.current_window.window.wid))
                index = clients.index(win)
                index = (index + 1) % len(clients)
                logger.info("Trying to raise window: {}".format(clients[index].window.wid))
                # don't use cmd_bring_to_front(), because it activates Floating
                self.win_bring_to_front(clients[index])

    def win_bring_to_front(self, win):
        """ Replacement for Window.cmd_bring_to_front() """
        self.group.current_window = win
        win.place(
            win.x, win.y,
            win.width, win.height,
            win.borderwidth,
            win.bordercolor,
            above=True,
        )

    def cmd_previous(self):
        # LV
        if self.group is not None:
            clients = self.find_clients(self.group)
            if len(clients) > 1:
                win = self.group.current_window
                index = clients.index(win)
                index -= 1
                if index < 0:
                    index += len(clients)
                clients[index].cmd_bring_to_front()
