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

function get_objects(select_id, tenant_uuid, div_id, input) {
    if (! select_id ) {

    }
    else {
        var option = document.getElementById(select_id).selectedIndex;
        tenant_uuid = document.getElementById(select_id).options[option].value;
    }
    if (! input) { input = false;}
    $.ajax({
            type:"GET",
            url: "/tenant/"+tenant_uuid+"/objects",
            processData: false,
            success: function(msg) {
                var obj = JSON.parse(msg);
                var html = "";
                for (var o in obj.objects) {
                    var name = obj.objects[o].name
                    if (name.length > 20) {name = obj.objects[o].name.slice(0,20) + "..."}
                    if (input==true) {
                        html += "<input type='checkbox' name='object_" + obj.objects[o].uuid +
                            "' value=" + obj.objects[o].uuid + ">" + name + "<br>";
                    }
                    else {
                        html += name + "<br>\n";
                    }
                }
                if (div_id) {
                    $(div_id).html(html);
                }
                else {
                    $("#objects_list").html(html);
                }
            }
    });
}

function get_subjects(select_id, tenant_uuid, div_id, input) {
    if (! select_id ) {

    }
    else {
        var option = document.getElementById(select_id).selectedIndex;
        tenant_uuid = document.getElementById(select_id).options[option].value;
    }
    if (! input) { input = false;}
    $.ajax({
            type:"GET",
            url: "/tenant/"+tenant_uuid+"/subjects",
            processData: false,
            success: function(msg) {
                var obj = JSON.parse(msg);
                var html = "";
                for (var o in obj.subjects) {
                    var name = obj.subjects[o].name
                    if (name.length > 20) {name = obj.subjects[o].name.slice(0,20) + "..."}
                    if (input==true) {
                        html += "<input type='checkbox' name='subject_" + obj.subjects[o].uuid +
                            "' value=" + obj.subjects[o].uuid + ">" + name + "<br>";
                    }
                    else {
                        html += name + "<br>\n";
                    }
                }
                if (div_id) {
                    console.log("div_id="+div_id);
                    $(div_id).html(html);
                }
                else {
                    $("#subjects_list").html(html);
                }
            }
    });
}
