stopTransitionOnLoad = () => {
    document.body.classList.remove('stop-transition')
};

stopEventBubblingFromTodoOptions = () => {
    const todoOptions = document.querySelectorAll('.todo__option');
    for (option of todoOptions) {
        option.addEventListener('click', (event) => {
            event.stopPropagation();
        });
    }
};

addToggleTodoMemoHandlers = () => {
    for (const todo of todos) {
        const todoMemo = todo.children[1];
        todo.addEventListener('click', () => {
            todoMemo.className = todoMemo.classList.contains('hidden--memo') ? `${'todo__memo showed--memo'}` : `${'todo__memo hidden--memo'}`;
            if (todoMemo.classList.contains('hidden--memo')) {
                setTimeout(() => {
                    todoMemo.style.display = 'none';
                }, 500)
            } else {
                setTimeout(() => {
                    todoMemo.style.display = 'block';
                }, 0)
            }
        });
    };
};

addTodoAppearAnimation = () => {
    animationDelay = 0;
    for (todo of todos) {
        animationDelay += .2;
        todo.style.animation = `fade-in-left .2s ${animationDelay}s ease-in both`;
    };
};

todos = document.querySelectorAll('.todo');

stopTransitionOnLoad();
addToggleTodoMemoHandlers();
stopEventBubblingFromTodoOptions();
addTodoAppearAnimation();