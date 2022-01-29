function deleteNote(note_id) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ note_id: note_id })
    }).then((_res) => {
        window.location.href = "/";
    });
}