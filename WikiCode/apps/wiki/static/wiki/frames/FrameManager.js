/*
    Copyright (C) 2016 Igor Soloduev <diahorver@gmail.com>

    This file is part of WikiCode.

    WikiCode is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    WikiCode is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with WikiCode.  If not, see <http://www.gnu.org/licenses/>.
*/

/**
 * Created by Igor on 29.01.2016.
 */

var FrameManager =
{
    registerFrame : function(frame)
    {
        pm({
          target: window.frames[frame.id],
          type:   "register",
          data:   {id:frame.id},
          url: frame.contentWindow.location
        });

        pm.bind(frame.id, function(data) {
            var iframe = document.getElementById(data.id);
            if (iframe == null) return;
            iframe.style.height = (data.height+12).toString() + "px";
        });
    }
};