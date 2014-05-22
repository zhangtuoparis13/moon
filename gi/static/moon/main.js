/**
 * Created by Thomas Duval on 14/04/14.
 */

$( document ).ready(function() {
    $("#useradd").hide();
    $("#tenantadd").hide();
    $("#elementadd").hide();
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

function opendiv(divelement) {
    $(divelement).show();
};