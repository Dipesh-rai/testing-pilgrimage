$(document).ready(function () {
    $(".testimonial_part").owlCarousel({
        items: 3,
        loop: true,
        margin: 10,
        lazyLoad: true,
        nav:true,
        dots:true,
        responsive: {
            0: {
                items: 1 // for mobile
            },
            768: {
                items: 2 // for tablets
            },
            1250: {
                items: 3 // for desktops
            }
        }
    }


    );
});



$(document).ready(function(){
    $(".category").owlCarousel({
        items: 3,
        loop: true,
        margin: 10,
        nav:true,
        lazyLoad: true,
        dots:false,
        responsive: {
            0: {
                items: 1 // for mobile
            },
            768: {
                items: 2 // for tablets
            },
            1250: {
                items: 3 // for desktops
            }
        }
  });
});