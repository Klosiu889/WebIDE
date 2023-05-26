let clickableDirectories = document.querySelectorAll('.clickable-directories')
let clickableFiles = document.querySelectorAll('.clickable-files')

const homeDirectory = JSON.parse(document.getElementById('home').textContent)
const directories = JSON.parse(document.getElementById('directories').textContent)
let files = JSON.parse(document.getElementById('files').textContent)

const codeBar = document.getElementById('file-name-display')

const textarea = document.getElementById('code-textarea')
const lineNumbers = document.querySelector('.line-numbers')

let openedFile = null
let openedDirectory = null
let lastOpened = null

const addFileForm = document.getElementById("add-file-form")
const addDirForm = document.getElementById('add-dir-form')
const deleteForm = document.getElementById('delete-form')
const saveForm = document.getElementById('save-form')


/*
 * File tree
 */

function clickDirectory(evt) {
	clickableDirectories.forEach((directory) => {
		directory.classList.remove('opened')
	})
	clickableFiles.forEach((file) => {
		file.classList.remove('opened')
	})
	evt.target.classList.toggle('opened')

	openedDirectory = null
	for (let i = 0; i < directories.length; i++) {
		if (directories[i].path.toString() === evt.target.id.toString()) {
			openedDirectory = directories[i]
		}
	}

	lastOpened = "directory"
}

function clickFile(evt) {
	clickableDirectories.forEach((directory) => {
		directory.classList.remove('opened')
	})
	clickableFiles.forEach((file) => {
		file.classList.remove('opened')
	})
	evt.target.classList.toggle('opened')

	openedFile = null
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

function generateFileTree(parent) {
	let content = ""
	const folderImage = document.getElementById('folder-image').value
	const fileImage = document.getElementById('file-image').value

	directories.forEach((dir) => {
		if (dir.availability && dir.parent === parent) {
			content +=
				`<li><details>
                <summary class="clickable-directories" id="${dir.path}">
                <img src="${folderImage}" class="folder" alt=""> ${dir.name}
                </summary>
                <ul>`

			content += generateFileTree(dir.path)

			content += `</ul></details></li>`
		}
	})

	files.forEach((file) => {
		if (file.availability && file.parent === parent) {
			content +=
				`<li class="clickable-files" id="${file.path}">
                <img src="${fileImage}" class="folder" alt=""> ${file.name}
            </li>`
		}
	})

	return content
}

function updateFileTree() {
	const fileTreeContent = generateFileTree(homeDirectory.path)
	const fileTree = document.getElementById('file-tree-container')
	fileTree.innerHTML = fileTreeContent

	clickableDirectories.forEach((directory) => {
		directory.classList.remove('opened')
	})
	clickableFiles.forEach((file) => {
		file.classList.remove('opened')
	})

	openedDirectory = null
	openedFile = null

	clickableDirectories = document.querySelectorAll('.clickable-directories')
	clickableFiles = document.querySelectorAll('.clickable-files')

	clickableDirectories.forEach((dir) => {
		dir.addEventListener('click', (evt) => clickDirectory(evt))
	})

	clickableFiles.forEach((file) => {
		file.addEventListener('click', (evt) => clickFile(evt))
	})
}

updateFileTree()

/*
 *  Code editor
 */
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

/*
 *  Files modifications
 */

function fetchHandler(evt, form, onSuccess, onFail) {
	evt.preventDefault()

	const data = new FormData(form)

	fetch(form.action, {
		method: form.method,
		body: data
	})
		.then(response => response.json())
		.then(data => {
			if (data.status === "ok") onSuccess(data)
			else onFail(data)

			updateFileTree()
		})
		.catch(error => {
			alert(error)
		})
}

function addFile(evt) {
	const parent_field = document.getElementById('add-file-parent')
	parent_field.value = openedDirectory != null ? openedDirectory.path : homeDirectory.path

	fetchHandler(evt, addFileForm,
		(data) => {
			files.push(
				{
					"path": data.path,
					"name": data.name,
					"parent": data.parent,
					"content": data.content,
					"availability": data.availability,
				}
			)
		}, (data) => {
			alert(data.message)
		})
}

function addDirectory(evt) {
	const parent_field = document.getElementById('add-dir-parent')
	parent_field.value = openedDirectory != null ? openedDirectory.path : homeDirectory.path

	fetchHandler(evt, addDirForm,
		(data) => {
			directories.push(
				{
					"path": data.path,
					"name": data.name,
					"parent": data.parent,
					"availability": data.availability,
				}
			)
		}, (data) => {
			alert(data.message)
		})
}

function deleteItem(evt) {
	if (lastOpened === "directory") {
		if (openedDirectory != null) {
			const path_field = document.getElementById('delete-path')
			const type_field = document.getElementById('delete-type')
			path_field.value = openedDirectory.path.toString()
			type_field.value = "directory"
		}
	} else if (lastOpened === "file") {
		if (openedFile != null) {
			const path_field = document.getElementById('delete-path')
			const type_field = document.getElementById('delete-type')
			path_field.value = openedFile.path.toString()
			type_field.value = "file"
		}
	}

	fetchHandler(evt, deleteForm,
		(_data) => {
			if (lastOpened === "directory") openedDirectory.availability = false;
			else if (lastOpened === "file") openedFile.availability = false;
		}, (data) => {
			alert(data.message)
		})
}

function saveChanges(evt) {
	if (openedFile != null) {
		const path_field = document.getElementById('save-path')
		const content_field = document.getElementById('save-content')
		path_field.value = openedFile.path.toString()
		content_field.value = textarea.value
	}

	fetchHandler(evt, saveForm,
		(data) => {
			openedFile.content = data.content
		}, (data) => {
			alert(data.message)
		})
}

addFileForm.addEventListener('submit', evt => addFile(evt))
addDirForm.addEventListener('submit', evt => addDirectory(evt))
deleteForm.addEventListener('submit', evt => deleteItem(evt))
saveForm.addEventListener('submit', evt => saveChanges(evt))

/*
 *  Compiler
 */

const compileForm = document.getElementById('compile-form')

function compile(evt) {
	const standard = document.querySelectorAll('#standard input[type="radio"]:checked')
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

	fetchHandler(evt, compileForm,
		(data) => {
			files.push(
				{
					"path": data.path,
					"name": data.name,
					"parent": data.parent,
					"content": data.content,
					"availability": data.availability,
				}
			)
		}, (data) => {
			alert(data.message + "\n" + data.error)
		})
}

compileForm.addEventListener('submit', evt => compile(evt))