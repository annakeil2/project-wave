/**
 * Used to submit a parent form when a select element changes
 */
function saveOnChange(element){
    let parent = element.parentElement;
    while (
        parent !== document.body 
        && parent.tagName.toLowerCase() !== 'form'
    ){
        parent = parent.parentElement;
    }

    if (parent !== document.body) {
        parent.submit();
    }
}