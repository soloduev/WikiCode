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