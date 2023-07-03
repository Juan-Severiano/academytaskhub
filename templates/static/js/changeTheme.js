const changeElement = document.querySelector('i#change-theme')
const body = document.querySelector('body')
let isDarkTheme = false


function toggleTheme() {
  isDarkTheme = !isDarkTheme
  if (isDarkTheme) {
    body.classList.add('dark-theme')
    changeElement.classList.replace('bi-moon-stars', 'bi-sun')
    localStorage.setItem('themePreference', 'dark')
  } else {
    body.classList.remove('dark-theme')
    changeElement.classList.replace('bi-sun', 'bi-moon-stars')
    localStorage.setItem('themePreference', 'light')
  }
}



const savedThemePreference = localStorage.getItem('themePreference')
if (savedThemePreference === 'dark') {
  toggleTheme()
}




changeElement.addEventListener('click', toggleTheme)