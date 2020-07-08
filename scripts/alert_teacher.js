

async function alert_teacher(teacher_id) {
    content = {'teacher_id': teacher_id};

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
        
        for (let i = 0; i < json.lesson_name.length; i++) {
            alert(json.group_name[i] + '\n' +
            json.pupil_name[i] + '\n' +
            json.lesson_name[i]);
        }
        
    } else {
        alert("Ошибка HTTP: " + fetched_response.status);
    }
}

async function start_alert_teacher(teacher_id) {
    if (true) {
        setTimeout(alert_teacher(teacher_id), 1000);        
    }
    setTimeout(start_alert_teacher, 1000);
}