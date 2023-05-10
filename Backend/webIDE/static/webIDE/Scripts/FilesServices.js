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

const addFileButton = document.getElementById('add-file-button')
const addDirButton = document.getElementById('add-dir-button')
const deleteButton = document.getElementById('delete-button')
const saveButton = document.getElementById('save-button')

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

function deleteItem() {
    if ((lastOpened === "directory" && openedDirectory != null) ||
        (lastOpened === "file" && openedFile != null)) {
        const xhr = new XMLHttpRequest()
        xhr.open('POST', '/webIDE/delete_item/', true)
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.onload = () => {
            if (xhr.status === 200) {
                console.log('Item deleted')
            }
            else {
                console.log('Error deleting item')
            }
        }
        xhr.onerror = () => {
            console.log('Error deleting item')
        }

        const dataToSend = {
            id: (lastOpened === "directory" ? openedDirectory.id.toString() : openedFile.id.toString()),
            type: lastOpened
        }

        xhr.send(JSON.stringify(dataToSend))
    }
}

function saveChanges() {
    if (openedFile != null) {
        openedFile.content = textarea.value

        const xhr = new XMLHttpRequest()
        xhr.open('POST', '/webIDE/save_file/', true)
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.onload = () => {
            if (xhr.status === 200) {
                console.log('File saved')
            }
            else {
                console.log('Error saving file')
            }
        }
        xhr.onerror = () => {
            console.log('Error saving file')
        }

        const dataToSend = {
            id: openedFile.id.toString(),
            content: openedFile.content.toString()
        }

        xhr.send(JSON.stringify(dataToSend))
    }
}

function clickDirectory(evt) {
    clickableDirectories.forEach((directory) => { directory.classList.remove('opened') })
    clickableFiles.forEach((file) => { file.classList.remove('opened') })
    evt.target.classList.toggle('opened')

    for (let i = 0; i < directories.length; i++) {
        if (directories[i].id.toString() === evt.target.id.toString()) {
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
        if (files[i].id.toString() === evt.target.id.toString()) {
            codeBar.innerHTML = files[i].name
            openedFile = files[i]
            textarea.value = files[i].content
            updateLineNumbers()
        }
    }

    lastOpened = "file"
}


deleteButton.addEventListener('click', () => deleteItem())
saveButton.addEventListener('click', () => saveChanges())

for (let i = 0; i < clickableDirectories.length; i++) {
    clickableDirectories[i].addEventListener('click', (evt) => clickDirectory(evt))
}

for (let i = 0; i < clickableFiles.length; i++) {
    clickableFiles[i].addEventListener('click', (evt) => clickFile(evt))
}