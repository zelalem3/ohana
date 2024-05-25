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

// IntersectionObserver for general elements with 'visible' class
const observerOptions = {
  root: null,
  rootMargin: '0px',
  threshold: 0.5
};

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    } else {
      entry.target.classList.remove('visible');
    }
  });
}, observerOptions);

const children = document.querySelectorAll('.child');
children.forEach(child => {
  observer.observe(child);
});

// Loader wrapper fade out
$(document).ready(function() {
  $(".loader-wrapper").fadeOut("slow");
});
