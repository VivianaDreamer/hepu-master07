'use strict'

function setPage(type="ppa", ppa, customized, user, ppa_type, nom_power) {
    if (type == "ppa") {
        if (ppa_type.value == "24/7") {
            customized.style.display = "none";
        }
        if (ppa_type.value == "Custom") {
            customized.style.display = "block";
        }
        ppa.style.display = "block";
        ppa_type.style.display = "block";
        user.style.display = "none";
        nom_power.style.display = "block";
    }
    if (type == "24/7") {
        ppa.style.display = "block";
        ppa_type.style.display = "block";
        customized.style.display = "none";
        user.style.display = "none";
        nom_power.style.display = "block";
    }
    if (type == "custom") {
        ppa.style.display = "block";
        ppa_type.style.display = "block";
        customized.style.display = "block";
        user.style.display = "none";
        nom_power.style.display = "block";
    }
    if (type == "user") {
        ppa.style.display = "none";
        ppa_type.style.display = "none";
        customized.style.display = "none";
        user.style.display = "block";
        nom_power.style.display = "none";
    }
};

function capex(electrolyzer, develop, instalation, indirect, elec_size, total){
    total.value = parseFloat(electrolyzer.value) + parseFloat(develop.value) + parseFloat(instalation.value) + (parseFloat(indirect.value)/(parseFloat(elec_size.value)*1000)) ;
    total.value = total.value * 1000;
}

function debt(debt_term, horizon){
    debt_term.value = parseFloat(horizon.value);
}

function check_debt(debt_term, horizon){
    if (horizon.value < debt_term.value){
        alert("Value of 'Debt Term' can't be gratter than 'Years of operation'");
        debt(debt_term,horizon)
    }
}

function setImage(elec_type, pem_img, alk_img, soec_img, pem_data){
    if (elec_type.value=="PEM"){
        pem_img.style.display = "block";
        pem_data.style.display = "block";
        alk_img.style.display = "none";
        soec_img.style.display = "none";
    }
    if (elec_type.value=="ALK") {
        pem_img.style.display = "none";
        pem_data.style.display = "none";
        alk_img.style.display = "block";
        soec_img.style.display = "none";
    }
    if (elec_type.value=="SOEC") {
        pem_img.style.display = "none";
        pem_data.style.display = "none";
        alk_img.style.display = "none";
        soec_img.style.display = "block";
    }
}

window.addEventListener('load',()=>{
    const ppa = document.getElementById("ppa");
    const ppa_type = document.getElementById("ppa_type");
    const customized = document.getElementById("customized");
    const user = document.getElementById("user");
    const nom_power = document.getElementById("nom_power");
    const total = document.getElementById("total_capex");
    const elec_type = document.getElementById("elec_type");
    const pem_img = document.getElementById("pem_img");
    const alk_img = document.getElementById("alk_img");
    const soec_img = document.getElementById("soec_img");
    const pem_data = document.getElementById("pem_data");
    const debt_term = document.getElementById("debt_term");
    const horizon = document.getElementById("horizon");
    const choice_ppa = document.getElementById("op_type_0");
    const choice_onsite = document.getElementById("op_type_1");
    const electrolyzer = document.getElementById("elect");
    const develop = document.getElementById("develop");
    const instalation = document.getElementById("instalation");
    const indirect = document.getElementById("indirect");
    const elec_size = document.getElementById("elec_size");  
    
    setPage("ppa", ppa, customized, user, ppa_type,nom_power);
    setImage(elec_type, pem_img, alk_img, soec_img, pem_data);
    debt(debt_term,horizon);
    
    choice_ppa.addEventListener('change', function() {
        if (this.checked) {
            setPage("ppa", ppa, customized, user, ppa_type,nom_power);
        }
    });
    ppa_type.addEventListener('change', function(){
        if (ppa_type.value=="24/7"){
            setPage("24/7",ppa,customized,user,ppa_type,nom_power);
        }
        if (ppa_type.value=="Custom"){
            setPage("custom",ppa,customized,user,ppa_type,nom_power);
        }
    });
    choice_onsite.addEventListener('change', function() {
        if (this.checked) {
            setPage("user", ppa, customized, user, ppa_type,nom_power);
        }
    });
    elec_type.addEventListener('change', function() {
        setImage(elec_type, pem_img, alk_img, soec_img, pem_data);
    });
    horizon.addEventListener('change', function(){
        debt(debt_term,horizon);
    });
    debt_term.addEventListener('change', function(){
        check_debt(debt_term,horizon);
    });
    electrolyzer.addEventListener('change', function(){
        capex(electrolyzer, develop, instalation, indirect, elec_size, total);
    });
    develop.addEventListener('change', function(){
        capex(electrolyzer, develop, instalation, indirect, elec_size, total);
    });
    instalation.addEventListener('change', function(){
        capex(electrolyzer, develop, instalation, indirect, elec_size, total);
    });
    indirect.addEventListener('change', function(){
        capex(electrolyzer, develop, instalation, indirect, elec_size, total);
    });
    elec_size.addEventListener('change', function(){
        capex(electrolyzer, develop, instalation, indirect, elec_size, total);
    });
});