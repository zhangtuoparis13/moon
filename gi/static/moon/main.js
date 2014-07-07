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
                    if (name.length > 20) {
                        l = name.length;
                        name = obj.objects[o].name.slice(0,10) + "..." + obj.objects[o].name.slice(l-3,l);
                    }
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

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function delete_inter_extension(uuid) {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    $.ajax({
            type:"DELETE",
            url: "/inter-extensions/"+uuid+"/",
            processData: false,
            success: function(msg) {
                var obj = JSON.parse(msg);
                if (obj["delete"]) {
                    window.location.href = "/inter-extensions/";
                }

            }
    });
}

function get_attributes(name, uuid) {
    var type_select = document.getElementById("type")
    var type_id = type_select.selectedIndex;
    var type = type_select.options[type_id].value;
    var category_select = document.getElementById("category");
    var value_select = document.getElementById("value");
    var category = "";
    if (name == "category") {
        var category_id = category_select.selectedIndex;
        category = category_select.options[category_id].value;
    }
    $.ajax({
            type:"GET",
            url: "/intra-extensions/"+uuid+"/type/"+type+"/",
            processData: false,
            success: function(msg) {
                var obj = JSON.parse(msg);
                var html = "";
                if (name == "type") {
                    var length = category_select.length;
                    for (var cpt = 0; cpt < length; cpt++) {
                        category_select.remove(0);
                    }
                    for (var c in obj.categories) {
                        var opt = document.createElement('option');
                        opt.value = obj.categories[c];
                        opt.innerHTML = obj.categories[c];
                        category_select.appendChild(opt);
                    }
                }
                length = value_select.length;
                for (cpt = 0 ; cpt<length ; cpt++) {
                    value_select.remove(0);
                }
                if (category.length == 0) {
                    category = category_select.options[category_select.selectedIndex].value;
                }
                for (var o in obj.attributes) {
                    if (obj.attributes[o].category == category) {
                        opt = document.createElement('option');
                        opt.value = obj.attributes[o].value;
                        opt.innerHTML = obj.attributes[o].value;
                        value_select.appendChild(opt);
                    }
                }
            }
    });
}

function add_temp_rule() {
    var type_select = document.getElementById("type")
    var type = type_select.options[type_select.selectedIndex].value;
    var category_select = document.getElementById("category");
    var category = category_select.options[category_select.selectedIndex].value;
    var value_select = document.getElementById("value");
    var value = value_select.options[value_select.selectedIndex].value;
    var rules_list = document.getElementById("rules_list");
    console.log(rules_list.innerHTML);
    rules_list.value += type + ":" + category + ":" + value + "\n";
}