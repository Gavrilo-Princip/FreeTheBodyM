#!/usr/bin/bash

#
#   This file is part of BodyMedia/bm_gui
#   BodyMedia/src/bm_gui/build_qt.sh
#
#
#   This script is only to convert the ui-code to python-code
#
#   Copyright (C) 2015  Kaj-Sören Grunow
#   Contact: bloody_wulf@mailbox.org
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA,
#   or look here: http://www.gnu.org/licenses/gpl.html
#


pyuic5 ./src/gui/ui/window.ui > ./src/gui/ui/window_ui.py
