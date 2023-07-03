const changeElement = document.querySelector('i#change-theme');
const body = document.querySelector('body');
let isDarkTheme = false;


function toggleTheme() {
  isDarkTheme = !isDarkTheme;
  if (isDarkTheme) {
    body.classList.add('dark-theme');
    changeElement.classList.toggle('bi-sun')
    localStorage.setItem('themePreference', 'dark');
  } else {
    body.classList.remove('dark-theme');
    changeElement.classList.replace('bi-moon', 'bi-sun');
    localStorage.setItem('themePreference', 'light');
  }
}



const savedThemePreference = localStorage.getItem('themePreference');
if (savedThemePreference === 'dark') {
  toggleTheme(); 
}




changeElement.addEventListener('click', toggleTheme);