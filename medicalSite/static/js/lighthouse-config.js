const lgContainer1 = document.getElementById('inline-gallery-facilities');
const inlineGallery1 = lightGallery(lgContainer1, {
    container: lgContainer1,
    dynamic: true,
    // Turn off hash plugin in case if you are using it
    // as we don't want to change the url on slide change
    hash: false,
    // Do not allow users to close the gallery
    closable: false,
    // Add maximize icon to enlarge the gallery
    showMaximizeIcon: true,
    // Append caption inside the slide item
    // to apply some animation for the captions (Optional)
    appendSubHtmlTo: '.lg-item',
    // Delay slide transition to complete captions animations
    // before navigating to different slides (Optional)
    // You can find caption animation demo on the captions demo page
    slideDelay: 100,
    allowMediaOverlap: false,
    download:false,
    toggleThumb:false,
    plugins: [lgZoom],
    dynamicEl: [
      {
        src:
          "https://images.unsplash.com/photo-1542103749-8ef59b94f47e?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@dann">Dan</a></h4>
                      <p>Published on November 13, 2018</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1473876988266-ca0860a443b8?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@kylepyt">Kyle Peyton</a></h4>
                      <p>Published on September 14, 2016</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1588953936179-d2a4734c5490?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@jxnsartstudio">Garrett Jackson</a></h4>
                      <p>Published on May 8, 2020</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1591634616938-1dfa7ee2e617?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@brookecagle">Brooke Cagle</a></h4>
                      <p>Description of the slide 4</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1543059509-6d53dbee1728?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@charlespostiaux">Charles Postiaux</a></h4>
                      <p>Published on November 24, 2018</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1609902726285-00668009f004?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@bruno_adam">Bruno Adam</a></h4>
                      <p>Published on January 6, 2021</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1573007974656-b958089e9f7b?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@sigmund">Sigmund</a></h4>
                      <p>Published on November 6, 2019</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1579406842270-ea87c39a8a12?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@chow_parij">Parij Borgohain</a></h4>
                      <p>Published on January 19, 2020</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1598911543663-37d77962beb1?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@inespiazzese">Ines Piazzese</a></h4>
                      <p>Published on September 1, 2020</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1560885673-2cdc12600ec8?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@rdsaunders">Richard Saunders</a></h4>
                      <p>Published on June 19, 2019</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1571292064306-669f0e758231?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@jalanmeier">J. Meier</a></h4>
                      <p>Published on October 17, 2019</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1601935111741-ae98b2b230b0?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@brookecagle">Brooke Cagle</a></h4>
                      <p>Published on October 6, 2020</p>
                  </div>`
      }
    ],
});


const lgContainer2 = document.getElementById('inline-gallery-beforeafter');
const inlineGallery2 = lightGallery(lgContainer2, {
    container: lgContainer2,
    dynamic: true,
    // Turn off hash plugin in case if you are using it
    // as we don't want to change the url on slide change
    hash: false,
    // Do not allow users to close the gallery
    closable: false,
    // Add maximize icon to enlarge the gallery
    showMaximizeIcon: true,
    // Append caption inside the slide item
    // to apply some animation for the captions (Optional)
    appendSubHtmlTo: '.lg-item',
    // Delay slide transition to complete captions animations
    // before navigating to different slides (Optional)
    // You can find caption animation demo on the captions demo page
    slideDelay: 100,
    allowMediaOverlap: false,
    download:false,
    toggleThumb:true,
    plugins: [lgZoom],
    selector: '.item',
    dynamicEl: [
      {
        src:
          "https://images.unsplash.com/photo-1542103749-8ef59b94f47e?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@dann">Dan</a></h4>
                      <p>Published on November 13, 2018</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1473876988266-ca0860a443b8?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@kylepyt">Kyle Peyton</a></h4>
                      <p>Published on September 14, 2016</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1588953936179-d2a4734c5490?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@jxnsartstudio">Garrett Jackson</a></h4>
                      <p>Published on May 8, 2020</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1591634616938-1dfa7ee2e617?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@brookecagle">Brooke Cagle</a></h4>
                      <p>Description of the slide 4</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1543059509-6d53dbee1728?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@charlespostiaux">Charles Postiaux</a></h4>
                      <p>Published on November 24, 2018</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1609902726285-00668009f004?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@bruno_adam">Bruno Adam</a></h4>
                      <p>Published on January 6, 2021</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1573007974656-b958089e9f7b?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@sigmund">Sigmund</a></h4>
                      <p>Published on November 6, 2019</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1579406842270-ea87c39a8a12?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@chow_parij">Parij Borgohain</a></h4>
                      <p>Published on January 19, 2020</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1598911543663-37d77962beb1?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@inespiazzese">Ines Piazzese</a></h4>
                      <p>Published on September 1, 2020</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1560885673-2cdc12600ec8?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@rdsaunders">Richard Saunders</a></h4>
                      <p>Published on June 19, 2019</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1571292064306-669f0e758231?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@jalanmeier">J. Meier</a></h4>
                      <p>Published on October 17, 2019</p>
                  </div>`
      },
      {
        src:
          "https://images.unsplash.com/photo-1601935111741-ae98b2b230b0?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1400&q=80",
        subHtml: `<div class="lightGallery-captions">
                      <h4>Photo by <a href="https://unsplash.com/@brookecagle">Brooke Cagle</a></h4>
                      <p>Published on October 6, 2020</p>
                  </div>`
      }
    ],
  
    // Completely optional
    // Adding as the codepen preview is usually smaller
    thumbHeight: "6rem"
});

// lightGallery(document.getElementById('selector1'), {
//   selector: '.item',
// });

inlineGallery1.openGallery();



