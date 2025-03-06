// Forms

function showRevision() {


        document.getElementById('h-form').classList.add('opacity-0');
        document.getElementById('h-form').classList.remove('opacity-100');
        document.getElementById('h-revision').classList.add('opacity-100');
        document.getElementById('h-revision').classList.remove('opacity-0');


        document.getElementById('insertStep').classList.remove('opacity-100');
        document.getElementById('insertStep').classList.add('opacity-40');
        document.getElementById('confirmStep').classList.remove('opacity-40');
        document.getElementById('confirmStep').classList.add('opacity-100');


    }

function backToInsert() {
    document.getElementById('h-form').classList.remove('opacity-0');
    document.getElementById('h-form').classList.add('opacity-100');
    document.getElementById('h-revision').classList.remove('opacity-100');
    document.getElementById('h-revision').classList.add('opacity-0');

    document.getElementById('insertStep').classList.remove('opacity-40');
    document.getElementById('insertStep').classList.add('opacity-100');
    document.getElementById('confirmStep').classList.remove('opacity-100');
    document.getElementById('confirmStep').classList.add('opacity-40');
}