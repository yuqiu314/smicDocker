/* Scroll to Top Button */

$(document).ready(function(){
  $('.otw-primary-menu').superfish({
    hoverClass:    'sfHover',
    delay:         500,
    speed:         'fast'
  });

  // Responsive Navigation
  $(".otw-primary-menu").tinyNav({
    active: 'active'
  });

  $(".tinynav").addClass("show-for-small");

  // Animate Box Shadow on some elements
  // Add the overlay. We don't need it in HTML so we create it here
  $('.animate-on-hover .image').append('<span class="shadow-overlay hide-for-small"></span>');
  //$('.otw-portfolio-item-link').append('<span class="shadow-overlay hide-for-small"></span>');
  
  $('.shadow-overlay').hover(function() {
      $(this).stop().stop().animate({boxShadow: '0 0 8px 0 rgba(0,0,0,0.7)'}, 200);
  }, function(){
      $(this).stop().stop().animate({boxShadow: '0 0 0 0'}, 150);
  });
  /*$('.otw-sc-portfolio .otw-portfolio-item').hover(function() {
      $(this).stop().stop().animate({boxShadow: '0 0 8px 0 rgba(0,0,0,0.7)'}, 200);
  }, function(){
      $(this).stop().stop().animate({boxShadow: '0 0 0 0'}, 150);
  });*/

  // jQuery UI Tabs
  $('.otw-sc-tabs').tabs();

  // jQuery UI Accordion
  $('.otw-sc-accordion').accordion({
    heightStyle: "content",
    collapsible: true
  });

  // Responsive tables
  $('.footable').footable({
      breakpoints: {
      phone: 480,
      tablet: 767
    }
  });

  // FAQ Toggle
  // Hide all DD innitialy
  $('.otw-sc-faq dl > dd').hide();
  //Add Spans
  $('.otw-sc-faq dl > dt').each(function(){
    $(this).addClass("open-faq").prepend("<span></span>");
  });
  //Toggle FAQ question on click.
  $('.otw-sc-faq dl > dt').click(function() {
    $(this).toggleClass('open-faq').next().slideToggle(350);
  });

  // Scroll to top link with animation
  $('.scroll-top a').click(function () {
    $('html, body').animate({ scrollTop: '0px' }, 700);
    return false;
  });
  
  // Content toggle
  // Toggle closed class and content box
  $('.toggle-trigger').click(function () {
    $(this).toggleClass('closed').next('.toggle-content').slideToggle(350);
  });
  // Innitial hide content of .closed toggles
  $('.toggle-trigger.closed').next('.toggle-content').hide();

  // Close message box button
  $(".otw-sc-message.closable-message").append("<div class=\"close-message\">x</div>").find(".close-message").click(function() {
    $(this).parent(".otw-sc-message").fadeOut("fast");
  });

	// Clone portfolio items to get a second collection for Quicksand plugin
  var $portfolioClone = $(".otw-portfolio").clone();

	// Attempt to call Quicksand on every click event handler
	$(".otw-portfolio-filter a").click(function(e){

		$(".otw-portfolio-filter li").removeClass("current");

		// Get the class attribute value of the clicked link
		var $filterClass = $(this).parent().attr("class");

		if ( $filterClass == "all" ) {
			var $filteredPortfolio = $portfolioClone.find("li");
		} else {
			var $filteredPortfolio = $portfolioClone.find("li[data-type~=" + $filterClass + "]");
		}

    //console.log($filteredPortfolio);
    $(".otw-portfolio").removeAttr('style');

		// Call quicksand
		$(".otw-portfolio").quicksand( $filteredPortfolio, {
			duration: 500,
			easing: 'easeInOutQuad'
		});

		$(this).parent().addClass("current");

		// Prevent the browser jump to the link anchor
		e.preventDefault();
	});

});

$(window).on('resize', function(){
  $(".otw-portfolio").removeAttr('style');
});