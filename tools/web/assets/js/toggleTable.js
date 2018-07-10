$(".toggleTable").ready(function(){
  $(".parent td.moreLess").bind('click', function(){
    if($(this).closest("tr").hasClass("open")) {
      $(".toggleTable tr.open").removeClass('open');
    }else{
      $(".toggleTable tr.open").removeClass('open');
      $(this).closest("tr").addClass('open');
    }

    $(".toggleTable tr").not(".open").fadeOut(
      function(){
        $('.toggleTable .constant').fadeIn();
        $('.toggleTable .parent').fadeIn();
        $('.toggleTable .open').fadeIn();
        /*$('.toggleTable .open').css({img: });*/
        $('.toggleTable .open').nextUntil(".parent").fadeIn();
        $('.toggleTable .open').nextUntil(".parent").addClass("metatable");
      });
  });
});




/*$(".toggleTable").ready(function(){
    $("tr.parent").bind('click', function(){
       if($(this).hasClass("open")) {
			$(".toggleTable tr.open").removeClass('open');
		}else{
			$(".toggleTable tr.open").removeClass('open');
			$(this).addClass('open');
		}
	   
       $(".toggleTable tr").not(".open").fadeOut(
        function(){
          $('.toggleTable .constant').fadeIn();
          $('.toggleTable .parent').fadeIn();
          $('.toggleTable .open').fadeIn();
          $('.toggleTable .open').nextUntil(".parent").fadeIn();
		  $('.toggleTable .open').nextUntil(".parent").addClass("metatable");
        });
    });
});*/

/*$(".toggleTable").on("click","a",function(e) {
    e.preventDefault();
	
	if ( $(this).closest("tr").prevUntil(".parent").hasClass("open") ){
    	$(this).closest("tr").prevUntil(".parent").removeClass("open");
		$(this).closest("tr").nextUntil(".parent").toggleClass("open");
    }
	else {$(this).closest("tr").nextUntil(".parent").toggleClass("open");}
});*/