/**
 * Created by vdsq3226 on 14/04/14.
 */

$( document ).ready(function() {
    $("#useradd").hide();
    $("#tenantadd").hide();
});

function show_user_add_actions() {
    $("#useradd").show();
};

function show_tenant_add_actions() {
    $("#tenantadd").show();
};