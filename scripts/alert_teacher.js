
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function alert_teacher(teacher_id, url) {
    let content = {'teacher_id': teacher_id};
    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    //console.log(url);
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
        
        if (json.lesson_name.length != 0){
            for (let i = 0; i < json.lesson_name.length; i++) {
                alert('Загружена домашняя работа\nГруппа: ' + json.group_name[i] + '\n' + 'Ученик: ' +
                json.pupil_name[i] + '\n' + 'Название урока: ' +
                json.lesson_name[i]);
            }
    }
        
    } else {
        alert("Ошибка HTTP: " + fetched_response.status);
    }
}
