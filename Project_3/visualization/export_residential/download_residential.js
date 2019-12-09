var data = source.data;
var filetext = 'city,' +
    'state,' +
    'housing_units,' +
    'total_pop,' +
    'elec_1kdollars,' +
    'elec_mwh,' +
    'gas_1kdollars,' +
    'gas_mcf,' +
    'elec_lb_ghg,' +
    'gas_lb_ghg\n';
for (var i = 0; i < data['city'].length; i++) {
    var currRow = [data['city'][i].toString(),
                   data['state'][i].toString(),
                   data['housing_units'][i].toString(),
        data['total_pop'][i].toString(),
        data['elec_1kdollars'][i].toString(),
        data['elec_mwh'][i].toString(),
        data['gas_1kdollars'][i].toString(),
        data['gas_mcf'][i].toString(),
        data['elec_lb_ghg'][i].toString(),
        data['gas_lb_ghg'][i].toString().concat('\n')];





    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'residential_data.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
} else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}
