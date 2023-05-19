const clickableDirectories = document.querySelectorAll('.clickable-directories')
const clickableFiles = document.querySelectorAll('.clickable-files')

const directories = JSON.parse(document.getElementById('directories').textContent)
const files = JSON.parse(document.getElementById('files').textContent)

const codeBar = document.getElementById('file-name-display')

const textarea = document.getElementById('code-textarea')
const lineNumbers = document.querySelector('.line-numbers')

let openedFile = null
let openedDirectory = null
let lastOpened = null

const addFileButton = document.getElementById('add-file-submit')
const addDirButton = document.getElementById('add-dir-submit')
const deleteButton = document.getElementById('delete-submit')
const saveButton = document.getElementById('save-submit')

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

function addFile() {
    const name_field = document.getElementById('add-file-name')
    const directory_field = document.getElementById('add-file-parent')
    name_field.value = name_field.value.trim()

    if (openedDirectory != null) directory_field.value = openedDirectory.path.toString()
    else directory_field.value = ""
}

function addDirectory() {
    const name_field = document.getElementById('add-dir-name')
    const directory_field = document.getElementById('add-dir-parent')
    name_field.value = name_field.value.trim()

    if (openedDirectory != null) directory_field.value = openedDirectory.path.toString()
    else directory_field.value = ""
}

function deleteItem() {
    if (lastOpened === "directory") {
        if (openedDirectory != null) {
            const path_field = document.getElementById('delete-path')
            const type_field = document.getElementById('delete-type')
            path_field.value = openedDirectory.path.toString()
            type_field.value = "directory"
        }
    }
    else if (lastOpened === "file") {
        if (openedFile != null) {
            const path_field = document.getElementById('delete-path')
            const type_field = document.getElementById('delete-type')
            path_field.value = openedFile.path.toString()
            type_field.value = "file"
        }
    }
}

function saveChanges() {
    if (openedFile != null) {
        const path_field = document.getElementById('save-path')
        const content_field = document.getElementById('save-content')
        path_field.value = openedFile.path.toString()
        content_field.value = textarea.value
    }
}

function clickDirectory(evt) {
    clickableDirectories.forEach((directory) => { directory.classList.remove('opened') })
    clickableFiles.forEach((file) => { file.classList.remove('opened') })
    evt.target.classList.toggle('opened')

    for (let i = 0; i < directories.length; i++) {
        if (directories[i].path.toString() === evt.target.id.toString()) {
            openedDirectory = directories[i]
        }
    }

    lastOpened = "directory"
}

function clickFile(evt) {
    clickableDirectories.forEach((directory) => { directory.classList.remove('opened') })
    clickableFiles.forEach((file) => { file.classList.remove('opened') })
    evt.target.classList.toggle('opened')

    for (let i = 0; i < files.length; i++) {
        if (files[i].path.toString() === evt.target.id.toString()) {
            codeBar.innerHTML = files[i].name
            openedFile = files[i]
            textarea.value = files[i].content
            updateLineNumbers()
        }
    }

    lastOpened = "file"
}

addFileButton.addEventListener('click', () => addFile())
addDirButton.addEventListener('click', () => addDirectory())
deleteButton.addEventListener('click', () => deleteItem())
saveButton.addEventListener('click', () => saveChanges())

for (let i = 0; i < clickableDirectories.length; i++) {
    clickableDirectories[i].addEventListener('click', (evt) => clickDirectory(evt))
}

for (let i = 0; i < clickableFiles.length; i++) {
    clickableFiles[i].addEventListener('click', (evt) => clickFile(evt))
}

function compile() {
    const standard= document.querySelectorAll('#standard input[type="radio"]:checked')
    const optimisations = document.querySelectorAll('#optimisation input[type="checkbox"]:checked')
    const processor = document.querySelectorAll('#processor input[type="radio"]:checked')
    let dependant = null;
    if (processor[0] != null) {
        switch (processor[0].value) {
            case 'mcs51':
                dependant = document.querySelectorAll('#dependent-mcs51 input[type="radio"]:checked')
                break
            case 'z80':
                dependant = document.querySelectorAll('#dependent-z80 input[type="radio"]:checked')
                break
            case 'stm8':
                dependant = document.querySelectorAll('#dependent-stm8 input[type="radio"]:checked')
                break
        }
    }

    const standardInput = document.getElementById('compile-standard')
    const optimisationsInput = document.getElementById('compile-optimisation')
    const processorInput = document.getElementById('compile-processor')
    const dependantInput = document.getElementById('compile-dependant')
    const fileInput = document.getElementById('compile-file')

    standardInput.value = standard[0] == null ? "" : standard[0].value
    optimisationsInput.value = ""
    for (let i = 0; i < optimisations.length; i++) {
        optimisationsInput.value += optimisations[i].value + " "
    }
    processorInput.value = processor[0] == null ? "" : processor[0].value
    fileInput.value = openedFile == null ? "" : openedFile.path.toString()
    dependantInput.value = dependant == null ? "" : dependant[0] == null ? "" : dependant[0].value
}

const compileButton = document.getElementById('compile-submit')
compileButton.addEventListener('click', compile)