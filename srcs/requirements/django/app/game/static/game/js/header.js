window.addEventListener('load', function() {
  const styledHeader = document.querySelector('.focus');
  function updateComponentSize() {
    const dataMessageWidth = styledHeader.scrollWidth;
    styledHeader.style.setProperty('--componentSize', `${dataMessageWidth}px`);
  }
  setTimeout(updateComponentSize, 50);
});
