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

var FrameHeightManager =
{
    FrameId: '',
    getCurrentHeight : function()
    {
          myHeight = 0;

          if( typeof( window.innerWidth ) == 'number' ) {
            myHeight = window.innerHeight;
          } else if( document.documentElement && document.documentElement.clientHeight ) {
            myHeight = document.documentElement.clientHeight;
          } else if( document.body && document.body.clientHeight ) {
            myHeight = document.body.clientHeight;
          }

          return myHeight;
    },
    publishHeight : function()
    {
        if (this.FrameId == '') return;
        // если нет jQuery - воспользуемся решениями для  определения размеров из яндекса
        if(typeof jQuery === "undefined") {
            var actualHeight = (document.body.scrollHeight > document.body.offsetHeight)?document.body.scrollHeight:document.body.offsetHeight;
            var currentHeight = this.getCurrentHeight();
        } else {
            var actualHeight = $("body").height();
            var currentHeight = $(window).height();
        }

        if(Math.abs(actualHeight - currentHeight) > 20)
        {
            pm({
              target: window.parent,
              type: this.FrameId,
              data: {height:actualHeight, id:this.FrameId}
            });
        }
    }

};

pm.bind("register", function(data) {
    FrameHeightManager.FrameId = data.id;
    // не забываем передать правильный this
    window.setInterval(function() {FrameHeightManager.publishHeight.call(FrameHeightManager)}, 300);
});