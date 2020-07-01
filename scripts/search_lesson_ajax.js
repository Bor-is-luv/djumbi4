// TODO add the url to the lesson to bind it to the button
function create_lesson_div(lesson_number, lesson_name, lesson_id, fetch_url) {
    // Create divs for the lesson
    let lesson_div = document.createElement('div');
    lesson_div.className = 'card-body border  d-flex flex-wrap flex-row justify-content-between';

    let lesson_number_div = document.createElement('div');
    lesson_number_div.className = 'lesson-number font-weight-bold';
    lesson_number_div.innerHTML = lesson_number;

    let lesson_name_div = document.createElement('div');
    lesson_name_div.className = 'text-center overflow-auto';
    lesson_name_div.innerHTML = lesson_name;

    let lesson_fetch_button = document.createElement('button');
    lesson_fetch_button.className = 'trigger a-button'
    lesson_fetch_button.innerHTML = 'Посмотреть занятие'
    lesson_fetch_button.onclick = function() {
        fetch_lesson_ajax(fetch_url, lesson_id);
    }

    // Construct the node tree
    lesson_div.append(lesson_number_div);
    lesson_div.append(lesson_name_div);
    lesson_div.append(lesson_fetch_button);

    return lesson_div;
}

// course name for the element to be appended to
async function search_lesson_ajax(course_name, user_id, url, fetch_url) {
    // A lesson name to find
    keywords = document.getElementById('search_input').value;
    // Clear the search field
    document.getElementById('search_input').value = '';

    // Le csrf
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    // This will go to the server
    content = {
        'keywords': keywords, 'course_name': course_name,
        'user_id': user_id
    };

    // request
    let fetched_response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(content)
    });

    // If we get a response
    if (fetched_response.ok) { // if 200
        let json = await fetched_response.json();

        // Node of the specific course
        let node_to_be_appended_to = document.getElementById(course_name);

        // Clear all the lessons without deleting the search bar
        while (node_to_be_appended_to.lastChild) {
            if (node_to_be_appended_to.lastChild == document.getElementById('search_div')) {
                break;
            }
            node_to_be_appended_to.removeChild(node_to_be_appended_to.lastChild);
        }

        // Appending new found lessons
        for (let i = 0; i < json.lesson_name.length; i++) {
            let tempLessonNode = create_lesson_div(json.lesson_number[i], json.lesson_name[i], json.lesson_id[i], fetch_url);
            node_to_be_appended_to.append(tempLessonNode);
        }
    } else {
        alert("Ошибка HTTP: " + fetched_response.status);
    }
}
