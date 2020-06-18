function build_query(base_url, ...args) {
    base_url += '?';
    for (let i = 0; i < args.length; i+=2) {
        base_url += args[i] + '=' + args[i + 1];
        if (i != args.length - 2) {
            base_url += '&';
        }
    }
    return base_url;
}

async function fetch_lesson_ajax(url, lesson_id, course_id, user_id) {
    // Build a query to pass to the server
    url = build_query(url, 'lesson_id', lesson_id, 'course_id', course_id, "user_id", user_id);
    // GET
    let fetched_response = await fetch(url);

    if (fetched_response.ok) { // if 200
        let json = await fetched_response.json();

        // Add url to lesson page
        let lesson_info = '№' + json.number + '\n\n\n' +
        json.name + '\n\n' +
        'Материалы к занятию:\n\n' +
        json.materials + '\n\n\n' + 'Домашнее задание:\n\n' +
        json.homework_task;

        alert(lesson_info);
        //document.getElementById('lesson_name').innerHTML = json.name;
        //console.log(json.name);
    } else {
        alert("Ошибка HTTP: " + fetched_response.status);
    }
}