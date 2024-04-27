// JavaScript for the scroll transition effect
window.addEventListener('scroll', function() {
  var header = document.querySelector('header');
  var sections = document.querySelectorAll('section');

  var triggerOffset = window.innerHeight * 0.8; // Adjust this value to your needs

  var scrollTop = window.scrollY;

  var headerOffset = header.offsetTop + triggerOffset;

  sections.forEach(function(section) {
    var sectionOffset = section.offsetTop + triggerOffset;

    if (scrollTop >= headerOffset) {
      header.classList.add('transition-effect');
    } else {
      header.classList.remove('transition-effect');
    }

    if (scrollTop >= sectionOffset) {
      section.classList.add('transition-effect');
    } else {
      section.classList.remove('transition-effect');
    }
  });
});
