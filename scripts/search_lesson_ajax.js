// TODO add the url to the lesson to bind it to the button
function create_lesson_div(lesson_number, lesson_name, lesson_id, lesson_group, fetch_url) {

    // Create divs for the lesson
    let lesson_div = document.createElement('div');
    lesson_div.className = 'card-body border  d-flex flex-wrap flex-row justify-content-start';

    let lesson_number_div = document.createElement('div');
    lesson_number_div.className = 'lesson-number font-weight-bold mr-5';
    lesson_number_div.innerHTML = lesson_number;

    let group_name_div;
    console.log(lesson_group);
    if (lesson_group != "") {
        group_name_div = document.createElement('div');
        group_name_div.className = 'text-center overflow-auto mx-5';
        group_name_div.innerHTML = lesson_group;
    }

    let lesson_name_div = document.createElement('div');
    lesson_name_div.className = 'text-center overflow-auto mx-5';
    lesson_name_div.innerHTML = lesson_name;

    let lesson_fetch_button = document.createElement('a');
    lesson_fetch_button.className = 'a-button ml-auto'
    fetch_url = fetch_url.slice(0, fetch_url.length - 2);
    lesson_fetch_button.href = fetch_url + lesson_id;
    lesson_fetch_button.innerHTML = 'Посмотреть занятие'

    // Construct the node tree
    lesson_div.append(lesson_number_div);
    if (lesson_group != "") {
        lesson_div.append(group_name_div);
    }
    lesson_div.append(lesson_name_div);
    lesson_div.append(lesson_fetch_button);

    return lesson_div;
}

// course name for the element to be appended to
async function search_lesson_ajax(course_id, user_id, url, fetch_url) {
    // A lesson name to find
    keywords = document.getElementById('search_input_' + course_id).value;
    // Clear the search field
    document.getElementById('search_input_' + course_id).value = '';

    // Le csrf
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    // This will go to the server
    content = {
        'keywords': keywords, 'course_id': course_id,
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
        let node_to_be_appended_to = document.getElementById('course_' + course_id);

        // Clear all the lessons without deleting the search bar
        while (node_to_be_appended_to.lastChild) {
            if (node_to_be_appended_to.lastChild == document.getElementById('search_div_' + course_id)) {
                break;
            }
            node_to_be_appended_to.removeChild(node_to_be_appended_to.lastChild);
        }

        // Appending new found lessons
        for (let i = 0; i < json.lesson_name.length; i++) {
            if (json.group.length != 0) {
                let tempLessonNode = create_lesson_div(json.lesson_number[i], json.lesson_name[i], json.lesson_id[i], json.group[i], fetch_url);
                node_to_be_appended_to.append(tempLessonNode);
            } else {
                let tempLessonNode = create_lesson_div(json.lesson_number[i], json.lesson_name[i], json.lesson_id[i], "", fetch_url);
                node_to_be_appended_to.append(tempLessonNode);
            }

        }
    } else {
        alert("Ошибка HTTP: " + fetched_response.status);
    }
}
