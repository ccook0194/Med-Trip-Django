feather.replace();

function openSearch() {
  $(".search-box-1").css('display', 'block');
  $("#search-header").focus();
  $('#search-open').css('display', 'none');
  $('#search-close').css('display', 'block');
}

function closeSearch($event) {
  if($event.target.id != "search-header"){
  $(".search-box-1").css('display', 'none');
  $("#search-header").blur();
  $('#search-open').css('display', 'block');
  $('#search-close').css('display', 'none');
  }
  //console.log("close search", $event.target.id);
}

function showFilters(){
  $(".filter-box").addClass("show");
  $(".body-overlay").addClass("show");
}

function closeFilters(){
  $(".filter-box").removeClass("show");
  $(".body-overlay").removeClass("show");
}

document.body.addEventListener('click',closeSearch, true);

function closeAlert(){
  $(".alert").alert('close')
}
// //owl carousel in blog
// $(document).ready(function(){
//   $('.owl-carousel').owlCarousel();
// });
$(document).ready(function(){
  $("#owl-carousel-image").owlCarousel({
    loop:false,
    margin:10,
    items:1,
    nav:true,
    dots:false,
    navElement:'div',
    navText: [
      `<button type="button" id="lg-prev-1" aria-label="Previous slide" class="lg-prev lg-icon" style="opacity:1;left:0;transform:translateX(-1rem)">  </button>`,
      `<button type="button" id="lg-next-1" aria-label="Next slide" class="lg-next lg-icon"  style="opacity:1;right:0;transform:translateX(1rem)">  </button>`],
  });


  $(".owl-carousel-blogs").owlCarousel({
    loop:false,
    margin:10,
    items:3,
    stagePadding:40,
    nav:true,
    dots:false,
    navElement:'button',
    navText: [
      ` <a class="btn-icon prev">
      <img src="./img/prev.png" alt="prev">
    </a>`,
      ` <a class="btn-icon next">
      <img src="./img/next.png" alt="prev">
    </a>`],
      responsive : {
        // breakpoint from 0 up
        0 : {
          items:1,
          stagePadding:0
        },
     
        480 : {
          items:1,
          stagePadding:50
        },
        781 : {
          items:2,
          stagePadding:50
        },
        900 : {
          items:3,
          stagePadding:20
        },
        1100 : {
          items:3,
          stagePadding:50
        }
      }
    });

  });

   //custom select js
   const elSelectCustom = document.querySelectorAll(".js-selectCustom");

   elSelectCustom.forEach(el => {
     const elSelectCustomValue = el.children[0];
     const elSelectCustomOptions = el.children[1];
     const defaultLabel = elSelectCustomValue.getAttribute("data-value");
 
     // Listen for each custom option click
     Array.from(elSelectCustomOptions.children).forEach(function (elOption) {
       elOption.addEventListener("click", (e) => {
         // Update custom select text too
         elSelectCustomValue.textContent = e.target.textContent;
         // Close select
         el.classList.remove("isActive");
       });
     });
 
     // Toggle select on label click
     elSelectCustomValue.addEventListener("click", (e) => {
       el.classList.toggle("isActive");
     });
 
     // close the custom select when clicking outside.
     document.addEventListener("click", (e) => {
       const didClickedOutside = !el.contains(event.target);
       if (didClickedOutside) {
         el.classList.remove("isActive");
       }
     });
   })

   function toggleNavbarInMobile() {
    var navbar = document.getElementById("websiteNavbar");
    const navbar_secondary = $(".navbar-secondary");
    
    const treatments = document.getElementById('treatments')
    const destinations = document.getElementById('destinations')
    
    treatments.classList.add('fa-chevron-down')
    treatments.classList.remove('fa-chevron-up')

    
    destinations.classList.add('fa-chevron-down')
    destinations.classList.remove('fa-chevron-up')

    navbar.classList.toggle("navbar-open")
    navbar.classList.remove("full-height")
    navbar_secondary.addClass("display-none")
  }