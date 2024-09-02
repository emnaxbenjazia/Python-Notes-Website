function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }), // this will send a post request containing the noteID to the server to the delete-note route
    }).then((_res) => {
        window.location.href = '/';
    }); // and then it will redirect the user to the home page
}