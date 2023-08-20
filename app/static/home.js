const save_plan = ()=> {
    let event_names = [];
    let event_descriptions = [];
    let event_rules = [];
    $(".event_name").each(function(){
        event_names.push($(this).val());
    });
    $(".event_description").each(function() {
        event_descriptions.push($(this).val());
    });
    $(".event_rules").each(function(){
        event_rules.push(JSON.parse($(this).val()));
    });
    all_events = [];
    for (let i=0; i<event_names.length;i++){
        all_events.push({"name": event_names[i], "description": event_descriptions[i], "rules": event_rules[i]});
    }
    
    let data = {
        "name": $('#plan_name').val(),
        "description": $('#plan_description').val(),
        "events": all_events,
    }
    $.ajax({
        async: true,
        url: "/save_tracking_plans",
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: function (response) {
            
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
        }
    });
}

const add_new_event = () => {
    new_event_html = `<br><br><div class="row">
    <div class="col-sm-2"><label for="event_name">Name:</label></div>
    <div class="col-sm-5"><input class="event_name" class="form-input" type="text" name="event_name"></div>
</div>
<br>
<div class="row">
    <div class="col-sm-2"><label for="event_description">Description:</label></div>
    <div class="col-sm-5"><input class="event_description class="form-input" type="text" name="event_description"></div>
</div>
<br>
<div class="row">
    <div class="col-sm-2"><label for="event_rules">Rules: </label></div>
    <div class="col-sm-5"><textarea class="event_rules" type="textar" placeholder="{ JSON SCHEMA }" name="event_rules"></textarea></div>
</div>`;
    $('#events_container').append(new_event_html);

}