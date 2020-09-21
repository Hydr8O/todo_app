stopTransitionOnLoad = () => {
    document.body.classList.remove('stop-transition')
};

addToggleNavHandler = () => {
    burger = document.querySelector('.burger');
    navList = document.querySelector('.nav__list');
    burger.addEventListener('click', () => {
        navList.classList.toggle('hidden--nav');
        burger.classList.toggle('change--burger');
    });
};

stopTransitionOnLoad();
addToggleNavHandler();