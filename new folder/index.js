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


// Event listener for the toggle button


// Check local storage for user's preference on page load

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
    document.addEventListener('DOMContentLoaded', function() {
  const testimonialContainer = document.querySelector('.testimonials-container');
  const testimonialsTitle = document.querySelector('.testimonials-title');
  const testimonialItems = document.querySelectorAll('.testimonial-item');

  let lastScrollPosition = 0;

  // Function to observe and animate testimonial items
  function observeElements() {
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          entry.target.classList.remove('hidden');
        } else {
          entry.target.classList.remove('visible');
          entry.target.classList.add('hidden');
        }
      });
    }, observerOptions);

    testimonialItems.forEach(item => {
      observer.observe(item);
    });
  }

  // Fade in the testimonials title when it comes into view
  const titleObserverOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };

  const titleObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        testimonialsTitle.classList.add('visible');
      } else {
        testimonialsTitle.classList.remove('visible');
      }
    });
  }, titleObserverOptions);

  titleObserver.observe(testimonialsTitle);

  // Handle scroll event to animate items when scrolling up
  window.addEventListener('scroll', () => {
    const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;

    // Check if scrolling up
    if (scrollPosition < lastScrollPosition) {
      testimonialItems.forEach(item => {
        item.classList.add('scroll-up');
        item.classList.remove('scroll-down');
      });
    } else {
      testimonialItems.forEach(item => {
        item.classList.add('scroll-down');
        item.classList.remove('scroll-up');
      });
    }

    lastScrollPosition = scrollPosition;
  });

  // Initial call to set up the observers
  observeElements();
});
$(document).ready(function() {
        $(".loader-wrapper").fadeOut("slow");
      });

