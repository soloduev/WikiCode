/**
 * Created by Igor on 11.04.2016.
 */

(function($) {
    $(document).ready(function() {
      var mySlidebars = new $.slidebars();
      $('#pollSlider-button').on('click', function() {
        mySlidebars.slidebars.open('left');
      });


    });
  }) (jQuery);