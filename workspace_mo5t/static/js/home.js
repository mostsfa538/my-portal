function startTime()
{
    const months = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ];

    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    const today = new Date();
    let day = days[today.getDay()];
    let month = months[today.getMonth()];
    let date = today.getDate();
    let h = today.getHours();
    let m = today.getMinutes();
    let s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('dateTime').innerHTML = day + " " + dateSuffix(date) + ", " + month + " " + h + ":" + m + ":" + s;
    setTimeout(startTime, 1000);
}

function checkTime(i)
{
    if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
    return i;
}

function dateSuffix(date)
{
    if (date >= 11 && date <= 13)
    {
        return date + "th";
    }
    switch (date % 10)
    {
        case 1: return date + "st";
        case 2: return date + "nd";
        case 3: return date + "rd";
        default: return date + "th";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const darkModeToggle = document.getElementById('toggle-dark-mode');
    const body = document.body;

    const isDarkMode = localStorage.getItem('darkMode') === 'enabled';

    if (isDarkMode) {
        body.classList.add('dark-mode');
					document.getElementById('toggle-dark-mode').checked = true;;

    }

    darkModeToggle.addEventListener('click', function () {
        body.classList.toggle('dark-mode');

        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });
});

