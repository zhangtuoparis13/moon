/**
 * Created by Thomas Duval on 14/04/14.
 */

$( document ).ready(function() {
    $("#useradd").hide();
    $("#tenantadd").hide();
    $("#elementadd").hide();
    $("#add_intra_rule").hide();
    $("#add_rule_help").hide();
    $("#add_inter_rule").hide();
    $(function() { $('#id_main_tables').change(function() {
        window.location.href='/userdb/?table=' + this[this.selectedIndex].value;
    }) });
    $(function() { $('#id_assignment_tables').change(function() {
        window.location.href='/userdb/?table=' + this[this.selectedIndex].value;
    }) });
});

function show_user_add_actions() {
    $("#useradd").show();
};

function show_tenant_add_actions() {
    $("#tenantadd").show();
};

function show_rule_add_actions() {
    $("#add_intra_rule").show();
};

function show_add_rule_help() {
    $("#add_rule_help").show();
};

function show_inter_extensions_add_actions() {
    $("#add_inter_rule").show();
};

function opendiv(divelement) {
    $(divelement).show();
};

function add_text_to_new_rule(select_id) {
    $("#new_rule").value += $(select_id).options[$(select_id).selectedIndex].text;
};

function get_objects(select_id) {
    var option = document.getElementById(select_id).selectedIndex;
    var tenant_uuid =  document.getElementById(select_id).options[option].value;
    console.log("load_plugin " + tenant_uuid);
    $.ajax({
            type:"GET",
            url: "/tenant/"+tenant_uuid+"/objects",
            processData: false,
            success: function(msg) {
                var obj = JSON.parse(msg);
                var html = "";
                for (var o in obj.objects) {
                    html += "<input type='checkbox' name='object_"+ obj.objects[o].uuid +
                    "' value="+ obj.objects[o].uuid +">"+ obj.objects[o].name+"<br>";
                }
                $("#objects_list").html(html);
            }
    });
}

function get_subjects(select_id) {
    var option = document.getElementById(select_id).selectedIndex;
    var tenant_uuid =  document.getElementById(select_id).options[option].value;
    console.log("load_plugin " + tenant_uuid);
    $.ajax({
            type:"GET",
            url: "/tenant/"+tenant_uuid+"/subjects",
            processData: false,
            success: function(msg) {
                var obj = JSON.parse(msg);
                var html = "";
                for (var o in obj.subjects) {
                    html += "<input type='checkbox' name='subject_"+ obj.subjects[o].uuid +
                        "' value="+ obj.subjects[o].uuid +">"+ obj.subjects[o].name+"<br>";
                }
                $("#subjects_list").html(html);
            }
    });
}
