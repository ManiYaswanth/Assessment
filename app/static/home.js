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
    let is_err = false;
    $(".event_rules").each(function(){
        try{
            event_rules.push(JSON.parse($(this).val()));
        }
        catch(err){
            show_error_msg(err.message)
            is_err = true;
        }
        
    });
    if(is_err)
        return;
    all_events = [];
    for (let i=0; i<event_names.length;i++){
        try{
            if(event_names[i] != "" && (event_descriptions[i].length > 0 || event_rules[i] != ""))
            all_events.push({"name": event_names[i], "description": event_descriptions[i], "rules": event_rules[i]});
            else{
                throw "empty Event"
            }
        }
        catch(err){
            show_error_msg("Event name cannot be empty")
            return;
        }
    }
    
    let data = {
        "tracking_plan":{
            "display_name": $('#plan_name').val(),
            "description": $('#plan_description').val(),
            "rules": {
                "events": all_events
            }
        }
    }
    $.ajax({
        async: true,
        url: "/api/v1/tracking_plan",
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        success: function (response) {
            
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR, textStatus, errorThrown);
        }
    });
}

const show_error_msg = (err_message) => {
    $('#error_msg').text(`${err_message}`)
    $(`#error_msg`).show();
    setTimeout(function showError() {
        $(`#error_msg`).hide()
    }, 3000)
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

const get_all_tracking_plans = () => {
    $.ajax({
        async: true,
        url: "/api/v1/tracking_plans",
        type: 'GET',
        contentType: 'application/json; charset=UTF-8',
        success: function (response) {
            console.log(response);
            for(tracking_plan of response)
                $('#tracking_plans_container').append(set_tracking_plan_view(tracking_plan));
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR, textStatus, errorThrown);
        }
    });
}

const set_tracking_plan_view = (tracking_plan) => {
    const events_html = tracking_plan.events.map(element => {
        return `<div>Name: ${element.name}</div>
                <div>Description: ${element.description}</div>
                <div> Rules: ${JSON.stringify(element.rules)}`
                
    });
   return `<h4>Name: ${tracking_plan.display_name}</h4>
    <h5> Description: ${tracking_plan.description}</h5>
    <h5>Events: </h5>
    <div>${events_html.join("<br><br>")}
    </div>
    <br> <br>`
}