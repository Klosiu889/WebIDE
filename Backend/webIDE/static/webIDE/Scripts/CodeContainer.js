const textarea = document.getElementById('code-textarea')
const lineNumbers = document.querySelector('.line-numbers')

const updateLineNumbers = () => {
    const numberOfLines = textarea.value.split('\n').length;
    lineNumbers.innerHTML = Array(numberOfLines).fill('<span></span>').join('');
};

textarea.addEventListener('keyup', () => {
    updateLineNumbers();
})

textarea.addEventListener('keydown', event => {
    if (event.key === 'Tab') {
        const start = textarea.selectionStart
        const end = textarea.selectionEnd

        textarea.value = textarea.value.substring(0, start) + '\t' + textarea.value.substring(end)

        event.preventDefault()
    }
})