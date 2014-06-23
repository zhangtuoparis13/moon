/**
 * Created by Thomas Duval on 14/04/14.
 */

$( document ).ready(function() {
    $("#useradd").hide();
    $("#tenantadd").hide();
    $("#elementadd").hide();
    $("#add_intra_rule").hide();
    $("#add_rule_help").hide();
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

function opendiv(divelement) {
    $(divelement).show();
};

function add_text_to_new_rule(select_id) {
    $("#new_rule").value += $(select_id).options[$(select_id).selectedIndex].text;
};