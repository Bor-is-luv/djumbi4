// build a GET query from url and an even number of parameters
function build_query(base_url, ...args) {
    base_url += '?';
    // error case returns base_url
    if (args.length % 2 != 0) {
        return base_url;
    }
    for (let i = 0; i < args.length; i += 2) {
        base_url += args[i] + '=' + args[i + 1];
        if (i != args.length - 2) {
            base_url += '&';
        }
    }
    return base_url;
}

async function fetch_lesson_ajax(url, lesson_id) {
    // Build a query to pass to the server
    url = build_query(url, 'lesson_id', lesson_id);
    // GET
    let fetched_response = await fetch(url);

    if (fetched_response.ok) { // if 200
        let json = await fetched_response.json();

        // TODO Add url to lesson page
        let lesson_info = '№' + json.number + '\n\n\n' +
        json.name + '\n\n' +
        'Материалы к занятию:\n\n' +
        json.materials + '\n\n\n' + 'Домашнее задание:\n\n' +
        json.homework_task;

        alert(lesson_info);
    } else {
        alert("Ошибка HTTP: " + fetched_response.status);
    }
}